{
	'name': 'Scheduler',
	'version': '17.0',
	'summary': 'Sale Order/purchase order',
	'category': 'Sales',
	'depends': ['sale', 'purchase','website','web'],
	'data': [
		'security/ir.model.access.csv',
		'views/portal_my_home.xml',
		'views/custom_portal_template.xml',
	],
	'installable': True,
	'application': False,
	'license': 'LGPL-3',
}
