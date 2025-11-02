# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeBonus(http.Controller):
#     @http.route('/employee_bonus/employee_bonus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_bonus/employee_bonus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_bonus.listing', {
#             'root': '/employee_bonus/employee_bonus',
#             'objects': http.request.env['employee_bonus.employee_bonus'].search([]),
#         })

#     @http.route('/employee_bonus/employee_bonus/objects/<model("employee_bonus.employee_bonus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_bonus.object', {
#             'object': obj
#         })

