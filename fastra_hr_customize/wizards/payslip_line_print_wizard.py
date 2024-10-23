from odoo import fields, models, _


class ReportHRPayslipCustomLineWizard(models.TransientModel):
    _name = 'report.fastra.payslip.print.report.wizard'

    payroll_line_id = fields.Many2one("hr.payslip.custom.line", "Payroll Line")
    gross_salary = fields.Boolean("Gross Salary")
    basic_salary = fields.Boolean("Basic Salary")
    housing_allowance = fields.Boolean("Housing Allowance")
    transport = fields.Boolean("Transport")
    interns_stipends = fields.Boolean("Interns Stipends")
    backpay = fields.Boolean("BackPay")
    bonus = fields.Boolean("Bonus")
    overtime = fields.Boolean("Overtime")
    gross_monthly = fields.Boolean("Gross Monthly")
    annual_gross_income = fields.Boolean("Annual Gross Income")
    pension = fields.Boolean("PENSION (8% of BHT)")
    nhf_annual = fields.Boolean("NHF ANNUAL")
    net_g_income = fields.Boolean("Net G.Income")
    consolidated_relief_allowance = fields.Boolean("Consolidated Relief Allowance")
    consolidated_relief_allowance_fixed = fields.Boolean("Consolidated Relief Allowance Fixed")
    consolidated_relief_allowance_monthly = fields.Boolean("Consolidated Relief Allowance MONTHLY TOTAL")
    taxable_income_annual = fields.Boolean("Taxable Income ANNUAL")
    taxable_income_monthly = fields.Boolean("Taxable Income MONTHLY")
    paye = fields.Boolean("PAYE")
    minimum_tax = fields.Boolean("MINIMUM TAX")
    monthly_paye = fields.Boolean("MONTHLY PAYE")
    monthly_pension = fields.Boolean("MONTHLY PENSION")
    monthly_nhf = fields.Boolean("MONTHLY NHF")
    deductions = fields.Boolean("DEDUCTIONS")
    net_payout = fields.Boolean("NET - PAYOUT")
    employee_pension_monthly = fields.Boolean("Employer Pension (Monthly)")
    nsitf = fields.Boolean("NSITF")
    itf = fields.Boolean("ITF")
    total_cost_employee_company_monthly = fields.Boolean("Total Cost of Employment to company (Monthly)")

    def _get_report_base_filename(self):
        return _('Payslip Report')

    def get_report(self):
        return self.env.ref('fastra_hr_customize.hr_payslip_custom_report').report_action(self)
        # data = {
        #     'model': self._name,
        #     'ids': self.ids,
        #     'values': self.id
        # }
        # return self.env.ref('fastra_hr_customize.hr_payslip_custom_report').report_action(self, data)


# class ReportHRPayslipCustomLineReportView(models.AbstractModel):
#     _name = 'report.fastra.payslip.print.hr_payslip_custom_report_view'
#
#     @api.model
#     def _get_report_values(self, docids, data):
#         getwizardvalue = self.env['report.fastra.payslip.print.report.wizard'].sudo().search([('id', '=', data['values'])])
#
#         doc = self.env['hr.payslip.custom.line'].sudo().search([('id', '=', getwizardvalue.resid)])
#         company = doc.payslip_custom_id.company_id
#         currency = company.currency_id
#
#         return {
#             'doc_ids': data['ids'],
#             'doc_model': "hr.payslip.custom.line",
#             'docs': doc,
#             'currency': currency,
#             'company': company,
#             'o': doc,
#             'report_wizard': getwizardvalue
#         }
