from odoo import api,models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
	_inherit='res.partner'

	# @api.model_create_multi
	# def create(self,vals_list):
	# 	result = super().create(vals_list)
	# 	for rec in result:
	# 		rec.vat = "JA12345"  

	# 	return result

	@api.constrains('name')
	def _check_name_length(self):
		for rec in self:
			if rec.name and len(rec.name) < 3:
				raise ValidationError("Plz enter 3 characters")