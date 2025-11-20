# -*- coding: utf-8 -*-
{
    'name': 'UPS Employees Reports',
    'version': '18.0',
    'sequence': 10,
    'category': 'Human Resources',
    'summary': 'Custom Employee Reports and Enhancements',
    'description': """
        Custom Employee Reports and Enhancements for HR Module.
        Includes PDF reports, tree/list view customization,
        form view customization, dashboards, etc.
    """,

'depends': [
    'base',
    'hr',
    'hr_contract',
    'website',
],

    # your XML files here
    'data': [
        'security/ir.model.access.csv',

        # 'security/portal_contract_rules.xml',

        'views/hr_contract_views.xml',
        'views/portal_contract_detail_template.xml',
        'views/portal_views.xml',
        'views/resignation_form_page.xml',
        'views/portal_detail_footer.xml',


        'reports/experience_letter_report.xml',
        'reports/experience_letter_report_template.xml',
        'reports/offer_latter_report.xml',
        'reports/offer_latter_report_template.xml',
        'reports/training_certificate_report.xml',
        'reports/training_certificate_report_template.xml',

    ],

    'assets': {
    },

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}



