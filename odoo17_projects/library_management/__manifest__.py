{
	'name': 'Library Management',
	'version': '17.0',
	'category': 'Tools',
	'summary': 'Manage Books and Authors',
	'depends': ['web','sale_crm','base','website','sale','report_xlsx'],
	'data': [
		'security/ir.model.access.csv',
		'data/mail_template_author.xml',

		'views/book_view.xml',
		'views/author_view.xml',
		'views/sale_data_template_controller.xml',
		# 'views/sale_order_line_search_browse.xml',
		'views/sale_order_view_xlxs_report_button.xml',
		'reports/author_report_book_wizard_action.xml',
		'reports/author_report_book_wizard_report.xml',

		'wizard/author_report_book_wizard_view.xml',
		'wizard/wizard_xlxs_sale_order.xml',
		'views/menu.xml',

	],
	'installable': True,
	'application': True,
	'license': 'LGPL-3',  
}
