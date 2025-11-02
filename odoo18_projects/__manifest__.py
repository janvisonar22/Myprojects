# -*- coding: utf-8 -*-
{
    'name': 'Custom Purchase Order',
    'version': '1.0',
    'summary': 'Customized Purchase Order Template with Dynamic Company Details and Signature',
    'description': """
Custom Purchase Order Module
============================
This module provides a customized Purchase Order PDF template with the following features:
- Dynamic company logo and name.
- Default Terms & Conditions (editable by salesperson).
- E-signature and company name in the signature section.
- Dynamic footer with company name, address, phone, and email.
""",
    'author': 'Your Company Name',
    'website': 'https://www.yourcompanywebsite.com',
    'category': 'Purchases',
    'depends': ['purchase', 'base', 'web'],
    'data': [
        'report/purchase_order_report_template.xml',
        'report/purchase_order_report_action.xml',
        'views/res_company_view.xml',
        'data/terms_conditions_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Add custom CSS/JS if needed
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
