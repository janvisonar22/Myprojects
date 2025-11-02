from odoo import http
from odoo.http import request 

class SaleData(http.Controller):
	@http.route('/salesdata',type='http',auth='public',website=True)

	def sale_data(self,**post):
		sale_data = request.env['sale.order'].sudo().search([])
		print(sale_data)
		values={
			'record' : sale_data
		}
		return request.render('library_management.tmp_sales_data',values)