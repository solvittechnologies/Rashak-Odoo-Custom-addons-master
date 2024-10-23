from odoo import fields, models, api


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    employee_unique_code = fields.Char('Employee Code', copy=False)
    gross_monthly_pay = fields.Float("Gross Monthly Pay")
    account_details = fields.Char("Account Details")
    birth_date = fields.Date(string='Date Of Bith')
    date_of_employment = fields.Date(string='Date Of Employment')

    @api.model
    def create(self, values):
        res = super(HREmployee, self).create(values)
        reference_code = self.env['ir.sequence'].next_by_code('employee.unique.code')
        if res.company_id:
            res.employee_unique_code = res.company_id.employee_code_start + '/' + reference_code
        return res

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for emp in self:
    #         result.append((emp.id, emp.employee_unique_code))
    #     return result

