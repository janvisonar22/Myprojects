# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeTrainingManagement(http.Controller):
#     @http.route('/employee_training_management/employee_training_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_training_management/employee_training_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_training_management.listing', {
#             'root': '/employee_training_management/employee_training_management',
#             'objects': http.request.env['employee_training_management.employee_training_management'].search([]),
#         })

#     @http.route('/employee_training_management/employee_training_management/objects/<model("employee_training_management.employee_training_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_training_management.object', {
#             'object': obj
#         })

