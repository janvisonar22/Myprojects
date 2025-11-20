/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

export class ProjectDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            kpis: {},
            projects: [],
            current_page: 1,
            page_size: 5,
            total_count: 0,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        // Fetch KPIs
        this.state.kpis = await this.orm.call("project.dashboard", "get_kpi_data", []);
        // Fetch projects with pagination
        const res = await this.orm.call("project.dashboard", "get_dashboard_data", [
            (this.state.current_page - 1) * this.state.page_size,
            this.state.page_size,
        ]);
        this.state.projects = res.projects;
        this.state.total_count = res.total_count;
    }

    async refreshData() {
        await this.loadData();
        this.render();
    }

    async nextPage() {
        if ((this.state.current_page * this.state.page_size) < this.state.total_count) {
            this.state.current_page += 1;
            await this.loadData();
            this.render();
        }
    }

    async prevPage() {
        if (this.state.current_page > 1) {
            this.state.current_page -= 1;
            await this.loadData();
            this.render();
        }
    }
    async openAction(type, projectId = false) {
        let domain = [];
        let name = "";

        if (projectId) {
            // Open only this project
            await this.action.doAction({
                type: "ir.actions.act_window",
                name: "Project Form",
                res_model: "project.project",
                views: [[false, "form"]],
                target: "current",
                res_id: projectId,  // <-- Open this specific project
            });
            return;
        }

        // For KPI tiles
        switch (type) {
            case "invoiced":
                name = "Invoiced Projects";
                domain = [["has_invoiced", "=", true]];
                break;
            case "committed":
                name = "Committed Projects";
                domain = [["has_committed", "=", true]];
                break;
            case "uninvoiced":
                name = "Uninvoiced Projects";
                domain = [["has_uninvoiced", "=", true]];
                break;
            case "hours":
                name = "Projects with Timesheets";
                domain = [["has_timesheet_hours", "=", true]];
                break;
            case "margin":
                name = "Profitable Projects";
                domain = [["has_margin", "=", true]];
                break;
            default:
                name = "All Projects";
                domain = [];
        }

        await this.action.doAction({
            type: "ir.actions.act_window",
            name,
            res_model: "project.project",
            views: [[false, "list"], [false, "form"]],
            target: "current",
            domain,
        });
    }
}

ProjectDashboard.template = "project_custom_dashboard.ProjectDashboard";
registry.category("actions").add("project_dashboard_action", ProjectDashboard);
