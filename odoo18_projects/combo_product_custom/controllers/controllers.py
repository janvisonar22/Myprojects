# -*- coding: utf-8 -*-
# from odoo import http


# class ComboProductCustom(http.Controller):
#     @http.route('/combo_product_custom/combo_product_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/combo_product_custom/combo_product_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('combo_product_custom.listing', {
#             'root': '/combo_product_custom/combo_product_custom',
#             'objects': http.request.env['combo_product_custom.combo_product_custom'].search([]),
#         })

#     @http.route('/combo_product_custom/combo_product_custom/objects/<model("combo_product_custom.combo_product_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('combo_product_custom.object', {
#             'object': obj
#         })

