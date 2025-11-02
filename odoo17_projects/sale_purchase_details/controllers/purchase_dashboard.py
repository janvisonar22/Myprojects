from odoo import http
from odoo.http import request

class PurchaseDashboardController(http.Controller):
    @http.route('/purchase_dashboard/data', type='json', auth='user')
    def get_dashboard_data(self):
        PurchaseOrder = request.env['purchase.order']
        data = {
            'rfq': PurchaseOrder.search_count([('state', '=', 'draft')]),
            'rfq_sent': PurchaseOrder.search_count([('state', '=', 'sent')]),
            'to_approve': PurchaseOrder.search_count([('state', '=', 'to approve')]),
            'purchase': PurchaseOrder.search_count([('state', '=', 'purchase')]),
            'done': PurchaseOrder.search_count([('state', '=', 'done')]),
            'cancel': PurchaseOrder.search_count([('state', '=', 'cancel')]),
            'purchase_order_count': PurchaseOrder.search_count([]),
        }
        return [data]
