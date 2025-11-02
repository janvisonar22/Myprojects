from odoo import models, fields

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'

	sale_id = fields.Many2one('sale.order', string='Related Sale Order', readonly=True)

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	sale_id = fields.Many2one('sale.order', string='Related Sale Order', readonly=True)
