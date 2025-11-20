from odoo import models, api

class ProjectDashboard(models.Model):
	_name = 'project.dashboard'
	_description = 'Project Dashboard'

	@api.model
	def get_dashboard_data(self, offset=0, limit=10, order='id asc'):
		"""Fetch projects with pagination"""
		projects = self.env['project.project'].sudo().search([], offset=offset, limit=limit, order=order)
		data = []
		for project in projects:
			data.append({
				'id': project.id,
				'name': project.name,
				'revenue_invoiced': getattr(project, 'revenue_invoiced', 0.0),
				'revenue_committed': getattr(project, 'revenue_committed', 0.0),
				'uninvoiced_amount': getattr(project, 'uninvoiced_amount', 0.0),
				'timesheet_hours': getattr(project, 'timesheet_hours', 0.0),
				'percent_complete': getattr(project, 'percent_complete', 0.0),
				'margin_estimate': getattr(project, 'margin_estimate', 0.0),
			})
		total_count = self.env['project.project'].sudo().search_count([])
		return {
			'projects': data,
			'total_count': total_count,
		}

	@api.model
	def get_kpi_data(self):
		"""Aggregate KPIs for top-bar tiles."""
		
		# 1️⃣ TOTAL INVOICED (all invoices)
		all_invoices = self.env['account.move'].sudo().search([
			('move_type', 'in', ['out_invoice', 'out_refund']),
			('state', '=', 'posted')
		])
		print("\n\nall_invoices===>",all_invoices)
		total_invoiced = sum(all_invoices.mapped('amount_total'))
		print("\n\ntotal_invoiced==>>",total_invoiced)
		
		# 2️⃣ TOTAL COMMITTED (all sale orders)
		sale_orders = self.env['sale.order'].sudo().search([
			('state', 'in', ['sale', 'done'])
		])
		print("\n\nsale_orders===>>",sale_orders)
		total_committed = sum(sale_orders.mapped('amount_total'))
		print("\n\ntotal_committed-->>",total_committed)
		# 3️⃣ TOTAL UNINVOICED = committed – invoiced
		total_uninvoiced = total_committed - total_invoiced
		print('\n\ntotal_uninvoiced==>>',total_uninvoiced)
		# 4️⃣ TOTAL HOURS (all timesheets)
		total_hours = sum(
			self.env['account.analytic.line'].sudo().search([]).mapped('unit_amount')
		)
		print("\n\ntotal_hours-->>",total_hours)
		# 5️⃣ TOTAL MARGIN (approx)
		total_cost = sum(
			self.env['account.analytic.line'].sudo().search([]).mapped('amount')
		)
		total_margin = total_invoiced - abs(total_cost)

		return {
			'total_invoiced': total_invoiced,
			'total_committed': total_committed,
			'total_uninvoiced': total_uninvoiced,
			'total_hours': total_hours,
			'total_margin': total_margin,
		}
