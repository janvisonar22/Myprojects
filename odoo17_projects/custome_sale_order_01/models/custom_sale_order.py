from odoo import models, fields ,api

class CustomOrder(models.Model):
	_name = 'custom.order'
	_description = 'Custom Order'

	name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, default='New')
	partner_id = fields.Many2one('res.partner', string='Customer', required=True)
	date_order = fields.Datetime(string='Order Date', required=True, readonly=True, default=fields.Datetime.now)
	order_line = fields.One2many('custom.order.line', 'order_id', string='Order Lines')
	state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], default='draft', string='Status')
	@api.model
	def default_get(self, fields_list):
		res = super().default_get(fields_list)
		sale_order_id = self.env.context.get('default_sale_order_id')
		print("\n\nsaleorder idddddddddddddd=============",sale_order_id)
		if sale_order_id:
			sale_order = self.env['sale.order'].browse(sale_order_id)
			order_lines_vals = []
			for line in sale_order.order_line:
				order_lines_vals.append((0, 0, {
					'product_id': line.product_id.id,
					'product_uom_qty': line.product_uom_qty,
					'price_unit': line.price_unit,
					'name' : line.name,
				}))
			res['order_line'] = order_lines_vals
		return res

class CustomOrderLine(models.Model):
	_name = 'custom.order.line'
	_description = 'Custom Order Line'

	order_id = fields.Many2one('custom.order', string='Order Reference')
	product_id = fields.Many2one('product.product', string='Product')
	name = fields.Char(string='Description')
	product_uom_qty = fields.Float(string='Quantity')
	price_unit = fields.Float(string='Unit Price')
	@api.onchange('product_id')
	def _onchange_product_id(self):
		if self.product_id:
			self.name = self.product_id.name
