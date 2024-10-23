from odoo import api, fields, models, tools


class HrPayrollReport(models.Model):
    _inherit='hr.payroll.report'
    

    identification_id = fields.Char(related='employee_id.identification_id', string='Employee ID')
    email = fields.Char(related='employee_id.work_email')
    designation = fields.Char('Designation')
    location = fields.Char(related='employee_id.work_location')
    bank_name = fields.Char(related='employee_id.bank_account_id.bank_name')
    account_number = fields.Char(related='employee_id.bank_account_id.acc_number')
    work_days = fields.Float(compute='_compute_work_days' , store=True)
    days_worked  = fields.Integer(string="Days worked")


