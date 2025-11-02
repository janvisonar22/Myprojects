from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
import xlsxwriter

class ReportMenuWizard(models.TransientModel):
	"""
	Wizard for Generating Report from E-Commerce Bidding
	"""
	_name = 'report.menu.wizard'
	_description = 'Quotation Report Wizard for Ecom Sale Website'

	# ------------------------------
	# Fields
	# ------------------------------
	start_date = fields.Date(
		string="Start Date",
		required=True,
		default=fields.Date.context_today
	)
	end_date = fields.Date(
		string="End Date",
		required=True
	)
	file_data = fields.Binary("File")
	file_name = fields.Char("File Name")

	# ------------------------------
	# Methods
	# ------------------------------
	def action_confirm_quotation(self):
		"""
		Generate PDF report of ecom.sale.website records between dates
		"""
		if self.start_date > self.end_date:
			raise UserError("End Date must be greater than Start Date.")

		# Fetch records in date range
		domain = [
			('create_date', '>=', self.start_date),
			('create_date', '<=', self.end_date),
		]
		records = self.env['ecom.sale.website'].search(domain)

		if not records:
			raise UserError("No records found in this date range.")

		# Call QWeb PDF report
		return self.env.ref('ecom_sale_website.action_report_ecom_bidding_pdf').report_action(records)
	def action_export_xlsx(self):
		""" Generate XLSX without report action """
		if self.start_date > self.end_date:
			raise UserError("End Date must be greater than Start Date.")

		# Fetch records
		domain = [
			('create_date', '>=', self.start_date),
			('create_date', '<=', self.end_date),
		]
		records = self.env['ecom.sale.website'].search(domain)

		if not records:
			raise UserError("No records found in this date range.")

		# Create in-memory file
		output = io.BytesIO()
		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
		sheet = workbook.add_worksheet("Bidding Report")

		# Formats
		bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
		date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

		# Headers
		headers = ["Customer", "Contact", "Product", "Price", "Suggestion Price", "Created On"]
		for col, header in enumerate(headers):
			sheet.write(0, col, header, bold)

		row = 1
		for rec in records:
			sheet.write(row, 0, rec.customer_id.name or '')              # Customer
			sheet.write(row, 1, rec.contact.name if rec.contact else '') # Contact
			sheet.write(row, 2, rec.product_id.name or '')               # Product
			sheet.write(row, 3, rec.price or 0.0)                        # Price
			sheet.write(row, 4, rec.suggestion_price or 0.0)             # Suggestion Price
			# Create Date formatted
			if rec.create_date:
				sheet.write_datetime(row, 5, rec.create_date, date_format)
			else:
				sheet.write(row, 5, '')
			row += 1

		workbook.close()
		file_data = base64.b64encode(output.getvalue())
		output.close()

		# Set values in wizard
		self.write({
			'file_data': file_data,
			'file_name': f"bidding_report_{self.start_date}_{self.end_date}.xlsx"
		})

		# Return download popup
		return {
			'type': 'ir.actions.act_url',
			'url': f"/web/content/?model={self._name}&id={self.id}&field=file_data&filename_field=file_name&download=true",
			'target': 'self',
		}
