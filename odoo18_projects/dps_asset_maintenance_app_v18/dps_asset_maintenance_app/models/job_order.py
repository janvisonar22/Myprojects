from odoo import models,fields

class MaintenanceJobOrder(models.Model):
    _name = 'maintenance.job.order'

    request_id = fields.Many2one('maintenance.request',"Maintenance Request")
    name = fields.Char(string="Name",related='request_id.name')
    project = fields.Char("Project")
    assiness_id = fields.Many2one('res.users','Assigness')
    customer_id = fields.Many2one('res.partner','Customer')
    planned_date = fields.Date("Planned Date")
    deadline_date = fields.Date("Deadline")
    descreption = fields.Text("Description")
    sequence = fields.Char("Sequence")
    email_cc = fields.Char("Email CC")
    company = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    cover_image = fields.Binary("Cover Image")
    assigned_date = fields.Date("Assigned Date")
    tags = fields.Many2many('maintenance.tag',string="Tags")



