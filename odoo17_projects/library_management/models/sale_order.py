# from odoo import models
# import io
# import base64
# import xlsxwriter
#------------>direct download xlsx
# class SaleOrder(models.Model):
# 	_inherit = 'sale.order'

# 	def action_download_xlsx(self):
# 		"""Generate XLSX for current sale order."""
# 		# Create an in-memory file
# 		output = io.BytesIO()
# 		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
# 		sheet = workbook.add_worksheet("Sale Order")

# 		# Add headers
# 		headers = ["Order Name", "Customer", "Date", "Total"]
# 		for col, header in enumerate(headers):
# 			sheet.write(0, col, header)

# 		# Add data
# 		for row, order in enumerate(self, start=1):
# 			sheet.write(row, 0, order.name)
# 			sheet.write(row, 1, order.partner_id.name)
# 			sheet.write(row, 2, str(order.date_order))
# 			sheet.write(row, 3, order.amount_total)

# 		workbook.close()

# 		# Prepare file for download
# 		file_data = output.getvalue()
# 		output.close()

# 		# attachment = self.env['ir.attachment'].create({
# 		# 	'name': f"{self.name}.xlsx",
# 		# 	'type': 'binary',
# 		# 	'datas': base64.b64encode(file_data),
# 		# 	'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
# 		# })

# 		# download_url = f'/web/content/{attachment.id}?download=true'
# 		# return {
# 		# 	'type': 'ir.actions.act_url',
# 		# 	'url': download_url,
# 		# 	'target': 'self',
# 		# }
from odoo import models, fields, api
#------------>in wizard in download xlsx

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def action_download_xlsx(self):
		return {
			'name': 'Sale Order XLSX Wizard',
			'type': 'ir.actions.act_window',
			'res_model': 'sale.order.xlsx.wizard',
			'view_mode': 'form',
			'target': 'new',
			'context': {
				'active_ids': self.ids,
				'active_model': 'sale.order',
			}
		}

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	name = fields.Char(string="Product Name")

	@api.onchange('product_id')
	def _onchange_product_template_id(self):
		product_id = self.env['product.template'].search([('id','=',self.product_template_id.id)])
		print("\n\nproduct_id==>",product_id)
		self.name=product_id.name