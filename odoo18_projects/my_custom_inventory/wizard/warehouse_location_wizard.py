# -*- coding: utf-8 -*-
from odoo import models, fields, api
import io
import base64
import xlsxwriter

class WarehouseLocationWizard(models.TransientModel):
	_name = "warehouse.location.wizard"
	_description = "Warehouse Location Wizard"

	warehouse_id = fields.Many2one(
		"stock.warehouse",
		string="Warehouse",
		required=True
	)
	product_ids = fields.Many2many("product.product", string="Products")
	start_date = fields.Datetime(string="Start Date")
	end_date = fields.Datetime(string="End Date")

	file_data = fields.Binary("File", readonly=True)
	file_name = fields.Char("Filename")

	# @api.onchange('warehouse_id')
	# def _onchange_warehouse_id(self):
	# 	"""Auto-load products for selected warehouse"""
	# 	if self.warehouse_id:
	# 		# उस warehouse की internal locations लो
	# 		locations = self.env['stock.location'].search([
	# 			('usage', '=', 'internal'),
	# 			('id', 'child_of', self.warehouse_id.view_location_id.id)
	# 		])
	# 		# Quant से products निकालो
	# 		products = self.env['stock.quant'].search([
	# 			('location_id', 'in', locations.ids)
	# 		]).mapped('product_id')
	# 		self.product_ids = [(6, 0, products.ids)]
	# 	else:
	# 		self.product_ids = [(5, 0, 0)]

	def _get_stock_movements(self):
		"""Fetch stock moves for selected warehouse/products"""
		domain = [('state', '=', 'done')]
		if self.start_date:
			domain.append(('date', '>=', self.start_date))
		if self.end_date:
			domain.append(('date', '<=', self.end_date))

		if self.product_ids:
			domain.append(('product_id', 'in', self.product_ids.ids))

		if self.warehouse_id:
			print("self,warehouseid==???",self.warehouse_id)
			# उस warehouse की locations filter करो
			locations = self.env['stock.location'].search([
				('usage', '=', 'internal'),
				('id', 'child_of', self.warehouse_id.view_location_id.id)
			])
			domain += ['|',
				('location_id', 'in', locations.ids),
				('location_dest_id', 'in', locations.ids)
			]

		moves = self.env['stock.move'].search(domain, order="date asc")
		print("\n\nmoves++++...",moves)
		data = []
		for move in moves:
			print("\n\ndatadata--??",data)
			data.append({
				'product': move.product_id.display_name,
				'from': move.location_id.complete_name,
				'to': move.location_dest_id.complete_name,
				'qty': move.product_uom_qty,
				'date': move.date,
			})
		return data

	def action_print_xlsx(self):
		stock_data = self._get_stock_movements()

		# Excel in memory
		output = io.BytesIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		sheet = workbook.add_worksheet("Stock Movements")

		# Header
		header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
		headers = ["Product", "From Location", "To Location", "Quantity", "Date"]
		for col, name in enumerate(headers):
			sheet.write(0, col, name, header_format)

		# Rows
		row = 1
		for line in stock_data:
			sheet.write(row, 0, line['product'])
			sheet.write(row, 1, line['from'])
			sheet.write(row, 2, line['to'])
			sheet.write(row, 3, line['qty'])
			sheet.write(row, 4, line['date'])
			row += 1

		workbook.close()
		xlsx_data = output.getvalue()
		output.close()

		# Save file
		filename = "stock_movements.xlsx"
		self.write({
			"file_data": base64.b64encode(xlsx_data),
			"file_name": filename,
		})

		# Download
		return {
			'type': 'ir.actions.act_url',
			'url': f"/web/content/{self._name}/{self.id}/file_data/{filename}?download=true",
			'target': 'self',
		}
	# def action_print_pdf(self):
	# 	"""Generate PDF report for selected warehouse and products"""
	# 	stock_data = self._get_stock_movements()

	# 	datas = {
	# 		'warehouse': self.warehouse_id.display_name if self.warehouse_id else '',
	# 		'start_date': self.start_date,
	# 		'end_date': self.end_date,
	# 		'product_data': stock_data,
	# 	}

	# 	return self.env.ref('my_custom_inventory.action_my_stock_pdf').report_action(
	# 		self,
	# 		data=datas
	# 	)
		# data = self._get_stock_movements()  # same as XLSX
		# return self.env.ref("my_custom_inventory.action_my_stock_pdf").report_action(
		# 	self, data={'product_data': data,
		# 				'warehouse': self.warehouse_id,
		# 				'start_date': self.start_date,
		# 				'end_date': self.end_date}
		# )



	# def action_print_pdf(self):
	# 	"""Generate PDF report for selected warehouse and products"""
	# 	stock_data = self._get_stock_movements()
	# 	print("\n\nstock_data===>>>",stock_data)
	# 	datas = {
	# 		# 'docs': self,  # Wizard ka record pass kar rahe hain
	# 		'product_data': stock_data,
	# 	}
	# 	print("\n\ndatas===>>",datas)
	# 	return self.env.ref('my_custom_inventory.action_my_stock_pdf').report_action(
	# 		self, data=datas
	# 	)
	def action_print_pdf(self):
		stock_data = self._get_stock_movements()
		datas = {
			'product_data': stock_data,
		}
		return self.env.ref('my_custom_inventory.action_my_stock_pdf').report_action(
			self, data=datas
		)
