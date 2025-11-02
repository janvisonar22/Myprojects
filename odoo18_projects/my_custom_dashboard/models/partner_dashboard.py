# from odoo import models, fields, api

# class PartnerDashboard(models.TransientModel):
# 	_name = 'partner.dashboard'
# 	_description = 'Partner Dashboard'

# 	partner_id = fields.Many2one('res.partner', string="Customer", required=True)
# 	sale_order_ids = fields.One2many('sale.order', compute="_compute_sale_orders", string=" Sale Orders")


# 	sale_order_count = fields.Integer(string="Sale Order Count", compute="_compute_sale_orders")

# 	@api.depends('partner_id')
# 	def _compute_sale_orders(self):
# 		for rec in self:
# 			if rec.partner_id:
# 				orders = self.env['sale.order'].search([('partner_id', '=', rec.partner_id.id)])
# 				rec.sale_order_ids = orders
# 				rec.sale_order_count = len(orders)
# 			else:
# 				rec.sale_order_ids = False
# 				rec.sale_order_count = 0

# 	def action_get_sale_orders(self):
# 		self.ensure_one()
# 		return {
# 			'type': 'ir.actions.act_window',
# 			'name': 'Sale Orders',
# 			'res_model': 'sale.order',
# 			'view_mode': 'list,form',
# 			'domain': [('partner_id', '=', self.partner_id.id)],
# 			'context': {'default_partner_id': self.partner_id.id},
# 			'target': 'current',
# 			'views': [
# 				(self.env.ref('sale.view_order_tree').id, 'list'),
# 				(self.env.ref('sale.view_order_form').id, 'form'),
# 			],
# 		}


from odoo import api,fields,models,_
import time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from datetime import datetime,timedelta
from babel.dates import format_datetime,format_date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF,DEFAULT_SERVER_DATETIME_FORMAT as DTF,format_datetime as tool_format_datetime
from odoo.release import version
import json
class PartnerDashboard(models.TransientModel):
	_name = 'partner.dashboard'
	_description = 'Partner Dashboard'
	_rec_name = 'display_name'

	display_name = fields.Char(string="Display Name", compute="_compute_display_name", store=True)
	@api.depends('partner_id')
	def _compute_display_name(self):
		for rec in self:
			if rec.partner_id:
				rec.display_name = f"Dashboard - {rec.partner_id.name}"
			else:
				rec.display_name = "Dashboard (No Partner)"

	partner_id = fields.Many2one('res.partner', string="Customer", required=True)
	
	sale_order_ids = fields.One2many('sale.order', compute="_compute_orders", string="Sale Orders")
	sale_order_count = fields.Integer(string="Sale Order Count", compute="_compute_orders")
	button_label = fields.Char(string="Sale order count", compute="_compute_button_label")
	total_amount = fields.Monetary(string="Total Amount", compute="_compute_orders", currency_field='company_currency_id')
	company_currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
	
	# Status counts
	draft_sale_count = fields.Integer(string="Quotation", compute="_compute_orders")
	sent_sale_count = fields.Integer(string="Quotation Sent", compute="_compute_orders")
	confirmed_sale_count = fields.Integer(string="Confirmed Orders", compute="_compute_orders")
	done_sale_count = fields.Integer(string="Done Orders", compute="_compute_orders")
	cancel_sale_count = fields.Integer(string="Cancelled Orders", compute="_compute_orders")

	# Sale Orders Graph
	# sale_order_bar_graph = fields.Text(compute='_compute_sale_order_graph')
	# sale_order_bar_graph_color = fields.Char(string='Sale Orders Bar Chart Color', default="#1f77b4")



	# FOR PURCHASE ORDERS
	purchase_order_ids = fields.One2many(
		'purchase.order', compute="_compute_orders",string="Purchase Orders", readonly=True
	)
	purchase_order_count = fields.Integer(string="Purchase Order Count", compute="_compute_orders")
	total_purchase_amount = fields.Monetary(string="Total Purchase Amount", compute="_compute_orders", currency_field='company_currency_id')
	draft_purchase_count = fields.Integer(string="RFQ (Draft)", compute="_compute_orders")
	sent_purchase_count = fields.Integer(string="RFQ Sent", compute="_compute_orders")
	confirmed_purchase_count = fields.Integer(string="Confirmed Purchase Orders", compute="_compute_orders")
	done_purchase_count = fields.Integer(string="Done Purchase Orders", compute="_compute_orders")
	cancel_purchase_count = fields.Integer(string="Cancelled Purchase Orders", compute="_compute_orders")

	company_currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

	@api.depends('sale_order_count')
	def _compute_button_label(self):
		for rec in self:
			rec.button_label = f"View Sale Orders ({rec.sale_order_count})"

	@api.depends('partner_id')
	def _compute_orders(self):
		for rec in self:
			if rec.partner_id:
				# Sale Orders
				sale_orders = self.env['sale.order'].search([('partner_id', '=', rec.partner_id.id)])
				rec.sale_order_ids = sale_orders
				rec.sale_order_count = len(sale_orders)
				rec.total_amount = sum(sale_orders.mapped('amount_total'))
				rec.draft_sale_count = len(sale_orders.filtered(lambda o: o.state == 'draft'))
				rec.sent_sale_count = len(sale_orders.filtered(lambda o: o.state == 'sent'))
				rec.confirmed_sale_count = len(sale_orders.filtered(lambda o: o.state == 'sale'))
				rec.done_sale_count = len(sale_orders.filtered(lambda o: o.state == 'done'))
				rec.cancel_sale_count = len(sale_orders.filtered(lambda o: o.state == 'cancel'))

				# Purchase Orders
				purchase_orders = self.env['purchase.order'].search([('partner_id', '=', rec.partner_id.id)])
				rec.purchase_order_ids = purchase_orders
				rec.purchase_order_count = len(purchase_orders)
				rec.total_purchase_amount = sum(purchase_orders.mapped('amount_total'))

				rec.draft_purchase_count = len(purchase_orders.filtered(lambda o: o.state == 'draft'))
				rec.sent_purchase_count = len(purchase_orders.filtered(lambda o: o.state == 'sent'))
				rec.confirmed_purchase_count = len(purchase_orders.filtered(lambda o: o.state == 'purchase'))
				rec.done_purchase_count = len(purchase_orders.filtered(lambda o: o.state == 'done'))
				rec.cancel_purchase_count = len(purchase_orders.filtered(lambda o: o.state == 'cancel'))

			else:
				# Sales Defaults
				rec.sale_order_ids = False
				rec.sale_order_count = 0
				rec.total_amount = 0.0
				rec.draft_sale_count = 0
				rec.sent_sale_count = 0
				rec.confirmed_sale_count = 0
				rec.done_sale_count = 0
				rec.cancel_sale_count = 0

				# Purchases Defaults
				rec.purchase_order_ids = False
				rec.purchase_order_count = 0
				rec.total_purchase_amount = 0.0
				rec.draft_purchase_count = 0
				rec.sent_purchase_count = 0
				rec.confirmed_purchase_count = 0
				rec.done_purchase_count = 0
				rec.cancel_purchase_count = 0

	def action_count_sale_orders(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Sale Orders',
			'res_model': 'sale.order',
			'view_mode': 'list,form',
			'domain': [('partner_id', '=', self.partner_id.id)],
			'target': 'current',
		}
	# def action_view_confirmed_orders(self):
	# 	self.ensure_one()
	# 	return {
	# 		'type': 'ir.actions.act_window',
	# 		'name': 'Confirmed Orders',
	# 		'res_model': 'sale.order',
	# 		'view_mode': 'list,form',
	# 		'domain': [('partner_id', '=', self.partner_id.id), ('state', '=', 'sale')],
	# 		'target': 'current',
	# 	}

	# def action_view_draft_orders(self):
	# 	self.ensure_one()
	# 	return {
	# 		'type': 'ir.actions.act_window',
	# 		'name': 'Draft Orders',
	# 		'res_model': 'sale.order',
	# 		'view_mode': 'list,form',
	# 		'domain': [('partner_id', '=', self.partner_id.id), ('state', '=', 'draft')],
	# 		'target': 'current',
	# 	}

	def action_view_draft_sales(self):
		self.ensure_one()
		return self._open_sale_action("Quotations", [('state', '=', 'draft')])

	def action_view_sent_sales(self):
		self.ensure_one()
		return self._open_sale_action("Quotation Sent", [('state', '=', 'sent')])

	def action_view_confirmed_sales(self):
		self.ensure_one()
		return self._open_sale_action("Confirmed Sales Orders", [('state', '=', 'sale')])

	def action_view_done_sales(self):
		self.ensure_one()
		return self._open_sale_action("Done Sales Orders", [('state', '=', 'done')])

	def action_view_cancelled_sales(self):
		self.ensure_one()
		return self._open_sale_action("Cancelled Sales Orders", [('state', '=', 'cancel')])

	def _open_sale_action(self, name, domain):
		return {
			'type': 'ir.actions.act_window',
			'name': name,
			'res_model': 'sale.order',
			'view_mode': 'list,form',
			'domain': [('partner_id', '=', self.partner_id.id)] + domain,
			'target': 'current',
		}


	# ----------------------------
	# SALE ORDER GRAPH
	# ----------------------------
# ----------------------------
# SALE ORDER QTY vs PRICE GRAPH
# ----------------------------
	qty_price_graph = fields.Text(compute='_compute_qty_price_graph')
	sale_order_line_ids = fields.One2many(
		'sale.order.line', compute="_compute_orders", string="Sale Order Lines"
	)

	@api.depends('partner_id')
	def _compute_qty_price_graph(self):
		for rec in self:
			if not rec.partner_id:
				print("⚠️ No partner selected, empty graph data")
				rec.qty_price_graph = json.dumps([])
				continue

			sale_lines = self.env['sale.order.line'].search([
				('order_id.partner_id', '=', rec.partner_id.id)
			])
			print(f"📊 Found {len(sale_lines)} sale order lines for partner: {rec.partner_id.name}")

			qty_data = [{'x': l.product_id.display_name, 'y': float(l.product_uom_qty)} for l in sale_lines]
			price_data = [{'x': l.product_id.display_name, 'y': float(l.price_unit)} for l in sale_lines]

			print("✅ Qty Data:", qty_data)
			print("✅ Price Data:", price_data)

			graph_data = [
				{'key': 'Quantity', 'values': qty_data, 'color': '#1f77b4'},
				{'key': 'Unit Price', 'values': price_data, 'color': '#ff7f0e'}
			]

			print("📈 Final Graph Data (JSON):", graph_data)

			rec.qty_price_graph = json.dumps(graph_data)







	# Purchase Order Actions
	def action_count_purchase_orders(self):
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Purchase Orders',
			'res_model': 'purchase.order',
			'view_mode': 'list,form',
			'domain': [('partner_id', '=', self.partner_id.id)],
			'target': 'current',
		}

	# def action_view_confirmed_purchases(self):
	# 	self.ensure_one()
	# 	return {
	# 		'type': 'ir.actions.act_window',
	# 		'name': 'Confirmed Purchases',
	# 		'res_model': 'purchase.order',
	# 		'view_mode': 'list,form',
	# 		'domain': [('partner_id', '=', self.partner_id.id), ('state', '=', 'purchase')],
	# 		'target': 'current',
	# 	}

	# def action_view_draft_purchases(self):
	# 	self.ensure_one()
	# 	return {
	# 		'type': 'ir.actions.act_window',
	# 		'name': 'Draft Purchases',
	# 		'res_model': 'purchase.order',
	# 		'view_mode': 'list,form',
	# 		'domain': [('partner_id', '=', self.partner_id.id), ('state', '=', 'draft')],
	# 		'target': 'current',
	# 	}

	def action_view_draft_purchases(self):
		self.ensure_one()
		return self._open_purchase_action("Draft RFQs", [('state', '=', 'draft')])

	def action_view_sent_purchases(self):
		self.ensure_one()
		return self._open_purchase_action("RFQ Sent", [('state', '=', 'sent')])

	def action_view_confirmed_purchases(self):
		self.ensure_one()
		return self._open_purchase_action("Confirmed Purchases", [('state', '=', 'purchase')])

	def action_view_done_purchases(self):
		self.ensure_one()
		return self._open_purchase_action("Done Purchases", [('state', '=', 'done')])

	def action_view_cancelled_purchases(self):
		self.ensure_one()
		return self._open_purchase_action("Cancelled Purchases", [('state', '=', 'cancel')])

	def _open_purchase_action(self, name, domain):
		return {
			'type': 'ir.actions.act_window',
			'name': name,
			'res_model': 'purchase.order',
			'view_mode': 'list,form',
			'domain': [('partner_id', '=', self.partner_id.id)] + domain,
			'target': 'current',
		}
