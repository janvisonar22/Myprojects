from odoo import models, fields, api

class SaleOrderWizard(models.TransientModel):
	_name = 'sale.order.wizard'
	_description = 'Sale Order Custom Wizard'

	partner_id = fields.Many2one('res.partner', string="Partner", required=True)

	def action_confirm(self):
		return {'type': 'ir.actions.act_window_close'}
