from odoo import models, fields

class TeacherType(models.Model):
	_name = 'teacher.type'
	_description = 'Student Type'

	name = fields.Char(string="Name", required=True)
	description = fields.Text(string="Description")
