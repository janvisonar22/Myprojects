# -*- coding: utf-8 -*-
{
    'name': "demo_module",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale','website','portal'],

    # always loaded
    'data': [
        'security/record_rule.xml',
        'security/student_security_group.xml',
        'security/ir.model.access.csv',
        'views/portal_sale_custom_view.xml',

        'views/menu.xml',
        'views/views.xml',


    ],
    # 'assets': {
    # 'web.assets_frontend': [
    #     'your_module/static/src/scss/portal_custom.scss',
    # ],
    # },

    'installable': True,
    'application': True,    
    'license': 'LGPL-3',  
}

