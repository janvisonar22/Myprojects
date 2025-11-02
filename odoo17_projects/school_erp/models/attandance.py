from odoo import models , fields ,api
from datetime import datetime


class SchoolAttandance(models.Model):
	_name = 'school.attandance'
	_description = 'attandance'

	teacher_id = fields.Many2one('res.teacher',string="Teacher")
	standard_id = fields.Many2one('student.standard',string="Standard")
	timetable_id = fields.Many2one('school.timetable',string="TimeTable")
	from_time = fields.Float(string="From Time")  
	to_time = fields.Float(string="To Time")
	student_line_ids = fields.One2many('school.attendance.line', 'attendance_id', string="Students")
	

	@api.model
	def cron_create_mail(self):
		today = datetime.today()
		print("\n\ntoday===========>>>",today)
		today_start = datetime.combine(today, datetime.min.time())
		today_end = datetime.combine(today, datetime.max.time())
		print("\n\ntoday_end----=======>>>",today_end)
		today_attendance_records = self.search([
			('create_date', '>=', today_start),
			('create_date', '<=', today_end),
		])
		print("\n\n\ntoday_attendance_records==========>",today_attendance_records)
		template = self.env.ref('school_erp.attandace_mail_template')
		print("\n\ntemplate-----------------<<<<<<<<<<<<<<<<M",template)
		for record in today_attendance_records:
			template.send_mail(record.id, force_send=True)
		# print("\n\nrecord==>",record)



class SchoolAttendanceLine(models.Model):
	_name = 'school.attendance.line'
	_description = 'Attendance Line'

	attendance_id = fields.Many2one('school.attandance', string="Attendance")
	student_id = fields.Many2one('res.student', string="Student")
	present = fields.Boolean(string="Present", default=False)

