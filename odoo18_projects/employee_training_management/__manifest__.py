{
    'name': 'Employee Training Management',
    'version': '18.0',
    'category': 'Human Resources',
    'summary': 'Manage and track employee training sessions',
    'description': """
Employee Training Management
============================
This module allows HR teams to manage employee training sessions.
Features include:
- Create and manage training sessions.
- Assign trainers and attendees.
- Automatically mark employees as trained.
- Prevent overlapping trainer sessions.
- Cancel old draft sessions automatically.
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',

        'data/cron_cancel_old_sessions.xml',
        'views/training_session_views.xml',
        'views/hr_employee_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
