from odoo import models, fields, api
from odoo.exceptions import UserError

class EcomSaleWebsiteQuotationWizard(models.TransientModel):
	"""
	Wizard Model: Quotation Wizard for E-Commerce Website Bidding
	This transient model is used to create a sale quotation from a bidding record.
	It allows the user to either create a quotation for a new customer (from bidding)
	or select an existing customer.
	"""
	_name = 'ecom.sale.website.quotation.wizard'
	_description = 'Quotation Wizard for Ecom Sale Website'

	# ------------------------------
	# Fields
	# ------------------------------
	action_type = fields.Selection([
		('new_customer', 'Create New Customer'),           # Use the customer from bidding
		('existing_customer', 'Select an existing customer'),  # Select an existing partner
	], string="Action", required=True, default='new_customer')

	existing_partner_id = fields.Many2one(
		'res.partner',
		string="Select Existing Customer",
		help="Choose an existing customer to assign to the quotation"
	)

	# ------------------------------
	# Methods
	# ------------------------------
	def action_confirm_quotation(self):
		"""
		Confirm Quotation:
		- Retrieves the active bidding record from context
		- Determines the customer based on wizard selection
		- Creates a sale.order (quotation) with the product and price
		- Updates the bidding record state to 'quotation'
		"""

		# Get the active bidding record (ensure one exists)
		bidding = self.env['ecom.sale.website'].browse(self.env.context.get('active_id'))
		if not bidding:
			raise UserError("No active bidding record found.")

		# Determine partner based on action type
		if self.action_type == 'new_customer':
			if not bidding.customer_id:
				raise UserError("Please select a Customer in the bidding before proceeding.")
			partner = bidding.customer_id
			bidding.contact = partner.id  # assign customer as contact

		elif self.action_type == 'existing_customer':
			if not self.existing_partner_id:
				raise UserError("Please select an existing customer.")
			partner = self.existing_partner_id
			bidding.contact = partner.id  # assign selected partner as contact

		# ------------------------------
		# Create Sale Quotation
		# ------------------------------
		order_vals = {
			'partner_id': partner.id,
			'order_line': [(0, 0, {
				'product_id': bidding.product_id.id,
				'product_uom_qty': 1,
				'price_unit': bidding.price or bidding.suggestion_price or 0.0,
			})] if bidding.product_id else [],  # only add line if product exists
		}

		order = self.env['sale.order'].create(order_vals)

		# Update bidding state to 'quotation'
		bidding.state = 'quotation'

		# Open the created sale order in form view
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'sale.order',
			'view_mode': 'form',
			'res_id': order.id,
			'target': 'current',
		}
