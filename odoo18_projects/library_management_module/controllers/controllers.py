# -*- coding: utf-8 -*-
# from odoo import http


# class LibraryManagementModule(http.Controller):
#     @http.route('/library_management_module/library_management_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/library_management_module/library_management_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('library_management_module.listing', {
#             'root': '/library_management_module/library_management_module',
#             'objects': http.request.env['library_management_module.library_management_module'].search([]),
#         })

#     @http.route('/library_management_module/library_management_module/objects/<model("library_management_module.library_management_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('library_management_module.object', {
#             'object': obj
#         })

