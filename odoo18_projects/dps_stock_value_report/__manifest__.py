# -*- coding: utf-8 -*-

{
    'name': "Inventory Status Report",
    'category': 'Inventory',
    'version': '18.0.0.1',
    'author': 'Dotsprime System LLP',

    'description': """
            This Module enables the generation of comprehensive Inventory Status Reports in both PDF and XLS formats.
            * Produce detailed Inventory Status Reports with customizable formats (PDF/XLS).
            * Support for multiple warehouses and locations for greater flexibility.
            * Organize inventory data by product categories for better insight.
            * Apply filters to view reports by specific products or categories.
            * Streamline stock management with location-wise inventory tracking.
        """,

    'summary': """
        A powerful tool to generate customizable Inventory Status Reports in PDF and XLS formats.
        Supports multiple warehouses and locations, with advanced filtering options by product or category. 
        Ideal for managing real-time stock and inventory insights, including location-wise reporting and category-based grouping.
    """,

    'depends': ['base', 'stock'],

    'price': 50,
    'currency': 'EUR',
    'license': '',

    'website': "",

    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_inventory_report_wizard_view.xml',
        'report/report.xml',
        'report/inventory_report_template.xml',
    ],


    'installable': True,
    'auto_install': False,
    'application': False,
}
