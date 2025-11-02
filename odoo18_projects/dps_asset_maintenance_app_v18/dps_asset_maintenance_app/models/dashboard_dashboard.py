from odoo import api,fields,models,_
import time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from datetime import datetime,timedelta
from babel.dates import format_datetime,format_date
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF,DEFAULT_SERVER_DATETIME_FORMAT as DTF,format_datetime as tool_format_datetime
from odoo.release import version
import json

DASHBOARD_FIELDS = ['total_requests','my_total_requests_color','inprogress_requests','inprogress_requests_color','repaired_requests','repaired_requests_color','scrap_requests','scrap_requests_color','total_equipments','total_equipments_color','total_job_order','total_job_order_color','total_requisition','total_requisition_color','draft_requisition','draft_requisition_color','ongoing_requisition','ongoing_requisition_color','close_requisition','close_requisition_color','cancel_requisition','cancel_requisition_color','maintenance_request_data','maintenance_bar_graph_color','maintenance_bar_graph']


class DashboardDashboard(models.Model):
	_name = 'dashboard.dashboard'

	@property
	def SELF_READABLE_FIELDS(self):
		return super().SELF_READABLE_FIELDS + DASHBOARD_FIELDS

	@property
	def SELF_WRITEABLE_FIELDS(self):
		return super().SELF_WRITEABLE_FIELDS + DASHBOARD_FIELDS

	dashboard_data_filter = fields.Selection([
		('today','Today'),
		('week','This Week'),
		('month','This Month'),
		('year','This Year'),
		('all','All'),
	],string="Dashboard Filter",default='today')

	total_requests = fields.Integer(string="Total Requests",compute="_compute_total_requests")
	my_total_requests_color = fields.Char(string='My Total Requests Color',default="#883F73")

	inprogress_requests = fields.Integer(string="In Progress Requests",compute="_compute_inprogress_requests")
	inprogress_requests_color = fields.Char(string="In Progress Requests Color",default="#883F73")
	
	repaired_requests = fields.Integer(string="Repaired Requests",compute="_compute_repaired_requests")
	repaired_requests_color = fields.Char(string="Repaired Requests Color",default="#883F73")
	scrap_requests = fields.Integer(string="scrap Requests",compute="_compute_scrap_requests")
	scrap_requests_color = fields.Char(string="Scrap Requests Color",default="#883F73")

	total_equipments = fields.Integer(string="Total Equipment",compute="_compute_equipments")
	total_equipments_color = fields.Char(string="Total Equipment Color",default="#883F73")
	
	total_job_order = fields.Integer(string="Total job order",compute="_compute_job_order")
	total_job_order_color = fields.Char(string="Total job order Color",default="#883F73")

	total_requisition = fields.Integer(string="Total requisition",compute="_compute_requisition")
	total_requisition_color = fields.Char(string="Total requisition Color",default="#883F73")

	draft_requisition = fields.Integer(string="Total requisition",compute="_compute_draft_requisition")
	draft_requisition_color = fields.Char(string="Total requisition Color",default="#883F73")
	ongoing_requisition = fields.Integer(string="ongoing requisition",compute="_compute_ongoing_requisition")
	ongoing_requisition_color = fields.Char(string="ongoing requisition Color",default="#883F73")
	close_requisition = fields.Integer(string="close requisition",compute="_compute_close_requisition")
	close_requisition_color = fields.Char(string="close requisition Color",default="#883F73")
	cancel_requisition = fields.Integer(string="cancel requisition",compute="_compute_cancel_requisition")
	cancel_requisition_color = fields.Char(string="cancel requisition Color",default="#883F73")

	maintenance_request_data = fields.Text(string="Maintenance Requests",compute="_compute_maintenance_requests")
	maintenance_bar_graph_color = fields.Char(string='Maintenance Bar Chart Color',default="#883F73")
	maintenance_bar_graph = fields.Text(compute='_compute_dashboard_data')

	@api.depends('dashboard_data_filter')
	def _compute_total_requests(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			rec.total_requests = self.env['maintenance.request'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_equipments(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			rec.total_equipments = self.env['maintenance.equipment'].search_count(domain)

	@api.depends('dashboard_data_filter')
	def _compute_job_order(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			rec.total_job_order = self.env['maintenance.job.order'].search_count(domain)


	@api.depends('dashboard_data_filter')
	def _compute_requisition(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			rec.total_requisition = self.env['maintenance.purchase.requisition'].search_count(domain)
	@api.depends('dashboard_data_filter')

	def _compute_draft_requisition(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			domain += [('state','=','draft')]
			rec.draft_requisition = self.env['maintenance.purchase.requisition'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_ongoing_requisition(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			domain += [('state','=','ongoing')]
			rec.ongoing_requisition = self.env['maintenance.purchase.requisition'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_close_requisition(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			domain += [('state','=','closed')]
			rec.close_requisition = self.env['maintenance.purchase.requisition'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_cancel_requisition(self):
		for rec in self:
			domain = rec.get_filter('create_date')
			domain += [('state','=','cancel')]
			rec.cancel_requisition = self.env['maintenance.purchase.requisition'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_inprogress_requests(self):
		for rec in self:
			domain = rec.get_filter('create_date') + [('stage_id.name','=','In Progress')] 
			rec.inprogress_requests = self.env['maintenance.request'].search_count(domain)


	@api.depends('dashboard_data_filter')
	def _compute_repaired_requests(self):
		for rec in self:
			domain = rec.get_filter('create_date') + [('stage_id.name','=','Repaired')]  
			rec.repaired_requests = self.env['maintenance.request'].search_count(domain)
	
	@api.depends('dashboard_data_filter')
	def _compute_scrap_requests(self):
		for rec in self:
			rec.scrap_requests = 0 
			if rec.dashboard_data_filter:
				domain = rec.get_filter('create_date') + [('stage_id.name','=','Scrap')]
				rec.scrap_requests = self.env['maintenance.request'].search_count(domain)
   
	def today_data(self):
		self.dashboard_data_filter = 'today'

	def week_data(self):
		self.dashboard_data_filter = 'week'

	def month_data(self):
		self.dashboard_data_filter = 'month'

	def year_data(self):
		self.dashboard_data_filter = 'year'

	def all_data(self):
		self.dashboard_data_filter = 'all'


	def get_filter(self,field_name):
		for rec in self:
			domain = []
			if rec.dashboard_data_filter=='today':
				domain = [(field_name,'>=',time.strftime('%Y-%m-%d 00:00:00')),(field_name,'<=',time.strftime('%Y-%m-%d 23:59:59'))]
			if rec.dashboard_data_filter=='week':
				domain = [(field_name,'>=',(fields.Datetime.today() + relativedelta(weeks=-1,days=1,weekday=0)).strftime('%Y-%m-%d')),(field_name,'<=',(fields.Datetime.today() + relativedelta(weekday=6)).strftime('%Y-%m-%d'))]
			if rec.dashboard_data_filter=='month':
				domain = [(field_name,'<',(fields.Datetime.today()+relativedelta(months=1)).strftime('%Y-%m-01')),(field_name,'>=',time.strftime('%Y-%m-01'))]
		return domain
		
	def open_requests(self):
		action = self.env["ir.actions.actions"]._for_xml_id("maintenance.hr_equipment_request_action")
		action['domain'] = self.get_filter('create_date')
		return action

	def open_equipment(self):
		action = self.env["ir.actions.actions"]._for_xml_id("maintenance.hr_equipment_action")
		action['domain'] = self.get_filter('create_date')
		return action

	def open_job_order(self):
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.job_order_action_form")
		action['domain'] = self.get_filter('create_date')
		return action

	def open_requisition(self):
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.action_equipment_purchase_requisition")
		action['domain'] = self.get_filter('create_date')
		return action

	def open_draft_requisition(self):
		domain = self.get_filter('create_date') + [('state','=','draft')]
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.action_equipment_purchase_requisition")
		action['domain'] = domain
		return action

	def open_ongoing_requisition(self):
		domain = self.get_filter('create_date') + [('state','=','ongoing')]
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.action_equipment_purchase_requisition")
		action['domain'] = domain
		return action

	def open_close_requisition(self):
		domain = self.get_filter('create_date') + [('state','=','closed')]
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.action_equipment_purchase_requisition")
		action['domain'] = domain
		return action

	def open_cancel_requisition(self):
		domain = self.get_filter('create_date') + [('state','=','cancel')]
		action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.action_equipment_purchase_requisition")
		action['domain'] = domain
		return action

	def open_inprogress_requests(self):
		domain = self.get_filter('create_date') + [('stage_id.name','=','In Progress')]
		action = self.env["ir.actions.actions"]._for_xml_id("maintenance.hr_equipment_request_action")
		action['domain'] = domain
		return action

	def open_repaired_requests(self):
		domain = self.get_filter('create_date') + [('stage_id.name','=','Repaired')]
		action = self.env["ir.actions.actions"]._for_xml_id("maintenance.hr_equipment_request_action")
		action['domain'] = domain
		return action

	def open_scrap_requests(self):
		domain = self.get_filter('create_date') + [('stage_id.name','=','Scrap')]
		action = self.env["ir.actions.actions"]._for_xml_id("maintenance.hr_equipment_request_action")
		action['domain'] = domain
		return action

	@api.depends('dashboard_data_filter')
	def _compute_maintenance_requests(self):
		maintenance_request = self.env['maintenance.request']
		request_domain = self.get_filter('create_date')

		self.total_requests = maintenance_request.search_count(request_domain)

		request_data = []
		request_list = maintenance_request.search(
			request_domain + [('user_id','=',self.env.uid)],limit=20
		)

		tzinfo = self.env.context.get('tz') or self.env.user.tz or 'UTC'
		locale = self.env.context.get('lang') or self.env.user.lang or 'en_US'

		for request in request_list:
			request = request.sudo()
			request_date = tool_format_datetime(self.env,request.create_date,dt_format=False)
			request_data.append({
				'id': request.id,
				'name': request.name,
				'equipment': request.equipment_id.name if request.equipment_id else '',
				'category': request.category_id.name if request.category_id else '',
				'priority': request.priority,
				'scheduled_date': request_date,
				'stage': request.stage_id.name if request.stage_id else '',
			})
		self.maintenance_request_data = json.dumps(request_data)


	def main_open_dashboard_action(self):
		method = self._context.get('main_action')
		if not method:
			raise UserError("No action Defined to call.")
		result = getattr(self,method)()
		return result

	@api.depends('dashboard_data_filter')
	def _compute_dashboard_data(self):
		for rec in self:
			rec.maintenance_bar_graph = json.dumps(rec.get_maintenance_bar_graph_datas())

	def get_maintenance_bar_graph_datas(self):
		data = []
		today = fields.Datetime.now()
		data.append({'label': _('Past'),'value': 0.0,'type': 'past'})
		day_of_week = int(format_datetime(today,'e',locale=self._context.get('lang') or 'en_US'))
		first_day_of_week = today + timedelta(days=-day_of_week+1)

		for i in range(-1,4):
			if i == 0:
				label = _('This Week')
			elif i == 3:
				label = _('Future')
			else:
				start_week = first_day_of_week + timedelta(days=i*7)
				end_week = start_week + timedelta(days=6)
				if start_week.month == end_week.month:
					label = f"{start_week.day}-{end_week.day} {format_date(end_week,'MMM',locale=self._context.get('lang') or 'en_US')}"
				else:
					label = f"{format_date(start_week,'d MMM',locale=self._context.get('lang') or 'en_US')} - {format_date(end_week,'d MMM',locale=self._context.get('lang') or 'en_US')}"
			data.append({'label': label,'value': 0.0,'type': 'past' if i < 0 else 'future'})

		(select_sql,args) = ("""SELECT count(id) as total,min(create_date) as aggr_date
								 FROM maintenance_request WHERE stage_id IS NOT NULL""",{})
		query = ''
		start_date = (first_day_of_week + timedelta(days=-7))
		for i in range(0,6):
			if i == 0:
				query += f"({select_sql} AND create_date < '{start_date.strftime(DF)}')"
			elif i == 5:
				query += f" UNION ALL ({select_sql} AND create_date >= '{start_date.strftime(DF)}')"
			else:
				next_date = start_date + timedelta(days=7)
				query += f" UNION ALL ({select_sql} AND create_date >= '{start_date.strftime(DF)}' AND create_date < '{next_date.strftime(DF)}')"
				start_date = next_date

		self.env.cr.execute(query,args)
		results = self.env.cr.dictfetchall()
		for idx,row in enumerate(results):
			if row.get('aggr_date'):
				data[idx]['value'] = row.get('total')

		return [{
			'values': data,
			'title': '',
			'key': _('Maintenance Requests')
		}]
