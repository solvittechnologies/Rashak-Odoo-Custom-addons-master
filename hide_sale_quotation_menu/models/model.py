# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        record.action_confirm()
        return record
    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        record = super(PurchaseOrder, self).create(vals)
        record.button_confirm()  # Confirmer le bon de commande automatiquement
        return record
    


