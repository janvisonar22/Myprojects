from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

# ===========================================
# Extend the default Customer Portal to add
# custom values like product count to the home page
# ===========================================
class CustomProductsPortal(CustomerPortal):

	def _prepare_home_portal_values(self, counters):
		"""
		Overrides the default portal home values to include
		the total number of products available in the website model.
		
		:param counters: Dictionary of existing counters (messages, tasks, etc.)
		:return: Updated dictionary including 'product_count'
		"""
		# Call the super method to get the default values
		values = super()._prepare_home_portal_values(counters)

		# Count all products in the custom model 'ecom.sale.website'
		product_count = request.env['ecom.sale.website'].sudo().search_count([])

		# Update the values dictionary to include product_count
		values.update({
			'product_count': product_count
		})

		return values


# ===========================================
# Controller to handle product listing pages
# ===========================================
class ProductsPortal(http.Controller):

	@http.route([
		'/my/products',                  # First page of products
		'/my/products/page/<int:page>'   # Additional pages with pagination
	], type='http', auth='user', website=True)
	def portal_my_products(self, page=1, **kw):
		"""
		Display products in the portal with pagination.
		
		:param page: Current page number (default 1)
		:param kw: Additional GET parameters
		:return: Rendered template with products and pager
		"""

		# Reference the custom product model
		Product = request.env['ecom.sale.website']

		# Total number of products (used for pagination)
		product_count = Product.sudo().search_count([])

		# Create pager object to handle pagination in the template
		pager = request.website.pager(
			url="/my/products",   # Base URL for pagination
			total=product_count,  # Total products
			page=page,            # Current page
			step=20               # Number of products per page
		)

		# Fetch products for the current page using limit and offset
		products = Product.sudo().search([], limit=20, offset=pager['offset'])
		# Render the template with products and pagination info
		return request.render(
			"ecom_sale_website.portal_my_products_template",
			{
				'products': products,      # List of products for this page
				'pager': pager,            # Pager object for template
				'page_name': 'products',   # Used for active menu highlighting
				'default_url': '/my/products'  # Base URL for pagination links
			}
		)
