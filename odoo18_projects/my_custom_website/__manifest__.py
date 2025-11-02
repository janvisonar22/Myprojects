# -*- coding: utf-8 -*-
{
    'name': "my_custom_website",

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
    'depends': ['web','website'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/my_website_menu.xml',
        'views/student_profile.xml',
        'views/student_profile_fronted_view.xml',
        'views/student_templates.xml',

        'views/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,    
    'license': 'LGPL-3',  

}

