odoo.define('sale_purchase_details.PurchaseDashboard', function (require) {
    "use strict";

    console.log("Purchase Dashboard Loaded Without Assets!");

    var publicWidget = require('web.public.widget');

    publicWidget.registry.PurchaseDashboard = publicWidget.Widget.extend({
        selector: '.container',
        start: function () {
            this.$el.append('<p>JS is working without assets!</p>');
        },
    });

    return publicWidget.registry.PurchaseDashboard;
});
// /** @odoo-module **/
// import { registry } from "@web/core/registry";
// import { Component, xml } from "@odoo/owl";

// class PurchaseDashboard extends Component {
//     static template = xml`<div class="o_purchase_dashboard"><h2>This is Purchase Dashboard</h2></div>`;
// }

// registry.category("actions").add("purchase_dashboard", PurchaseDashboard);
// odoo.define('sale_purchase_details.PurchaseDashboard', function (require) {
//     "use strict";
    
//     var core = require('web.core');
//     console.log("Purchase Dashboard JS Loaded");
    
//     // Your logic here
// });