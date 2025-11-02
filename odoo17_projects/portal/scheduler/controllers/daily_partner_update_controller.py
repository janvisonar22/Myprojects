from odoo import http
from odoo.http import request

class CustomPortalController(http.Controller):

    @http.route(['/my/custom-portal'], type='http', auth="user", website=True)
    def custom_portal_page(self, **kwargs):
        values = {
            'custom_data': 'Hello from custom portal!',
        }
        return request.render('scheduler.custom_portal_template', values)
