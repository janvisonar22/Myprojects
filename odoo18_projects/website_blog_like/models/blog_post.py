from odoo import models, fields, api

class BlogPost(models.Model):
	_name = "website.blog.post"
	_description = "Blog Likes"

	blog_name = fields.Char(string="Blog Title")
	description = fields.Text(string="Description")
	like_count = fields.Integer(string="Likes", default=0)
