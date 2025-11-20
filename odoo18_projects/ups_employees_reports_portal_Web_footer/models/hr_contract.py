from odoo import models, fields

class HrContractResignationLine(models.Model):
	_name = "hr.contract.resignation.line"
	_description = "HR Contract Resignation Line"

	contract_id = fields.Many2one('hr.contract', string="Contract")

	submit_date = fields.Date(string="Submit Resignation Date")
	reason = fields.Char(string="Reason For Resignation")
	approved_date = fields.Date(string="Approved Date")
	rejected_date = fields.Date(string="Rejected Date")


	state = fields.Selection([
		('draft', 'Draft'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
	], string="Status", default='draft')

	def action_approve(self):
		for rec in self:
			rec.state = 'approved'
			rec.approved_date = fields.Date.today()

	def action_reject(self):
		for rec in self:
			rec.state = 'rejected'
			rec.rejected_date = fields.Date.today()

	def action_reset_draft(self):
		for rec in self:
			rec.state = 'draft'

class HrContract(models.Model):
	_inherit = 'hr.contract'

	current_date = fields.Date(string="Current Date", default=fields.Date.today)
	salary_start_month = fields.Date(string="First Salary Month")

	resignation_line_ids = fields.One2many(
		'hr.contract.resignation.line',
		'contract_id',
		string="Resignation Details"
	)
