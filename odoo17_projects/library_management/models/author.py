from odoo import models, fields , api
from odoo.exceptions import ValidationError

class LibraryAuthor(models.Model):
	_name = 'library.author'
	_description = 'Library Author'

	name = fields.Char(string='Name', required=True, help="Enter the name")
	state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
	partner_id= fields.Many2one('res.partner',string='Partner', required=True)
	birth_date = fields.Date(string='Birth Date')
	book_ids = fields.One2many('library.book', 'author_id', string='Books')

	
	# @api.model
	# def create(self, vals):
	# 	return super(LibraryAuthor, self).create({'name': 'Nimi'})
	# @api.model
	# def create(self, vals):
	# 	print('--------------------------------',vals)birth_date
	# 	vals.update({
	# 		'name': 'Nimi',
	# 		'birth_date': '2003-04-22',
	# 	})
	# 	return super(LibraryAuthor, self).create(vals)
	def action_confirm(self):
		self.state="done"
	def action_send_mail(self):
		template=self.env.ref('library_management.email_template_author')
		template.send_mail(self.id,force_send=True)

	def action_send_notification(self):
		if self.partner_id:
			self.state='done'
			return{
				'effect':{
				'fadeout':'slow',
				'message':'Successfully send',
				'type':'rainbow_man',

				}
			}
		else:
			raise ValidationError("maneger is missing")
