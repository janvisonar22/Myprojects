from odoo import models,fields,api

class SaleCustomWizardLine(models.TransientModel):
    _name = 'sale.custom.wizard.line'
    _description = 'Wizard Order Line'

    wizard_id = fields.Many2one('sale.custom.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_uom_qty = fields.Float(string='Quantity', readonly=True)
    price_unit = fields.Float(string='Unit Price', readonly=True)
    tax_id = fields.Many2many('account.tax', string='Taxes', readonly=True)
    tax_display = fields.Char(string='Taxes', compute="_compute_tax_display", store=True)  # New field

    @api.depends('tax_id')
    def _compute_tax_display(self):
        for line in self:
            tax_values = [f"{tax.amount}%" for tax in line.tax_id]  # Extract tax percentage
            line.tax_display = ", ".join(tax_values) if tax_values else "No Tax"
