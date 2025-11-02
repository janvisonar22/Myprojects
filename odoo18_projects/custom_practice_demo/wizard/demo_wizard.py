from odoo import models, fields, api

class DemoWizard(models.TransientModel):  # TransientModel = temporary wizard
	_name = 'demo.wizard'
	_description = 'Custom Practice Demo Wizard'

	remark = fields.Text(string="Remark")
	status = fields.Selection([
		('draft', 'Draft'),
		('done', 'Done'),
	], string="Status")

	def action_confirm(self):
		"""Example action: update selected record"""
		active_id = self.env.context.get('active_id')
		record = self.env['custom.practice.demo'].browse(active_id)
		record.description = (record.description or '') + f"\nWizard Remark: {self.remark}"
		return {'type': 'ir.actions.act_window_close'}
