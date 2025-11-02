// /** @odoo-module */

// import { usePos } from "@point_of_sale/app/store/pos_hook";
// import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
// import { Component } from "@odoo/owl";
// import { useService } from "@web/core/utils/hooks";

// export class SaleOrderButton extends Component {
//     static template = "pos_sale_order.SaleOrderButton";

//     setup() {
//         this.pos = usePos();
//         this.popup = useService("popup");
//     	this.notification = useService("notification");  // ✅ naya service

//     }

//     async onClick() {
//         const order = this.pos.get_order();
//         const partner = order.get_partner();

//         if (!partner) {
//             this.pos.gui.showPopup("ErrorPopup", {
//                 title: "No Customer Selected",
//                 body: "Please select a customer before creating a Sale Order.",
//             });
//             return;
//         }

// 		this.notification.add("Sale Order Created Successfully!");
//     }
// }

// // Add button to POS product screen
// ProductScreen.addControlButton({
//     component: SaleOrderButton,
//     condition: () => true,
// });


/** @odoo-module **/

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SaleOrderButton extends Component {
	static template = "pos_sale_order.SaleOrderButton";

	setup() {
		this.pos = usePos();
		this.popup = useService("popup");
		this.rpc = useService("rpc");
		this.notification = useService("notification");
	}

	async onClick() {
		const order = this.pos.get_order();
		const partner = order.get_partner();

		if (!partner) {
			await this.popup.add("ErrorPopup", {
				title: "No Customer Selected",
				body: "Please select a customer before creating a Sale Order.",
			});
			return;
		}

		if (order.get_orderlines().length === 0) {
			await this.popup.add("ErrorPopup", {
				title: "No Products",
				body: "Please add products to the order before creating a Sale Order.",
			});
			return;
		}

		const order_lines = order.get_orderlines().map(line => ({
			product_id: line.product.id,
			quantity: line.get_quantity(),
			price: line.get_unit_price(),
			discount: line.get_discount(),
		}));

		try {
			const result = await this.rpc("/web/dataset/call_kw/sale.order/create_sale_order_from_pos", {
				params: {
					model: "sale.order",
					method: "create_sale_order_from_pos",
					args: [partner.id, order_lines],
					kwargs: {},
				},
			});

			if (result.success) {
				this.notification.add(`Sale Order Created! (ID: ${result.order_id})`);
				this.pos.add_new_order(); // Reset POS order
			} else {
				await this.popup.add("ErrorPopup", {
					title: "Error",
					body: result.error || "Failed to create Sale Order",
				});
			}
		} catch (err) {
			await this.popup.add("ErrorPopup", {
				title: "RPC Error",
				body: err.message,
			});
		}
	}
}

// Add button to POS Product Screen
ProductScreen.addControlButton({
	component: SaleOrderButton,
	condition: () => true,
});

