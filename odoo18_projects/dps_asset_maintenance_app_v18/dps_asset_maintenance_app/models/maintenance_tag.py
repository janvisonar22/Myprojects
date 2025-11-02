from odoo import models, fields, api


class MaintenanceTag(models.Model):
    _name = 'maintenance.tag'
    _description = 'Maintenance Tag'

    name = fields.Char(required=True)