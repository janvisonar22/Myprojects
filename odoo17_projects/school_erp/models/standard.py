from odoo import models, fields

class Standard(models.Model):
	_name = 'student.standard'
	_rec_name = 'standard'	
	standard = fields.Char(string="Name", required=True)
