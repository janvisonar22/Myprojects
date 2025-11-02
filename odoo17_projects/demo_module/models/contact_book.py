from odoo import models, fields

class ContactBook(models.Model):
	_name = 'contact.book'
	_description = 'Contact Book'

	name = fields.Char(string="name")


	
