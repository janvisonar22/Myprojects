from odoo import api,models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
	_inherit='product.product'

	def unlink(self):
		for product in self:
			if product.lst_price >= 500:
				raise ValidationError("You are not allowed to the delete product having sale price 500 or grater than 500")
		return super().unlink()