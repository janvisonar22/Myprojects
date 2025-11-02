# -*- coding: utf-8 -*-
{
	'name': "my_custom_dashboard",

	'summary': "Short (1 phrase/line) summary of the module's purpose",

	'description': """
Long description of module's purpose
	""",

	'author': "My Company",
	'website': "https://www.yourcompany.com",
	'category': 'Uncategorized',
	'version': '18.0',
	'depends': ['base','sale','website','purchase'],

	# always loaded
	'data': [
		'security/ir.model.access.csv',
		'views/partner_dashboard_view.xml',
		# 'views/sale_order_line_graph_view.xml',
		'views/menu.xml',
	],
	'assets': {
		'web.assets_backend': [
			'my_custom_dashboard/static/src/css/dashboard.scss',
			'my_custom_dashboard/static/src/js/dashboard_graph.js',
       		 'my_custom_dashboard/static/src/xml/dashboard_graph.xml',


		],
	},


	'installable': True,
	'auto_install': False,
	'application': False,

}

