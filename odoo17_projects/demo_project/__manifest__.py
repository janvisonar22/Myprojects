{
	'name': 'Demo Project',
	'version': '17.0',
	'category': 'A simple odoo17 module',
	'summary': 'A custom module for Odoo 17',
	'description': 'This module provides custom functionality for Odoo 17.',
	'depends': ['base','sale'],
	'data': [
		'security/ir.model.access.csv',

		'views/customer_desc.xml',  
		'views/sale_order_view.xml',
		'wizard/sale_order_view_wizard.xml'
	],
	'installable': True,
	'application': True,
	'license': 'LGPL-3',  
}
