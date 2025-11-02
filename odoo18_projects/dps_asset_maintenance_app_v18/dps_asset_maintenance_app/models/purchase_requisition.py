from odoo import models,fields,api,_

class MaintenancePurchaseRequisition(models.Model):
    _name = 'maintenance.purchase.requisition'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    purchase_rep_id = fields.Many2one('res.users',string='Purchase Representative',default=lambda self: self.env.user)
    agreement_type = fields.Selection([('maintenance','Maintenance')],string="Agreement Type")
    vendor_id = fields.Many2one('res.partner',string='Vendor')
    agreement_deadline = fields.Date(string='Agreement Deadline')
    ordering_date = fields.Date(string='Ordering Date')
    delivery_date = fields.Date(string='Delivery Date')
    source_document = fields.Char(string='Source Document')
    maintenance_request_id = fields.Many2one('maintenance.request',string="Maintenance Request")
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)
    state = fields.Selection([('draft','Draft'),('ongoing','Ongoing'),('closed','Closed'),('cancel','Cancelled')],string="Status",default='draft',tracking=True)
    product_line_ids = fields.One2many('maintenance.product','purchase_requisition_id',string="Products")

    @api.model
    def create(self, vals):
        if vals.get('reference_number', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('maintenance.purchase.requisition')
        return super(MaintenancePurchaseRequisition, self).create(vals)

    def action_new_quotation(self):
        self.write({'state': 'ongoing'})

    def action_close(self):
        self.write({'state': 'closed'})
        for requisition in self:
            if requisition.maintenance_request_id:
                requisition.maintenance_request_id.action_repaired()

    def action_cancel(self):
        self.write({'state': 'cancel'})
