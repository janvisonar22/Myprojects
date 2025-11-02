# -*- coding: utf-8 -*-
{
    'name': 'Custom Purchase Order',
    'version': '1.0',
    'summary': 'Customized Purchase Order Template with Dynamic Company Details and E-Signature',
    'description': """
        Custom Purchase Order
        =====================
        This module customizes the Purchase Order template with:
        - Dynamic company logo and name
        - Editable Terms & Conditions
        - Company e-signature in the signature section
        - Dynamic footer with company address, phone, and email
    """,
    'category': 'Purchases',
    'author': 'Your Company Name',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['purchase', 'base'],
    'data': [
        'reports/purchase_order_report.xml',
        'reports/purchase_order_template.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
