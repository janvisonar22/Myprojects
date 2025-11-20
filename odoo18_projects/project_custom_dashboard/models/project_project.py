from odoo import models, fields, api

class ProjectProject(models.Model):
	_inherit = 'project.project'

			
	revenue_invoiced = fields.Float(string="Revenue Invoiced", compute="_compute_dashboard_metrics", store=False)
	revenue_committed = fields.Float(string="Revenue Committed", compute="_compute_dashboard_metrics", store=False)
	uninvoiced_amount = fields.Float(string="Uninvoiced Amount", compute="_compute_dashboard_metrics", store=False)
	timesheet_hours = fields.Float(string="Timesheet Hours", compute="_compute_dashboard_metrics", store=False)
	percent_complete = fields.Float(string="Percent Complete", compute="_compute_dashboard_metrics", store=False)
	margin_estimate = fields.Float(string="Margin Estimate", compute="_compute_dashboard_metrics", store=False)

	# ✅ Boolean flags for KPI filters
	has_invoiced = fields.Boolean(string="Has Invoiced", compute="_compute_dashboard_metrics", store=False)
	has_committed = fields.Boolean(string="Has Committed", compute="_compute_dashboard_metrics", store=False)
	has_uninvoiced = fields.Boolean(string="Has Uninvoiced", compute="_compute_dashboard_metrics", store=False)
	has_timesheet_hours = fields.Boolean(string="Has Timesheet Hours", compute="_compute_dashboard_metrics", store=False)
	has_margin = fields.Boolean(string="Has Margin", compute="_compute_dashboard_metrics", store=False)

	@api.depends('task_ids')
	def _compute_dashboard_metrics(self):
		for project in self:
			# Invoiced Revenue
			invoices = self.env['account.move'].sudo().search([
				('invoice_origin', '=', project.name),
				('state', '=', 'posted'),
			])
			project.revenue_invoiced = sum(invoices.mapped('amount_total'))

			# Committed Revenue
			analytic_id = getattr(project, 'analytic_account_id', False)
			if analytic_id:
				orders = self.env['sale.order'].sudo().search([
					('analytic_account_id', '=', analytic_id.id),
					('state', 'in', ['sale', 'done'])
				])
			else:
				orders = self.env['sale.order'].sudo().search([
					('state', 'in', ['sale', 'done'])
				])
			project.revenue_committed = sum(orders.mapped('amount_total'))

			# Uninvoiced Amount
			project.uninvoiced_amount = project.revenue_committed - project.revenue_invoiced

			# Timesheet Hours
			timesheets = self.env['account.analytic.line'].sudo().search([
				('project_id', '=', project.id),
			])
			project.timesheet_hours = sum(timesheets.mapped('unit_amount'))

			# Percent Complete
			total_tasks = len(project.task_ids)
			done_tasks = len(project.task_ids.filtered(lambda t: t.stage_id.fold))
			project.percent_complete = (done_tasks / total_tasks * 100) if total_tasks else 0.0

			# Margin Estimate
			total_cost = sum(timesheets.mapped('amount'))
			project.margin_estimate = project.revenue_invoiced - abs(total_cost)

			# KPI flags
			project.has_invoiced = project.revenue_invoiced > 0
			project.has_committed = project.revenue_committed > 0
			project.has_uninvoiced = project.uninvoiced_amount > 0
			project.has_timesheet_hours = project.timesheet_hours > 0
			project.has_margin = project.margin_estimate > 0
