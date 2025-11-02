/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class EmptyDashboard extends Component {}
EmptyDashboard.template = "empty_dashboard_template";

registry.category("actions").add("empty_dashboard_action", EmptyDashboard);

// /** @odoo-module **/
// import { Component ,useState} from "@odoo/owl";
// import { registry } from "@web/core/registry";
// // const actionRegistry = registry.category("actions");
// class SaleDashboard extends Component {
// 	setup() {
//         this.state = useState({ message: "Welcome to Sale Dashboard" });
//     }
// }
// SaleDashboard.template = "sale_purchase_details.SaleDashboard";
// registry.category("actions").add("sale_dashboard_action", SaleDashboard);