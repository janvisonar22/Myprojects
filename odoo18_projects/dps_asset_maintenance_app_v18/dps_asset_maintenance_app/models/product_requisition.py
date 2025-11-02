from odoo import models,fields,api

class MaintenanceProduct(models.Model):
    _name = 'maintenance.product'

    maintenance_equipment_id= fields.Many2one('maintenance.equipment',string="maintenance")
    maintenance_request_id= fields.Many2one('maintenance.request',string="maintenance")
    purchase_requisition_id= fields.Many2one('maintenance.purchase.requisition',string="Maintenance Purchase Requisition")
    product_id = fields.Many2one('product.product',required=True)
    quantity = fields.Float()
    uom_id = fields.Many2one('uom.uom', string='UoM')
    unit_price = fields.Float('Unit Price')


    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.lst_price