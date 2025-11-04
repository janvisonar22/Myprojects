from odoo import models, api, _


class front_sales_report_pdf_template(models.AbstractModel):
    _name = 'report.dps_pos_session_xzreport.front_sales_report_pdf_template'
    _description = "pos report sale report temp"

    @api.model
    def _get_report_values(self, docids, data=None):

        if len(docids) > 0:
            report = self.env['ir.actions.report']._get_report_from_name('dps_pos_session_xzreport.front_sales_report_pdf_template')
            if data and data.get('form') and data.get('form').get('session_ids'):
                docids = self.env['pos.session'].browse(data['form']['session_ids'])
            return {'doc_ids': docids,
                    'doc_model': report.model,
                    'docs': self.env['pos.session'].browse(docids),
                    'data': data,
                    }
        else:
            report = self.env['ir.actions.report']._get_report_from_name('dps_pos_session_xzreport.front_sales_report_pdf_template')
            if data and data.get('form') and data.get('form').get('session_ids'):
                docids = self.env['pos.session'].browse(data['form']['session_ids'])
            return {'doc_ids': self.env['wizard.pos.x.report'].browse(data['ids']),
                    'doc_model': report.model,
                    'docs': self.env['pos.session'].browse(data['form']['session_ids']),
                    'data': data,
                    }
