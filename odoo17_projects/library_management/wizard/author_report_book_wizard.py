from odoo import api, fields, models, _

class AuthorReportBookWizard(models.TransientModel):
	_name = 'author.report.book.wizard'
	_description = 'create report'


	author_ids = fields.Many2many('library.author',string='Authors Names')
	start_date = fields.Date(string='Start Date')
	end_date = fields.Date(string="End Date")

	def generate_pdf_report(self):
		# data = {
		# 	'author_ids': self.author_ids,
		# 	'start_date': self.start_date,
		# 	'end_date': self.end_date,
		# }
		return self.env.ref('library_management.action_report_author_book_view').report_action(self)

