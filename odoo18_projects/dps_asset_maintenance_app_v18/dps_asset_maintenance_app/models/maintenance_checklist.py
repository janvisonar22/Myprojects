from odoo import fields,models

class MaintenanceChecklistItem(models.Model):
    _name = 'maintenance.checklist'

    title = fields.Char(string="Title",required=True)
    description = fields.Text(string="Description")
    maintenance_id = fields.Many2one('maintenance.request',string="Maintenance")
    equipment_checklist_id = fields.Many2one('maintenance.equipment',string="Maintenance Equipment")
