{
	'name': "ecom_sale_website",
	'summary': "Custom E-Commerce Bidding Button",
	'description': "Add Bidding button next to Add to Cart button on product page.",
	'author': "My Company",
	'website': "https://www.yourcompany.com",
	'category': 'Website/Website',
	'version': '0.1',
	'depends': ['website_sale','portal','purchase','sale'],
	'data': [
		'security/ecom_sale_website_groups.xml',
		'security/ir.model.access.csv',
		'security/ecom_sale_website_rules.xml',
		'views/main_page.xml',
		'views/snippets/bidding_portal_front_view.xml',
		'views/snippets/templates.xml',
		'reports/report_ecom_bidding_action.xml',
		'reports/report_ecom_bidding_templates.xml',
																																																																																																																																																 

		'wizard/ecom_sale_website_quotation_wizard.xml',
		'wizard/report_menu_wizard.xml',


		'views/menu.xml',
	],
	'installable': True,
	'application': False,
	'auto_install': False,

	'assets': {
	'web.assets_frontend': [
		'ecom_sale_website/static/src/scss/portal_products.scss',
	],
},

}
