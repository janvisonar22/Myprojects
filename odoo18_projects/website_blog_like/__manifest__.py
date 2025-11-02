{
    'name': 'Website Blog Like',
    'version': '18.0',
    'summary': 'Simple blog with like button on website',
    'category': 'Website',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'data/website_menu.xml',
        'views/blog_templates.xml',
        'views/blog_post_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,    
    'license': 'LGPL-3',
}
