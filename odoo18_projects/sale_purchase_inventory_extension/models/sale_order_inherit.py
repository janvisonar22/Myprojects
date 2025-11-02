from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
	_inherit = 'sale.order'



	# Existing field
	purchase_order_ids = fields.One2many('purchase.order', 'sale_id', string="Purchase Orders")
	
	# New field: Related Receipts/Stock Pickings
	picking_ids = fields.One2many('stock.picking', 'sale_id', string="Related Pickings")
	def action_view_purchase_orders(self):
		self.ensure_one()
		action = self.env.ref('purchase.purchase_rfq').read()[0]
		action['domain'] = [('sale_id', '=', self.id)]
		action['context'] = {'default_sale_id': self.id}
		return action
	def action_view_pickings(self):
		self.ensure_one()
		action = self.env.ref('stock.action_picking_tree_all').read()[0]  # Default tree action for stock pickings
		action['domain'] = [
			('sale_id', '=', self.id),
			('picking_type_code', '=', 'incoming')# Show only receipts
		]
		action['context'] = {'default_sale_id': self.id}
		return action

	def action_confirm(self):
		"""
		Confirm sale order(s) then automatically create purchase orders (POs)
		for products that have stock shortages.
		Each PO will be grouped by vendor.
		"""
		# ✅ Step 1: Run Odoo’s standard sale order confirmation process
		res = super(SaleOrder, self).action_confirm()
		print("\n\nres===", res)

		# ✅ Step 2: Initialize the Purchase Order model for later use
		Purchase = self.env['purchase.order']
		print("\n\nPurchase===>><<", Purchase)

		# ✅ Step 3: Process each confirmed sale order
		for order in self:
			# Dictionary to store products grouped by vendor
			# Structure: {vendor_id: {'vendor': vendor_record, 'lines': [purchase_line_values, ...]}}
			vendor_lines = {}
			print("\n\nvendor_lines==>>>", vendor_lines)

			# ✅ Step 4: Iterate through each sale order line
			for line in order.order_line:
				print("\n\nline---<<<", line)

				product = line.product_id
				if not product:
					continue  # Skip if no product found

				# ✅ Step 5: Get available stock and ordered quantity
				qty_available = product.qty_available or 0.0
				print("\n\nqty_available-->>", qty_available)
				qty_ordered = line.product_uom_qty or 0.0
				print("\n\nqty_ordered-==>>", qty_ordered)

				# ✅ Step 6: Check if there is a shortage in stock
				if qty_available < qty_ordered:
					required_qty = float(qty_ordered) - float(qty_available)

					# ✅ Step 7: Find a preferred vendor for the product
					seller = False
					if product.seller_ids:
						seller = product.seller_ids[0]  # Prefer product-level vendor
					elif product.product_tmpl_id and product.product_tmpl_id.seller_ids:
						seller = product.product_tmpl_id.seller_ids[0]  # Fallback: template-level vendor

					# ✅ Step 8: Raise error if no vendor is defined
					if not seller:
						raise UserError("Please define a vendor for product %s." % product.display_name)

					# ✅ Step 9: Get vendor partner record
					vendor = getattr(seller, 'name', None) or getattr(seller, 'partner_id', None)
					if not vendor:
						raise UserError("Please define a vendor for product %s." % product.display_name)

					vendor_id = vendor.id

					# ✅ Step 10: Get vendor price from supplier info
					price_unit = line.price_unit or 0.0

					# ✅ Step 11: Prepare values for purchase order line
					pol_vals = {
						'product_id': product.id,
						'name': line.name or product.display_name,
						'product_qty': required_qty,
						'product_uom': line.product_uom.id,
						'price_unit': price_unit,
						'date_planned': fields.Datetime.now(),
					}
					print("\n\npol_vals==>>", pol_vals)

					# ✅ Step 12: Group PO lines by vendor
					vendor_lines.setdefault(vendor_id, {'vendor': vendor, 'lines': []})
					vendor_lines[vendor_id]['lines'].append(pol_vals)

			# ✅ Step 13: Create Purchase Orders grouped by vendor
			for info in vendor_lines.values():
				vendor = info['vendor']
				lines = info['lines']

				# Odoo expects order_line in the format [(0, 0, <vals>), (0, 0, <vals>), ...]
				order_line_vals = [(0, 0, l) for l in lines]

				# ✅ Step 14: Prepare Purchase Order values
				po_vals = {
					'partner_id': vendor.id,
					'date_order': fields.Datetime.now(),
					'origin': order.name,  # Link PO back to Sale Order
					'order_line': order_line_vals,
					'sale_id': order.id,  # Custom link field to trace the origin sale order
				}

				# ✅ Step 15: Create the Purchase Order
				Purchase.create(po_vals)

		# ✅ Step 16: Return the result of sale order confirmation
		return res
