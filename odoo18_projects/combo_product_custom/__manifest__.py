# -*- coding: utf-8 -*-
{
    'name': 'Combo Product Custom',
    'version': '18.0.1.0.0',
    'summary': 'Manage combo or bundled products with custom logic',
    'description': """
        Combo Product Custom
        =====================
        This module allows the creation and management of combo (bundled) products.
        Useful for businesses that sell products in combinations or kits.
    """,
    'author': 'Your Company Name',
    'website': 'https://www.yourcompany.com',
    'category': 'Sales/Product',

    # Dependencies
    'depends': [
        'base',
        'product',
        'sale',  # optional if you are working with sales
        'stock',
    ],

    # Data files
    'data': [
        'security/ir.model.access.csv',
        'views/product_combo_view.xml',
        'views/website_cart_inherit.xml',
        'views/website_ecom_inside.xml',

    ],

    # Technical info
    'license': 'LGPL-3',

    'installable': True,
    'application': True,
    'auto_install': False,
}
