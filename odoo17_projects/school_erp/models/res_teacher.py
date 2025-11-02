from odoo import models, fields

class ResTeacher(models.Model):
	_name = 'res.teacher'
	_description = 'Teacher'

	name = fields.Char(string="Name")
	email = fields.Char(string="Email")
	address = fields.Text(string="Address")
	designation_id = fields.Many2one('teacher.designation', string="Designation")
	teacher_type_id = fields.Many2one('teacher.type', string="Teacher Type")
