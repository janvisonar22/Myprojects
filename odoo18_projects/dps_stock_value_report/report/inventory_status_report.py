# -*- coding: utf-8 -*-

import pytz
import time
from operator import itemgetter
from itertools import groupby
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, date


class dps_stock_value_report_stock_inventory_report(models.AbstractModel):
    _name = 'report.dps_stock_value_report.stock_inventory_report'
    _description = "Report Stock Inventory"

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name(
            'dps_stock_value_report.stock_inventory_template_report')
        record_id = data['form']['id'] if data and data['form'] and data['form'].get('id') else docids[0]
        records = self.env['wizard.stock.inventory'].browse(record_id)

        return {
            'doc_model': report.model,
            'docs': records,
            'data': data,
            'fetch_beginning_inventory': self._get_beginning_inventory,
            'fetch_products': self._fetch_product_data,
            'get_product_sale_qty': self.get_product_sale_qty,
            'get_location_wise_product': self.fetch_location_wise_product,
            'get_warehouse_wise_location': self.fetch_warehouse_wise_location
        }

    def fetch_warehouse_wise_location(self, record, warehouse):
        stock_location_obj = self.env['stock.location']
        location_ids = stock_location_obj.search([('location_id', 'child_of', warehouse.view_location_id.id)])
        final_location_ids = record.location_ids & location_ids
        return final_location_ids or location_ids

    def fetch_location_wise_product(self, record, warehouse, product, location_ids, product_categ_id=None):
        group_by_location = {}
        begning_qty = product_qty_in = product_qty_out = product_qty_internal = product_qty_adjustment = ending_qty = product_ending_qty = 0.00

        for location in location_ids:
            group_by_location.setdefault(location, [])
            group_by_location[location].append(self._get_beginning_inventory(record, product, warehouse, [location.id]))

            get_product_sale_qty = self.get_product_sale_qty(record, warehouse, product, [location.id])
            location_begning_qty = group_by_location[location][0]

            group_by_location[location].extend([
                get_product_sale_qty['product_qty_in'],
                get_product_sale_qty['product_qty_out'],
                get_product_sale_qty['product_qty_internal'],
                get_product_sale_qty['product_qty_adjustment']
            ])

            ending_qty = location_begning_qty + get_product_sale_qty['product_qty_in'] + get_product_sale_qty[
                'product_qty_out'] + \
                         get_product_sale_qty['product_qty_internal'] + get_product_sale_qty['product_qty_adjustment']

            group_by_location[location].append(ending_qty)
            ending_qty = 0.00

            begning_qty += location_begning_qty
            product_qty_in += get_product_sale_qty['product_qty_in']
            product_qty_out += get_product_sale_qty['product_qty_out']
            product_qty_internal += get_product_sale_qty['product_qty_internal']
            product_qty_adjustment += get_product_sale_qty['product_qty_adjustment']

        product_ending_qty = begning_qty + product_qty_in + product_qty_out + product_qty_internal + product_qty_adjustment
        return group_by_location, [begning_qty, product_qty_in, product_qty_out, product_qty_internal,
                                   product_qty_adjustment, product_ending_qty]

    def fetch_location(self, records, warehouse):
        stock_location_obj = self.env['stock.location'].sudo()
        location_ids = [warehouse.view_location_id.id]
        domain = [
            ('company_id', '=', records.company_id.id),
            ('usage', '=', 'internal'),
            ('location_id', 'child_of', location_ids)
        ]
        final_location_ids = stock_location_obj.search(domain).ids
        return final_location_ids

    def with_timezone_convert(self, userdate):
        timezone = pytz.timezone(self._context.get('tz') or 'UTC')
        if timezone:
            utc = pytz.timezone('UTC')
            end_dt = timezone.localize(fields.Datetime.from_string(userdate), is_dst=False)
            end_dt = end_dt.astimezone(utc)
            return end_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return userdate.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _fetch_product_data(self, record):
        product_product_obj = self.env['product.product']
        domain = [('type', '=', 'consu'), ('is_storable', '=', True)]

        if record.category_ids:
            domain.append(('categ_id', 'in', record.category_ids.ids))
            product_ids = product_product_obj.search(domain)
        elif record.product_ids:
            product_ids = record.product_ids
        else:
            product_ids = product_product_obj.search(domain)

        return product_ids

    def _get_beginning_inventory(self, record, product, warehouse, location=None):
        locations = location if location else self.fetch_location(record, warehouse)

        if isinstance(product, int):
            product_data = product
        else:
            product_data = product.id

        start_date = record.start_date
        from_date = self.with_timezone_convert(start_date)

        self._cr.execute(''' 
            SELECT id as product_id, coalesce(sum(qty), 0.0) as qty
            FROM
                ((
                SELECT pp.id, pp.default_code, m.date,
                    CASE 
                        WHEN pt.uom_id = m.product_uom THEN u.name 
                        ELSE (SELECT name FROM uom_uom WHERE id = pt.uom_id) 
                    END AS name,

                    CASE 
                        WHEN pt.uom_id = m.product_uom THEN coalesce(sum(-m.product_qty)::decimal, 0.0)
                        ELSE coalesce(sum(-m.product_qty * pu.factor / u.factor)::decimal, 0.0) 
                    END AS qty

                FROM product_product pp 
                LEFT JOIN stock_move m ON (m.product_id = pp.id)
                LEFT JOIN stock_move_line ml ON (ml.move_id = m.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id = pt.id)
                LEFT JOIN stock_location l ON (m.location_id = l.id)    
                LEFT JOIN stock_picking p ON (m.picking_id = p.id)
                LEFT JOIN uom_uom pu ON (pt.uom_id = pu.id)
                LEFT JOIN uom_uom u ON (m.product_uom = u.id)
                WHERE m.date < %s AND (m.location_id IN %s) AND m.state = 'done' AND pp.active = True AND pp.id = %s
                GROUP BY pp.id, pt.uom_id, m.product_uom, pp.default_code, u.name, m.date
                ) 
                UNION ALL
                (
                SELECT pp.id, pp.default_code, m.date,
                    CASE 
                        WHEN pt.uom_id = m.product_uom THEN u.name 
                        ELSE (SELECT name FROM uom_uom WHERE id = pt.uom_id) 
                    END AS name,

                    CASE 
                        WHEN pt.uom_id = m.product_uom THEN coalesce(sum(m.product_qty)::decimal, 0.0)
                        ELSE coalesce(sum(m.product_qty * pu.factor / u.factor)::decimal, 0.0) 
                    END AS qty

                FROM product_product pp 
                LEFT JOIN stock_move m ON (m.product_id = pp.id)
                LEFT JOIN stock_move_line ml ON (ml.move_id = m.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id = pt.id)
                LEFT JOIN stock_location l ON (m.location_dest_id = l.id)    
                LEFT JOIN stock_picking p ON (m.picking_id = p.id)
                LEFT JOIN uom_uom pu ON (pt.uom_id = pu.id)
                LEFT JOIN uom_uom u ON (m.product_uom = u.id)
                WHERE m.date < %s AND (m.location_dest_id IN %s) AND m.state = 'done' AND pp.active = True AND pp.id = %s
                GROUP BY pp.id, pt.uom_id, m.product_uom, pp.default_code, u.name, m.date
                ))
            AS foo
            GROUP BY id
        ''', (from_date, tuple(locations), product_data, from_date, tuple(locations), product_data))

        res = self._cr.dictfetchall()

        return res[0].get('qty', 0.00) if res else 0.00

    def get_product_sale_qty(self, record, warehouse, product=None, location=None):
        if not product:
            product = self._fetch_product_data(record)

        product_data = tuple(product) if isinstance(product, list) else tuple(product.ids)

        if product_data:
            locations = location if location else self.fetch_location(record, warehouse)

            start_date = record.start_date.strftime("%Y-%m-%d") + ' 00:00:00'
            end_date = record.end_date.strftime("%Y-%m-%d") + ' 23:59:59'

            self._cr.execute('''
                SELECT 
                    pp.id AS product_id,
                    pt.categ_id,
                    sum((
                        CASE 
                            WHEN spt.code in ('outgoing') 
                                 AND smline.location_id in %s 
                                 AND sourcel.usage != 'inventory' 
                                 AND destl.usage != 'inventory'
                            THEN -(smline.quantity * pu.factor / pu2.factor)
                            ELSE 0.0 
                        END
                    )) AS product_qty_out,

                    sum((
                        CASE 
                            WHEN spt.code in ('incoming') 
                                 AND smline.location_dest_id in %s 
                                 AND sourcel.usage != 'inventory' 
                                 AND destl.usage != 'inventory' 
                            THEN (smline.quantity * pu.factor / pu2.factor) 
                            ELSE 0.0 
                        END
                    )) AS product_qty_in,

                    sum((
                        CASE 
                            WHEN (spt.code = 'internal') 
                                 AND smline.location_dest_id in %s 
                                 AND sourcel.usage != 'inventory' 
                                 AND destl.usage != 'inventory' 
                            THEN (smline.quantity * pu.factor / pu2.factor)  
                            WHEN (spt.code = 'internal' OR spt.code IS NULL) 
                                 AND smline.location_id in %s 
                                 AND sourcel.usage != 'inventory' 
                                 AND destl.usage != 'inventory' 
                            THEN -(smline.quantity * pu.factor / pu2.factor) 
                            ELSE 0.0 
                        END
                    )) AS product_qty_internal,

                    sum((
                        CASE 
                            WHEN sourcel.usage = 'inventory' 
                                 AND smline.location_dest_id in %s  
                            THEN (smline.quantity * pu.factor / pu2.factor)
                            WHEN destl.usage = 'inventory' 
                                 AND smline.location_id in %s 
                            THEN -(smline.quantity * pu.factor / pu2.factor)
                            ELSE 0.0 
                        END
                    )) AS product_qty_adjustment

                FROM 
                    product_product pp 
                    LEFT JOIN stock_move sm ON (
                        sm.product_id = pp.id 
                        AND sm.date >= %s 
                        AND sm.date <= %s 
                        AND sm.state = 'done' 
                        AND sm.location_id != sm.location_dest_id
                    )
                    LEFT JOIN stock_move_line smline ON (
                        smline.product_id = pp.id 
                        AND smline.state = 'done' 
                        AND smline.location_id != smline.location_dest_id 
                        AND smline.move_id = sm.id
                    )
                    LEFT JOIN stock_picking sp ON (sm.picking_id = sp.id)
                    LEFT JOIN stock_picking_type spt ON (spt.id = sp.picking_type_id)
                    LEFT JOIN stock_location sourcel ON (smline.location_id = sourcel.id)
                    LEFT JOIN stock_location destl ON (smline.location_dest_id = destl.id)
                    LEFT JOIN uom_uom pu ON (sm.product_uom = pu.id)
                    LEFT JOIN uom_uom pu2 ON (sm.product_uom = pu2.id)
                    LEFT JOIN product_template pt ON (pp.product_tmpl_id = pt.id)
                WHERE 
                    pp.id IN %s
                GROUP BY 
                    pt.categ_id, pp.id 
                ORDER BY 
                    pt.categ_id
            ''', (
                tuple(locations), tuple(locations), tuple(locations),
                tuple(locations), tuple(locations), tuple(locations),
                start_date, end_date, product_data
            ))

            values = self._cr.dictfetchall()

            if record.group_by_categ and not location:
                from itertools import groupby
                from operator import itemgetter

                sorted_by_category = sorted(values, key=itemgetter('categ_id'))
                grouped_by_category = {
                    k: list(v) for k, v in groupby(sorted_by_category, itemgetter('categ_id'))
                }
                return grouped_by_category
            else:
                return values[0]
