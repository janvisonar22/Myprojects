from odoo import models, fields

class Profile(models.Model):
	_name = 'student.profile'
	_description = "Student Record"

	name = fields.Char(string="Student Name", required=True)
	roll_number = fields.Char(string="Roll Number", required=True)
	class_name = fields.Selection([
		('1', 'Class 1'),
		('2', 'Class 2'),
		('3', 'Class 3'),
		('4', 'Class 4'),
		('5', 'Class 5'),
	], string="Class")
	dob = fields.Date(string="Date of Birth")
	gender = fields.Selection([
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other')
	], string="Gender")
	email = fields.Char(string="Email")
	phone = fields.Char(string="Phone Number")
	address = fields.Text(string="Address")
	teacher_id = fields.Many2one(
		'res.users',
		string="Assigned Teacher",
		domain=lambda self: [('groups_id', 'in', self.env.ref('demo_module.group_school_erp_teacher').id)]
	)
