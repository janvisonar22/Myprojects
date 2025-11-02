from odoo import models, fields

class ComboProductLine(models.Model):
    _name = 'combo.product.line'
    _description = 'Combo Product Line'

    combo_id = fields.Many2one('product.template', string='Combo')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price = fields.Float(string='Price')
