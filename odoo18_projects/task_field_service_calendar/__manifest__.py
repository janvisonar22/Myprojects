{
    'name': 'Task Field Service Calendar Filter',
    'version': '18.0.1.0.0',
    'summary': 'Adds Assigned To filter in Field Service calendar view',
    'description': '''
        Adds an "Assigned To" filter (for user/team) in the Field Service calendar view.
        Helps users quickly view tasks assigned to specific users or teams.
    ''',
    'author': 'TechUltra',
    'depends': ['field_service', 'project','mail'],
    'data': [
        'views/fieldservice_calendar_search.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
