# from odoo import models, fields

# class SaleOrderXlsxWizard(models.TransientModel):
# 	_name = "sale.order.xlsx.wizard"
# 	_description = "Sale Order XLSX Wizard"

# 	file_name = fields.char(string='name')
# 	attachment_id = fields.Many2one(
# 		'ir.attachment',
# 		string="Attachment",
# 		help="Select the file you want to link"
# 	)

from odoo import models, fields, api
import io
import base64
import xlsxwriter


class SaleOrderXlsxWizard(models.TransientModel):
	_name = "sale.order.xlsx.wizard"
	_description = "Sale Order XLSX Wizard"

	file_name = fields.Char(string='File Name', readonly=True)
	attachment_id = fields.Many2one(
		'ir.attachment',
		string="Attachment",
		readonly=True
	)

	@api.model
	def default_get(self, fields_list):
		"""Generate the XLSX file when the wizard opens."""
		res = super().default_get(fields_list)

		active_ids = self.env.context.get('active_ids', [])
		orders = self.env['sale.order'].browse(active_ids)

		# Create XLSX in memory
		output = io.BytesIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		sheet = workbook.add_worksheet("Sale Order")

		# Headers
		headers = ["Order Name", "Customer", "Date", "Total"]
		for col, header in enumerate(headers):
			sheet.write(0, col, header)

		# Data
		for row, order in enumerate(orders, start=1):
			sheet.write(row, 0, order.name)
			sheet.write(row, 1, order.partner_id.name)
			sheet.write(row, 2, str(order.date_order))
			sheet.write(row, 3, order.amount_total)

		workbook.close()
		file_data = output.getvalue()
		output.close()

		# Create attachment
		attachment = self.env['ir.attachment'].create({
			'name': f"SaleOrders.xlsx",
			'type': 'binary',
			'datas': base64.b64encode(file_data),
			'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
		})

		res.update({
			'file_name': attachment.name,
			'attachment_id': attachment.id,
		})
		return res

	def action_download_file(self):
		"""Return the file as a downloadable link."""
		return {
			'type': 'ir.actions.act_url',
			'url': f'/web/content/{self.attachment_id.id}?download=true',
			'target': 'self',
		}


