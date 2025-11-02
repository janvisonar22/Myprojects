# -*- coding: utf-8 -*-
{
    'name': 'Sale Purchase Inventory Extension',
    'version': '18.0',
    'category': 'Sales',
    'sequence': 10,
    'summary': 'Automate Purchase Order creation from Sale Orders when stock is insufficient.',
    'description': """
Sale → Purchase → Inventory Automation
======================================

This module extends the standard Odoo workflow between Sales, Purchase, and Inventory 
to introduce automation, reporting, and data integrity.

**Key Features:**
- Automatically creates Purchase Orders upon Sale Order confirmation for products with insufficient stock.
- Groups Purchase Orders by Vendor.
- Links Purchase Orders back to their originating Sale Orders.
- Ensures Vendor availability with error handling.
    """,
    'author': 'Your Company Name',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',

    'depends': [
        'sale',
        'purchase',
        'stock',
    ],
'data': [
    'security/ir.model.access.csv',
    'views/purchase_order_view_inherit.xml',
    'views/sale_order_view_inherit.xml',

],

    'installable': True,
    'application': False,
    'auto_install': False,

}
