from odoo import http
from odoo.http import request

# ===========================================
# Controller to handle bidding pages and saving bids
# ===========================================
class BiddingController(http.Controller):

	# -------------------------------------------
	# Route to display the bidding page for a product
	# -------------------------------------------
	@http.route(['/bidding/<int:product_id>'], type='http', auth="public", website=True)
	def bidding_page(self, product_id, **kwargs):
		"""
		Renders the bidding page for a specific product.

		:param product_id: ID of the product to bid on
		:param kwargs: Additional GET parameters (if any)
		:return: Rendered template or 404 if product doesn't exist
		"""
		# Fetch the product record using the ID
		product = request.env['product.template'].sudo().browse(product_id)

		# Check if the product exists
		if not product.exists():
			return request.not_found()  # Return 404 page if not found

		# Render the bidding template with the product in context
		return request.render(
			"ecom_sale_website.bidding_template",  # XML template for bidding page
			{'product': product}                   # Pass product record to template
		)


	# -------------------------------------------
	# Route to save a bid submitted by a user
	# -------------------------------------------
	@http.route(
		['/bidding/save/<int:product_id>'],
		type='http',
		auth="public",
		website=True,
		csrf=True,     # CSRF protection enabled for POST requests
		methods=['POST']  # Only allow POST request
	)
	def save_bidding(self, product_id, **post):
		"""
		Handles saving a bid submitted by a user.

		:param product_id: ID of the product being bid on
		:param post: POST parameters from form (customer info and suggestion price)
		:return: Confirmation page after saving the bid
		"""
		# Fetch the product record using the ID
		product = request.env['product.template'].sudo().browse(product_id)
		if not product.exists():
			return request.not_found()  # Return 404 if product doesn't exist

		# Extract customer info and suggested price from POST data
		customer_name = post.get('customer_name')
		customer_phone = post.get('customer_phone')
		customer_email = post.get('customer_email')
		suggestion_price = post.get('suggestion_price')

		# -------------------------------------------
		# Check if a partner already exists with the given email
		# -------------------------------------------
		partner = request.env['res.partner'].sudo().search([('email', '=', customer_email)], limit=1)
		if not partner:
			# If partner doesn't exist, create a new one
			partner = request.env['res.partner'].sudo().create({
				'name': customer_name,
				'phone': customer_phone,
				'email': customer_email,
			})
		else:
			# If partner exists, update their name and phone
			partner.sudo().write({
				'name': customer_name,
				'phone': customer_phone,
			})

		# -------------------------------------------
		# Create a new bidding record
		# -------------------------------------------
		request.env['ecom.sale.website'].sudo().create({
			'name': product.name,           # Name of the product
			'product_id': product.id,       # Link to product
			'price': product.list_price,    # Current product price
			'suggestion_price': suggestion_price,  # Customer's suggested bid
			'customer_id': partner.id,      # Link to customer (res.partner)
		})

		# Render a confirmation template after bid is saved
		return request.render(
			'ecom_sale_website.bidding_confirmation',  # Confirmation page template
			{
				'product': product,
				'suggestion_price': suggestion_price,
				'customer': partner,  # Show customer details
			}
		)
