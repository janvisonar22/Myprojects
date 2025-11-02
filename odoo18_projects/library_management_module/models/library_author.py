from odoo import models, fields, api


class LibraryAuthor(models.Model):
	_name = 'library.author'
	_description = 'Library Author'


	name = fields.Char(string='Name', required=True)
	bio = fields.Text(string='Biography')