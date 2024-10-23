from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    state = fields.Selection(selection_add=
                             [('to_approve', 'To Approve'),
                              ('sent',)], ondelete={'to_approve': 'cascade'})

    def button_send_approve(self):
        self.write({'state': 'to_approve'})

    def action_cancel(self):
        self.state = 'cancel'
