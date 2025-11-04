from odoo import fields, models, api, _


class wizard_pos_sale_report(models.TransientModel):
    _name = 'wizard.pos.sale.report'
    _description = 'Wizard Pos Sale Report'


    def print_receipt(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'wizard.pos.sale.report'
                 }
        return self.env.ref('pos_x_report.report_pos_sales_pdf').report_action(self, data=datas)

    session_ids = fields.Many2many('pos.session', 'pos_session_list', 'wizard_id', 'session_id',
                                   string="Closed Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                    ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
