from odoo import models, fields, api

class SalesPurchaseDetailsWizard(models.TransientModel):
    _name = 'sales.purchase.details.wizard'
    _description = 'Sales and Purchase Details Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)

    def get_sales_data(self):
        sales_order = self.env['sale.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('partner_id', '=', self.partner_id.id),
        ])
        sales_data = []
        for order in sales_order:
            for line in order.order_line:
                sales_data.append({
                    'order_no':order.name,
                    'product':line.product_id.name,
                    'qty':line.product_uom_qty,
                    'price':line.price_unit,
                    'tax':line.tax_id.name,
                    'total_without_tax':line.price_subtotal,
                    'total_with_tax':line.price_total,
                    'status':order.state
                    })
        return sales_data


    def get_purchase_data(self):
        purchase_order = self.env['purchase.order'].search([
            ('date_order', '>=', self.start_date),
            ('date_order', '<=', self.end_date),
            ('partner_id', '=', self.partner_id.id),
        ])
        purchase_data = []
        for order in purchase_order:
            for line in order.order_line:
                purchase_data.append({
                    'order_no':order.name,
                    'product': line.product_id.name,
                    'qty': line.product_qty,
                    'price': line.price_unit,
                    'tax': line.taxes_id.name,
                    'total_without_tax': line.price_subtotal,
                    'total_with_tax': line.price_total,
                    'status': order.state
                    })
        print("Purchase Data",purchase_data)
        return purchase_data

    def action_generate_report(self):
        return self.env.ref('sale_purchase_details.action_sales_purchase_report').report_action(self)
    def action_generate_xlsx_report(self):
            return self.env.ref('sale_purchase_details.action_sales_purchase_xlsx_report').report_action(self)

