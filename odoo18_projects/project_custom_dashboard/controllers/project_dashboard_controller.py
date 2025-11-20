# from odoo import http
# from odoo.http import request
#
# class ProjectDashboardController(http.Controller):
#
#     @http.route('/project_dashboard/data', type='json', auth='user')
#     def get_dashboard_data(self):
#         return request.env['project.dashboard'].sudo().get_dashboard_data()
#
#     @http.route('/project_dashboard/kpi', type='json', auth='user')
#     def get_kpi_data(self):
#         return request.env['project.dashboard'].sudo().get_kpi_data()
#
#     @http.route('/project/dashboard/data', type='json', auth='user')
#     def project_dashboard_data(self, **kwargs):
#         user = request.env.user
#         if not (user.has_group('project.group_project_manager') or user.has_group('project_custom_dashboard.group_finance_viewer')):
#             return {'error': 'Access Denied'}
#
#         # normal data return
#         return {'ok': True, 'data': 'your dashboard data'}

from odoo import http
from odoo.http import request


class ProjectDashboardController(http.Controller):

    # Fetch main dashboard data (for managers/admins)
    @http.route('/project_dashboard/data', type='json', auth='user')
    def get_dashboard_data(self):
        user = request.env.user
        # Access control check
        if not (user.has_group('project.group_project_manager') or user.has_group(
                'project_custom_dashboard.group_finance_viewer') or user.has_group('base.group_system')):
            return {'error': 'Access Denied'}

        return request.env['project.dashboard'].sudo().get_dashboard_data()

    # Fetch KPI data for charts or tiles
    @http.route('/project_dashboard/kpi', type='json', auth='user')
    def get_kpi_data(self):
        user = request.env.user
        if not (user.has_group('project.group_project_manager') or user.has_group(
                'project_custom_dashboard.group_finance_viewer') or user.has_group('base.group_system')):
            return {'error': 'Access Denied'}

        return request.env['project.dashboard'].sudo().get_kpi_data()

    # Example demo route
    @http.route('/project/dashboard/test', type='json', auth='user')
    def project_dashboard_data(self, **kwargs):
        user = request.env.user
        if not (user.has_group('project.group_project_manager') or user.has_group(
                'project_custom_dashboard.group_finance_viewer') or user.has_group('base.group_system')):
            return {'error': 'Access Denied'}

        return {'ok': True, 'data': 'Dashboard access successful ✅'}
