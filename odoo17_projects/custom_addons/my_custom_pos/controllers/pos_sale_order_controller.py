from odoo import http
from odoo.http import request

class PosSaleOrderController(http.Controller):

	@http.route('/pos/create_sale_order', type='json', auth='user')
	def create_sale_order(self, partner_id=None, orderlines=None):
		""" Create Sale Order from POS """
		print("partner_id:", partner_id)

		print("POS Create Sale Order Called")
		if not partner_id:
			return {'success': False, 'error': 'Customer not selected'}
		if not orderlines:
			return {'success': False, 'error': 'No products in order'}

		lines = [(0, 0, {
			'product_id': l['product_id'],
			'product_uom_qty': l['product_uom_qty'],
			'price_unit': l['price_unit'],
			'name': l.get('name', ''),
		}) for l in orderlines]

		order = request.env['sale.order'].sudo().create({
			'partner_id': partner_id,
			'order_line': lines,
		})

		return {'success': True, 'order_id': order.id, 'order_name': order.name}
