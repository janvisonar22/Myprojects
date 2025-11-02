from odoo import models

class SaleOrder(models.Model):
	_inherit = 'sale.order'
	 # custom_record_count = fields.Integer(string="Custom Records", compute='_compute_custom_record_count')

    # @api.depends('id')
    # def _compute_custom_record_count(self):
    #     for order in self:
    #         order.custom_record_count = self.env['custom.record'].search_count([('sale_order_id', '=', order.id)])
	def action_custom_button(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Custom Order',
			'res_model': 'custom.order',
			'view_mode': 'form',
			'target': 'current',
			'context': {
				'default_partner_id': self.partner_id.id,
				'default_date_order': self.date_order,
			},
		}


	def action_custom_button(self):
		self.ensure_one()

		ctx = {
			'default_partner_id': self.partner_id.id,
			'default_date_order': self.date_order,
			'default_sale_order_id': self.id,
		}

		return {
			'type': 'ir.actions.act_window',
			'name': 'Custom Order',
			'res_model': 'custom.order',
			'view_mode': 'form',
			'target': 'current',
			'context': ctx,
		}
	def action_get_vehicles_record(self):
		passs