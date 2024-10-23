from odoo import models, api, fields, _

class OvertimeGuide(models.Model):
    _name = 'overtime.guide'

    company_id = fields.Many2one('res.company', string="Company")
    week = fields.Char("Week")
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    overtime_guide_line_ids = fields.One2many('overtime.guide.line', 'overtime_guide_id', string="Staff Lines")

class OvertimeGuideLine(models.Model):
    _name = 'overtime.guide.line'

    name = fields.Many2one('hr.employee', string="Name")
    designation = fields.Char("Designation")
    day = fields.Char("Day")
    remarks = fields.Char("Remarks")
    amount = fields.Integer("Amount")
    overtime_guide_id = fields.Many2one('overtime.guide',string="Overtime Guide")

    @api.onchange('name')
    def onchange_name(self):
        self.designation = ''
        if self.name and self.name.work_location:
            self.designation = self.name.work_location