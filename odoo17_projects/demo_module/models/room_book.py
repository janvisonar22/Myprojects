from odoo import models, fields

class RoomBook(models.Model):
	_name = 'room.book'
	_description = 'Room Book'

	name = fields.Char(string='Room Number', required=True)
	room_type = fields.Selection([
		('single', 'Single'),
		('double', 'Double'),
		('suite', 'Suite'),
	], string='Room Type')
	is_available = fields.Boolean(string='Is Available', default=True)
	price_per_night = fields.Float(string='Price Per Night')


