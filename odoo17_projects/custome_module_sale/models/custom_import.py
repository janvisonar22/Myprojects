from odoo import api, fields, models


class CustomImport(models.Model):
    _name = 'custom.import'

    name = fields.Char("Namesss")
