from odoo import models, fields

class StudentType(models.Model):
	_name = 'student.type'
	_description = 'Student Type'

	name = fields.Char(string="Name", required=True)
	description = fields.Text(string="Description")
