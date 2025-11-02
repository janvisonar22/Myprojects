from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_record_ids = fields.One2many('custom.record', 'sale_order_id', string="Custom Records")
    custom_record_count = fields.Integer(string="Custom Record Count", compute='_compute_custom_record_count')

    @api.depends('custom_record_ids')
    def _compute_custom_record_count(self):
        for order in self:
            order.custom_record_count = len(order.custom_record_ids)

    def action_open_custom_records(self):
        """ Open form/tree view of all related custom records """
        self.ensure_one()
        return {
            'name': 'Custom Records',
            'type': 'ir.actions.act_window',
            'res_model': 'custom.record',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id},
        }

class CustomRecord(models.Model):
    _name = 'custom.record'
    _description = 'Custom Record'

    name = fields.Char(string="Name")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")

