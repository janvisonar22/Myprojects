# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderTask(http.Controller):
#     @http.route('/purchase_order_task/purchase_order_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_task/purchase_order_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_task.listing', {
#             'root': '/purchase_order_task/purchase_order_task',
#             'objects': http.request.env['purchase_order_task.purchase_order_task'].search([]),
#         })

#     @http.route('/purchase_order_task/purchase_order_task/objects/<model("purchase_order_task.purchase_order_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_task.object', {
#             'object': obj
#         })

