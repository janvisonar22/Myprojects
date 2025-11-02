from odoo import models

class SalesPurchaseReportXlsx(models.AbstractModel):
	_name = 'report.demo_module.report_sales_purchase_xlsx'
	_inherit = 'report.report_xlsx.abstract'

	def generate_xlsx_report(self, workbook, data, records):
		for wizard in records:
			sheet = workbook.add_worksheet("Sales & Purchase")
			bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
			border = workbook.add_format({'border': 1})

			sheet.merge_range('A1:I1', 'Sales And Purchase Report', bold)
			sheet.write(2, 0, 'Partner:', bold)
			sheet.write(2, 1, wizard.partner_id.name)
			sheet.write(3, 0, 'Date Range:', bold)
			sheet.write(3, 1, f"{wizard.start_date} to {wizard.end_date}")

			header = ['Sr.No.', 'Order No.', 'Product', 'Qty', 'Unit Price', 'Tax', 'Total Without Tax', 'Total With Tax', 'Status']
			row = 5
			sheet.write(row, 0, 'Sale Orders', bold)
			row += 1
			sheet.write_row(row, 0, header, bold)
			row += 1

			sales = wizard.get_sales_data()
			if sales:
				for idx, sale in enumerate(sales, 1):
					sheet.write_row(row, 0, [
						idx, sale['order_no'], sale['product'], sale['qty'],
						sale['price'], sale['tax'], sale['total_without_tax'],
						sale['total_with_tax'], sale['status']
					], border)
					row += 1
			else:
				sheet.write(row, 0, 'No Sale Data', border)

			row += 2
			sheet.write(row, 0, 'Purchase Orders', bold)
			row += 1
			sheet.write_row(row, 0, header, bold)
			row += 1

			purchases = wizard.get_purchase_data()
			if purchases:
				for idx, purchase in enumerate(purchases, 1):
					sheet.write_row(row, 0, [
						idx, purchase['order_no'], purchase['product'], purchase['qty'],
						purchase['price'], purchase['tax'], purchase['total_without_tax'],
						purchase['total_with_tax'], purchase['status']
					], border)
					row += 1
			else:
				sheet.write(row, 0, 'No Purchase Data', border)
