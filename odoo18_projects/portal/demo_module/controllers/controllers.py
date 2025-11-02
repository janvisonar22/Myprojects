from odoo import http, _
from odoo.http import request

class SaleOrderPortal(http.Controller):

	@http.route(['/my/sale_orders'], type='http', auth="user", website=True)
	def portal_my_sale_orders(self, page=1, **kw):
		SaleOrder = request.env['sale.order']
		partner = request.env.user.partner_id
		values = {}

		domain = [
			('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
			('state', 'in', ['sale', 'done'])
		]

		# --- Sorting (date wise desc) ---
		sort_order = "date_order desc"

		# --- Fetch orders ---
		orders = SaleOrder.sudo().search(domain, order=sort_order)

		print("\n\n Current Partner:", partner.name, partner.id)
		print("Fetched Orders:", orders.ids)

		values.update({
			'orders': orders,
			'page_name': 'sale_order',
			'default_url': '/my/sale_orders',
		})
		return request.render("demo_module.portal_my_sale_orders_custom", values)
