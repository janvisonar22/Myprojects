from odoo import http


class MyPage(http.Controller):
	@http.route('/mypage',auth='public')
	def mypage(self,**kwargs):
		return "Hello World"