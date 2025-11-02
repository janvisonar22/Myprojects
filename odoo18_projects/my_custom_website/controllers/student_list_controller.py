from odoo import http

class StudentList(http.Controller):
	@http.route('/student/list',auth='public')
	def mypage(self,**kwargs):
		return "Hello World"