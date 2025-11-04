
{
    "name": "POS Session XZ Report | POS X-Z Report |  POS X-Z Report from front and Backend in Odoo POS ",
    'category': 'Point of Sale',
    'summary': """POS X and Z Reports""",
    "description": """Using this module you can print POS X and Z Report from front and Backend in odoo POS""",
    'version': '18.0.1.1.1',
    'author': 'Dotsprime System',
    'sequence': 1,
    'email': 'dotsprime@gmail.com',
    'support': 'sales@dotsprime.com',
    "website":'https://dotsprime.com/',
    'price': 20,
    "currency": "EUR",
    "license": 'AGPL-3',    
    'depends': ['point_of_sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'report/reports.xml',
        'report/front_sales_report_pdf_template.xml',
        'report/front_sales_thermal_report_template.xml',
        "report/report_pos_session.xml",
        'wizard/wizard_pos_x_report.xml',
        'wizard/wizard_pos_sale_report_view.xml',
        "views/pos_session_view.xml",
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            "dps_pos_session_xzreport/static/src/js/PosXReport.js",
            'dps_pos_session_xzreport/static/src/xml/PosXReport.xml',
        ],
    },
    'images': ['static/description/main_screenshot.png'],      
    'installable': True,
    'auto_install': False,
    'application': True,
}
