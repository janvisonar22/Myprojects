from odoo import models, fields , api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class EcomSaleWebsite(models.Model):
	"""
	Model: E-Commerce Website Bidding
	This model represents bidding requests or inquiries from the e-commerce website.
	Users can create quotations based on selected products and customers.
	"""
	_name = 'ecom.sale.website'
	_description = 'E-Commerce Website Bidding'
	_rec_name = 'name'  

	user_id = fields.Many2one(
		'res.users',
		string="Responsible",
		default=lambda self: self.env.user
	)

	# ------------------------------
	# Fields
	# ------------------------------
	name = fields.Char(string="Product Name")
	def name_get(self):
		result = []
		for rec in self:
			display = rec.name or "Unnamed"
			if rec.customer_id:
				display = f"{display} ({rec.customer_id.name})"
			result.append((rec.id, display))
		return result

	# Customer linked to the bid
	customer_id = fields.Many2one('res.partner', string="Customer", required=True)
	
	# Related fields to automatically fetch customer's contact details
	customer_phone = fields.Char(related="customer_id.phone", string="Phone", store=True)
	customer_email = fields.Char(related="customer_id.email", string="Email", store=True)
	
	# Optional: a different contact can be selected (like a sales contact)
	contact = fields.Many2one('res.partner', string="Contact")
	
	# Product involved in the bid
	product_id = fields.Many2one('product.template', string="Product")
	
	# Bid-related prices
	price = fields.Float(string="Product Price")
	suggestion_price = fields.Float(string="Suggestion Price")
	
	# Status of the bid
	state = fields.Selection([
		('draft', 'Draft'),
		('quotation', 'Quotation'),
		('done', 'Done'),
		('cancel', 'Cancel'),
	], string="State", default='draft', tracking=True)
	#for smart button show the button inside tree and form view
	sale_order_ids = fields.One2many(
		'sale.order',  # related model
		'ecom_bidding_id',  # reverse Many2one field we will add to sale.order
		string="Quotations"
	)
	#for smart button (Qutation count)
	quotation_count = fields.Integer(
		string="  Quotation Count",
		compute='_compute_quotation_count'
	)

	#MANY2MANY field for notebook(get the sale.order last6 month data--- base contact selected)
	contact_sale_order_ids = fields.Many2many(
		'sale.order',
		compute='_compute_contact_sale_orders',#finctional field
		string="Contact Sale Orders",
		store=False   # Functional है, 
	)

	
	@api.depends('contact')
	def _compute_contact_sale_orders(self):
		"""
		Compute and fetch all Sale Orders of the selected contact from the last six months.

		- This method is triggered whenever the 'contact' field changes.
		- It calculates the date six months prior to the current date.
		- Searches the 'sale.order' model for orders linked to the contact created within this period.
		- Stores the resulting records in 'contact_sale_order_ids' field.
		- If no contact is selected, the 'contact_sale_order_ids' field is cleared.
		"""
		for rec in self:
			if rec.contact:
				# Calculate date six months ago from today
				six_months_ago = fields.Date.to_string(datetime.today() - timedelta(days=180))

				# Fetch all sale orders for this contact from last 6 months
				orders = self.env['sale.order'].search([
					('partner_id', '=', rec.contact.id),
					('date_order', '>=', six_months_ago)
				])

				rec.contact_sale_order_ids = orders
			else:
				rec.contact_sale_order_ids = False

	#MANY2MANY field for notebook(get the purchase.order last6 month data--- base contact selected)
	contact_purchase_order_ids = fields.Many2many(
		'purchase.order', 
		string="Recent Purchase Orders", 
		compute='_compute_contact_purchase_orders'
	)


	@api.depends('contact')
	def _compute_contact_purchase_orders(self):
		"""
		Compute and fetch all Purchase Orders of the selected contact from the last six months.

		- Triggered whenever the 'contact' field changes.
		- Calculates the date six months prior to today.
		- Searches 'purchase.order' model for orders linked to the contact created within this period.
		- Populates the Many2many field 'contact_purchase_order_ids' with the resulting records.
		- Clears the field if no contact is selected.
		"""
		for rec in self:
			if rec.contact:
				six_months_ago = fields.Date.to_string(datetime.today() - timedelta(days=180))
				
				orders = self.env['purchase.order'].search([
					('partner_id', '=', rec.contact.id),
					('date_order', '>=', six_months_ago)
				])
				
				rec.contact_purchase_order_ids = orders
			else:
				rec.contact_purchase_order_ids = False


	#for smart button compute method (for count order)(Qutation)

	@api.depends('sale_order_ids')
	def _compute_quotation_count(self):
		for record in self:
			record.quotation_count = len(record.sale_order_ids)

	# Open quotations linked to this bidding
	def action_view_quotations(self):
		self.ensure_one()
		return {
			'name': 'Quotations',
			'type': 'ir.actions.act_window',
			'res_model': 'sale.order',
			'view_mode': 'list,form',
			'domain': [('ecom_bidding_id', '=', self.id)],
			'context': {'create': False},
		}

	# ------------------------------
	# Methods
	# ------------------------------
	def action_new_quotation(self):
		"""
		Action to create a new quotation from the bidding record.
		
		- If a contact is selected, a sale order (quotation) is created directly.
		- If no contact is selected, a wizard form is opened to handle quotation creation.
		"""
		self.ensure_one()  # Ensure that this method is called for a single record

		# Case 1: Contact is selected → create quotation directly
		if self.contact:
			partner = self.contact
			order = self.env['sale.order'].create({
				'partner_id': partner.id,  # Assign the contact as the customer for the sale order
				'ecom_bidding_id': self.id,  # link quotation to bidding

				'order_line': [(0, 0, {
					'product_id': self.product_id.id,  # Product to be added in the order line
					'product_uom_qty': 1,             # Default quantity is 1
					'price_unit': self.price or self.suggestion_price or 0.0,  # Price logic
				})] if self.product_id else [],  # Only add product line if a product is selected
			})
			# Update bidding record
			# self.customer_id = partner.id
			self.state = 'quotation'

			# Open the created sale order in form view
			return {
				'type': 'ir.actions.act_window',
				'res_model': 'sale.order',
				'view_mode': 'form',
				'res_id': order.id,
				'target': 'current',
			}

		# Case 2: No contact selected → open quotation wizard
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'ecom.sale.website.quotation.wizard',
			'view_mode': 'form',
			'target': 'new',  # Open in a modal popup
			'context': {
				'active_id': self.id,  # Pass current bidding record to the wizard
				'default_name': f"Quotation for {self.name or 'Product'}",  # Default title
			}
		}

		#for state done (when user click the "done" button so state are gone to done)
	def action_done(self):
		"""Mark the bidding record as Done"""
		for rec in self:
			rec.state = 'done'

		return {
			'type': 'ir.actions.client',
			'tag': 'reload',
		}

	def action_cancel(self):
		"""Mark the bidding record as Done"""
		for rec in self:
			rec.state = 'cancel'

		return {
			'type': 'ir.actions.client',
			'tag': 'reload',
		}


from odoo import models, fields

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	ecom_bidding_id = fields.Many2one(
		'ecom.sale.website',
		string="E-Commerce Bidding"
	)

