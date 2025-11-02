from odoo import models,fields,api
from odoo.exceptions import UserError


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    destination_location_id = fields.Many2one('stock.location',string="Destination Location")
    customer_id = fields.Many2one('res.partner',string="Customer",required=1)
    requisition_vendor_id = fields.Many2one('res.partner',string="Requisition Vendor",required=1)
    maintenance_cost = fields.Float(string="Maintenance Cost", related="equipment_id.cost", store=True,readonly=False)
    job_order_id = fields.Many2one('maintenance.job.order',string="Job Order")
    checklist_ids = fields.One2many(comodel_name='maintenance.checklist',inverse_name='maintenance_id',string="Check list")
    requisition_maintenance_ids = fields.One2many(comodel_name='maintenance.product',inverse_name='maintenance_request_id',string="Product Requisitions")
    invoice_id = fields.Many2one('account.move',string="Invoice")
    job_order_ids = fields.One2many('maintenance.job.order','request_id',string='Job Order')
    purchase_requisition_ids = fields.One2many('maintenance.purchase.requisition','maintenance_request_id',string='Purchase Requisitions')
    purchase_requisition_id = fields.Many2one('maintenance.purchase.requisition',string='Purchase Requisitions')
    is_scrapped = fields.Boolean("Scrap ",default=False)
    
    def create_invoice(self):
        self.ensure_one()

        partner = self.customer_id or self.equipment_id.partner_id
        if not partner:
            raise UserError("No customer assigned to this maintenance request.")

        account = partner.property_account_receivable_id
        if not account:
            raise UserError("No receivable account found for the customer.")

        if not self.equipment_id.cost:
            raise UserError("Maintenance cost must be set before creating an invoice.")

        product_name = self.equipment_id.name
        product = self.env['product.product'].search([('name','=',product_name)],limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': self.equipment_id.name,
                'lst_price': self.equipment_id.cost,
                'uom_id': self.env.ref('uom.product_uom_unit').id,
                'type': 'service',
            })
        if product:
            invoice_product = product.id
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_line_ids': [(0,0,{
                'product_id': invoice_product,
                'quantity': 1,
                'price_unit': self.equipment_id.cost,
            })],
        })
        self.invoice_id = invoice.id
        in_progress_stage = self.env['maintenance.stage'].search([('name','=','In Progress')],limit=1)
        if in_progress_stage:
            self.stage_id = in_progress_stage.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }



    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.maintenance_cost = self.equipment_id.cost
            self.requisition_maintenance_ids = [(5,0,0)] 
            lines = []
            for line in self.equipment_id.requisition_ids:
                lines.append((0,0,{
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                }))
            self.requisition_maintenance_ids = lines

            self.checklist_ids = [(5,0,0)]  
            checklist_lines = []             

            for item in self.equipment_id.checklist_equipment_ids:
                checklist_lines.append((0,0,{
                    'title': item.title,
                    'description': item.description,
                }))

            self.checklist_ids = checklist_lines

    def action_repaired(self):
        repaired_stage = self.env['maintenance.stage'].search([('name','=','Repaired')])
        if not repaired_stage:
            return

        for request in self:
            if request.invoice_id.state == 'posted' and request.purchase_requisition_id.state == 'closed':
                request.stage_id = repaired_stage.id

        
    def action_scrap(self):
        scrap_stage = self.env['maintenance.stage'].search([('name','=','Scrap')],limit=1)
        if scrap_stage:
            self.stage_id = scrap_stage.id
            self.is_scrapped = True

   
    def action_create_job_order(self):
        self.ensure_one()

        if self.job_order_id:
            raise UserError("Job Order already exists.")

        job_order = self.env['maintenance.job.order'].create({
            'request_id': self.id,
            'project': self.name,
            'assiness_id':  self.env.uid,
            'customer_id': self.customer_id.id,
            'planned_date': fields.Date.today(),
            'assigned_date': fields.Date.today(),
            'sequence': self.name,
            'email_cc': self.email_cc,
            'company': self.company_id.id,
        })

        self.job_order_id = job_order.id
        in_progress_stage = self.env['maintenance.stage'].search([('name','=','In Progress')],limit=1)
        if in_progress_stage:
            self.stage_id = in_progress_stage.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.job.order',
            'res_id': job_order.id,
            'view_mode': 'form',
            'view_id': self.env.ref('dps_asset_maintenance_app.job_order_form_view').id,
            'target': 'current',
        }

    def action_view_job_order(self):
        self.ensure_one()
        job_order = self.job_order_id
        if not job_order:
            return {'type': 'ir.actions.act_window_close'}

        action = self.env["ir.actions.actions"]._for_xml_id("dps_asset_maintenance_app.job_order_action_form")
        
        if job_order:
            action.update({
                'views': [(self.env.ref('dps_asset_maintenance_app.job_order_form_view').id,'form')],
                'res_id': job_order.id,
                'context': dict(self.env.context),
            })
        return action

    def action_create_equipment_purchase_requisition(self):
        self.ensure_one()
        if self.purchase_requisition_id:
            raise UserError("Job Order already exists.")

        line_vals = []
        for line in self.requisition_maintenance_ids:
            line_vals.append((0,0,{
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'uom_id': line.uom_id.id,
                'unit_price': line.product_id.lst_price,
            }))

        requisition = self.env['maintenance.purchase.requisition'].create({
            'purchase_rep_id': self.env.user.id,
            'vendor_id': self.requisition_vendor_id.id,
            'agreement_type': 'maintenance',
            'ordering_date': fields.Date.today(),
            'source_document': self.name,
            'maintenance_request_id': self.id,
            'company_id': self.company_id.id,
            'product_line_ids': line_vals,
        })
        self.purchase_requisition_id = requisition.id
        in_progress_stage = self.env['maintenance.stage'].search([('name','=','In Progress')],limit=1)
        if in_progress_stage:
            self.stage_id = in_progress_stage.id

        return {
            'name': 'Equipment Purchase Requisition',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.purchase.requisition',
            'view_mode': 'form',
            'res_id': requisition.id,
            'target': 'current',
        }

    def action_open_purchase_requisition(self):
        self.ensure_one()
        requisition = self.env['maintenance.purchase.requisition'].search([
            ('maintenance_request_id','=',self.id)
        ],limit=1)
        if requisition:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'maintenance.purchase.requisition',
                'view_mode': 'form',
                'res_id': requisition.id,
                'target': 'current',
            }

  

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    requisition_ids = fields.One2many(comodel_name='maintenance.product',inverse_name='maintenance_equipment_id',string="Product Requisitions")
    checklist_equipment_ids = fields.One2many(comodel_name='maintenance.checklist',inverse_name='equipment_checklist_id',string="Check list")


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def action_post(self):
        result = super().action_post()
        maintenance=self.env['maintenance.request'].search([('invoice_id','in',self.ids)])
        maintenance.action_repaired()
        return result