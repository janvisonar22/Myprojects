from odoo import models
import io
import xlsxwriter

class SalesPurchaseReportXlsx(models.AbstractModel):
    _name = 'report.sale_purchase_details.report_sales_purchase_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, records):
        for wizard in records:
            sheet = workbook.add_worksheet("Sales and Purchase")
            bold = workbook.add_format({'bold':True,'bg_color':'#D3D3D3','border':1})
            border = workbook.add_format({'border':1,'align':'right'})
            red_text = workbook.add_format({'font_color':'red','bold':True})
            green_bg = workbook.add_format({'bg_color':'#C6EFCE','border':1})
            yellow_bg = workbook.add_format({'bg_color':'#FFFF00','border':1})
            sheet.set_column(0,0,15)
            sheet.set_column(1,1,15)
            sheet.set_column(2,2,20)
            sheet.set_column(3,3,5)
            sheet.set_column(4,4,10)
            sheet.set_column(5,5,12)
            sheet.set_column(6,6,18)
            sheet.set_column(7,7,18)
            sheet.set_column(8,8,12)

            sheet.merge_range('A1:I1',"Sales And Purchase Report ",bold)
            sheet.write(2,0,"Partner:",bold)
            sheet.write(2,1,wizard.partner_id.name)
            sheet.write(3,0,"Date Range",bold)
            sheet.write(3,1,f"{wizard.start_date} to {wizard.end_date}")

            header = ['Sr.No.','Order No.','Product','Qty','Unit Price','Tax','Total Without Tax','Total With Tax','Status']
            row = 5
            sheet.write(row,0,"Sale Orders", bold)
            row += 1
            sheet.write_row(row,0,header,bold)
            row += 1
            sales_data = wizard.get_sales_data()
            if sales_data:
                index = 1
                for sale in sales_data:
                    sheet.write(row, 0, index,border)
                    sheet.write(row,1,sale['order_no'],border)
                    sheet.write(row,2,sale['product'],border)

                    sheet.write(row,3,sale['qty'],border)
                    sheet.write(row,4,sale['price'],border)
                    sheet.write(row,5,sale['tax'],border)                    
                    sheet.write(row,6,sale['total_without_tax'],border)
                    sheet.write(row,7,sale['total_with_tax'],border)
                    sheet.write(row,8,sale['status'],border)
                    row += 1
                    index += 1
            else:
                sheet.write(row,0,"No Sale Date",border)

            row += 2
            sheet.write(row,0,"Purchase Orders",bold)
            row += 1
            sheet.write_row(row,0,header,bold)
            row += 1
            purchase_data = wizard.get_purchase_data()
            if purchase_data:
                index = 1
                for purchase in purchase_data:
                    sheet.write(row,0,index,border)                    
                    sheet.write(row,1,purchase['order_no'],border)
                    sheet.write(row,2,purchase['product'],border)
                    sheet.write(row,3,purchase['qty'],border)
                    sheet.write(row,4,purchase['price'],border)
                    sheet.write(row,5,purchase['tax'],border)
                    sheet.write(row,6,purchase['total_without_tax'],border)
                    sheet.write(row,7,purchase['total_with_tax'],border)
                    sheet.write(row,8,purchase['status'],border)
                    row += 1
                    index += 1

            else:
                sheet.write(row,0,"No Purchase Data",border)




