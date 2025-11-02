# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
import xlsxwriter
import base64


class WizardStockInventory(models.TransientModel):
    _name = 'wizard.stock.inventory'
    _description = "Wizard Stock Inventory"

    xlsx_file = fields.Binary(
        string="XLSX File",
        help="Upload the Excel file containing the data to be processed."
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.user.company_id.id,
        help="The company associated with this record. Defaults to the current user's company."
    )
    warehouse_ids = fields.Many2many(
        'stock.warehouse',
        string='Warehouse',
        help="Select the warehouses to include in the report."
    )
    location_ids = fields.Many2many(
        'stock.location',
        string='Location',
        help="Select the stock locations to include in the report."
    )
    start_date = fields.Date(
        string="Start Date",
        help="The start date for filtering data in the report."
    )
    end_date = fields.Date(
        string="End Date",
        help="The end date for filtering data in the report."
    )
    filter_by = fields.Selection(
        [('product', 'Product'), ('category', 'Category')],
        string="Filter By",
        help="Choose whether to filter the data by product or category."
    )
    group_by_categ = fields.Boolean(
        string="Group By Category",
        help="Enable this option to group the report data by product category."
    )
    state = fields.Selection(
        [('choose', 'Choose'), ('get', 'Get')],
        default='choose',
        help="Indicates the current state of the report generation process."
    )
    name = fields.Char(
        string='File Name',
        readonly=True,
        help="The name of the generated report file."
    )
    data = fields.Binary(
        string='File',
        readonly=True,
        help="The generated report file in binary format."
    )
    product_ids = fields.Many2many(
        'product.product',
        string="Products",
        help="Select the products to include in the report."
    )
    category_ids = fields.Many2many(
        'product.category',
        string="Categories",
        help="Select the product categories to include in the report."
    )
    report_type = fields.Selection(
        [('pdf', 'PDF'), ('xlsx', 'Excel') ,('preview','Preview')],
        string="Report Type",
        default='pdf',
        help="Choose the format of the generated report: PDF or XLSX."
    )
    excel_format_type = fields.Selection(
        [('xls', 'XLS'), ('xlsx', 'XLSX')],
        string="Excel Format",
        default='xlsx',
        help="Choose the format of the generated report: XLS or XLSX."
    )
    html_preview = fields.Html(
        string="Preview",
        readonly=True,
        help="Preview of the report data in HTML format."
    )

    @api.onchange('report_type')
    def _onchange_report_type(self):
        if self.report_type == 'xlsx':
            self.excel_format_type = 'xlsx' 
        else:
            self.excel_format_type = False

    @api.onchange('excel_format_type')
    def _onchange_excel_format_type(self):
        if self.excel_format_type == 'xls':
            self.report_type = 'xlsx'

    @api.onchange('company_id')
    def onchange_company_id(self):
        domain = [('id', 'in', self.env.user.company_ids.ids)]
        if self.company_id:
            self.warehouse_ids = False
            self.location_ids = False
        return {'domain': {'company_id': domain}}

    @api.onchange('warehouse_ids')
    def onchange_warehouse_ids(self):
        stock_location_obj = self.env['stock.location']

        if self.warehouse_ids:
            self.location_ids = stock_location_obj.search([
                ('usage', '=', 'internal'),
                ('location_id', 'child_of', self.warehouse_ids.mapped('view_location_id.id')),
            ])
        else:
            self.location_ids = False

        return {'domain': {'location_ids': [('id', 'in', self.location_ids.ids)]}}

    def check_date_range(self):
        if self.end_date < self.start_date:
            raise ValidationError(_('End Date should be greater than Start Date.'))

    @api.onchange('filter_by')
    def onchange_filter_by(self):
        self.product_ids = False
        self.category_ids = False

    def pdf_report_print(self):
        self.check_date_range()

        datas = {
            'form': {
                'company_id': self.company_id.id,
                'warehouse_ids': [warehouse.id for warehouse in self.warehouse_ids],
                'location_ids': self.location_ids.ids or False,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'id': self.id,
                'product_ids': self.product_ids.ids,
                'product_categ_ids': self.category_ids.ids,
            },
            'docs': [self],  
        }

        report_action = self.env.ref('dps_stock_value_report.action_product_inventory_stock').report_action(self,
                                                                                                            data=datas)

        return report_action
    def choose_again(self):
        self.state = 'choose'

        action = {
            'name': 'Stock Status Report',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

        return action

    def action_preview_report(self):
        report_stock_inv_obj = self.env['report.dps_stock_value_report.stock_inventory_report']
        products = self.product_ids if self.product_ids else self.env['product.product'].search([])
        locations = self.location_ids if self.location_ids else self.env['stock.location'].search(
            [('usage', '=', 'internal')])
        if self.filter_by == 'category':
            if self.category_ids and not self.product_ids:
                products = self.env['product.product'].search([('categ_id', 'in', self.category_ids.ids)])
        grouped_products = {}
        if self.group_by_categ:
            categories = self.env['product.category'].search([])
            for category in categories:
                grouped_products[category] = products.filtered(lambda p: p.categ_id == category)
        else:
            grouped_products[False] = products

        preview_content = "<div style='font-size:20px; font-weight:bold;'>"
        preview_content += f"Date From: {self.start_date} <br/> Date To: {self.end_date}</div><br/><br/>"
        preview_content += "<div style='font-size:35px; font-weight:bold; text-align:center;'>Stock Inventory Report</div><br/>"
        preview_content += "<table border='1' style='width:100%; border-collapse:collapse; border: 1px solid #000;'>"

        preview_content += "<thead><tr style='background-color: #EDE9E4; font-color:#000000;'>"
        preview_content += "<th style='text-align:center; border: 1px solid #000; width:25%;'>Product Name</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000; width:30%;'>Location</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Opening</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Received</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Sales</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Internal</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Adjustment</th>"
        preview_content += "<th style='text-align:center; border: 1px solid #000;'>Closing</th>"
        preview_content += "</tr></thead><tbody>"

        grand_total_beginning = 0
        grand_total_received = 0
        grand_total_sales = 0
        grand_total_internal = 0
        grand_total_adjustment = 0
        grand_total_ending = 0

        for category, category_products in grouped_products.items():
            if category and category_products: 
                preview_content += f"<tr style='background-color:#e0e0e0;'>"
                preview_content += f"<td colspan='8' style='text-align:center; font-weight:bold; border: 1px solid #000;'>{category.name}</td>"
                preview_content += "</tr>"

            category_total_beginning = 0
            category_total_received = 0
            category_total_sales = 0
            category_total_internal = 0
            category_total_adjustment = 0
            category_total_ending = 0

            for product in category_products:
                product_total_beginning = 0
                product_total_received = 0
                product_total_sales = 0
                product_total_internal = 0
                product_total_adjustment = 0
                product_total_ending = 0

                preview_content += f"<tr style='background-color:#f1f1f1;'>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;' rowspan='{len(locations) + 1}'>{product.display_name}</td>"

                first_location = True  
                for location in locations:
                    product_data = report_stock_inv_obj._get_beginning_inventory(self, product, self.warehouse_ids[0],
                                                                                 [location.id])
                    sale_qty_data = report_stock_inv_obj.get_product_sale_qty(self, self.warehouse_ids[0], product,
                                                                              [location.id])

                    beginning_qty = product_data
                    received_qty = sale_qty_data['product_qty_in']
                    sales_qty = sale_qty_data['product_qty_out']
                    internal_qty = sale_qty_data['product_qty_internal']
                    adjustment_qty = sale_qty_data['product_qty_adjustment']
                    ending_qty = beginning_qty + received_qty - sales_qty + internal_qty + adjustment_qty

                    product_total_beginning += beginning_qty
                    product_total_received += received_qty
                    product_total_sales += sales_qty
                    product_total_internal += internal_qty
                    product_total_adjustment += adjustment_qty
                    product_total_ending += ending_qty

                    if not first_location:
                        preview_content += "<tr>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{location.complete_name}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{beginning_qty:.2f}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{received_qty:.2f}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{sales_qty:.2f}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{internal_qty:.2f}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{adjustment_qty:.2f}</td>"
                    preview_content += f"<td style='text-align:center; border: 1px solid #000;'>{ending_qty:.2f}</td>"
                    preview_content += "</tr>"
                    first_location = False

                preview_content += "<tr style='background-color:#f9f9f9;'>"
                preview_content += "<td style='text-align:center; border: 1px solid #000;' align='right'><strong>Total</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_beginning:.2f}</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_received:.2f}</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_sales:.2f}</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_internal:.2f}</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_adjustment:.2f}</strong></td>"
                preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{product_total_ending:.2f}</strong></td>"
                preview_content += "</tr>"

                category_total_beginning += product_total_beginning
                category_total_received += product_total_received
                category_total_sales += product_total_sales
                category_total_internal += product_total_internal
                category_total_adjustment += product_total_adjustment
                category_total_ending += product_total_ending

            grand_total_beginning += category_total_beginning
            grand_total_received += category_total_received
            grand_total_sales += category_total_sales
            grand_total_internal += category_total_internal
            grand_total_adjustment += category_total_adjustment
            grand_total_ending += category_total_ending

        preview_content += "<tr style='background-color:#d9d9d9;'>"
        preview_content += "<td colspan='2' style='text-align:center; font-weight:bold; border: 1px solid #000;'>Grand Total</td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_beginning:.2f}</strong></td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_received:.2f}</strong></td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_sales:.2f}</strong></td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_internal:.2f}</strong></td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_adjustment:.2f}</strong></td>"
        preview_content += f"<td style='text-align:center; border: 1px solid #000;'><strong>{grand_total_ending:.2f}</strong></td>"
        preview_content += "</tr>"

        preview_content += "</tbody></table>"
        self.html_preview = preview_content

        return {
            'name': 'Stock Inventory Preview',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def xlsx_report_print(self):
        self.check_date_range()
        import datetime
        import io

        current_datetime = datetime.datetime.now()


        if self.excel_format_type == 'xls':
            file_name = f"Product_Stock_Report_{current_datetime.strftime('%d_%m_%Y_%H_%M_%S')}.xls"
        else:
            file_name = f"Product_Stock_Report_{current_datetime.strftime('%d_%m_%Y_%H_%M_%S')}.xlsx"

        file_data = io.BytesIO()

        workbook = xlsxwriter.Workbook(file_data, {'in_memory': True})

        report_stock_inv_obj = self.env['report.dps_stock_value_report.stock_inventory_report']

        header_merge_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 10,
            'bg_color': '#EDE9E4',
            'font_color':'#000000;',  
            'border': 1 ,
            'font_name': 'Arial',
        })

        header_data_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1,
            'font_name': 'Arial',  
        })

        product_header_format = workbook.add_format({
            'valign': 'vcenter',
            'font_size': 10,
            'border': 1 ,
            'font_name': 'Arial',
        })

        for warehouse in self.warehouse_ids:
            worksheet = workbook.add_worksheet(warehouse.name)
            worksheet.merge_range(0, 0, 2, 8, "Inventory Stock Report", header_merge_format)

            worksheet.set_column('A:B', 18)
            worksheet.set_column('C:H', 12)

            worksheet.write(5, 0, 'Company', header_merge_format)
            worksheet.write(5, 1, 'Warehouse', header_merge_format)
            worksheet.write(5, 2, 'Start Date', header_merge_format)
            worksheet.write(5, 3, 'End Date', header_merge_format)

            worksheet.write(6, 0, self.company_id.name, header_data_format)
            worksheet.write(6, 1, warehouse.name, header_data_format)
            worksheet.write(6, 2, str(self.start_date), header_data_format)
            worksheet.write(6, 3, str(self.end_date), header_data_format)


            if not self.location_ids:
                worksheet.merge_range(9, 0, 9, 1, "Product Name", header_merge_format)
                worksheet.write(9, 2, "Opening", header_merge_format)
                worksheet.write(9, 3, "Received", header_merge_format)
                worksheet.write(9, 4, "Sales", header_merge_format)
                worksheet.write(9, 5, "Internal", header_merge_format)
                worksheet.write(9, 6, "Adjustments", header_merge_format)
                worksheet.write(9, 7, "Closing", header_merge_format)

                rows = 10
                prod_beginning_qty = prod_qty_in = prod_qty_out = prod_qty_int = prod_qty_adjust = prod_ending_qty = 0.00

                if not self.group_by_categ:
                    for product in report_stock_inv_obj._fetch_product_data(self):
                        beginning_qty = report_stock_inv_obj._get_beginning_inventory(self, product, warehouse)

                        product_val = report_stock_inv_obj.get_product_sale_qty(self, warehouse, product)
                        product_qty_in = product_val.get('product_qty_in')
                        product_qty_out = product_val.get('product_qty_out')
                        product_qty_internal = product_val.get('product_qty_internal')
                        product_qty_adjustment = product_val.get('product_qty_adjustment')

                        ending_qty = beginning_qty + product_qty_in + product_qty_out + product_qty_internal + product_qty_adjustment

                        worksheet.merge_range(rows, 0, rows, 1, product.name_get()[0][1], product_header_format)
                        worksheet.write(rows, 2, beginning_qty, header_data_format)
                        worksheet.write(rows, 3, product_qty_in, header_data_format)
                        worksheet.write(rows, 4, abs(product_qty_out), header_data_format)
                        worksheet.write(rows, 5, product_qty_internal, header_data_format)
                        worksheet.write(rows, 6, product_qty_adjustment, header_data_format)
                        worksheet.write(rows, 7, ending_qty, header_data_format)

                        prod_beginning_qty += beginning_qty
                        prod_qty_in += product_qty_in
                        prod_qty_out += product_qty_out
                        prod_qty_int += product_qty_internal
                        prod_qty_adjust += product_qty_adjustment
                        prod_ending_qty += ending_qty
                        rows += 1

                    worksheet.merge_range(rows + 1, 0, rows + 1, 1, 'Total', header_merge_format)
                    worksheet.write(rows + 1, 2, prod_beginning_qty, header_merge_format)
                    worksheet.write(rows + 1, 3, prod_qty_in, header_merge_format)
                    worksheet.write(rows + 1, 4, abs(prod_qty_out), header_merge_format)
                    worksheet.write(rows + 1, 5, prod_qty_int, header_merge_format)
                    worksheet.write(rows + 1, 6, prod_qty_adjust, header_merge_format)
                    worksheet.write(rows + 1, 7, prod_ending_qty, header_merge_format)

                else:
                    rows += 1
                    product_val = report_stock_inv_obj.get_product_sale_qty(self, warehouse)
                    if product_val:
                        for categ, product_value in product_val.items():
                            categ_prod_beginning_qty = categ_prod_qty_in = categ_prod_qty_out = categ_prod_qty_int = categ_prod_qty_adjust = categ_prod_ending_qty = 0.00

                            worksheet.merge_range(rows, 0, rows, 7, self.env['product.category'].browse(categ).name,
                                                  header_merge_format)
                            rows += 1

                            for product in product_value:
                                product_id = self.env['product.product'].browse(product['product_id'])
                                beginning_qty = report_stock_inv_obj._get_beginning_inventory(self, product_id.id,
                                                                                              warehouse)

                                product_qty_in = product.get('product_qty_in')
                                product_qty_out = product.get('product_qty_out')
                                product_qty_internal = product.get('product_qty_internal')
                                product_qty_adjustment = product.get('product_qty_adjustment')

                                ending_qty = beginning_qty + product_qty_in + product_qty_out + product_qty_internal + product_qty_adjustment

                                worksheet.merge_range(rows, 0, rows, 1, product_id.name_get()[0][1], product_header_format)
                                worksheet.write(rows, 2, beginning_qty, header_data_format)
                                worksheet.write(rows, 3, product_qty_in, header_data_format)
                                worksheet.write(rows, 4, abs(product_qty_out), header_data_format)
                                worksheet.write(rows, 5, product_qty_internal, header_data_format)
                                worksheet.write(rows, 6, product_qty_adjustment, header_data_format)
                                worksheet.write(rows, 7, ending_qty, header_data_format)

                                categ_prod_beginning_qty += beginning_qty
                                categ_prod_qty_in += product_qty_in
                                categ_prod_qty_out += product_qty_out
                                categ_prod_qty_int += product_qty_internal
                                categ_prod_qty_adjust += product_qty_adjustment
                                categ_prod_ending_qty += ending_qty
                                rows += 1

                            worksheet.merge_range(rows, 0, rows, 1, 'Total', header_merge_format)
                            worksheet.write(rows, 2, categ_prod_beginning_qty, header_merge_format)
                            worksheet.write(rows, 3, categ_prod_qty_in, header_merge_format)
                            worksheet.write(rows, 4, abs(categ_prod_qty_out), header_merge_format)
                            worksheet.write(rows, 5, categ_prod_qty_int, header_merge_format)
                            worksheet.write(rows, 6, categ_prod_qty_adjust, header_merge_format)
                            worksheet.write(rows, 7, categ_prod_ending_qty, header_merge_format)

                            prod_qty_in += categ_prod_qty_in
                            prod_qty_out += categ_prod_qty_out
                            prod_qty_int += categ_prod_qty_int
                            prod_qty_adjust += categ_prod_qty_adjust
                            prod_ending_qty += categ_prod_ending_qty
                            prod_beginning_qty += categ_prod_beginning_qty
                            rows += 2

                        worksheet.merge_range(rows, 0, rows, 1, "Total", header_merge_format)
                        worksheet.write(rows, 2, prod_beginning_qty, header_merge_format)
                        worksheet.write(rows, 3, prod_qty_in, header_merge_format)
                        worksheet.write(rows, 4, abs(prod_qty_out), header_merge_format)
                        worksheet.write(rows, 5, prod_qty_int, header_merge_format)
                        worksheet.write(rows, 6, prod_qty_adjust, header_merge_format)
                        worksheet.write(rows, 7, prod_ending_qty, header_merge_format)


            #
            else:
                worksheet.merge_range(9, 0, 9, 1, "Products", header_merge_format)
                worksheet.write(9, 2, "Location", header_merge_format)
                worksheet.write(9, 3, "Beginning", header_merge_format)
                worksheet.write(9, 4, "Received", header_merge_format)
                worksheet.write(9, 5, "Sales", header_merge_format)
                worksheet.write(9, 6, "Internal", header_merge_format)
                worksheet.write(9, 7, "Adjustments", header_merge_format)
                worksheet.write(9, 8, "Ending", header_merge_format)

                rows = 10
                prod_beginning_qty = prod_qty_in = prod_qty_out = prod_qty_int = prod_qty_adjust = prod_ending_qty = 0.00

                location_ids = report_stock_inv_obj.fetch_warehouse_wise_location(self, warehouse)

                if not self.group_by_categ:
                    for product in report_stock_inv_obj._fetch_product_data(self):
                        location_wise_data = report_stock_inv_obj.fetch_location_wise_product(self, warehouse, product,
                                                                                              location_ids)

                        beginning_qty = location_wise_data[1][0]
                        product_qty_in = location_wise_data[1][1]
                        product_qty_out = location_wise_data[1][2]
                        product_qty_internal = location_wise_data[1][3]
                        product_qty_adjustment = location_wise_data[1][4]
                        ending_qty = location_wise_data[1][5]

                        worksheet.merge_range(rows, 0, rows, 1, product.display_name, product_header_format)
                        worksheet.write(rows, 2, '', header_data_format)
                        worksheet.write(rows, 3, beginning_qty, header_merge_format)
                        worksheet.write(rows, 4, product_qty_in, header_merge_format)
                        worksheet.write(rows, 5, abs(product_qty_out), header_merge_format)
                        worksheet.write(rows, 6, product_qty_internal, header_merge_format)
                        worksheet.write(rows, 7, product_qty_adjustment, header_merge_format)
                        worksheet.write(rows, 8, ending_qty, header_merge_format)
                        rows += 1

                        for location, value in location_wise_data[0].items():
                            worksheet.merge_range(rows, 0, rows, 1, '', header_data_format)
                            worksheet.write(rows, 2, location.display_name, header_data_format)
                            worksheet.write(rows, 3, value[0], header_data_format)
                            worksheet.write(rows, 4, value[1], header_data_format)
                            worksheet.write(rows, 5, abs(value[2]), header_data_format)
                            worksheet.write(rows, 6, value[3], header_data_format)
                            worksheet.write(rows, 7, value[4], header_data_format)
                            worksheet.write(rows, 8, value[5], header_data_format)
                            rows += 1

                        prod_beginning_qty += beginning_qty
                        prod_qty_in += product_qty_in
                        prod_qty_out += product_qty_out
                        prod_qty_int += product_qty_internal
                        prod_qty_adjust += product_qty_adjustment
                        prod_ending_qty += ending_qty

                    rows += 1
                    worksheet.merge_range(rows, 0, rows, 1, 'Total', header_merge_format)
                    worksheet.write(rows, 2, '', header_merge_format)
                    worksheet.write(rows, 3, prod_beginning_qty, header_merge_format)
                    worksheet.write(rows, 4, prod_qty_in, header_merge_format)
                    worksheet.write(rows, 5, abs(prod_qty_out), header_merge_format)
                    worksheet.write(rows, 6, prod_qty_int, header_merge_format)
                    worksheet.write(rows, 7, prod_qty_adjust, header_merge_format)
                    worksheet.write(rows, 8, prod_ending_qty, header_merge_format)

                else:
                    product_val = report_stock_inv_obj.get_product_sale_qty(self, warehouse)

                    if product_val:
                        for categ, product_value in product_val.items():
                            categ_prod_beginning_qty = categ_prod_qty_in = categ_prod_qty_out = categ_prod_qty_int = categ_prod_qty_adjust = categ_prod_ending_qty = 0.00

                            worksheet.merge_range(rows, 0, rows, 8, self.env['product.category'].browse(categ).name,
                                                  header_merge_format)
                            rows += 1

                            for product in product_value:
                                product_id = self.env['product.product'].browse(product['product_id'])
                                location_wise_data = report_stock_inv_obj.fetch_location_wise_product(self, warehouse,
                                                                                                      product_id,
                                                                                                      location_ids)

                                beginning_qty = location_wise_data[1][0]
                                product_qty_in = location_wise_data[1][1]
                                product_qty_out = abs(location_wise_data[1][2])
                                product_qty_internal = location_wise_data[1][3]
                                product_qty_adjustment = location_wise_data[1][4]
                                ending_qty = location_wise_data[1][5]

                                worksheet.merge_range(rows, 0, rows, 1, product_id.display_name, product_header_format)
                                worksheet.write(rows, 2, '', header_data_format)
                                worksheet.write(rows, 3, beginning_qty, header_merge_format)
                                worksheet.write(rows, 4, product_qty_in, header_merge_format)
                                worksheet.write(rows, 5, product_qty_out, header_merge_format)
                                worksheet.write(rows, 6, product_qty_internal, header_merge_format)
                                worksheet.write(rows, 7, product_qty_adjustment, header_merge_format)
                                worksheet.write(rows, 8, ending_qty, header_merge_format)

                                rows += 1

                                for location, value in location_wise_data[0].items():
                                    worksheet.merge_range(rows, 0, rows, 1, '', header_data_format)
                                    worksheet.write(rows, 2, location.display_name, header_data_format)
                                    worksheet.write(rows, 3, value[0], header_data_format)
                                    worksheet.write(rows, 4, value[1], header_data_format)
                                    worksheet.write(rows, 5, abs(value[2]), header_data_format)
                                    worksheet.write(rows, 6, value[3], header_data_format)
                                    worksheet.write(rows, 7, value[4], header_data_format)
                                    worksheet.write(rows, 8, value[5], header_data_format)
                                    rows += 1

                                categ_prod_beginning_qty += beginning_qty
                                categ_prod_qty_in += product_qty_in
                                categ_prod_qty_out += product_qty_out
                                categ_prod_qty_int += product_qty_internal
                                categ_prod_qty_adjust += product_qty_adjustment
                                categ_prod_ending_qty += ending_qty

                                rows += 1

                                worksheet.merge_range(rows, 0, rows, 1, "Total", header_merge_format)
                                worksheet.write(rows, 2, '', header_merge_format)
                                worksheet.write(rows, 3, categ_prod_beginning_qty, header_merge_format)

                            worksheet.write(rows, 4, categ_prod_qty_in, header_merge_format)
                            worksheet.write(rows, 5, categ_prod_qty_out, header_merge_format)
                            worksheet.write(rows, 6, categ_prod_qty_int, header_merge_format)
                            worksheet.write(rows, 7, categ_prod_qty_adjust, header_merge_format)
                            worksheet.write(rows, 8, categ_prod_ending_qty, header_merge_format)
                            rows += 2

        workbook.close()

        file_data.seek(0)

        encoded_data = base64.b64encode(file_data.read())

        self.write({'xlsx_file': encoded_data})

        response = {
            'type': 'ir.actions.act_url',
            'url': f"web/content/?model=wizard.stock.inventory&id={self.id}&field=xlsx_file&download=true&filename={file_name}",
            'target': 'new',  
            'filename': file_name,  
        }

        return response


