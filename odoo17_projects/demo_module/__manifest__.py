{
	'name': 'Hotel book',
	'version': '17.0',
	'category': 'A simple odoo17 module',
	'summary': 'A custom module for Odoo 17',
	'description': 'This module provides custom functionality for Odoo 17.',
	'depends': ['base','sale','purchase','report_xlsx'],
	'data': [
		'security/ir.model.access.csv',

		'views/room_book_views.xml',  
		'views/contact_book_views.xml',
		'report/sales_purchase_report_templates.xml',
		'report/sale_purchase_pdf_template.xml',
		'wizard/hotel_fees_wizard_views.xml',
		'wizard/sales_purchase_wizard_views.xml',
		

		'views/menu.xml',
	],
	'assets': {
		'web.report_assets_common': [
			'demo_module/static/src/scss/report_styles.scss',
		],
	},

	'installable': True,
	'application': True,
	'license': 'LGPL-3',  
}
