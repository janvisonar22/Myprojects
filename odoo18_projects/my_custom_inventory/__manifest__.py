# -*- coding: utf-8 -*-
{
    'name': "My custom inventory",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'report/action_report.xml',    
        'report/my_stock_report_template.xml',
        'wizard/warehouse_location_wizard_view.xml',

        'views/menu.xml',


    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,    
   
}

