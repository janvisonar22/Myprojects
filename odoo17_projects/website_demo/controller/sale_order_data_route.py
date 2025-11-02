# from odoo import http
# from odoo.http import request

# class WebsiteSaleOrder(http.Controller):

# 	@http.route('/create-sale-order', type='http', auth="public", website=True, methods=['GET', 'POST'], csrf=False)
# 	def create_sale_order(self, **post):
# 		message = False  # define first so it always exists

# 		if request.httprequest.method == 'POST':
# 			partner_name = post.get('partner_name')
# 			order_date = post.get('date_order')

# 			if partner_name and order_date:
# 				partner = request.env['res.partner'].sudo().create({'name': partner_name})
# 				request.env['sale.order'].sudo().create({
# 					'partner_id': partner.id,
# 					'date_order': order_date,
# 				})
# 				message = "✅ Sale Order created successfully!"
# 			else:
# 				message = "⚠ Please fill in all fields."

# 		return request.render('website_demo.website_sale_order_form', {'message': message})

from odoo import http
from odoo.http import request

class WebsiteSaleOrder(http.Controller):

	@http.route('/create-sale-order', type='http', auth="public", website=True, methods=['GET', 'POST'], csrf=False)
	def create_sale_order(self, **post):
		message = False  # define first so it always exists

		if request.httprequest.method == 'POST':
			partner_name = post.get('partner_name')
			order_date = post.get('date_order')
			product_id = post.get('product_id')   # id of the product
			qty = post.get('quantity')            # quantity for the line

			if partner_name and order_date and product_id and qty:
				# 1️⃣ Create partner
				partner = request.env['res.partner'].sudo().create({'name': partner_name})

				# 2️⃣ Create sale order with order line
				sale_order = request.env['sale.order'].sudo().create({
					'partner_id': partner.id,
					'date_order': order_date,
					'order_line': [(0, 0, {
						'product_id': int(product_id),
						'product_uom_qty': float(qty),
					})]
				})

				message = "✅ Sale Order with line created successfully"
			else:
				message = "Please fill in all fields (Partner, Date, Product, Quantity)."

		return request.render('website_demo.website_sale_order_form', {'message': message})
