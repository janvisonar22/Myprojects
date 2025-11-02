from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)

class SaleCustomWizard(models.TransientModel):
    _name = 'sale.custom.wizard'
    _description = 'Custom Wizard for Sale Order'

    order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    # amount_total = fields.Float(string='Total Amount', readonly=True)
    # state = fields.Selection(selection=[('draft', 'Draft'), ('sent', 'Quotation Sent'), ('sale', 'Sales Order'), ('done', 'Locked'), ('cancel', 'Cancelled')], string='State', readonly=True)
    date_order = fields.Datetime(string='Order Date', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', readonly=True)
    order_line_ids = fields.One2many('sale.custom.wizard.line', 'wizard_id', string='Order Lines')

    @api.model
    def default_get(self, fields_list):
        res = super(SaleCustomWizard, self).default_get(fields_list)
        if self.env.context.get('default_order_id'):
            sale_order = self.env['sale.order'].browse(self.env.context['default_order_id'])
            for field in self._fields:
                if field in sale_order._fields and field in fields_list:
                    res[field] = getattr(sale_order, field)
            
            order_lines = []
            for line in sale_order.order_line:
                tax_values = [f"{tax.amount}%" for tax in line.tax_id]  
                tax_string = ", ".join(tax_values) if tax_values else "No Tax"

                order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'tax_id': [(6, 0, line.tax_id.ids)],
                    'tax_display': tax_string,  # Pass the formatted tax string
                }))
            res['order_line_ids'] = order_lines
        return res


    def confirm_action(self):
        return {'type': 'ir.actions.act_window_close'}
