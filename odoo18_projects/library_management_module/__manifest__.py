# -*- coding: utf-8 -*-
{
    'name': "Library Management",

    'summary': "Manage Books, Authors and Members",

    'description': """
        Long description of module's purpose
    """,

        'author': "My Company",
        'website': "https://www.yourcompany.com",
        'category': 'Tools',
        'version': '18.0',
        'depends': ['base','web'],

        # always loaded
        'data': [
            'security/ir.model.access.csv',
            'views/library_author_view.xml',
            'views/menu.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}

# 👉 Task:

# Build a custom module “Library Management” (Books, Authors, Members)

# Implement CRUD operations

# Add access rights (Admin, Librarian, Member)