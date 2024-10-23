from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
import base64
from io import BytesIO


Months = [('January', 'January'),
          ('february', 'February'),
          ('march', 'March'),
          ('april', 'April'),
          ('may', 'May'),
          ('june', 'June'),
          ('july', 'July'),
          ('august', 'August'),
          ('september', 'September'),
          ('october', 'October'),
          ('november', 'November'),
          ('december', 'December')]


class HRPayslipCustom(models.Model):
    _name = 'hr.payslip.custom'

    name = fields.Char("Payslip Name")
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated')], string="State", default='draft')
    location_id = fields.Many2one('stock.location', "Location")
    date_from = fields.Date(string='Date From', required=True,
                            default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            )
    date_to = fields.Date(string='Date To', required=True,
                          default=lambda self: fields.Date.to_string(
                              (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
                          )
    month = fields.Selection(Months, string="Month")
    reference_number = fields.Char("Reference Number")
    account_analytic_id = fields.Many2one('account.analytic.account', "Project")
    payslip_custom_line_ids = fields.One2many('hr.payslip.custom.line', 'payslip_custom_id', string="Lines", copy=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    excel_file = fields.Binary('Excel File')
    file_name = fields.Char('File Name')

    @api.model
    def create(self, values):
        if not values.get('reference_number', False):
            reference_code = self.env['ir.sequence'].next_by_code('employee.payroll.reference')
            values['reference_number'] = reference_code[:-1]
        return super(HRPayslipCustom, self).create(values)

    def generate_excel(self):
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)

        worksheet = workbook.add_worksheet('Payroll Report')

        bold = workbook.add_format({'bold': True})
        border = workbook.add_format({'border': 1})
        format1 = workbook.add_format({'bold': True, 'border': 1})

        row = 0
        worksheet.write(row, 0, 'Employee Name', format1)
        worksheet.write(row, 1, 'Employee ID', format1)
        worksheet.write(row, 2, 'Employee Address', format1)
        worksheet.write(row, 3, 'Designation', format1)
        worksheet.write(row, 4, 'Location', format1)
        worksheet.write(row, 5, 'Bank Name', format1)
        worksheet.write(row, 6, 'Account Number', format1)
        worksheet.write(row, 7, 'Pension Fund Administrator', format1)
        worksheet.write(row, 8, 'Pension Number', format1)
        worksheet.write(row, 9, 'NHF Number', format1)
        worksheet.write(row, 10, 'Work days in month', format1)
        worksheet.write(row, 11, 'Days worked', format1)
        worksheet.write(row, 12, 'Gross Salary', format1)
        worksheet.write(row, 13, 'Basic Salary', format1)
        worksheet.write(row, 14, 'Housing Allowance', format1)
        worksheet.write(row, 15, 'Transport', format1)
        worksheet.write(row, 16, 'Interns Stipends', format1)
        worksheet.write(row, 17, 'BackPay', format1)
        worksheet.write(row, 18, 'Bonus', format1)
        worksheet.write(row, 19, 'Overtime', format1)
        worksheet.write(row, 20, 'Gross Monthly', format1)
        worksheet.write(row, 21, 'Annual Gross Income', format1)
        worksheet.write(row, 22, 'PENSION', format1)
        worksheet.write(row, 23, 'NHF ANNUAL', format1)
        worksheet.write(row, 24, 'Net G.Income', format1)
        worksheet.write(row, 25, 'Consolidated Relief Allowance', format1)
        worksheet.write(row, 26, 'Consolidated Relief Allowance Fixed', format1)
        worksheet.write(row, 27, 'Consolidated Relief Allowance MONTHLY TOTAL', format1)
        worksheet.write(row, 28, 'Taxable Income ANNUAL', format1)
        worksheet.write(row, 29, 'axable Income MONTHLY', format1)
        worksheet.write(row, 30, 'PAYE', format1)
        worksheet.write(row, 31, 'MINIMUM TAX', format1)
        worksheet.write(row, 32, 'MONTHLY PAYE', format1)
        worksheet.write(row, 33, 'MONTHLY PENSION', format1)
        worksheet.write(row, 34, 'MONTHLY NHF', format1)
        worksheet.write(row, 35, 'DEDUCTIONS', format1)
        worksheet.write(row, 36, 'NET - PAYOUT', format1)
        worksheet.write(row, 37, 'Employer Pension (Monthly)', format1)
        worksheet.write(row, 38, 'NSITF', format1)
        worksheet.write(row, 39, 'ITF', format1)
        worksheet.write(row, 40, 'Total Cost of Employment to company (Monthly)', format1)

        row += 1

        gross_salary = basic_salary = housing_allowance = transport = interns_stipends = backpay = bonus = overtime = gross_monthly = annual_gross_income = 0.0
        pension = nhf_annual = net_g_income = consolidated_relief_allowance = consolidated_relief_allowance_fixed = consolidated_relief_allowance_monthly = taxable_income_annual = taxable_income_monthly = paye = minimum_tax = 0.0
        monthly_paye = monthly_pension = monthly_nhf = deductions = net_payout = employee_pension_monthly = nsitf = itf = total_cost_employee_company_monthly = 0.0

        for line in self.payslip_custom_line_ids:
            worksheet.write(row, 0, line.employee_id and line.employee_id.name or '')
            worksheet.write(row, 1, line.employee_code or '')
            worksheet.write(row, 2, line.employee_email or '')
            worksheet.write(row, 3, line.department_id and line.department_id.name or '')
            worksheet.write(row, 4, line.location_id and line.location_id.name or '')
            worksheet.write(row, 5, line.bank_name or '')
            worksheet.write(row, 6, line.account_number or '')
            worksheet.write(row, 7, line.pension_fund_administrator or '')
            worksheet.write(row, 8, line.pension_number or '')
            worksheet.write(row, 9, line.nhf_number or '')
            worksheet.write(row, 10, line.work_days_month or '')
            worksheet.write(row, 11, line.days_worked or '')

            worksheet.write(row, 12, line.gross_salary or '')
            gross_salary += line.gross_salary

            worksheet.write(row, 13, line.basic_salary or '')
            basic_salary += line.basic_salary

            worksheet.write(row, 14, line.housing_allowance or '')
            housing_allowance += line.housing_allowance

            worksheet.write(row, 15, line.transport or '')
            transport += line.transport

            worksheet.write(row, 16, line.interns_stipends or '')
            interns_stipends += line.interns_stipends

            worksheet.write(row, 17, line.backpay or '')
            backpay += line.backpay

            worksheet.write(row, 18, line.bonus or '')
            bonus += line.bonus

            worksheet.write(row, 19, line.overtime or '')
            overtime += line.overtime

            worksheet.write(row, 20, line.gross_monthly or '')
            gross_monthly += line.gross_monthly

            worksheet.write(row, 21, line.annual_gross_income or '')
            annual_gross_income += line.annual_gross_income

            worksheet.write(row, 22, line.pension or '')
            pension += line.pension

            worksheet.write(row, 23, line.nhf_annual or '')
            nhf_annual += line.nhf_annual

            worksheet.write(row, 24, line.net_g_income or '')
            net_g_income += line.net_g_income

            worksheet.write(row, 25, line.consolidated_relief_allowance or '')
            consolidated_relief_allowance += line.consolidated_relief_allowance

            worksheet.write(row, 26, line.consolidated_relief_allowance_fixed or '')
            consolidated_relief_allowance_fixed += line.consolidated_relief_allowance_fixed

            worksheet.write(row, 27, line.consolidated_relief_allowance_monthly or '')
            consolidated_relief_allowance_monthly += line.consolidated_relief_allowance_monthly

            worksheet.write(row, 28, line.taxable_income_annual or '')
            taxable_income_annual += line.taxable_income_annual

            worksheet.write(row, 29, line.taxable_income_monthly or '')
            taxable_income_monthly += line.taxable_income_monthly

            worksheet.write(row, 30, line.paye or '')
            paye += line.paye

            worksheet.write(row, 31, line.minimum_tax or '')
            minimum_tax += line.minimum_tax

            worksheet.write(row, 32, line.monthly_paye or '')
            monthly_paye += line.monthly_paye

            worksheet.write(row, 33, line.monthly_pension or '')
            monthly_pension += line.monthly_pension

            worksheet.write(row, 34, line.monthly_nhf or '')
            monthly_nhf += line.monthly_nhf

            worksheet.write(row, 35, line.deductions or '')
            deductions += line.deductions

            worksheet.write(row, 36, line.net_payout or '')
            net_payout += line.net_payout

            worksheet.write(row, 37, line.employee_pension_monthly or '')
            employee_pension_monthly += line.employee_pension_monthly

            worksheet.write(row, 38, line.nsitf or '')
            nsitf += line.nsitf

            worksheet.write(row, 39, line.itf or '')
            itf += line.itf

            worksheet.write(row, 40, line.total_cost_employee_company_monthly or '')
            total_cost_employee_company_monthly += line.total_cost_employee_company_monthly

            row += 1

        worksheet.write(row, 12, gross_salary, bold)
        worksheet.write(row, 13, basic_salary, bold)
        worksheet.write(row, 14, housing_allowance, bold)
        worksheet.write(row, 15, transport, bold)
        worksheet.write(row, 16, interns_stipends, bold)
        worksheet.write(row, 17, backpay, bold)
        worksheet.write(row, 18, bonus, bold)
        worksheet.write(row, 19, overtime, bold)
        worksheet.write(row, 20, gross_monthly, bold)
        worksheet.write(row, 21, annual_gross_income, bold)
        worksheet.write(row, 22, pension, bold)
        worksheet.write(row, 23, nhf_annual, bold)
        worksheet.write(row, 24, net_g_income, bold)
        worksheet.write(row, 25, consolidated_relief_allowance, bold)
        worksheet.write(row, 26, consolidated_relief_allowance_fixed, bold)
        worksheet.write(row, 27, consolidated_relief_allowance_monthly, bold)
        worksheet.write(row, 28, taxable_income_annual, bold)
        worksheet.write(row, 29, taxable_income_monthly, bold)
        worksheet.write(row, 30, paye, bold)
        worksheet.write(row, 31, minimum_tax, bold)
        worksheet.write(row, 32, monthly_paye, bold)
        worksheet.write(row, 33, monthly_pension, bold)
        worksheet.write(row, 34, monthly_nhf, bold)
        worksheet.write(row, 35, deductions, bold)
        worksheet.write(row, 36, net_payout, bold)
        worksheet.write(row, 37, employee_pension_monthly, bold)
        worksheet.write(row, 38, nsitf, bold)
        worksheet.write(row, 39, itf, bold)
        worksheet.write(row, 40, total_cost_employee_company_monthly, bold)

        workbook.close()
        file_data.seek(0)
        self.write(
            {'excel_file': base64.encodebytes(file_data.read()),
             'file_name': 'Payroll.xlsx'})

        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=hr.payslip.custom&id=" + str(self.id) + "&filename_field=filename&field=excel_file&download=true&filename=" + self.file_name,
            'target': 'current'
        }


class HRPayslipCustomLine(models.Model):
    _name = 'hr.payslip.custom.line'

    payslip_custom_id = fields.Many2one('hr.payslip.custom', string="Payslip Custom Id")
    employee_id = fields.Many2one('hr.employee', string="Employee Name")
    employee_code = fields.Char('Employee ID')
    employee_email = fields.Char('Email Address')
    department_id = fields.Many2one('hr.department', string='Designation')
    location_id = fields.Many2one('stock.location', "Location")
    bank_name = fields.Char("Bank Name")
    account_number = fields.Char("Account Number")
    pension_fund_administrator = fields.Char("Pension Fund Administrator")
    pension_number = fields.Char('Pension Number')
    nhf_number = fields.Char('NHF Number')
    work_days_month = fields.Integer("Work days in month")
    days_worked = fields.Integer("Days worked")
    gross_salary = fields.Float("Gross Salary")
    basic_salary = fields.Float("Basic Salary")
    housing_allowance = fields.Float("Housing Allowance")
    transport = fields.Float("Transport")
    interns_stipends = fields.Float("Interns Stipends")
    backpay = fields.Float("BackPay")
    bonus = fields.Float("Bonus")
    overtime = fields.Float("Overtime")
    gross_monthly = fields.Float("Gross Monthly")
    annual_gross_income = fields.Float("Annual Gross Income")
    pension = fields.Float("PENSION (8% of BHT)")
    nhf_annual = fields.Float("NHF ANNUAL")
    net_g_income = fields.Float("Net G.Income")
    consolidated_relief_allowance = fields.Float("Consolidated Relief Allowance")
    consolidated_relief_allowance_fixed = fields.Float("Consolidated Relief Allowance Fixed")
    consolidated_relief_allowance_monthly = fields.Float("Consolidated Relief Allowance MONTHLY TOTAL")
    taxable_income_annual = fields.Float("Taxable Income ANNUAL")
    taxable_income_monthly = fields.Float("Taxable Income MONTHLY")
    paye = fields.Float("PAYE")
    minimum_tax = fields.Float("MINIMUM TAX")
    monthly_paye = fields.Float("MONTHLY PAYE")
    monthly_pension = fields.Float("MONTHLY PENSION")
    monthly_nhf = fields.Float("MONTHLY NHF")
    deductions = fields.Float("DEDUCTIONS")
    net_payout = fields.Float("NET - PAYOUT")
    employee_pension_monthly = fields.Float("Employer Pension (Monthly)")
    nsitf = fields.Float("NSITF")
    itf = fields.Float("ITF")
    total_cost_employee_company_monthly = fields.Float("Total Cost of Employment to company (Monthly)")

    @api.onchange('gross_monthly')
    def calculate_basic(self):
        try:
            self.basic_salary = (self.gross_monthly * 55) / 100
        except:
            self.basic_salary = 0.0
        try:
            self.housing_allowance = (self.gross_monthly * 25) / 100
        except:
            self.housing_allowance = 0.0
        try:
            self.transport = (self.gross_monthly * 20) / 100
        except:
            self.transport = 0.0

    @api.onchange('gross_monthly')
    def calculate_annual_gross_income(self):
        self.annual_gross_income = self.gross_monthly * 12

    @api.onchange('basic_salary', 'housing_allowance', 'transport', 'interns_stipends', 'backpay', 'bonus', 'overtime')
    def calculate_gross_monthly(self):
        self.gross_monthly = self.basic_salary + self.housing_allowance + self.transport + self.interns_stipends + self.backpay + self.bonus + self.overtime

    @api.onchange('basic_salary', 'housing_allowance', 'transport')
    def calculate_pension(self):
        try:
            self.pension = (((self.basic_salary + self.housing_allowance + self.transport) * 12) * 8) / 100
        except:
            self.pension = 0.0

    @api.onchange('annual_gross_income')
    def calculate_nhf(self):
        try:
            self.nhf_annual = (self.annual_gross_income * 2.5) / 100
        except:
            self.nhf_annual = 0.0
        try:
            self.minimum_tax = (self.annual_gross_income * 1) / 100
        except:
            self.minimum_tax = 0.0

    @api.onchange('annual_gross_income', 'pension', 'nhf_annual')
    def calculate_net_g_income(self):
        self.net_g_income = self.annual_gross_income - self.pension - self.nhf_annual

    @api.onchange('annual_gross_income')
    def calculate_consolidated_relief_allowance(self):
        try:
            consolidated_relief_allowance = (self.annual_gross_income * 1) / 100
            if consolidated_relief_allowance > 200000:
                self.consolidated_relief_allowance = consolidated_relief_allowance
            else:
                self.consolidated_relief_allowance = 200000
        except:
            self.consolidated_relief_allowance = 0.0

    @api.onchange('net_g_income')
    def calculate_consolidated_relief_allowance_fixed(self):
        try:
            self.consolidated_relief_allowance_fixed = (self.net_g_income * 20) / 100
        except:
            self.consolidated_relief_allowance_fixed = 0.0

    @api.onchange('consolidated_relief_allowance', 'consolidated_relief_allowance_fixed')
    def calculate_consolidated_relief_allowance_monthly(self):
        try:
            self.consolidated_relief_allowance_monthly = (self.consolidated_relief_allowance + self.consolidated_relief_allowance_fixed) / 12
        except:
            self.consolidated_relief_allowance_monthly = 0.0

    @api.onchange('net_g_income', 'consolidated_relief_allowance', 'consolidated_relief_allowance_fixed')
    def calculate_taxable_income_annual(self):
        self.taxable_income_annual = self.net_g_income - self.consolidated_relief_allowance - self.consolidated_relief_allowance_fixed

    @api.onchange('taxable_income_annual')
    def calculate_taxable_income_monthly(self):
        try:
            self.taxable_income_monthly = self.taxable_income_annual / 12
        except:
            self.taxable_income_monthly = 0.0

    @api.onchange('paye')
    def calculate_monthly_paye(self):
        try:
            self.monthly_paye = float(round(self.paye / 12, 2))
        except:
            self.monthly_paye = 0.0

    @api.onchange('pension')
    def calculate_monthly_pension(self):
        try:
            self.monthly_pension = self.pension / 12
        except:
            self.monthly_pension = 0.0

    @api.onchange('nhf_annual')
    def calculate_monthly_nhf(self):
        try:
            self.monthly_nhf = self.nhf_annual / 12
        except:
            self.monthly_nhf = 0.0

    @api.onchange('monthly_paye', 'monthly_pension', 'monthly_nhf')
    def calculate_deductions(self):
        self.deductions = self.monthly_paye + self.monthly_pension + self.monthly_nhf

    @api.onchange('gross_monthly', 'deductions')
    def calculate_net_payout(self):
        self.net_payout = self.gross_monthly - self.deductions

    @api.onchange('basic_salary', 'housing_allowance', 'transport')
    def calculate_employee_pension_monthly(self):
        try:
            self.employee_pension_monthly = ((self.basic_salary + self.housing_allowance + self.transport) * 10) / 100
        except:
            self.employee_pension_monthly = 0.0

    @api.onchange('basic_salary', 'housing_allowance', 'transport')
    def calculate_nsitf(self):
        try:
            self.nsitf = ((self.basic_salary + self.housing_allowance + self.transport) * 1) / 100
        except:
            self.nsitf = 0.0

    @api.onchange('gross_monthly')
    def calculate_itf(self):
        try:
            self.itf = (self.gross_monthly * 1) / 100
        except:
            self.itf = 0.0

    @api.onchange('employee_pension_monthly', 'nsitf', 'itf')
    def calculate_total_cost_employee_company_monthly(self):
        self.total_cost_employee_company_monthly = self.employee_pension_monthly + self.nsitf + self.itf

    @api.onchange('gross_salary', 'consolidated_relief_allowance', 'consolidated_relief_allowance_fixed', 'pension')
    def onchange_paye_amount(self):
        paye = 0.0
        if self.gross_salary < 300000:
            paye = (self.gross_salary * 1) / 100
            self.update({'paye': paye})
            return
        taxable_amount = self.gross_salary - (self.consolidated_relief_allowance + self.consolidated_relief_allowance_fixed) - self.pension
        if taxable_amount > 3200000:
            paye += (300000 * 7) / 100
            paye += (300000 * 11) / 100
            paye += (500000 * 15) / 100
            paye += (500000 * 19) / 100
            paye += (1600000 * 21) / 100
            taxable_amount -= 3200000
            paye += (taxable_amount * 24) / 100
            self.update({'paye': paye})
            return
        elif taxable_amount > 1600000:
            paye += (300000 * 7) / 100
            paye += (300000 * 11) / 100
            paye += (500000 * 15) / 100
            paye += (500000 * 19) / 100
            taxable_amount -= 1600000
            paye += (taxable_amount * 21) / 100
            self.update({'paye': paye})
            return
        elif taxable_amount > 1100000:
            paye += (300000 * 7) / 100
            paye += (300000 * 11) / 100
            paye += (500000 * 15) / 100
            taxable_amount -= 1100000
            paye += (taxable_amount * 19) / 100
            self.update({'paye': paye})
            return
        elif taxable_amount > 600000:
            paye += (300000 * 7) / 100
            paye += (300000 * 11) / 100
            taxable_amount -= 600000
            paye += (taxable_amount * 15) / 100
            self.update({'paye': paye})
            return
        elif taxable_amount > 300000:
            paye += (300000 * 7) / 100
            taxable_amount -= 300000
            paye += (taxable_amount * 11) / 100
            self.update({'paye': paye})
            return
        else:
            paye += (taxable_amount * 7) / 100
            self.update({'paye': paye})
            return

    def launch_print_wizard(self):
        wizard_id = self.env['report.fastra.payslip.print.report.wizard'].create({"payroll_line_id": self.id}).id
        return {
            'name': 'My Wizard',
            'view_mode': 'form',
            'res_model': 'report.fastra.payslip.print.report.wizard',
            'res_id': wizard_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
