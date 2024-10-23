from odoo import models, api, fields, _

class HrLabors(models.Model):
    _name = 'hr.labors'

    company_id = fields.Many2one('res.company',string="Company")
    week = fields.Char("Week")
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    labors_line_ids = fields.One2many('hr.labors.line', 'hr_labors_id', string="Staff Lines")

class HrLaborsLine(models.Model):
    _name = 'hr.labors.line'

    staff_id = fields.Many2one('hr.employee',string="Staff")
    saturday = fields.Boolean("Saturday")
    sunday = fields.Boolean("Sunday")
    monday = fields.Boolean("Monday")
    tuesday = fields.Boolean("Tuesday")
    wednesday = fields.Boolean("Wednesday")
    thursday = fields.Boolean("Thursday")
    friday = fields.Boolean("Friday")
    comment = fields.Text("Comment")
    amount = fields.Integer("Amount")
    hr_labors_id = fields.Many2one('hr.labors',string="skilled workers")