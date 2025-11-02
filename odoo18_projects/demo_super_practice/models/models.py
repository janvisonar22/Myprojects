from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # custom logic before calling parent method
        print("Custom logic before confirming sale order")

        # call the original method from parent class
        res = super(SaleOrder, self).action_confirm()

        # custom logic after calling parent method
        print("Custom logic after confirming sale order")

        return res
