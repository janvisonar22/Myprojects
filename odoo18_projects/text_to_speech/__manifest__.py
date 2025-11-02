{
	'name': 'Text To Speech',
	'version': '18.0',
	'depends': ['web'],
	'data': [
		'security/ir.model.access.csv',  
		'views/text_to_speech.xml', # Corrected XML file name assumption
	],
	'assets': {
		'web.assets_backend': [
			'text_to_speech/static/src/js/text_to_speech.js', # This path is used in JS
		],
	},
	'installable': True,
	'application': False,
	'auto_install': False,
	'license': 'LGPL-3',
}