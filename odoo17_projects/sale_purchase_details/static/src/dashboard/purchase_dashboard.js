/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class PurchaseDashboard extends Component {
    static template = xml`<div class="o_purchase_dashboard"><h2>This is Purchase Dashboard</h2></div>`;
}

registry.category("actions").add("purchase_dashboard", PurchaseDashboard);
// /** @odoo-module **/
// import { registry } from "@web/core/registry";
// import { Component, useState, onWillStart } from "@odoo/owl";
// import { useService } from "@web/core/utils/hooks";

// class PurchaseDashboard extends Component {
//     setup() {
//         this.rpc = useService("rpc");
//         this.state = useState({
//             data: {},
//         });

//         onWillStart(async () => {
//             this.state.data = await this.rpc("/purchase_dashboard/data", {});
//         });
//     }
// }

// PurchaseDashboard.template = "purchase_dashboard.PurchaseDashboard";

// registry.category("actions").add("purchase_dashboard", PurchaseDashboard);
// /* @odoo-module */
// import { registry } from '@web/core/registry';
// import { Component, useState, onWillStart} from "@odoo/owl";
// import { useService } from "@web/core/utlis/hooks";
// import { PurchaseCard } from './purchase_card';
// export class PurchaseDashboard extends Component{
// 	setup(){
// 		this.orm = useService("orm");
// 		this.purchase_order_count= useState({
// 			all_purchase_order:0,
// 			rfq:0,
// 			rfq_sent:0,
// 			to_approve:0,
// 			purchase:0,
// 			done:0,
// 			cancel:0,
// 		});
// 	onWillStart(async () => {
// 		await this.loadDashboardData();

// 		});
// 	}
// 	async loadDashboardData(){
// 		try{
// 		const result = await this.orm.call(
// 			'purchase.order',
// 			'get_purchase_order_count',
// 			[]
// 		);
// 		object.assign(this.purchase_order_count, result);
// 		}catch(error){
// 			console.error("Error loading dashboarrd data:",error)

// 		}
// 	}
// 		// const context = {};
// 		// this.purchase_order_count = await this.or,.call(
// 		// 	'purchase.order',
// 		// 	'get_purchase_order_count',[],
// 		// 	{context: context});}
// 	}
// 	registry.category("actions").add("purchase_dashboard",PurchaseDashboard);
// 	PurchaseDashboard.components = {PurchaseCard};
// 	PurchaseDashboard.template = 'purchase_dashboard.PurchaseDashboard';
// 	