from odoo import models, fields
from datetime import datetime

class SaleReport(models.AbstractModel):
    _name = "report.your_module_name.sale_report"

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'docs': docs,
            'ctx_today': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

# from odoo import models, fields
# from odoo.tools import format_datetime
# from datetime import datetime

# class SalesPurchaseReport(models.AbstractModel):
#     _name = 'report.sale_purchase_details.report_sales_purchase_template'
#     _description = 'Sales and Purchase Report'

#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sales.purchase.details.wizard'].browse(docids)
#         return {
#             'docs': docs,
#             'current_datetime': format_datetime(self.env, datetime.now()),  # Pre-format datetime
#         }
