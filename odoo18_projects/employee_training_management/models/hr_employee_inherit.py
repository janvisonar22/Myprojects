from odoo import models, fields

class HREmployee(models.Model):
	_inherit = 'hr.employee'

	is_trained = fields.Boolean(string='Trained', default=False)
	training_hours = fields.Float(
		string='Training Hours', compute='_compute_training_hours', store=True)

	def _compute_training_hours(self):
		for emp in self:
			sessions = self.env['training.session'].search([
				('attendee_ids', 'in', emp.id),
				('state', '=', 'done')
			])
			total_hours = 0.0
			for session in sessions:
				print("\n\ntotal_hours==>>>",total_hours)
				if session.start_date and session.end_date:
					duration = (session.end_date - session.start_date).total_seconds() / 3600
					print("\n\nduration===>>>",duration)
					total_hours += duration
					print("\n\ntotal_hours===>>",total_hours)
			emp.training_hours = total_hours
			print("\n\nemp.training_hours==>>",emp.training_hours)
	def action_open_trainings(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Trainings',
			'res_model': 'training.session',
			'view_mode': 'list,form',
			'domain': [('attendee_ids', 'in', self.id)],
			'target': 'current',
		}
