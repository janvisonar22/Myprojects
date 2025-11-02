from odoo import models, api, _ , fields
from collections import defaultdict


class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	order_line_warehouse_id = fields.Many2one(
		"stock.warehouse",
		string="Warehouse",
	)


	def _prepare_procurement_values(self, group_id=False):
		"""Include warehouse_id in procurement values so warehouse-aware logic can use it."""
		vals = super()._prepare_procurement_values(group_id=group_id)
		# When a line has a warehouse set, pass the warehouse id into procurement vals
		if self.order_line_warehouse_id:
			vals['warehouse_id'] = self.order_line_warehouse_id.id
		return vals

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def _create_picking_for_warehouse(self, warehouse, so_lines, picking_type=None):
		"""Create a picking for a given warehouse and attach those stock.move lines."""
		StockPicking = self.env['stock.picking']
		print("\n\nStockPicking==>>",StockPicking)
		StockMove = self.env['stock.move']

		# Determine default picking type for warehouse (sale type)
		if not picking_type:
			picking_type = warehouse.out_type_id  # standard way to get outgoing picking type

		vals = {
			'picking_type_id': picking_type.id,
			'location_id': picking_type.default_location_src_id.id,
			'location_dest_id': picking_type.default_location_dest_id.id,
			'partner_id': self.partner_shipping_id.id,
			'origin': self.name,
			'sale_id': self.id,
			'company_id': self.company_id.id,
		}
		picking = StockPicking.create(vals)

		# Create stock moves for each sale.order.line in this warehouse group
		for line in so_lines:
			# Reuse line._prepare_stock_moves if available — fallback to simple move creation
			# Many Odoo versions implement _prepare_procurement_values -> procurement creation -> moves
			move_vals = {
				'name': line.name or line.product_id.display_name,
				'product_id': line.product_id.id,
				'product_uom_qty': line.product_uom_qty,
				'product_uom': line.product_uom.id,
				'picking_id': picking.id,
				'picking_type_id': picking_type.id,
				'location_id': picking_type.default_location_src_id.id,
				'location_dest_id': picking_type.default_location_dest_id.id,
				'partner_id': self.partner_shipping_id.id,
				'origin': self.name,
				'sale_line_id': line.id,
				'company_id': self.company_id.id,
			}
			StockMove.create(move_vals)

		return picking

	def _create_picking_split_by_warehouse(self):
		"""Group order lines by warehouse and create pickings per group."""
		# Only process draft or confirmed orders (call from action_confirm)
		# Build mapping: warehouse_id -> lines
		so_lines_by_warehouse = defaultdict(list)
		print("\n\nso_lines_by_warehouse==>>",so_lines_by_warehouse)
		# Determine default warehouse for entire order (if you want fallback)
		default_warehouse = False
		print("\n\ndefault_warehouse==<",default_warehouse)
		# try to find a warehouse from order.warehouse_id if you have such field else fallback to company first warehouse
		if hasattr(self, 'warehouse_id') and self.warehouse_id:
			default_warehouse = self.warehouse_id
		else:
			# find first warehouse of company
			wh = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
			print("\n\nwhwhwhwhwh===>>",wh)
			default_warehouse = wh or False

		for line in self.order_line.filtered(lambda l: l.product_id.type != 'service'):
			wh = line.order_line_warehouse_id or default_warehouse
			print("\n\nwh==>>>",wh)
			if not wh:
				# if no warehouse at all, fallback to any warehouse to avoid crash
				wh = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
			so_lines_by_warehouse[wh.id].append(line)

		pickings = []
		print("\n\npickingspickingspickingspickings->>",pickings)
		for wh_id, lines in so_lines_by_warehouse.items():
			print("\n\nwh_id",wh_id)
			print("\n\nvvvlineslineslineslineslines==>>",lines)
			wh = self.env['stock.warehouse'].browse(wh_id)
			picking = self._create_picking_for_warehouse(warehouse=wh, so_lines=lines)
			pickings.append(picking)

		return pickings

	def action_confirm(self):
		"""Override confirmation so pickings are created per-line-warehouse."""
		# you may want to keep the standard flow that creates procurements and then pickings.
		# To avoid duplicating procurement logic, one way is to call super() then move pickings afterwards.
		# But simpler and more deterministic: call super to perform usual checks and creation,
		# then split pickings if a per-line warehouse is used.
		res = super().action_confirm()
		print("\n\nres+++...",res)
		# Only split if any line has order_line_warehouse_id set
		if any(self.order_line.mapped('order_line_warehouse_id')):
			# Remove the standard pickings created by default (optional approach) and recreate grouped pickings.
			# Safer approach: if you don't want duplicates, delete auto-created pickings that belong to this sale and are in draft.
			auto_pickings = self.picking_ids.filtered(lambda p: p.state in ('draft', 'waiting'))
			print("\n\nauto_pickings=======>>>",auto_pickings)
			if auto_pickings:
				auto_pickings.unlink()

			# Create grouped pickings
			created = self._create_picking_split_by_warehouse()
			print("\n\ncreatedcreated-->><><>",created)
			# post-process: confirm/reserve moves if you want
			for p in created:
				print("\n\nppppppppppp====>>>",p)
				p.action_confirm()   # confirm the picking
				# optionally run reservation
				try:
					p.action_confirm()
					p._action_assign()
				except Exception:
					pass

		return res


