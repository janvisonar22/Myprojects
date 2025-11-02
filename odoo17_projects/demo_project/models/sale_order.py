from odoo import models, fields, api

# class SaleOrder(models.Model):
# 	_inherit = 'sale.order'

# 	def action_custom_button(self):
# 		view = self.env.ref('demo_project.view_sale_order_custom_wizard')
# 		return {
# 			'type': 'ir.actions.act_window',
# 			'name': 'Custom Wizard',
# 			'res_model': 'sale.order.wizard',
# 			'view_mode': 'form',
# 			'view_id': view.id,
# 			'target': 'new',  
# 			'context': {
# 				'default_order_id': self.id,  # Pass the sale.order record ID to the wizard			
# 			}
# 		}


# class SaleOrder(models.Model):
# 	_inherit = 'sale.order'

# 	def action_custom_button(self):
# 		view = self.env.ref('demo_project.view_sale_order_custom_wizard')
# 		return {
# 			'type': 'ir.actions.act_window',
# 			'name': 'Custom Wizard',
# 			'res_model': 'sale.order.wizard',
# 			'view_mode': 'form',
# 			'view_id': view.id,
# 			'target': 'new',  
# 			'context': {
# 				'default_order_id': self.id,  # Pass the sale.order record ID to the wizard
# 				'default_partner_id': self.partner_id.id,  # Pass partner_id to the wizard
# 				'default_date_order': self.date_order,  # Pass date_order to the wizard
# 				'default_order_line_ids': [(6, 0, self.order_line_ids)],  # Pass order lines to the wizard
# 				# You can add more fields here if necessary
# 			}
# 		}

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_custom_button(self):
        view_id = self.env.ref('demo_project.view_sale_order_custom_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order Custom Wizard',
            'res_model': 'sale.order.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
            'default_partner_id': self.partner_id.id
            },
        }
