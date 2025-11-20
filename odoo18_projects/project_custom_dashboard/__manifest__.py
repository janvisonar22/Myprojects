{
    "name": "Project Custom Dashboard",
    "version": "18.0.1.0.0",
    "category": "Project",
    "summary": "Dashboard for project KPIs",
    "depends": ["base", "web", "project", "sale_management", "account", "hr_timesheet"],
    "data": [
        "security/project_dashboard_security.xml",

        "security/ir.model.access.csv",

        "views/project_dashboard_menu.xml",
        # "views/project_project.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_custom_dashboard/static/src/js/project_dashboard.js",
            "project_custom_dashboard/static/src/xml/project_dashboard_template.xml",
        ],
    },
    "installable": True,
    "application": True,
}
