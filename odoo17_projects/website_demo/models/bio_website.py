from odoo import models, fields, api

class WebsiteBio(models.Model):
	_name = 'bio.website'
	_description = "Website Demo"

	name = fields.Char(string="Name")
	date = fields.Date(string="Date")
	bio = fields.Html(string="Bio")
