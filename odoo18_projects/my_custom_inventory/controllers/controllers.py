# -*- coding: utf-8 -*-
# from odoo import http


# class MyCustomInventory(http.Controller):
#     @http.route('/my_custom_inventory/my_custom_inventory', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_custom_inventory/my_custom_inventory/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_custom_inventory.listing', {
#             'root': '/my_custom_inventory/my_custom_inventory',
#             'objects': http.request.env['my_custom_inventory.my_custom_inventory'].search([]),
#         })

#     @http.route('/my_custom_inventory/my_custom_inventory/objects/<model("my_custom_inventory.my_custom_inventory"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_custom_inventory.object', {
#             'object': obj
#         })

