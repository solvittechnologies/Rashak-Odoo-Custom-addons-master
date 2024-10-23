from odoo import models, api, fields, _

class SkilledWorkers(models.Model):
    _name = 'skilled.workers'

    company_id = fields.Many2one('res.company',string="Company")
    week = fields.Char("Week")

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    staff_line_ids = fields.One2many('skilled.workers.staff.line','skilled_workers_id',string="Staff Lines")

class SkilledWorkersStaffLine(models.Model):
    _name = 'skilled.workers.staff.line'

    staff_id = fields.Many2one('hr.employee',string="Staff")
    worker_department_id = fields.Many2one('hr.department',"Worker Department")
    saturday = fields.Boolean("Saturday")
    sunday = fields.Boolean("Sunday")
    monday = fields.Boolean("Monday")
    tuesday = fields.Boolean("Tuesday")
    wednesday = fields.Boolean("Wednesday")
    thursday = fields.Boolean("Thursday")
    friday = fields.Boolean("Friday")
    comment = fields.Text("Comment")
    skilled_workers_id = fields.Many2one('skilled.workers',string="skilled workers")


    @api.onchange('staff_id')
    def onchange_staff_id(self):
        if self.staff_id:
            self.worker_department_id = self.staff_id.department_id
