{
    "name": "All in one Maintenance | Equipment Maintenance | Asset Equipment Maintenance",
    "summary": "All in one Maintenance | Equipment Maintenance | Asset Equipment Maintenance > Asset Equipment Maintenance Management(Asset Maintenance, Repair and Operation)",
    'version' : '18.0.5.3.2',
    "description": """
    All in one Maintenance | Equipment Maintenance | Asset Equipment Maintenance
    Asset Equipment Maintenance Management(Asset Maintenance, Repair and Operation)

    Key Feature:
        - Equipment maintenance management
        - Equipment maintenance dashboard
        - Manage all type of maintenance
        - Checklist configuration
        - Purchase order for equipment and product
        - Easy to manage maintenance process
        - Create Job order for staff and technician
        - Create Purchase Requisition
        - Maintenance request stages
        - Create customer invoice
    """,    
    'author': 'Dotsprime System',
    'sequence': 1,
    'email': 'dotsprime@gmail.com',
    'support': 'sales@dotsprime.com',
    "website":'https://dotsprime.com/',
    "license": 'OPL-1',
    "category": "Extra Tools",
    "depends": ['maintenance','stock','account','contacts'],
    "data": [
        'security/ir.model.access.csv',
        'data/maintenance_purchase_sequence.xml',
        'views/maintenance_request_view.xml',
        'views/job_order_view.xml',
        'views/maintenance_purchase_requisition_view.xml',
        'demo/dashboard_dashboard_demo.xml',
        'views/dashboard_dashboard.xml',
        'wizard/wizard_maintenance_report.xml',
        'wizard/wizard_maintenance_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dps_asset_maintenance_app/static/src/scss/maintenance_dashboard.scss'
        ]
    },
    'price': 49,
    'currency': 'EUR',  
    "live_test_url" : "",    
    'images': ['static/description/main_screenshot.png'],  
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
