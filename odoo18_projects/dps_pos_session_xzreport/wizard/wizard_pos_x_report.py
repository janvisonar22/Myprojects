from odoo import fields, models, api, _


class WizardPOSXReport(models.TransientModel):
    _name = 'wizard.pos.x.report'
    _description = 'Print Session in Progress Report Wizard'


    def print_x_report(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'wizard.pos.x.report'}
        return self.env.ref('dps_pos_session_xzreport.report_pos_sales_pdf_front').report_action(self, data=datas)

    session_ids = fields.Many2many('pos.session', 'pos_session_wizard_rel', 'x_wizard_id', 'pos_session_id',
                                   string="Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                    ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
    