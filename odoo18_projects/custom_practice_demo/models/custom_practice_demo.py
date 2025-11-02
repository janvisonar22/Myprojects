# -*- coding: utf-8 -*-

from odoo import models, fields, api


class custom_practice_demo(models.Model):
	_name = 'custom.practice.demo'
	_description = 'Custom Practice Demo'

	name = fields.Char()
	value = fields.Integer()
	# value2 = fields.Float(compute="_value_pc", store=True)
	partner_id	= fields.Many2one("res.partner",string="Partner")
	description = fields.Text()

	def demo_button1(self):
		pass
	def open_demo_wizard(self):
		return {
			'name': 'Add Remark',
			'type': 'ir.actions.act_window',
			'res_model': 'demo.wizard',
			'view_mode': 'form',
			'target': 'new',  # open as popup
			'context': {'active_id': self.id},
		}
