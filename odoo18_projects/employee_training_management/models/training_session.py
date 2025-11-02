from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class TrainingSession(models.Model):
	_name = 'training.session'
	_description = 'Training Session'
	_order = 'start_date desc'

	name = fields.Char(string='Session Name', required=True)
	trainer_id = fields.Many2one('hr.employee', string='Trainer', required=True)
	start_date = fields.Datetime(string='Start Date', required=True)
	end_date = fields.Datetime(string='End Date', required=True)
	capacity = fields.Integer(string='Capacity', required=True)
	attendee_ids = fields.Many2many('hr.employee', string='Attendees')
	attendee_count = fields.Integer(string='Attendee Count', compute='_compute_attendee_count', store=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('confirmed', 'Confirmed'),
		('done', 'Done'),
		('cancelled', 'Cancelled')
	], string='Status', default='draft', tracking=True)

	# -----------------------------
	# COMPUTE METHODS
	# -----------------------------
	@api.depends('attendee_ids')
	def _compute_attendee_count(self):
		for rec in self:
			rec.attendee_count = len(rec.attendee_ids)

	# -----------------------------
	# CONSTRAINTS
	# -----------------------------
	@api.constrains('start_date', 'end_date')
	def _check_dates(self):
		for rec in self:
			if rec.start_date and rec.end_date and rec.start_date >= rec.end_date:
				raise ValidationError("Start Date must be earlier than End Date.")

	@api.constrains('trainer_id', 'start_date', 'end_date')
	def _check_trainer_overlap(self):
		for rec in self:
			if rec.trainer_id:
				overlapping = self.search([
					('id', '!=', rec.id),
					('trainer_id', '=', rec.trainer_id.id),
					('state', '!=', 'cancelled'),
					('start_date', '<', rec.end_date),
					('end_date', '>', rec.start_date)
				])
				if overlapping:
					raise ValidationError("Trainer has overlapping sessions.")

	# -----------------------------
	# BUSINESS LOGIC
	# -----------------------------
	def action_confirm(self):
		for rec in self:
			if rec.attendee_count > rec.capacity:
				raise UserError("Number of attendees exceeds the session capacity!")
			rec.state = 'confirmed'

	def action_done(self):
		for rec in self:
			# Mark employees as trained
			rec.attendee_ids.write({'is_trained': True})
			rec.state = 'done'

	def action_cancel(self):
		self.write({'state': 'cancelled'})

	def action_draft(self):
		self.write({'state': 'draft'})

	# -----------------------------
	# CRON JOB METHOD
	# -----------------------------
	@api.model
	def _cron_cancel_old_draft_sessions(self):
		cutoff_date = datetime.now() - timedelta(days=60)
		old_sessions = self.search([
			('state', '=', 'draft'),
			('start_date', '<', cutoff_date)
		])
		old_sessions.write({'state': 'cancelled'})

