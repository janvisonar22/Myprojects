# -*- coding: utf-8 -*-
# from odoo import http


# class DemoSuperPractice(http.Controller):
#     @http.route('/demo_super_practice/demo_super_practice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/demo_super_practice/demo_super_practice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('demo_super_practice.listing', {
#             'root': '/demo_super_practice/demo_super_practice',
#             'objects': http.request.env['demo_super_practice.demo_super_practice'].search([]),
#         })

#     @http.route('/demo_super_practice/demo_super_practice/objects/<model("demo_super_practice.demo_super_practice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('demo_super_practice.object', {
#             'object': obj
#         })

