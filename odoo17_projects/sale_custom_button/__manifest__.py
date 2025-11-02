{
    'name': 'Sale Custom Button',
    'version': '17.0',
    'summary': 'Adds a custom button to Sale Order',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/sale_custom_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}