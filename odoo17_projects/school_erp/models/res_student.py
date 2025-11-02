from odoo import models , fields

class ResStudent(models.Model):
	_name = 'res.student'
	_description = 'Student'

	name = fields.Char(string="name")
	email = fields.Char(string="Email")
	address = fields.Text(string="Address")
	class_teacher_id = fields.Many2one('res.teacher', string="Class Teacher")
	student_type_id = fields.Many2one('student.type', string="Student Type")
	timetable_id = fields.Many2one(
		'school.timetable',
		string="Timetable")
