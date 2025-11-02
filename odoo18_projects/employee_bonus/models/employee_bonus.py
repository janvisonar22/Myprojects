from odoo import models, fields, api
from odoo.exceptions import UserError

class EmployeeBonus(models.Model):
	_name = "employee.bonus"
	_description = "Employee Bonus"
	employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
	month = fields.Selection([
		('jan', 'January'), ('feb', 'February'), ('mar', 'March'), 
		('apr', 'April'), ('may', 'May'), ('jun', 'June'), 
		('jul', 'July'), ('aug', 'August'), ('sep', 'September'), 
		('oct', 'October'), ('nov', 'November'), ('dec', 'December')
	], string="Month", required=True)
	bonus_amount = fields.Monetary(string="Bonus Amount", required=True, currency_field='company_currency_id')
	total_bonus = fields.Monetary(
	string="Total Bonus",
	compute="_compute_total_bonus",
	store=True,
	currency_field='company_currency_id'
	)




	state = fields.Selection([
		('draft', 'Draft'),
		('approved', 'Approved')
	], string="Status", default='draft')
	company_currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

	@api.depends('employee_id', 'bonus_amount')  # Triggers when these fields change
	def _compute_total_bonus(self):
		for record in self:
			# Sum all bonus_amounts for this employee
			total = sum(self.env['employee.bonus'].search([('employee_id','=',record.employee_id.id)]).mapped('bonus_amount'))
			record.total_bonus = total
	_sql_constraints = [
		('employee_month_unique', 'unique(employee_id, month)', 'A bonus record for this employee and month already exists.')
	]
	@api.model
	def create(self, vals):
		"""Override create method to implement automatic workflow"""
		record = super(EmployeeBonus, self).create(vals)
		record._check_auto_approve()
		return record

	@api.depends('employee_id')
	def _check_auto_approve(self):
		"""Automatically approve if salary > 50,000"""
		for rec in self:
			if rec.employee_id and rec.employee_id.contract_id.wage > 50000:
				
				rec.state = 'approved'
