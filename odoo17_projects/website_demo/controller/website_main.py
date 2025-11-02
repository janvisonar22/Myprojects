from odoo import http
from odoo.http import request

class WebsiteBio(http.Controller):
	@http.route('/biography',type="http",auth="public",website=True)
	def website_biography(self):
		bio_records=request.env['bio.website'].search([])
		values={
			'bio_records':bio_records
		}
		return request.render('website_demo.website_bio',values)