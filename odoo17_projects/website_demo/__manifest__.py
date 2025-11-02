{
	'name': 'Website data demo',
	'version': '17.0',
	'category': 'A simple odoo17 module',
	'summary': 'A custom module for Odoo 17',
	'description': 'This module provides custom functionality for Odoo 17.',
	'depends': ['web','website','sale','point_of_sale','product'],
	'data': [
		'security/ir.model.access.csv',
		'data/website_bio_data.xml',
		'data/website_data_menu.xml',
		'data/my_page_menu.xml',

		'data/sale_order_menu.xml',
		'views/website_bio_templates.xml',
		'views/sale_order_data_fronted_view.xml',
		'views/product_brand_view.xml',

	],
	'assets':{
		'point_of_sale._assets_pos':[
		'website_demo/static/src/js/pos_store.js']
	},
	
    'images': ['static/description/icon.png','product'],  # module icon

	'installable': True,
	'application': True,
	'license': 'LGPL-3',  
}
