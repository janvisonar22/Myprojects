# from odoo import http
# from odoo.http import request

# class WebsiteBlog(http.Controller):

# 	@http.route('/blogs', type='http', auth='public', website=True)
# 	def list_blogs(self, **kw):
# 		return "hello"
from odoo import http
from odoo.http import request

class WebsiteBlog(http.Controller):

	@http.route('/blogs', type='http', auth='public', website=True)
	def list_blogs(self, **kw):
		blogs = request.env['website.blog.post'].sudo().search([])
		return request.render("website_blog_like.blog_list_template", {
			'blogs': blogs
		})

	@http.route('/blogs/like/<int:blog_id>', type='http', auth='public', website=True)
	def like_blog(self, blog_id, **kw):
		blog = request.env['website.blog.post'].sudo().browse(blog_id)
		if blog:
			blog.like_count += 1
		return request.redirect('/blogs')




