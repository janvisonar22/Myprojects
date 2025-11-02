{
	'name': 'My Sale order',
	'version': '17.0',
	'category': 'A simple odoo17 module',
	'summary': 'A custom module for Odoo 17',
	'description': 'This module provides custom functionality for Odoo 17.',
	'depends': ['base','sale','purchase'],
	'data': [
		'security/ir.model.access.csv',
		'views/menu.xml',
		'views/custom_import.xml'
	],
	

	'installable': True,
	'application': True,
	'license': 'LGPL-3',  
}
