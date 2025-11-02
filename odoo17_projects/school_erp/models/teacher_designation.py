from odoo import models, fields

class StudentType(models.Model):
	_name = 'teacher.designation'
	_description = 'Teacher Designation'

	name = fields.Char(string="Name", required=True)
	description = fields.Text(string="Description")
