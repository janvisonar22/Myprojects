from odoo import models, fields


class MyModel(models.Model):
	_name = 'customer.desc'
	_description = 'Customer Desc'

	name = fields.Char(string='Name', required=True)
	description = fields.Text(string='Description')