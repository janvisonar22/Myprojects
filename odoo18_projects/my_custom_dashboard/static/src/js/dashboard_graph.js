/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, onMounted } from "@odoo/owl";
import * as Chart from "chart.js/auto";

class DashboardGraph extends Component {
    setup() {
        onMounted(() => {
            let parsed = [];
            try {
                parsed = JSON.parse(this.props.value || "[]");
            } catch (e) {
                console.warn("⚠️ Invalid graph data", e);
            }
            console.log("📥 Raw value from Odoo:", this.props.value);
            console.log("✅ Parsed graph data:", parsed);

            if (!parsed.length) {
                console.log("⚠️ No data to render graph");
                return;
            }

            const ctx = this.refs.canvas.getContext("2d");
            console.log("🎨 Canvas context:", ctx);

            const labels = parsed[0].values.map(v => v.x);
            console.log("🏷 Labels:", labels);

            const datasets = parsed.map(serie => ({
                label: serie.key,
                data: serie.values.map(v => v.y),
                backgroundColor: serie.color,
            }));
            console.log("📊 Datasets:", datasets);

            new Chart(ctx, {
                type: this.props.graphType || "bar",
                data: { labels, datasets },
                options: {
                    responsive: true,
                    plugins: { legend: { position: "top" } },
                }
            });

            console.log("✅ Chart rendered successfully");
        });
    }
}
DashboardGraph.template = "partner_dashboard.DashboardGraphTemplate";
registry.category("fields").add("dashboard_graph", DashboardGraph);
