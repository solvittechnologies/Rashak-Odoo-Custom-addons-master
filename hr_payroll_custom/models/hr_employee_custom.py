from odoo import api, fields, models, tools


class HremployeeCustom(models.Model):
    _inherit='hr.employee'
    _description = "Hr employee for report"

    bank_name               = fields.Char(related='bank_account_id.bank_name' , store=True)
    account_number          = fields.Char(related='bank_account_id.acc_number' , store=True)
    company_currency_id     = fields.Many2one(string='Company Currency', readonly=True,related='company_id.currency_id')
    work_days               = fields.Integer()
    days_worked             = fields.Integer()
    op_for_nhf              = fields.Boolean(default = True)


    gross_salary            = fields.Monetary(related = "contract_id.wage" , store=True , currency_field="company_currency_id")
    basic_salary            = fields.Float( compute = "_compute_basic_salary" , store=True )
    housing_allow           = fields.Float( compute = "_compute_housing_allow" , store=True )
    transport               = fields.Float(compute = "_compute_transport" , store=True)
    interns_stipends        = fields.Float()
    back_pay                = fields.Float()
    bonus                   = fields.Float()
    overtime                = fields.Float()
    gross_monthly           = fields.Float(compute = "_compute_gross_monthly" , store=True)
    annual_gross_income     = fields.Float( compute = "_compute_annual_gross_income" , store=True)
    pension                 = fields.Float( compute="_compute_pension" , store = True)
    nhf_annual              = fields.Float(compute="_compute_nhf_annual" , store = True)
    net_g_income            = fields.Float(compute="_compute_net_g_income" , store = True)
    
    consollidated_relief_all_variable = fields.Float(compute="_compute_consollidated_relief_all_variable" , store = True)
    consollidated_relief_all_fixed    = fields.Float(compute="_compute_consollidated_relief_all_fixed" , store = True)
    consolidated_relief_all_mth_total = fields.Float(compute="_compute_consolidated_relief_all_mth_total" , store = True)
    taxable_income_annual             = fields.Float(compute="_compute_taxable_income_annual" , store = True)
    taxable_income_monthly            = fields.Float(compute="_compute_taxable_income_monthly" , store = True)
    first_300_7                       = fields.Float(compute="_compute_first_300_7" , store = True)
    next_300_11                       = fields.Float(compute="_compute_next_300_11" , store = True)
    next_500_15                       = fields.Float(compute="_compute_next_500_15" , store = True)
    next_500_19                       = fields.Float(compute="_compute_next_500_19" , store = True)
    next_160_21                       = fields.Float(compute="_compute_next_160_21" , store = True)
    next_320_24                       = fields.Float(compute="_compute_next_320_24" , store = True)
    annual_paye                       = fields.Float(compute="_compute_annual_paye" , store = True)
    min_tax                           = fields.Float(compute="_compute_min_tax" , store = True)
    month_paye                        = fields.Float(compute="_compute_month_paye" , store = True)
    month_pension                     = fields.Float(compute="_compute_month_pension" , store = True)
    month_nhf                         = fields.Float(compute="_compute_month_nhf" , store = True)
    deduction                         = fields.Float(compute="_compute_deduction" , store = True)
    net_payout                        = fields.Float(compute="_compute_net_payout" , store = True)
    
    
    employee_pension_month            = fields.Float(compute="_computte_employee_pension_month" , store = True)
    nsitf                             = fields.Float(compute="_computte_nsitf" , store= True)
    itf                               = fields.Float(compute="_computte_itf" , store= True)
    total_cost_to_company             = fields.Float(compute="_computte_total_cost_to_company" , store= True)




    @api.depends('gross_salary')
    def _compute_annual_gross_income(self):
        for element in self:
            element.annual_gross_income = element.gross_monthly * 12



    @api.depends('gross_salary')
    def _compute_basic_salary(self):
        for element in self:
            element.basic_salary = element.gross_salary * 0.55


    @api.depends('gross_salary')
    def _compute_housing_allow(self):
        for element in self:
            element.housing_allow = element.gross_salary * 0.25


    @api.depends('gross_salary')
    def _compute_transport(self):
        for element in self:
            element.transport = element.gross_salary * 0.20


    @api.depends('basic_salary','housing_allow','transport','interns_stipends','back_pay','bonus','overtime')
    def _compute_gross_monthly(self):
        for element in self:
            element.gross_monthly = element.basic_salary   + element.housing_allow + element.transport + element.interns_stipends + element.back_pay + element.bonus + element.overtime


    @api.depends('basic_salary' , 'housing_allow' , 'transport')
    def _compute_pension(self):
        for element in self:
            element.pension = (((element.basic_salary + element.housing_allow + element.transport)*12)* 0.08)



    @api.depends('gross_salary', 'op_for_nhf')
    def _compute_nhf_annual(self):
        for element in self:
            element.nhf_annual = 0

            if element.op_for_nhf :
                element.nhf_annual = 0.025 * element.annual_gross_income

    @api.depends('annual_gross_income', 'pension' , 'nhf_annual')
    def _compute_net_g_income(self):
        for element in self:
            element.net_g_income = element.annual_gross_income - element.pension - element.nhf_annual



    
    @api.depends('annual_gross_income')
    def _compute_consollidated_relief_all_variable(self):
        for element in self:
            if 0.01 * element.annual_gross_income > 200000:
                element.consollidated_relief_all_variable = 0.01 * element.annual_gross_income 
            else:
                element.consollidated_relief_all_variable = 200000
            

    @api.depends('net_g_income')
    def _compute_consollidated_relief_all_fixed(self):
        for element in self:
            element.consollidated_relief_all_fixed = 0.20 * element.net_g_income
            

    @api.depends('consollidated_relief_all_variable','consollidated_relief_all_fixed')
    def _compute_consolidated_relief_all_mth_total(self):
        for element in self:
            element.consolidated_relief_all_mth_total = ( element.consollidated_relief_all_variable + element.consollidated_relief_all_fixed ) / 12


    @api.depends('net_g_income','consollidated_relief_all_variable','consollidated_relief_all_fixed')
    def _compute_taxable_income_annual(self):
        for element in self:
            element.taxable_income_annual = element.net_g_income -  element.consollidated_relief_all_variable - element.consollidated_relief_all_fixed 
        
    
    @api.depends('taxable_income_annual')
    def _compute_taxable_income_monthly(self):
        for element in self:
            element.taxable_income_monthly = element.taxable_income_annual / 12
        

    
    @api.depends('taxable_income_annual')
    def _compute_first_300_7(self):
        for element in self:
            element.first_300_7 = 0.0
            if element.taxable_income_annual  > 0:
                element.first_300_7 = element.taxable_income_annual *0.07

            if element.taxable_income_annual >= 300001:
                element.first_300_7 += (300000 - element.taxable_income_annual)* 0.07
            else:
                element.first_300_7 += (300000 - element.taxable_income_annual) * 0
    

    @api.depends('taxable_income_annual')
    def _compute_next_300_11(self):
        for element in self:
            element.next_300_11 = 0.0
            if element.taxable_income_annual  >= 300001:
                element.next_300_11 = (element.taxable_income_annual - 300000) *0.11
            else:
                element.next_300_11 = (element.taxable_income_annual - 300000) * 0

            if element.taxable_income_annual >= 600001:
                element.next_300_11 += (600000 - element.taxable_income_annual)* 0.11
            else:
                element.next_300_11 += (600000 - element.taxable_income_annual) * 0
    

    @api.depends('taxable_income_annual')
    def _compute_next_500_15(self):
        for element in self:
            element.next_500_15 = 0.0
            if element.taxable_income_annual  >= 600001:
                element.next_500_15 = (element.taxable_income_annual - 600000) *0.15
            else:
                element.next_500_15 = (element.taxable_income_annual - 600000) * 0

            if element.taxable_income_annual >= 1100001:
                element.next_500_15 += (1100000 - element.taxable_income_annual)* 0.15
            else:
                element.next_500_15 += (1100000 - element.taxable_income_annual) * 0
    

    @api.depends('taxable_income_annual')
    def _compute_next_500_19(self):
        for element in self:
            element.next_500_19 = 0.0
            if element.taxable_income_annual  >= 1100001:
                element.next_500_19 = (element.taxable_income_annual - 1100000) *0.19
            else:
                element.next_500_19 = (element.taxable_income_annual - 1100000) * 0

            if element.taxable_income_annual >= 1600001:
                element.next_500_19 += (1600000 - element.taxable_income_annual)* 0.19
            else:
                element.next_500_19 += (1600000 - element.taxable_income_annual) * 0
    

    @api.depends('taxable_income_annual')
    def _compute_next_160_21(self):
        for element in self:
            element.next_160_21 = 0.0
            if element.taxable_income_annual  >= 1600001:
                element.next_160_21 = (element.taxable_income_annual - 1600000) *0.21
            else:
                element.next_160_21 = (element.taxable_income_annual - 1600000) * 0

            if element.taxable_income_annual >= 3200000:
                element.next_160_21 += (3200000 - element.taxable_income_annual)* 0.21
            else:
                element.next_160_21 += (3200000 - 14) * 0
    

    @api.depends('taxable_income_annual')
    def _compute_next_320_24(self):
        for element in self:
            element.next_320_24 = 0.0
            if element.taxable_income_annual  >= 3200001:
                element.next_320_24 = (element.taxable_income_annual - 3200000) *0.24
            else:
                element.next_320_24 = element.taxable_income_annual * 0


    @api.depends('first_300_7','next_300_11','next_500_15','next_500_19','next_160_21','next_320_24')
    def _compute_annual_paye(self):
        for element in self:
            element.annual_paye = element.first_300_7 + element.next_300_11 + element.next_500_15 +element.next_500_19 + element.next_160_21 + element.next_320_24

    
    @api.depends('annual_gross_income')
    def _compute_min_tax(self):
        for element in self:
            element.min_tax = 0
            if element.annual_gross_income  <= 30000:
                element.min_tax = 0.01 * element.annual_gross_income
            
    @api.depends('annual_paye')
    def _compute_month_paye(self):
        for element in self:
            element.month_paye = element.annual_paye / 12
          
    
    @api.depends('pension')
    def _compute_month_pension(self):
        for element in self:
            element.month_pension = element.pension / 12
          

    @api.depends('nhf_annual')
    def _compute_month_nhf(self):
        for element in self:
            element.month_nhf = element.nhf_annual / 12
          

    @api.depends('month_paye','month_pension','month_nhf')
    def _compute_deduction(self):
        for element in self:
            element.deduction = element.month_paye  + element.month_pension + element.month_nhf
          

    @api.depends('gross_monthly','deduction')
    def _compute_net_payout(self):
        for element in self:
            element.net_payout = element.gross_monthly  - element.deduction
     

    
    @api.depends('basic_salary','housing_allow' ,'transport')
    def _computte_employee_pension_month(self):
        for element in self:
            element.employee_pension_month = 0.1 * ( element.basic_salary + element.housing_allow + element.transport)
     

    @api.depends('basic_salary','housing_allow' ,'transport')
    def _computte_nsitf(self):
        for element in self:
            element.nsitf = 0.01 * ( element.basic_salary + element.housing_allow + element.transport)
     
    
    @api.depends('gross_monthly')
    def _computte_itf(self):
        for element in self:
            element.itf = 0.01 * element.gross_monthly


    @api.depends('gross_monthly' , 'employee_pension_month' , 'nsitf' , 'itf')
    def _computte_total_cost_to_company(self):
        for element in self:
            element.total_cost_to_company = element.gross_monthly + element.employee_pension_month + element.nsitf + element.itf


    
    