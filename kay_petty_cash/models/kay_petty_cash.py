# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class KayPettyCash(models.Model):
    _name = "kay.petty.cash"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Name")
    location = fields.Char('Location')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    amount_allocated = fields.Float('Amount Allocated', compute='get_amount_allocated_total')
    amount_expended = fields.Float('Amount Expended', compute="get_amount_expended_total")
    balance = fields.Float(string='Balance', compute="get_balance_total")
    petty_cash_lines = fields.One2many('kay.petty.cash.line',
                                       'key_petty_cash_id', string="Lines")
    petty_cash_breakdown_lines = fields.One2many('petty.cash.breakdown', 'key_petty_cash_id', string="Beakdown Lines")
    move_ids = fields.Many2many('account.move', 'kay_petty_cash_move_rel', 'kay_petty_cash_id', 'move_id',
                                string="Moves", compute="get_move_ids")

    @api.depends('petty_cash_lines')
    def get_amount_allocated_total(self):
        for rec in self:
            total = 0.0
            for line in rec.petty_cash_lines.filtered(lambda l: l.state == 'approved'):
                total += line.amount
            rec.amount_allocated = total

    @api.depends('petty_cash_breakdown_lines')
    def get_amount_expended_total(self):
        for rec in self:
            total = 0.0
            for line in rec.petty_cash_breakdown_lines.filtered(lambda l: l.status == 'approved'):
                total += line.amount
            rec.amount_expended = total

    @api.depends('amount_allocated', 'amount_expended')
    def get_balance_total(self):
        for rec in self:
            rec.balance = rec.amount_allocated - rec.amount_expended

    @api.depends('petty_cash_lines', 'petty_cash_breakdown_lines')
    def get_move_ids(self):
        for rec in self:
            move_ids_list = []
            for line in rec.petty_cash_lines:
                if line.move_id:
                    move_ids_list.append(line.move_id.id)
            for line in rec.petty_cash_breakdown_lines:
                if line.move_id:
                    move_ids_list.append(line.move_id.id)
            rec.move_ids = [(6, 0, move_ids_list)]

    def button_journal_entries(self):
        return {
            'name': _('Journal Entries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.move_ids.ids)],
        }


class KayPettyCashLine(models.Model):
    _name = "kay.petty.cash.line"

    key_petty_cash_id = fields.Many2one('kay.petty.cash', string="Petty Cash")
    name = fields.Char('Request Description')
    date = fields.Date('Request Date')
    amount = fields.Float('Request Amount')
    account_debit = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Credit Account', domain=[('deprecated', '=', False)])
    journal_id = fields.Many2one('account.journal', string='Journal')
    state = fields.Selection([('draft', 'Draft'), ('send_for_approval', 'Send for Approval'), ('approved', 'Approved')], default='draft', string="Status")
    move_id = fields.Many2one('account.move', string="Move")

    @api.model
    def create(self, vals):
        res = super(KayPettyCashLine, self).create(vals)
        if res and res.state == 'approved':
            if not res.journal_id:
                raise UserError(_('Journal is not set!! Please Set Journal.'))
            if not res.account_credit or not res.account_debit:
                raise UserError(_('You need to set debit/credit account for validate.'))

            debit_vals = {
                'name': res.name,
                'debit': res.amount,
                'credit': 0.0,
                'account_id': res.account_debit.id,
            }
            credit_vals = {
                'name': res.name,
                'debit': 0.0,
                'credit': res.amount,
                'account_id': res.account_credit.id,
            }
            vals = {
                'journal_id': res.journal_id.id,
                'date': datetime.now().date(),
                'ref': res.name,
                'state': 'draft',
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.action_post()
            res.write({'move_id': move.id})
        return res

    def write(self, vals):
        res = super(KayPettyCashLine, self).write(vals)
        if vals.get('state', False) and vals['state'] == 'approved' and not self.move_id:
            if not self.journal_id:
                raise UserError(_('Journal is not set!! Please Set Journal.'))
            if not self.account_credit or not self.account_debit:
                raise UserError(_('You need to set debit/credit account for validate.'))

            debit_vals = {
                'name': self.name,
                'debit': self.amount,
                'credit': 0.0,
                'account_id': self.account_debit.id,
            }
            credit_vals = {
                'name': self.name,
                'debit': 0.0,
                'credit': self.amount,
                'account_id': self.account_credit.id,
            }
            vals = {
                'journal_id': self.journal_id.id,
                'date': datetime.now().date(),
                'ref': self.name,
                'state': 'draft',
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.action_post()
            self.write({'move_id': move.id})
        if vals.get('state', False) and vals['state'] == 'approved' and self.move_id:
            self.move_id.button_cancel()
            self.move_id.line_ids.unlink()
            debit_vals = {
                'name': res.name,
                'debit': self.amount,
                'credit': 0.0,
                'account_id': self.account_debit.id,
            }
            credit_vals = {
                'name': res.name,
                'debit': 0.0,
                'credit': self.amount,
                'account_id': self.account_credit.id,
            }
            self.move_id.write({'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]})
            self.move_id.action_post()
        return res


class PettyCashBreakdown(models.Model):
    _name = "petty.cash.breakdown"

    key_petty_cash_id = fields.Many2one('kay.petty.cash', string="Petty Cash")
    name = fields.Char('Description')
    date = fields.Date("Expended Date")
    amount = fields.Float('Amount')
    account_debit = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Credit Account', domain=[('deprecated', '=', False)])
    journal_id = fields.Many2one('account.journal', string='Journal')
    status = fields.Selection([('draft', 'Draft'), ('approved', 'Approved')], default='draft', string="Status")
    move_id = fields.Many2one('account.move', string="Move")

    @api.model
    def create(self, vals):
        res = super(PettyCashBreakdown, self).create(vals)
        if res and res.status == 'approved':
            if not res.journal_id:
                raise UserError(_('Journal is not set!! Please Set Journal.'))
            if not res.account_credit or not res.account_debit:
                raise UserError(_('You need to set debit/credit account for validate.'))

            debit_vals = {
                'name': res.name,
                'debit': res.amount,
                'credit': 0.0,
                'account_id': res.account_debit.id,
            }
            credit_vals = {
                'name': res.name,
                'debit': 0.0,
                'credit': res.amount,
                'account_id': res.account_credit.id,
            }
            vals = {
                'journal_id': res.journal_id.id,
                'date': datetime.now().date(),
                'ref': res.name,
                'state': 'draft',
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)],

            }
            move = self.env['account.move'].create(vals)
            move.action_post()
            res.write({'move_id': move.id})
        return res

    def write(self, vals):
        res = super(PettyCashBreakdown, self).write(vals)
        if vals.get('status', False) and vals['status'] == 'approved' and not self.move_id:
            if not self.journal_id:
                raise UserError(_('Journal is not set!! Please Set Journal.'))
            if not self.account_credit or not self.account_debit:
                raise UserError(_('You need to set debit/credit account for validate.'))

            debit_vals = {
                'name': self.name,
                'debit': self.amount,
                'credit': 0.0,
                'account_id': self.account_debit.id,
            }
            credit_vals = {
                'name': self.name,
                'debit': 0.0,
                'credit': self.amount,
                'account_id': self.account_credit.id,
            }
            vals = {
                'journal_id': self.journal_id.id,
                'date': datetime.now().date(),
                'ref': self.name,
                'state': 'draft',
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)],

            }
            move = self.env['account.move'].create(vals)
            move.action_post()
            self.write({'move_id': move.id})
        if vals.get('status', False) and vals['status'] == 'approved' and self.move_id:
            self.move_id.button_cancel()
            self.move_id.line_ids.unlink()
            debit_vals = {
                'name': self.name,
                'debit': self.amount,
                'credit': 0.0,
                'account_id': self.account_debit.id,
            }
            credit_vals = {
                'name': self.name,
                'debit': 0.0,
                'credit': self.amount,
                'account_id': self.account_credit.id,
            }
            self.move_id.write({'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]})
            self.move_id.action_post()
        return res


