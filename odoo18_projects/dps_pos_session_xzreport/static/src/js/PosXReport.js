/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    async printXReport() {
        var pos_session_id = this.session.id;
        await this.env.services.report.doAction("dps_pos_session_xzreport.report_pos_sales_pdf_front", [
            pos_session_id,
        ]);
    },
    async printZReport() {
        var pos_session_id = this.session.id;
        await this.env.services.report.doAction("dps_pos_session_xzreport.action_report_session_z", [
            pos_session_id,
        ]);
    },
});


