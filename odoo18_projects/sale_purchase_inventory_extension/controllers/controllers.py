# -*- coding: utf-8 -*-
# from odoo import http


# class SalePurchaseInventoryExtension(http.Controller):
#     @http.route('/sale_purchase_inventory_extension/sale_purchase_inventory_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_purchase_inventory_extension/sale_purchase_inventory_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_purchase_inventory_extension.listing', {
#             'root': '/sale_purchase_inventory_extension/sale_purchase_inventory_extension',
#             'objects': http.request.env['sale_purchase_inventory_extension.sale_purchase_inventory_extension'].search([]),
#         })

#     @http.route('/sale_purchase_inventory_extension/sale_purchase_inventory_extension/objects/<model("sale_purchase_inventory_extension.sale_purchase_inventory_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_purchase_inventory_extension.object', {
#             'object': obj
#         })

