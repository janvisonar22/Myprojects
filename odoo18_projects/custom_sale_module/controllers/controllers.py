# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSaleModule(http.Controller):
#     @http.route('/custom_sale_module/custom_sale_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_module/custom_sale_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_module.listing', {
#             'root': '/custom_sale_module/custom_sale_module',
#             'objects': http.request.env['custom_sale_module.custom_sale_module'].search([]),
#         })

#     @http.route('/custom_sale_module/custom_sale_module/objects/<model("custom_sale_module.custom_sale_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_module.object', {
#             'object': obj
#         })

