from odoo import fields, models, api


class Contract(models.Model):
    _inherit = 'hr.contract'

    state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Active'),
        ('resigned', 'Resigned'),
        ('close', 'Terminated'),
        ('suspended', 'Suspended'),
        ('retired', 'Retired'),
        ('cancel', 'Cancelled')
    ], string='Status', group_expand='_expand_states', copy=False,
        tracking=True, help='Status of the contract', default='draft')
