from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_line_ids = fields.One2many(
        'combo.product.line',
        'combo_id',
        string='Product Lines'
    )
