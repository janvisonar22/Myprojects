from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_custom_wizard(self):
        return {
            'name': 'Custom Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.custom.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
            },
        }
