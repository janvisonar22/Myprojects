from odoo import models, fields , api
from datetime import datetime

class Timetable(models.Model):
	_name = 'school.timetable'
	_description = 'Timetable'
	name = fields.Char(string="Reference", required=True, copy=False, readonly=True, default='New')
	standard = fields.Many2one('student.standard',string="Standard")
	from_date = fields.Date(string="From Date")
	to_date = fields.Date(string="To Date")
	teacher_id = fields.Many2one('res.teacher', string='Class Teacher')
	timetable_line_ids = fields.One2many('school.timetable.line', 'timetable_id', string="Timetable Lines")
	student_ids = fields.One2many(
		'res.student',          
		'timetable_id',        
		string="Students")
	subject_id = fields.Many2one('school.subject', string="Subject")


	# start_time = fields.Float(string='Start Time')
	# end_time = fields.Float(string='End Time')
	# subject_id = fields.Many2one('school.subject', string='Subject', required=True)
	# teacher_id = fields.Many2one('res.teacher', string='Teacher')
	# student_id = fields.Many2one('res.student', string='Student')

	# @api.onchange('subject_id')
	# def _onchange_subject(self):
	#   self.teacher_id = self.subject_id.teacher_id
	@api.model
	def create(self, vals):
		if vals.get('name', 'New') == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('school.timetable') or 'New'
		return super().create(vals)
	# def cron_create_attendance(self):
	#   timetable_ids = self.env['school.timetable'].search([])
	#   print("timetable_ids:", timetable_ids)
		
	#   for timetable_id in timetable_ids:
	#       print("-----------------timetable_id.standard",timetable_id.standard)
	#       print("\n\nstudent_ids--->",timetable_id.student_ids)
	#       for line in timetable_id.timetable_line_ids:
	#           print("Teacher:", timetable_id.teacher_id.name)
	#           print("Subject:", line.subject_id.name)
	#           print("From:", line.from_time)
	#           print("To:", line.to_time)
	#           print("dayssssssssssssssssssssssssssssssssssssssss:",line.day)
	@api.model
	def cron_create_attendance(self):
		today_day = datetime.today().strftime('%A')  
		print("Today is:", today_day)

		timetable_ids = self.env['school.timetable'].search([])

		for timetable_id in timetable_ids:
			line_ids = []
			student_data = []
			for student_id in timetable_id.student_ids:
				student_data.append([0, False, {
					'student_id': student_id.id
				}])
			for line in timetable_id.timetable_line_ids:
				if line.day == "mon" and today_day == "Monday":
					line_ids.append(line)
				elif line.day == "tue" and today_day == "Tuesday":
					line_ids.append(line)
				elif line.day == "wed" and today_day == "Wednesday":
					line_ids.append(line)
				elif line.day == "thu" and today_day == "Thursday":
					line_ids.append(line)
				elif line.day == "fri" and today_day == "Friday":
					line_ids.append(line)
				elif line.day == "sat" and today_day == "Saturday":
					line_ids.append(line)
				elif line.day == "sun" and today_day == "Sunday":
					line_ids.append(line)
			for line in line_ids:
				teacher_id = line.teacher_id.id
				standard_id = timetable_id.standard and timetable_id.standard.id or False
				self.env['school.attandance'].create({
					'teacher_id': teacher_id,
					'standard_id': standard_id,
					'timetable_id': timetable_id.id,
					'from_time': line.from_time,
					'to_time': line.to_time,
					'student_line_ids': student_data
				})

class TimetableLine(models.Model):
	_name = 'school.timetable.line'
	_description = 'Timetable Line'

	day = fields.Selection([
		('mon', 'Monday'),
		('tue', 'Tuesday'),
		('wed', 'Wednesday'),
		('thu', 'Thursday'),
		('fri', 'Friday'),
		('sat', 'Saturday'),
	], string='Day', required=True)

	timetable_id = fields.Many2one('school.timetable', string="Timetable", ondelete='cascade')
	from_time = fields.Float(string="From Time")  
	to_time = fields.Float(string="To Time")
	class_timing = fields.Char(string="Class Timing", compute="_compute_class_timing", store=True)
	subject_id = fields.Many2one('school.subject', string="Subject", required=True)
	@api.depends('from_time', 'to_time')
	def _compute_class_timing(self):
		for rec in self:
			if rec.from_time and rec.to_time and rec.to_time > rec.from_time:
				total_minutes = int((rec.to_time - rec.from_time) * 60)
				hours = total_minutes // 60
				minutes = total_minutes % 60
				rec.class_timing = f"{hours:02}:{minutes:02}"
			else:
				rec.class_timing = "00:00"
	teacher_id = fields.Many2one('res.teacher', string='Class Teacher')
	@api.onchange('subject_id')
	def _onchange_subject(self):
		self.teacher_id = self.subject_id.teacher_id
