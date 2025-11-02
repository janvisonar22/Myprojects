from odoo import models, fields

class LibraryBook(models.Model):
	_name = 'library.book'
	_description = 'Library Book'
	_rec_name = 'title'  
	title = fields.Char(string='Title', required=True)
	publish_date = fields.Date(string='Publish Date')
	pages = fields.Integer(string='Number of Pages')
	author_id = fields.Many2one('library.author', string='Author', required=True)
