from odoo import models, fields

class PurchaseDashboard(models.Model):
    _name = "purchase.dashboard"
    _description = "Purchase Dashboard"
    _rec_name = "name"  # Display field in views

    name = fields.Char(string="Dashboard Name")
    total_orders = fields.Integer(string="Total Orders")
    total_amount = fields.Float(string="Total Amount")
# from odoo import models,fields,api

# class PurchaseOrder(models.Model):
# 	_inherit="purchase.order"

# 	@api.model
# 	def get_purchase_order_count(self):
# 		purchase_order_count = {
# 		'all_purchase_order':len(self.env['purchase.order'].search([])),
# 		'rfq':len(self.env['purchase.order'].search([('state','=','draft')])),
# 		'rfq_sent':len(self.env['purchase.order'].search([('state','=','sent')])),
# 		'to_approve':len(self.env['purchase.order'].search([('state','=','to approve')])),
# 		'purchase':len(self.env['purchase.order'].search([('state','=','purchase')])),
# 		'done':len(self.env['purchase.order'].search([('state','=','done')])),
# 		'cancel':len(self.env['purchase.order'].search([('state','=','cancel')])),
# 		}
# 		return purchase_order_count