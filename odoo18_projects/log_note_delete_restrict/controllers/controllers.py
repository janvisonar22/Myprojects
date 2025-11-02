# -*- coding: utf-8 -*-
# from odoo import http


# class TaskFieldServiceCalendar(http.Controller):
#     @http.route('/task_field_service_calendar/task_field_service_calendar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_field_service_calendar/task_field_service_calendar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_field_service_calendar.listing', {
#             'root': '/task_field_service_calendar/task_field_service_calendar',
#             'objects': http.request.env['task_field_service_calendar.task_field_service_calendar'].search([]),
#         })

#     @http.route('/task_field_service_calendar/task_field_service_calendar/objects/<model("task_field_service_calendar.task_field_service_calendar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_field_service_calendar.object', {
#             'object': obj
#         })

