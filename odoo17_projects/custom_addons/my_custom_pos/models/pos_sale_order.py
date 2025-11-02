from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create_sale_order_from_pos(self, partner_id, order_lines):
        """Create Sale Order from POS"""
        if not partner_id or not order_lines:
            return {'success': False, 'error': 'Missing data'}

        lines = [(0, 0, {
            'product_id': l['product_id'],
            'product_uom_qty': l['quantity'],
            'price_unit': l['price'],
            'discount': l.get('discount', 0),
        }) for l in order_lines]

        order = self.create({
            'partner_id': partner_id,
            'order_line': lines,
        })

        return {'success': True, 'order_id': order.id, 'order_name': order.name}
