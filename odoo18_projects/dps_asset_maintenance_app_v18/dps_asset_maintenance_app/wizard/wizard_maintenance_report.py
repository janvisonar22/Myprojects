import xlsxwriter
import base64
from io import BytesIO
from odoo import fields, models, api, _
from odoo.tools import html2plaintext


class WizardMaintenanceReport(models.TransientModel):
    _name = 'wizard.maintenance.report'
    _description = 'Wizard Maintenance Report'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    xls_file = fields.Binary(string='Download')
    name = fields.Char(string='File name')
    state = fields.Selection([('choose', 'Choose'),
                              ('download', 'Download')],
                             default="choose", string="Status")
    maintenance_ids = fields.Many2many(
        'maintenance.request',
        string="Maintenance Requests",
        default=lambda self: self._context.get('active_ids'),
        compute="_compute_maintenance_ids"
    )
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    report_type = fields.Selection([('pdf', 'PDF'), ('xlsx', 'XLSX')],
                                   string="Report Type", default='pdf')
    customer_ids = fields.Many2many('res.partner',string="Customer")

    @api.depends('start_date', 'end_date')
    def _compute_maintenance_ids(self):
        for wizard in self:
            domain = [
                ('request_date', '>=', wizard.start_date),
                ('request_date', '<=', wizard.end_date),
            ]
            if wizard.customer_ids:
                domain.append(('customer_id', 'in', wizard.customer_ids.ids))
            wizard.maintenance_ids = self.env['maintenance.request'].search(domain)

    def action_print_pdf(self):
        self.ensure_one()
        return self.env.ref('dps_asset_maintenance_app.dps_action_maintenance_report_pdf').report_action(self)

    def action_print_xlsx(self):
        request_ids = self.maintenance_ids
        xls_filename = 'Maintenance_Report.xlsx'
        file_path = f'/tmp/{xls_filename}'
        company_details_html = self.env.company.company_details or ''
        company_details_plain = html2plaintext(company_details_html)
        workbook = xlsxwriter.Workbook(file_path)
        sheet = workbook.add_worksheet("Maintenance Report")
        dp_text_center = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'border': 1,
            'font_name': 'Arial',
        })

        dp_first_dp_header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#EDE9E4',
            'font_color': '#000000',
            'border': 1,
            'font_name': 'Arial',
        })
        dp_header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#EDE9E4',
            'font_color': '#000000',
            'border': 1,
            'font_name': 'Arial',
        })
        dp_content_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_color': '#000000',
            'font_name': 'Arial',
        })
        dp_footer_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'bg_color': '#f5ec4c',
            'font_name': 'Arial',
        })
        sheet.set_column('A:AZ', 18)
        for i in range(3):
            sheet.set_row(i, 18)
        logo = self.env.company.logo
        if logo:
            logo_binary = base64.b64decode(logo)
            logo_stream = BytesIO(logo_binary)
        sheet.set_column('A:B', 25)
        sheet.set_row(0, 20)
        sheet.set_row(1, 20)
        sheet.insert_image('A1', 'logo.png', {'image_data': logo_stream, 'x_scale': 0.3, 'y_scale': 0.3, 'width': 150, 'height': 50})
        sheet.write('C1', 'User Name', dp_first_dp_header_format)
        sheet.merge_range('D1:E1', self.env.user.name or '', dp_text_center)
        sheet.write('C2', 'Company Name', dp_first_dp_header_format)
        sheet.merge_range('D2:E2', self.env.company.name or '', dp_text_center)
        sheet.merge_range('H1:H3', 'Company Address', dp_first_dp_header_format)
        sheet.merge_range('I1:J3', company_details_plain, dp_text_center)
        date_from = self.start_date
        date_to = self.end_date
        sheet.write('D7', 'Start Date', dp_first_dp_header_format)
        sheet.merge_range('E7:F7', str(date_from), dp_text_center)
        sheet.write('G7', 'End Date', dp_first_dp_header_format)
        sheet.merge_range('H7:I7', str(date_to), dp_text_center)
        sheet.merge_range('F5:G5', 'Maintenance Report', dp_first_dp_header_format)
        row = 8
        sr_no = 1
        final_cost = 0
        for req in request_ids:
            sheet.write(row, 0, 'No', dp_header_format)
            sheet.write(row, 1, 'Request No', dp_header_format)
            sheet.write(row, 2, 'Equipment', dp_header_format)
            sheet.write(row, 3, 'Category', dp_header_format)
            sheet.write(row, 4, 'Request Date', dp_header_format)
            sheet.write(row, 5, 'Close Date', dp_header_format)
            sheet.write(row, 6, 'Responsible', dp_header_format)
            sheet.write(row, 7, 'Maintenance Cost', dp_header_format)
            sheet.write(row, 8, 'Vendor', dp_header_format)
            sheet.write(row, 9, 'Invoice', dp_header_format)
            row += 1

            sheet.write(row, 0, sr_no, dp_content_format)
            sheet.write(row, 1, req.name or '', dp_content_format)
            sheet.write(row, 2, req.equipment_id.name or '', dp_content_format)
            sheet.write(row, 3, req.category_id.name or '', dp_content_format)
            sheet.write(row, 4, str(req.request_date or ''), dp_content_format)
            sheet.write(row, 5, str(req.close_date or ''), dp_content_format)
            sheet.write(row, 6, req.user_id.name or '', dp_content_format)
            sheet.write(row, 7, req.maintenance_cost or 0.0, dp_content_format)
            final_cost += req.maintenance_cost or 0.0
            sheet.write(row, 8, req.requisition_vendor_id.name or '', dp_content_format)
            sheet.write(row, 9, req.invoice_id.name or '', dp_content_format)

            row += 2

            sheet.merge_range(row, 3, row, 6, f"Checklist of {req.name}", dp_first_dp_header_format)
            row += 1
            sheet.write(row, 4, "Title", dp_header_format)
            sheet.write(row, 5, "Description", dp_header_format)
            row += 1
            for chk in req.checklist_ids:
                sheet.write(row, 4, chk.title or '', dp_content_format)
                sheet.write(row, 5, chk.description or '', dp_content_format)
                row += 1
            row += 1
            sheet.merge_range(row, 3, row, 6, f"Product requisition of {req.name}", dp_first_dp_header_format)
            row += 1
            sheet.write(row, 4, "Product", dp_header_format)
            sheet.write(row, 5, "Quantity", dp_header_format)
            sheet.write(row, 6, "UOM", dp_header_format)
            row += 1
            for line in req.requisition_maintenance_ids:
                sheet.write(row, 4, line.product_id.name or '', dp_content_format)
                sheet.write(row, 5, line.quantity or 0, dp_content_format)
                sheet.write(row, 6, line.uom_id.name or '', dp_content_format)
                row += 1
            row += 2
            sr_no += 1
        row += 1
        workbook.close()
        with open(file_path, 'rb') as file:
            encoded_file = base64.b64encode(file.read())
        self.write({'state': 'download', 'name': xls_filename, 'xls_file': encoded_file})

        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": "/web/content?model={}&download=true&field=xls_file&filename=Maintenance_Report.xlsx&id={}".format(
                self._name, self.id
            ),
        }