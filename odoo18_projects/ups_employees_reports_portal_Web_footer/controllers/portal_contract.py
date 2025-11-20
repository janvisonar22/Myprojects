from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalContracts(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user = request.env.user
        print("\n\nuser==??>>",user)
        contract_count = request.env['hr.contract'].sudo().search_count([
            ('employee_id.user_id', '=', user.id)
        ])
        print("\n\ncontract_count-->>",contract_count)
        values['contract_count'] = contract_count
        return values

    @http.route(['/my/contracts'], type='http', auth="user", website=True)
    def portal_my_contracts(self, **kw):
        user = request.env.user

        contracts = request.env['hr.contract'].sudo().search([
            ('employee_id.user_id', '=', user.id)
        ])
        print("\n\ncontracts===>>",contracts)
        values = {
            'contracts': contracts,
        }
        print("\n\nvalues-->>>",values)
        return request.render("ups_employees_reports.portal_my_contracts", values)
    @http.route(['/my/contracts/<int:contract_id>'], type='http', auth="user", website=True)
    def portal_contract_detail(self, contract_id, **kw):
        user = request.env.user
        contract = request.env['hr.contract'].sudo().search([
            ('id', '=', contract_id),
            ('employee_id.user_id', '=', user.id)
        ], limit=1)

        if not contract:
            return request.redirect('/my/contracts')  # Redirect if no access

        values = {
            'contract': contract,
        }
        return request.render("ups_employees_reports.portal_contract_detail_template", values)
    @http.route(['/my/contracts/<int:contract_id>/resign'], type='http', auth="user", website=True)
    def portal_resignation_form(self, contract_id, **kw):
        contract = request.env['hr.contract'].sudo().search([
            ('id', '=', contract_id),
            ('employee_id.user_id', '=', request.env.user.id)
        ], limit=1)

        if not contract:
            return request.redirect('/my/contracts')

        return request.render("ups_employees_reports.portal_resignation_form", {
            'contract': contract,
        })

    @http.route(['/my/contracts/resignation/submit'], type='http', auth="user", website=True, csrf=False)
    def portal_resignation_submit(self, **post):
        print("\n\n >>> RESIGNATION ROUTE CALLED <<< \n\n")
        print("POST DATA: ", post)

        contract_id = int(post.get('contract_id'))
        submit_date = post.get('submit_date')
        reason = post.get('reason')

        contract = request.env['hr.contract'].sudo().browse(contract_id)

        # Security check
        if contract.employee_id.user_id.id != request.env.user.id:
            print(" ACCESS DENIED ")
            return request.redirect('/my/contracts')

        # Create resignation line
        new_line = request.env['hr.contract.resignation.line'].sudo().create({
            'contract_id': contract_id,
            'submit_date': submit_date,
            'reason': reason,
        })

        print("\n\n CREATED LINE: ", new_line)

        return request.redirect('/my/contracts/%s' % contract_id)
