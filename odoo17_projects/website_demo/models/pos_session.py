from odoo import models,api


class PosSession(models.Model):
	_inherit='pos.session'


	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		result['search_params']['fields'].append('brand')
		return result
	def _pos_ui_models_to_load(self):
		result = super()._pos_ui_models_to_load()
		result += ['product.product']
		return result