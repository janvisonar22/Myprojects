{
    'name': 'Log Note Delete Restrict',
    'version': '18.0.1.0.0',
    'summary': 'Prevents deletion of chatter log notes (with admin audit override).',
    'description': '''
        Disables the delete option for log note entries in chatter.
        Regular users cannot delete log notes.
        Only system administrators can delete, and such deletions are logged for audit purposes.
    ''',
    'author': 'TechUltra',
    'depends': ['mail', 'base'],
    'data': [
        'views/mail_message_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}

