/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
	async _processData(loadedData) {
		await super._processData(...arguments);
		this.product_temp=loadedData['product.product']
		console.log('this',this)
		console.log('brand',this.product_temp)

}
})