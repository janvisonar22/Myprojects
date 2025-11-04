import pytz
import logging
import ast
from odoo import fields, models, api, _
import json
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from collections import Counter
from pytz import timezone, UTC
from datetime import datetime, date, timedelta

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = "pos.session"


    def get_total_tax(self):
        if self:
            self.env.cr.execute("""SELECT COALESCE(SUM(amount_tax), 0.0) AS total 
                                    FROM pos_order WHERE state != 'draft' AND session_id = %s""" % self.id)
            return self.env.cr.dictfetchall()[0]['total']
        return 0.0

    def get_total_first(self):
        total = 0.0
        return total

    def get_session_date_time(self, flag):
        date_time_dict = {'start_date': '', 'end_date': '', 'time': ''}
        local = pytz.timezone(self._context.get('tz', 'utc') or 'utc')

        start_date = pytz.utc.localize(datetime.strptime(str(self.start_at), DEFAULT_SERVER_DATETIME_FORMAT))
        if self.stop_at:
            stop_date = pytz.utc.localize(datetime.strptime(str(self.stop_at), DEFAULT_SERVER_DATETIME_FORMAT))
            converted_stop_date = datetime.strftime(stop_date.astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
            date_time_dict.update({'end_date': converted_stop_date})
        final_converted_date = datetime.strftime(start_date.astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        final_converted_time = datetime.strptime(final_converted_date, DEFAULT_SERVER_DATETIME_FORMAT)
        date_time_dict.update({'time': final_converted_time.strftime('%I:%M:%S %p'),
                               'start_date': final_converted_time.date() if flag else final_converted_time})
        return date_time_dict

    def get_current_date_time(self):
        user_tz = self.env.user.tz or pytz.utc
        return {'date': datetime.now(timezone(user_tz)).date(),
                'time': datetime.now(timezone(user_tz)).strftime('%I:%M:%S %p')}

    def get_total_sales(self):
        self.env.cr.execute("""SELECT
                                COALESCE(SUM(pol.price_unit * pol.qty), 0.0) AS total 
                                FROM pos_order AS po
                                LEFT JOIN pos_order_line AS pol ON pol.order_id = po.id 
                                WHERE po.amount_total > 0 
                                AND po.session_id = %s
                                AND po.state != 'draft' 
                                """ % self.id)
        return self.env.cr.dictfetchall()[0]['total']

    def get_total_return_sales(self):
        self.env.cr.execute("""SELECT
                                COALESCE(SUM(amount_total), 0.0) AS total 
                                FROM pos_order
                                WHERE amount_total < 0
                                AND session_id = %s
                                AND state != 'draft'
                                """ % self.id)
        return abs(self.env.cr.dictfetchall()[0]['total'])

    def get_gross_total(self):
        total_price = 0.0
        if self:
            self.env.cr.execute("""SELECT COALESCE(SUM(amount_total), 0.0) AS total 
                                    FROM pos_order 
                                    WHERE session_id = %s AND state != 'draft'""" % self.id)
            return self.env.cr.dictfetchall()[0]['total']
        return total_price

    def get_gross_profit(self):
        total_cost = 0.0
        if self and self.order_ids:
            for order in self.order_ids:
                if not order.state == 'draft':
                    for line in order.lines:
                        total_cost += line.qty * line.product_id.standard_price
        return total_cost

    def get_product_cate_total_x(self):
        balance_end_real = 0.0
        if self and self.order_ids:
            for order in self.order_ids:
                for line in order.lines:
                    balance_end_real += (line.qty * line.price_unit)
        return balance_end_real

    # # PAYMENT DATA FROM X AND Z REPORT
    def get_payments(self):
        pos_payment_ids = self.env["pos.payment"].search([('session_id', '=', self.id)]).ids
        if pos_payment_ids:
            self.env.cr.execute("""
                SELECT COALESCE(method.name->>%s, method.name->>'en_US') as name, sum(amount) total
                FROM pos_payment AS payment,
                     pos_payment_method AS method
                WHERE payment.payment_method_id = method.id
                    AND payment.id IN %s
                GROUP BY method.name
            """, (self.env.lang, tuple(pos_payment_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []
        return payments

    # DISCOUNT DATA FROM X AND Z REPORT
    def get_total_discount(self):
        sql = """SELECT 
                    COALESCE(SUM((((pol.price_unit * pol.qty) * pol.discount) / 100)), 0.0) AS total
                    FROM pos_order AS po
                    INNER JOIN pos_order_line AS pol ON pol.order_id = po.id
                    WHERE session_id = %s 
                    AND po.state != 'draft'
                    AND pol.discount > 0 
                    AND pol.price_subtotal > 0""" % self.id
        self.env.cr.execute(sql)
        return abs(self.env.cr.dictfetchall()[0]['total'])

    # PRODUCT CATEGORY DATA FROM X AND Z REPORT
    def get_product_category(self):
        sold_product = {}
        pos_order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
        for pos_order in pos_order_ids:
            for line in pos_order.lines:
                if line.product_id.pos_categ_ids:
                    if len(line.product_id.pos_categ_ids) > 1:
                        for categ_id in line.product_id.pos_categ_ids:
                            if categ_id.name:
                                if categ_id.name in sold_product:
                                    sold_product[categ_id.name] += line.qty
                                else:
                                    sold_product.update({categ_id.name: line.qty})
                            else:
                                if 'undefine' in sold_product:
                                    sold_product['undefine'] += line.qty
                                else:
                                    sold_product.update({'undefine': line.qty})
                            
                    else:
                        if line.product_id.pos_categ_ids.name:
                            if line.product_id.pos_categ_ids.name in sold_product:
                                sold_product[line.product_id.pos_categ_ids.name] += line.qty
                            else:
                                sold_product.update({line.product_id.pos_categ_ids.name: line.qty})
                        else:
                            if 'undefine' in sold_product:
                                sold_product['undefine'] += line.qty
                            else:
                                sold_product.update({'undefine': line.qty})
                else:
                    if 'undefine' in sold_product:
                        sold_product['undefine'] += line.qty
                    else:
                        sold_product.update({'undefine': line.qty})

        return {'sold_product': sold_product}


    def get_taxes_data(self):
        order_ids = self.env['pos.order'].search([('session_id', '=', self.id)])
        taxes = {}
        for order in order_ids:
            currency = order.pricelist_id.currency_id
            for line in order.lines:
                if line.tax_ids_after_fiscal_position:
                    for tax in line.tax_ids_after_fiscal_position:
                        discount_amount = 0
                        if line.discount > 0:
                            discount_amount = ((line.qty*line.price_unit)* line.discount) / 100
                        untaxed_amount = (line.qty*line.price_unit) - discount_amount
                        tax_amount = ((untaxed_amount * tax.amount) / 100)
                        if tax.name:
                            if tax.name in taxes:
                                taxes[tax.name] += tax_amount
                            else:
                                taxes.update({tax.name : tax_amount})
                        else:
                            if 'undefine' in taxes:
                                taxes['undefine'] += tax_amount
                            else:
                                taxes.update({'undefine': tax_amount})
        return taxes


    def action_session_z_report(self):
        return self.env.ref(
            "dps_pos_session_xzreport.action_report_session_z"
        ).report_action(self)

    def get_current_datetime(self):
        current = fields.datetime.now()
        return current.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def get_opened_date(self):
        return datetime.strptime(
            str(self.start_at), DEFAULT_SERVER_DATETIME_FORMAT
        )

    def get_closed_date(self):
        if self.stop_at:
            return datetime.strptime(
                str(self.stop_at), DEFAULT_SERVER_DATETIME_FORMAT
            )

    def get_session_amount_data(self):
        pos_order_ids = self.env["pos.order"].search(
            [("session_id", "=", self.id)]
        )
        discount_amount = 0.0
        taxes_amount = 0.0
        total_sale_amount = 0.0
        total_gross_amount = 0.0
        sold_product = {}
        session_wise_product = {}
        for pos_order in pos_order_ids:
            currency = self.currency_id
            total_gross_amount += pos_order.amount_total
            for line in pos_order.lines:
                if line.product_id.display_name in session_wise_product:
                    update_details = session_wise_product[
                        line.product_id.display_name
                    ]
                    update_details["qty"] += line.qty
                    update_details["price"] += line.price_subtotal_incl
                else:
                    vals = {"qty": line.qty, "price": line.price_subtotal_incl}
                    session_wise_product[line.product_id.display_name] = vals

                if line.product_id.pos_categ_ids:
                    if len(line.product_id.pos_categ_ids) > 1:
                        for categ_id in line.product_id.pos_categ_ids:
                            if categ_id.name:
                                if categ_id.name in sold_product:
                                    sold_product[categ_id.name] += line.qty
                                else:
                                    sold_product.update(
                                        {categ_id.name: line.qty}
                                    )
                            else:
                                if "undefine" in sold_product:
                                    sold_product["undefine"] += line.qty
                                else:
                                    sold_product.update({"undefine": line.qty})

                    else:
                        if line.product_id.pos_categ_ids.name:
                            if (
                                line.product_id.pos_categ_ids.name
                                in sold_product
                            ):
                                sold_product[
                                    line.product_id.pos_categ_ids.name
                                ] += line.qty
                            else:
                                sold_product.update(
                                    {
                                        line.product_id.pos_categ_ids.name: line.qty
                                    }
                                )
                        else:
                            if "undefine" in sold_product:
                                sold_product["undefine"] += line.qty
                            else:
                                sold_product.update({"undefine": line.qty})
                else:
                    if "undefine" in sold_product:
                        sold_product["undefine"] += line.qty
                    else:
                        sold_product.update({"undefine": line.qty})

                if line.tax_ids_after_fiscal_position:
                    line_taxes = (
                        line.tax_ids_after_fiscal_position.compute_all(
                            line.price_unit
                            * (1 - (line.discount or 0.0) / 100.0),
                            currency,
                            line.qty,
                            product=line.product_id,
                            partner=line.order_id.partner_id or False,
                        )
                    )
                    for tax in line_taxes["taxes"]:
                        taxes_amount += tax.get("amount", 0)
                if line.discount > 0:
                    discount_amount += (
                        (line.price_unit * line.qty) * line.discount
                    ) / 100
                if line.qty > 0:
                    total_sale_amount += line.price_unit * line.qty

        return {
            "total_sale": total_sale_amount,
            "discount": discount_amount,
            "tax": taxes_amount,
            "products_sold": sold_product,
            "total_gross": total_gross_amount - taxes_amount - discount_amount,
            "final_total": total_gross_amount,
            "session_wise_product": session_wise_product,
        }

    def get_taxes_data(self):
        order_ids = self.env["pos.order"].search(
            [("session_id", "=", self.id)]
        )
        taxes = {}
        for order in order_ids:
            for line in order.lines:
                if line.tax_ids_after_fiscal_position:
                    for tax in line.tax_ids_after_fiscal_position:
                        discount_amount = 0
                        if line.discount > 0:
                            discount_amount = (
                                (line.qty * line.price_unit) * line.discount
                            ) / 100
                        untaxed_amount = (
                            line.qty * line.price_unit
                        ) - discount_amount
                        tax_amount = (untaxed_amount * tax.amount) / 100
                        if tax.name:
                            if tax.name in taxes:
                                taxes[tax.name] += tax_amount
                            else:
                                taxes.update({tax.name: tax_amount})
                        else:
                            if "undefine" in taxes:
                                taxes["undefine"] += tax_amount
                            else:
                                taxes.update({"undefine": tax_amount})
        return taxes

    def get_price_product(self, price):
        return int(price)

    def get_qty_product(self, qty):
        return int(qty)

    def get_pricelist(self):
        pos_order_ids = self.env["pos.order"].search(
            [("session_id", "=", self.id)]
        )
        pricelist = {}
        for pos_order in pos_order_ids:
            if pos_order.pricelist_id.name:
                if pos_order.pricelist_id.name in pricelist:
                    pricelist[
                        pos_order.pricelist_id.name
                    ] += pos_order.amount_total
                else:
                    pricelist.update(
                        {pos_order.pricelist_id.name: pos_order.amount_total}
                    )
            else:
                if "undefine" in pricelist:
                    pricelist["undefine"] += pos_order.amount_total
                else:
                    pricelist.update({"undefine": pos_order.amount_total})
        return pricelist

    def get_pricelist_qty(self, pricelist):
        if pricelist:
            qty_pricelist = 0
            pricelist_obj = self.env["product.pricelist"].search(
                [("name", "=", str(pricelist))]
            )
            if pricelist_obj:
                pos_order_ids = self.env["pos.order"].search(
                    [
                        ("session_id", "=", self.id),
                        ("pricelist_id.id", "=", pricelist_obj.id),
                    ]
                )
                qty_pricelist = len(pos_order_ids)
            else:
                if pricelist == "undefine":
                    pos_order_ids = self.env["pos.order"].search(
                        [
                            ("session_id", "=", self.id),
                            ("pricelist_id", "=", False),
                        ]
                    )
                    qty_pricelist = len(pos_order_ids)
            return int(qty_pricelist)

    def get_payment_data(self):
        pos_payment_ids = (
            self.env["pos.payment"].search([("session_id", "=", self.id)]).ids
        )
        if pos_payment_ids:
            self.env.cr.execute(
                """
                SELECT COALESCE(method.name->>%s, method.name->>'en_US') as name, sum(amount) total
                FROM pos_payment AS payment,
                     pos_payment_method AS method
                WHERE payment.payment_method_id = method.id
                    AND payment.id IN %s
                GROUP BY method.name
            """,
                (
                    self.env.lang,
                    tuple(pos_payment_ids),
                ),
            )
            payments = self.env.cr.dictfetchall()
        else:
            payments = []
        return payments

    def get_payment_qty(self, payment_method):
        qty_payment_method = 0
        if payment_method:
            orders = self.env["pos.order"].search(
                [("session_id", "=", self.id)]
            )
            st_line_obj = self.env["account.bank.statement.line"].search(
                [("pos_statement_id", "in", orders.ids)]
            )
            if len(st_line_obj) > 0:
                res = []
                for line in st_line_obj:
                    res.append(line.journal_id.name)
                res_dict = ast.literal_eval(json.dumps(dict(Counter(res))))
                if payment_method in res_dict:
                    qty_payment_method = res_dict[payment_method]
        return int(qty_payment_method)

    sc_session_report = fields.Boolean(
        related="config_id.sc_session_report",
        store=False,
        string="Allow to Print Session Z Report",
    )

class PosConfig(models.Model):
    _inherit = "pos.config"

    sc_session_report = fields.Boolean(
        string="Allow to Print Session Z Report"
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sc_session_report = fields.Boolean(
        related="pos_config_id.sc_session_report",
        readonly=False
    )
