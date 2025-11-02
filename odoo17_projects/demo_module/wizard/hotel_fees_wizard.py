from odoo import models, fields, api , _

class HotelFeesWizard(models.TransientModel):
	_name = 'hotel.fees.wizard'
	_description = 'Hotel Fees Wizard'

	hotel_number = fields.Integer(string="Number of Hotels")
	entry_fees = fields.Float(string="Entry Fees")
	exit_fees = fields.Float(string="Exit Fees")
	result = fields.Float(string="Total Needed", compute="_compute_result", store=True)

	@api.depends('hotel_number', 'entry_fees', 'exit_fees')
	def _compute_result(self):
		for rec in self:
			money_needed = 0.0
			for _ in range(rec.hotel_number):
				money_needed = (money_needed + rec.exit_fees) / 2.0
				print("\n\nmoney_needed--->>>",money_needed)
				money_needed += rec.entry_fees
				print("\n\nmoney_needed---<<>>",money_needed)
			rec.result = round(money_needed, 2)
			print("\n\nrec.result-->>",rec.result)