from odoo import models, fields, api

class StockWarehouse(models.Model):
	_inherit = "stock.warehouse"

	total_stock_value = fields.Monetary(
		string="Total Stock Value",
		compute="_compute_total_stock_value",
		currency_field="currency_id",
		store=False
	)

	currency_id = fields.Many2one(
		"res.currency",
		string="Currency",
		default=lambda self: self.env.company.currency_id
	)

	@api.depends("lot_stock_id")
	def _compute_total_stock_value(self):
		"""Compute total stock value per warehouse = qty_available * standard_price"""
		Product = self.env["product.product"]
		print("\n\nProduct====???",Product)
		for warehouse in self:
			print("\n\nwarehousewarehousewarehousewarehouse--->>",warehouse)
			# all internal locations under warehouse
			locations = self.env["stock.location"].search([
				("id", "child_of", warehouse.view_location_id.id),
				("usage", "=", "internal"),
			])
			products = Product.search([])
			print("\n\n====products++++???>>>",products)
			total_value = 0.0

			for product in products:
				qty = product.with_context(
					location=locations.ids
				).qty_available
				total_value += qty * product.standard_price
				print("\n\n\ntotal_value==>><<<<",total_value)
			warehouse.total_stock_value = total_value
			print("\n\nwarehouse.total_stock_value--->>",warehouse.total_stock_value)