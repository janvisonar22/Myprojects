# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPracticeDemo(http.Controller):
#     @http.route('/custom_practice_demo/custom_practice_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_practice_demo/custom_practice_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_practice_demo.listing', {
#             'root': '/custom_practice_demo/custom_practice_demo',
#             'objects': http.request.env['custom_practice_demo.custom_practice_demo'].search([]),
#         })

#     @http.route('/custom_practice_demo/custom_practice_demo/objects/<model("custom_practice_demo.custom_practice_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_practice_demo.object', {
#             'object': obj
#         })

