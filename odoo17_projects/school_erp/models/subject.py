from odoo import models, fields

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subjects'

    name = fields.Char(string="Subject Name")
    code = fields.Char(string="Subject Code")
    teacher_id = fields.Many2one('res.teacher', string='Teacher')
