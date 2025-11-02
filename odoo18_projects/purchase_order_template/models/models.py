from odoo import models, fields

class ResCompany(models.Model):
	_inherit = 'res.company'

	purchase_terms = fields.Text(string="Default Purchase Terms")
	signature_image = fields.Binary("Signature Image")
