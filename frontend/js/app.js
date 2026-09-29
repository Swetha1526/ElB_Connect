// frontend/js/app.js
/**
 * VoltFlow — Core Frontend Controller
 */

// Global Application State
const State = {
    currentView: "dashboard",
    applications: {
        items: [],
        total: 0,
        page: 1,
        pageSize: 10,
        totalPages: 1,
        search: "",
        status: "All",
        category: "All",
        substation: "All"
    },
    inspections: [],
    meters: [],
    grievances: {
        items: [],
        status: "All",
        priority: "All",
        search: ""
    },
    selectedApplication: null,
    selectedInspection: null,
    selectedMeter: null,
    selectedGrievance: null
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    initGlobalEventListeners();
    initQuotationCalculator();
    
    // Check initial URL hash
    const initialHash = window.location.hash.replace("#", "");
    if (initialHash && ["dashboard", "applications", "inspections", "meters", "grievances", "track"].includes(initialHash)) {
        switchView(initialHash);
    } else {
        loadDashboard();
    }
});

// --- Navigation & View Switching ---
function initNavigation() {
    const navLinks = document.querySelectorAll(".nav-link[data-view]");
    navLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const view = link.getAttribute("data-view");
            if (view) {
                switchView(view);
                window.location.hash = view;
            }
            document.querySelector(".sidebar")?.classList.remove("mobile-open");
        });
    });

    window.addEventListener("hashchange", () => {
        const hash = window.location.hash.replace("#", "");
        if (hash && ["dashboard", "applications", "inspections", "meters", "grievances", "track"].includes(hash)) {
            switchView(hash);
        }
    });

    const toggleBtn = document.getElementById("mobile-menu-toggle");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            document.querySelector(".sidebar")?.classList.toggle("mobile-open");
        });
    }
}

function switchView(viewName) {
    State.currentView = viewName;

    // Update active nav item
    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.toggle("active", link.getAttribute("data-view") === viewName);
    });

    // Toggle view sections
    document.querySelectorAll(".view-section").forEach(sec => {
        sec.classList.remove("active");
    });
    const target = document.getElementById(`view-${viewName}`);
    if (target) {
        target.classList.add("active");
    }

    // Fetch view specific data
    switch (viewName) {
        case "dashboard":
            loadDashboard();
            break;
        case "applications":
            loadApplications();
            break;
        case "inspections":
            loadInspections();
            break;
        case "meters":
            loadMeters();
            break;
        case "grievances":
            loadGrievances();
            break;
    }
}

// --- Dynamic Live Quotation Calculator ---
function initQuotationCalculator() {
    const categorySelect = document.getElementById("app-form-category");
    const loadInput = document.getElementById("app-form-load");
    const phaseSelect = document.getElementById("app-form-phase");

    const updateCalc = () => {
        const cat = categorySelect?.value || "Domestic";
        const load = parseFloat(loadInput?.value) || 1.0;
        const phase = phaseSelect?.value || "Single Phase";

        let depositPerKw = 600;
        let baseService = 1200;
        let phaseMultiplier = phase.toLowerCase().includes("single") ? 1.0 : 1.8;
        let meterCost = 1500;

        if (cat === "Commercial") {
            depositPerKw = 1200;
            baseService = 2500;
            phaseMultiplier = phase.toLowerCase().includes("single") ? 1.0 : 1.7;
            meterCost = 3000;
        } else if (cat === "Industrial") {
            depositPerKw = 2500;
            baseService = 8000;
            phaseMultiplier = 2.5;
            meterCost = 7500;
        } else if (cat === "Agricultural") {
            depositPerKw = 200;
            baseService = 800;
            phaseMultiplier = phase.toLowerCase().includes("single") ? 1.0 : 1.2;
            meterCost = 1000;
        }

        const secDeposit = load * depositPerKw;
        const connFee = baseService * phaseMultiplier;
        const total = secDeposit + connFee + meterCost;

        const quoteEl = document.getElementById("app-form-quote-preview");
        if (quoteEl) {
            quoteEl.textContent = UI.formatCurrency(total);
        }
        const breakdownEl = document.getElementById("app-form-quote-breakdown");
        if (breakdownEl) {
            breakdownEl.textContent = `Security Deposit: ${UI.formatCurrency(secDeposit)} | Connection Fee: ${UI.formatCurrency(connFee)} | Meter: ${UI.formatCurrency(meterCost)}`;
        }
    };

    if (categorySelect) categorySelect.addEventListener("change", updateCalc);
    if (loadInput) loadInput.addEventListener("input", updateCalc);
    if (phaseSelect) phaseSelect.addEventListener("change", updateCalc);
}

// --- Event Listeners Initialization ---
function initGlobalEventListeners() {
    const headerSearch = document.getElementById("header-global-search");
    if (headerSearch) {
        headerSearch.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                const term = headerSearch.value.trim();
                if (term) {
                    if (/^APP-\d{4}-\d{4}$/i.test(term)) {
                        switchView("track");
                        document.getElementById("track-input").value = term;
                        searchTrackApplication(term);
                    } else {
                        switchView("applications");
                        State.applications.search = term;
                        document.getElementById("app-search-input").value = term;
                        loadApplications();
                    }
                }
            }
        });
    }

    // Modal background close
    document.querySelectorAll(".modal").forEach(modal => {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                UI.closeModal(modal.id);
            }
        });
    });

    document.querySelectorAll(".modal-close, [data-close-modal]").forEach(btn => {
        btn.addEventListener("click", () => {
            UI.closeAllModals();
        });
    });

    // Form handlers
    document.getElementById("form-new-application")?.addEventListener("submit", handleCreateApplication);
    document.getElementById("form-edit-application")?.addEventListener("submit", handleUpdateApplication);
    document.getElementById("form-schedule-inspection")?.addEventListener("submit", handleScheduleInspection);
    document.getElementById("form-record-inspection")?.addEventListener("submit", handleCompleteInspection);
    document.getElementById("form-allocate-meter")?.addEventListener("submit", handleAllocateMeter);
    document.getElementById("form-file-grievance")?.addEventListener("submit", handleCreateGrievance);
    document.getElementById("form-update-grievance")?.addEventListener("submit", handleUpdateGrievance);
    document.getElementById("form-track-application")?.addEventListener("submit", (e) => {
        e.preventDefault();
        const num = document.getElementById("track-input").value.trim();
        if (num) searchTrackApplication(num);
    });
}

// =============================================================================
// 1. DASHBOARD
// =============================================================================
async function loadDashboard() {
    try {
        const stats = await API.getDashboardStats();

        document.getElementById("kpi-total-apps").textContent = stats.total_applications;
        document.getElementById("kpi-active-meters").textContent = stats.active_meters;
        document.getElementById("kpi-sanctioned-load").textContent = `${stats.total_sanctioned_load_mw} MW`;
        document.getElementById("kpi-sanctioned-sub").textContent = `${stats.total_sanctioned_load_kw.toLocaleString()} kW total load`;
        document.getElementById("kpi-pending-verif").textContent = stats.pending_verifications;
        document.getElementById("kpi-active-grievances").textContent = stats.active_grievances;
        document.getElementById("kpi-revenue").textContent = UI.formatCurrency(stats.estimated_revenue_inr);

        // Render Load Distribution Bars
        const catContainer = document.getElementById("dashboard-category-bars");
        if (catContainer) {
            const maxLoad = Math.max(...stats.category_distribution.map(c => c.total_load_kw), 1);
            catContainer.innerHTML = stats.category_distribution.map(cat => {
                const percent = Math.min(100, Math.round((cat.total_load_kw / maxLoad) * 100));
                const fillClass = `fill-${cat.category.toLowerCase()}`;
                return `
                    <div class="cat-progress-item">
                        <div class="cat-progress-header">
                            <div>
                                ${UI.getCategoryBadge(cat.category)}
                                <span style="font-size: 0.78rem; color: var(--text-muted); margin-left: 6px;">(${cat.count} connections)</span>
                            </div>
                            <span style="font-weight: 700; color: var(--text-white);">${cat.total_load_kw} kW</span>
                        </div>
                        <div class="cat-progress-bar">
                            <div class="cat-progress-fill ${fillClass}" style="width: ${percent}%;"></div>
                        </div>
                    </div>
                `;
            }).join("") || `<div class="empty-state"><p>No category data</p></div>`;
        }

        // Render Substation metrics
        const subContainer = document.getElementById("dashboard-substations-list");
        if (subContainer) {
            subContainer.innerHTML = stats.substation_metrics.map(sub => `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                    <div>
                        <div style="font-size: 0.84rem; font-weight: 600;">${sub.substation_name}</div>
                        <div style="font-size: 0.74rem; color: var(--text-dim);">${sub.active_meters} active meters / ${sub.total_applications} apps</div>
                    </div>
                    <span class="badge badge-primary">${sub.total_load_kw} kW</span>
                </div>
            `).join("") || `<div class="empty-state"><p>No substation data</p></div>`;
        }

        // Render Recent Activity Timeline
        const timelineEl = document.getElementById("dashboard-activity-timeline");
        if (timelineEl) {
            timelineEl.innerHTML = stats.recent_activity.map(act => `
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <div class="timeline-action">${act.action.replace(/_/g, " ")} — <a href="#" onclick="openDossierById(${act.application_id}); return false;">App #${act.application_id}</a></div>
                        <div class="timeline-note">${act.notes || "Status updated"} (By: ${act.performed_by})</div>
                        <div class="timeline-time">${UI.formatDateTime(act.timestamp)}</div>
                    </div>
                </div>
            `).join("") || `<div class="empty-state"><p>No recent activity</p></div>`;
        }

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

// =============================================================================
// 2. APPLICATIONS CRUD
// =============================================================================
async function loadApplications() {
    const tableBody = document.getElementById("applications-table-body");
    const countBadge = document.getElementById("apps-total-count");
    if (!tableBody) return;

    tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 30px;"><div class="spinner" style="margin:0 auto 8px;"></div>Loading applications...</td></tr>`;

    try {
        const res = await API.getApplications({
            search: State.applications.search,
            status: State.applications.status,
            category: State.applications.category,
            substation: State.applications.substation,
            page: State.applications.page,
            page_size: State.applications.pageSize
        });

        State.applications.items = res.items;
        State.applications.total = res.total;
        State.applications.totalPages = res.total_pages;

        if (countBadge) countBadge.textContent = `${res.total} Total`;

        document.getElementById("app-page-num").textContent = `Page ${res.page} of ${res.total_pages}`;
        document.getElementById("app-prev-btn").disabled = res.page <= 1;
        document.getElementById("app-next-btn").disabled = res.page >= res.total_pages;

        if (!res.items || res.items.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">
                            <div class="empty-state-title">No Applications Found</div>
                            <div class="empty-state-desc">Try adjusting your filters or click Apply New Connection.</div>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = res.items.map(app => {
            const consumer = app.consumer || {};
            return `
                <tr>
                    <td>
                        <a href="#" onclick="openDossierById(${app.id}); return false;" style="font-weight: 700; color: #38bdf8;">
                            ${app.application_number}
                        </a>
                        <div style="font-size: 0.74rem; color: var(--text-dim);">${UI.formatDate(app.created_at)}</div>
                    </td>
                    <td>
                        <div style="font-weight: 600;">${consumer.full_name || "—"}</div>
                        <div style="font-size: 0.76rem; color: var(--text-muted);">${consumer.phone || "—"}</div>
                    </td>
                    <td>
                        ${UI.getCategoryBadge(app.category)}
                        <div style="font-size: 0.74rem; color: var(--text-dim); margin-top: 2px;">${app.connection_type}</div>
                    </td>
                    <td>
                        <span style="font-weight: 700; color: var(--text-white);">${app.requested_load_kw} kW</span>
                        <div style="font-size: 0.74rem; color: var(--text-dim);">${app.phase}</div>
                    </td>
                    <td>
                        <div style="font-weight: 600; color: #38bdf8;">${UI.formatCurrency(app.quotation_amount)}</div>
                        <span style="font-size: 0.7rem; color: ${app.payment_status === 'Paid' ? '#34d399' : '#f59e0b'}; font-weight: 700;">
                            ${app.payment_status.toUpperCase()}
                        </span>
                    </td>
                    <td>
                        ${UI.getStatusBadge(app.status)}
                    </td>
                    <td>
                        <div style="display: flex; gap: 6px;">
                            <button class="btn btn-secondary btn-sm" title="View Dossier & Timeline" onclick="openDossierById(${app.id})">
                                👁️ View
                            </button>
                            <button class="btn btn-primary btn-sm" title="Update Status / Sanction Load" onclick="openEditAppModal(${app.id})">
                                ⚙️ Action
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join("");

    } catch (error) {
        tableBody.innerHTML = `<tr><td colspan="7" style="text-align:center; color: var(--rose); padding: 20px;">Error: ${error.message}</td></tr>`;
    }
}

function onAppSearchChange() {
    State.applications.search = document.getElementById("app-search-input").value;
    State.applications.page = 1;
    loadApplications();
}

function onAppStatusFilterChange() {
    State.applications.status = document.getElementById("app-status-filter").value;
    State.applications.page = 1;
    loadApplications();
}

function onAppCategoryFilterChange() {
    State.applications.category = document.getElementById("app-category-filter").value;
    State.applications.page = 1;
    loadApplications();
}

function onAppSubstationFilterChange() {
    State.applications.substation = document.getElementById("app-substation-filter").value;
    State.applications.page = 1;
    loadApplications();
}

function changeAppPage(delta) {
    const newPage = State.applications.page + delta;
    if (newPage >= 1 && newPage <= State.applications.totalPages) {
        State.applications.page = newPage;
        loadApplications();
    }
}

function openNewApplicationModal() {
    document.getElementById("form-new-application").reset();
    document.getElementById("app-form-load").value = "5.0";
    document.getElementById("app-form-category").value = "Domestic";
    document.getElementById("app-form-phase").value = "Single Phase";
    document.getElementById("app-form-category").dispatchEvent(new Event("change"));
    UI.openModal("modal-new-application");
}

async function handleCreateApplication(e) {
    e.preventDefault();
    const btn = e.target.querySelector("button[type=submit]");
    btn.disabled = true;
    btn.textContent = "Submitting...";

    const payload = {
        connection_type: document.getElementById("app-form-conn-type").value,
        category: document.getElementById("app-form-category").value,
        requested_load_kw: parseFloat(document.getElementById("app-form-load").value),
        phase: document.getElementById("app-form-phase").value,
        premises_type: document.getElementById("app-form-premises").value,
        substation_name: document.getElementById("app-form-substation").value,
        remarks: document.getElementById("app-form-remarks").value,
        consumer: {
            full_name: document.getElementById("app-form-name").value.trim(),
            email: document.getElementById("app-form-email").value.trim(),
            phone: document.getElementById("app-form-phone").value.trim(),
            national_id: document.getElementById("app-form-national-id").value.trim(),
            address: document.getElementById("app-form-address").value.trim(),
            city: document.getElementById("app-form-city").value.trim(),
            pincode: document.getElementById("app-form-pincode").value.trim(),
            consumer_category: document.getElementById("app-form-category").value
        }
    };

    try {
        const created = await API.createApplication(payload);
        UI.closeModal("modal-new-application");
        UI.showToast(`Application ${created.application_number} submitted successfully!`, "success");
        loadApplications();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Submission failed: ${error.message}`, "error");
    } finally {
        btn.disabled = false;
        btn.textContent = "Submit Application";
    }
}

async function openDossierById(appId) {
    try {
        const app = await API.getApplication(appId);
        State.selectedApplication = app;

        document.getElementById("dossier-app-num").textContent = app.application_number;
        document.getElementById("dossier-status-badge").innerHTML = UI.getStatusBadge(app.status);
        document.getElementById("dossier-category-badge").innerHTML = UI.getCategoryBadge(app.category);

        const stages = [
            "Submitted",
            "Document_Verified",
            "Field_Inspection_Scheduled",
            "Inspection_Approved",
            "Payment_Pending",
            "Meter_Assigned_Active"
        ];
        const currentIdx = stages.indexOf(app.status);
        const stepperHtml = stages.map((stg, i) => {
            let cls = "";
            if (app.status === "Rejected") {
                cls = i === 0 ? "completed" : "";
            } else if (i < currentIdx) {
                cls = "completed";
            } else if (i === currentIdx) {
                cls = "active";
            }
            const labels = ["Submitted", "Doc Verified", "Inspection", "Approved", "Payment", "Meter Active"];
            return `
                <div class="step-item ${cls}">
                    <div class="step-circle">${cls === "completed" ? "✓" : (i + 1)}</div>
                    <div class="step-label">${labels[i]}</div>
                </div>
            `;
        }).join("");
        document.getElementById("dossier-stepper").innerHTML = stepperHtml;

        const c = app.consumer || {};
        document.getElementById("dossier-consumer-name").textContent = c.full_name || "—";
        document.getElementById("dossier-consumer-contact").textContent = `${c.phone || "—"} | ${c.email || "—"}`;
        document.getElementById("dossier-consumer-id").textContent = c.national_id || "—";
        document.getElementById("dossier-consumer-address").textContent = `${c.address || "—"}, ${c.city || ""}, PIN: ${c.pincode || ""}`;

        document.getElementById("dossier-tech-load").textContent = `${app.requested_load_kw} kW (${app.phase})`;
        document.getElementById("dossier-tech-sanctioned").textContent = app.sanctioned_load_kw ? `${app.sanctioned_load_kw} kW` : "Pending Sanction";
        document.getElementById("dossier-tech-substation").textContent = app.substation_name;
        document.getElementById("dossier-tech-premises").textContent = app.premises_type;
        document.getElementById("dossier-tech-quote").textContent = `${UI.formatCurrency(app.quotation_amount)} (${app.payment_status})`;

        const inspBlock = document.getElementById("dossier-inspection-block");
        if (app.inspection) {
            inspBlock.style.display = "block";
            document.getElementById("dossier-insp-inspector").textContent = app.inspection.inspector_name;
            document.getElementById("dossier-insp-status").textContent = app.inspection.feasibility_status;
            document.getElementById("dossier-insp-pole").textContent = `${app.inspection.pole_distance_meters} meters`;
            document.getElementById("dossier-insp-transformer").textContent = `${app.inspection.transformer_id} (${app.inspection.transformer_capacity_kva} kVA)`;
            document.getElementById("dossier-insp-remarks").textContent = app.inspection.remarks || "No remarks";
        } else {
            inspBlock.style.display = "none";
        }

        const meterBlock = document.getElementById("dossier-meter-block");
        if (app.meter) {
            meterBlock.style.display = "block";
            document.getElementById("dossier-meter-serial").textContent = app.meter.meter_serial_number;
            document.getElementById("dossier-meter-type").textContent = `${app.meter.meter_type} (${app.meter.phase})`;
            document.getElementById("dossier-meter-feeder").textContent = app.meter.feeder_line;
            document.getElementById("dossier-meter-reading").textContent = `${app.meter.current_reading_kwh} kWh`;
        } else {
            meterBlock.style.display = "none";
        }

        const auditContainer = document.getElementById("dossier-audit-timeline");
        auditContainer.innerHTML = (app.audit_logs || []).map(log => `
            <div class="timeline-item">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="timeline-action">${log.action.replace(/_/g, " ")} ➔ <span class="badge badge-default">${log.new_status}</span></div>
                    <div class="timeline-note">${log.notes || "System update"} (By: ${log.performed_by})</div>
                    <div class="timeline-time">${UI.formatDateTime(log.timestamp)}</div>
                </div>
            </div>
        `).join("") || `<p style="color:var(--text-dim);">No audit logs recorded.</p>`;

        UI.openModal("modal-application-dossier");
    } catch (error) {
        UI.showToast(`Failed to load dossier: ${error.message}`, "error");
    }
}

async function openEditAppModal(appId) {
    try {
        const app = await API.getApplication(appId);
        State.selectedApplication = app;

        document.getElementById("edit-app-id").value = app.id;
        document.getElementById("edit-app-num-display").textContent = app.application_number;
        document.getElementById("edit-app-status").value = app.status;
        document.getElementById("edit-app-sanctioned-load").value = app.sanctioned_load_kw || app.requested_load_kw;
        document.getElementById("edit-app-payment-status").value = app.payment_status;
        document.getElementById("edit-app-quote-amount").value = app.quotation_amount;
        document.getElementById("edit-app-officer").value = "Section Officer";
        document.getElementById("edit-app-note").value = "";

        UI.openModal("modal-edit-application");
    } catch (error) {
        UI.showToast("Failed to fetch application", "error");
    }
}

async function handleUpdateApplication(e) {
    e.preventDefault();
    const appId = document.getElementById("edit-app-id").value;
    const btn = e.target.querySelector("button[type=submit]");
    btn.disabled = true;

    const payload = {
        status: document.getElementById("edit-app-status").value,
        sanctioned_load_kw: parseFloat(document.getElementById("edit-app-sanctioned-load").value) || null,
        payment_status: document.getElementById("edit-app-payment-status").value,
        quotation_amount: parseFloat(document.getElementById("edit-app-quote-amount").value) || 0.0,
        performed_by: document.getElementById("edit-app-officer").value.trim() || "Officer",
        action_note: document.getElementById("edit-app-note").value.trim() || "Status and load updated."
    };

    try {
        await API.updateApplication(appId, payload);
        UI.closeModal("modal-edit-application");
        UI.showToast("Application successfully updated!", "success");
        loadApplications();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Update failed: ${error.message}`, "error");
    } finally {
        btn.disabled = false;
    }
}

function promptDeleteApplication(appId) {
    if (confirm("Are you sure you want to cancel and delete this connection application?")) {
        API.deleteApplication(appId).then(() => {
            UI.showToast("Application deleted successfully", "success");
            UI.closeAllModals();
            loadApplications();
            loadDashboard();
        }).catch(err => {
            UI.showToast(`Delete failed: ${err.message}`, "error");
        });
    }
}

// =============================================================================
// 3. INSPECTIONS
// =============================================================================
async function loadInspections() {
    const container = document.getElementById("inspections-table-body");
    if (!container) return;

    container.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 30px;"><div class="spinner" style="margin:0 auto 8px;"></div>Loading inspections...</td></tr>`;

    try {
        const inspections = await API.getInspections();
        State.inspections = inspections;

        if (!inspections || inspections.length === 0) {
            container.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">
                            <div class="empty-state-title">No Field Surveys Recorded</div>
                            <div class="empty-state-desc">Schedule a site feasibility inspection for pending applications.</div>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = inspections.map(insp => `
            <tr>
                <td>
                    <a href="#" onclick="openDossierById(${insp.application_id}); return false;" style="font-weight: 700; color: #38bdf8;">
                        App #${insp.application_id}
                    </a>
                </td>
                <td style="font-weight: 600;">${insp.inspector_name}</td>
                <td>
                    <span class="badge ${insp.feasibility_status === 'Feasible' ? 'badge-approved' : (insp.feasibility_status === 'Non_Feasible' ? 'badge-rejected' : 'badge-scheduled')}">
                        ${insp.feasibility_status.replace(/_/g, " ")}
                    </span>
                </td>
                <td>${insp.pole_distance_meters} m</td>
                <td>
                    <div>${insp.transformer_id}</div>
                    <div style="font-size: 0.74rem; color: var(--text-dim);">${insp.transformer_capacity_kva} kVA</div>
                </td>
                <td>${insp.completed_at ? UI.formatDateTime(insp.completed_at) : '<span style="color:var(--amber);">Scheduled</span>'}</td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="openRecordInspectionModal(${insp.id})">
                        📝 Record Survey
                    </button>
                </td>
            </tr>
        `).join("");

    } catch (error) {
        container.innerHTML = `<tr><td colspan="7" style="text-align:center; color: var(--rose); padding: 20px;">Failed: ${error.message}</td></tr>`;
    }
}

function openScheduleInspectionModal() {
    document.getElementById("form-schedule-inspection").reset();
    UI.openModal("modal-schedule-inspection");
}

async function handleScheduleInspection(e) {
    e.preventDefault();
    const payload = {
        application_id: parseInt(document.getElementById("sched-insp-app-id").value),
        inspector_name: document.getElementById("sched-insp-inspector").value.trim(),
        feasibility_status: "Feasible",
        pole_distance_meters: parseFloat(document.getElementById("sched-insp-pole").value) || 25.0,
        transformer_id: document.getElementById("sched-insp-transformer").value.trim() || "TR-CENTRAL-04",
        transformer_capacity_kva: parseFloat(document.getElementById("sched-insp-kva").value) || 100.0,
        meter_box_ready: true,
        remarks: document.getElementById("sched-insp-remarks").value.trim()
    };

    try {
        await API.scheduleInspection(payload);
        UI.closeModal("modal-schedule-inspection");
        UI.showToast("Field inspection scheduled successfully!", "success");
        loadInspections();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Scheduling failed: ${error.message}`, "error");
    }
}

async function openRecordInspectionModal(inspId) {
    const insp = State.inspections.find(i => i.id === inspId);
    if (!insp) return;

    document.getElementById("record-insp-id").value = insp.id;
    document.getElementById("record-insp-status").value = insp.feasibility_status;
    document.getElementById("record-insp-pole").value = insp.pole_distance_meters;
    document.getElementById("record-insp-transformer").value = insp.transformer_id;
    document.getElementById("record-insp-kva").value = insp.transformer_capacity_kva;
    document.getElementById("record-insp-meter-box").checked = insp.meter_box_ready;
    document.getElementById("record-insp-remarks").value = insp.remarks || "";

    UI.openModal("modal-record-inspection");
}

async function handleCompleteInspection(e) {
    e.preventDefault();
    const inspId = document.getElementById("record-insp-id").value;
    const payload = {
        feasibility_status: document.getElementById("record-insp-status").value,
        pole_distance_meters: parseFloat(document.getElementById("record-insp-pole").value),
        transformer_id: document.getElementById("record-insp-transformer").value.trim(),
        transformer_capacity_kva: parseFloat(document.getElementById("record-insp-kva").value),
        meter_box_ready: document.getElementById("record-insp-meter-box").checked,
        remarks: document.getElementById("record-insp-remarks").value.trim()
    };

    try {
        await API.completeInspection(inspId, payload);
        UI.closeModal("modal-record-inspection");
        UI.showToast("Survey recorded and status updated!", "success");
        loadInspections();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Recording failed: ${error.message}`, "error");
    }
}

// =============================================================================
// 4. SMART METERS
// =============================================================================
async function loadMeters() {
    const container = document.getElementById("meters-table-body");
    if (!container) return;

    container.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 30px;"><div class="spinner" style="margin:0 auto 8px;"></div>Loading smart meters...</td></tr>`;

    try {
        const meters = await API.getMeters();
        State.meters = meters;

        if (!meters || meters.length === 0) {
            container.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">
                            <div class="empty-state-title">No Active Meters</div>
                            <div class="empty-state-desc">Allocate smart meters to approved power connection applications.</div>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = meters.map(meter => `
            <tr>
                <td>
                    <span style="font-family: monospace; font-weight: 700; color: #38bdf8; font-size: 0.9rem;">
                        ${meter.meter_serial_number}
                    </span>
                    <div style="font-size: 0.74rem; color: var(--text-dim);">App #${meter.application_id}</div>
                </td>
                <td>
                    <div style="font-weight: 600;">${meter.meter_type}</div>
                    <div style="font-size: 0.74rem; color: var(--text-dim);">${meter.phase}</div>
                </td>
                <td>${meter.substation_name}</td>
                <td>${meter.feeder_line}</td>
                <td>
                    <span style="font-weight: 700; color: #34d399;">${meter.current_reading_kwh} kWh</span>
                </td>
                <td>
                    <span class="badge ${meter.status === 'Active' ? 'badge-active' : 'badge-danger'}">
                        ${meter.status}
                    </span>
                </td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="openUpdateMeterModal(${meter.id})">
                        ⚡ Reading / Status
                    </button>
                </td>
            </tr>
        `).join("");

    } catch (error) {
        container.innerHTML = `<tr><td colspan="7" style="text-align:center; color: var(--rose); padding: 20px;">Failed: ${error.message}</td></tr>`;
    }
}

function openAllocateMeterModal() {
    document.getElementById("form-allocate-meter").reset();
    UI.openModal("modal-allocate-meter");
}

async function handleAllocateMeter(e) {
    e.preventDefault();
    const payload = {
        application_id: parseInt(document.getElementById("meter-form-app-id").value),
        meter_serial_number: document.getElementById("meter-form-serial").value.trim() || null,
        meter_type: document.getElementById("meter-form-type").value,
        phase: document.getElementById("meter-form-phase").value,
        initial_reading_kwh: parseFloat(document.getElementById("meter-form-reading").value) || 0.0,
        substation_name: document.getElementById("meter-form-substation").value,
        feeder_line: document.getElementById("meter-form-feeder").value.trim(),
        status: "Active"
    };

    try {
        const created = await API.allocateMeter(payload);
        UI.closeModal("modal-allocate-meter");
        UI.showToast(`Meter ${created.meter_serial_number} allocated!`, "success");
        loadMeters();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Allocation failed: ${error.message}`, "error");
    }
}

function openUpdateMeterModal(meterId) {
    const meter = State.meters.find(m => m.id === meterId);
    if (!meter) return;

    const newReading = prompt(`Enter updated reading for meter ${meter.meter_serial_number} (Current: ${meter.current_reading_kwh} kWh):`, meter.current_reading_kwh);
    if (newReading !== null && !isNaN(parseFloat(newReading))) {
        API.updateMeter(meterId, { current_reading_kwh: parseFloat(newReading) }).then(() => {
            UI.showToast("Meter reading updated successfully", "success");
            loadMeters();
        }).catch(err => {
            UI.showToast(`Update error: ${err.message}`, "error");
        });
    }
}

// =============================================================================
// 5. GRIEVANCES
// =============================================================================
async function loadGrievances() {
    const container = document.getElementById("grievances-table-body");
    if (!container) return;

    container.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 30px;"><div class="spinner" style="margin:0 auto 8px;"></div>Loading grievance desk...</td></tr>`;

    try {
        const grievances = await API.getGrievances({
            status: State.grievances.status,
            priority: State.grievances.priority,
            search: State.grievances.search
        });
        State.grievances.items = grievances;

        if (!grievances || grievances.length === 0) {
            container.innerHTML = `
                <tr>
                    <td colspan="6">
                        <div class="empty-state">
                            <div class="empty-state-title">No Grievances Logged</div>
                            <div class="empty-state-desc">Grid power supplies and consumer meters operating normally.</div>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }

        container.innerHTML = grievances.map(grv => {
            const c = grv.consumer || {};
            return `
                <tr>
                    <td>
                        <span style="font-family: monospace; font-weight: 700; color: #f59e0b;">
                            ${grv.grievance_number}
                        </span>
                        <div style="font-size: 0.74rem; color: var(--text-dim);">${UI.formatDateTime(grv.created_at)}</div>
                    </td>
                    <td>
                        <div style="font-weight: 600;">${c.full_name || "Consumer"}</div>
                        <div style="font-size: 0.76rem; color: var(--text-muted);">${c.phone || "—"}</div>
                    </td>
                    <td>
                        <div style="font-weight: 600;">${grv.category}</div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); max-width: 240px; white-space: normal;">
                            ${grv.description}
                        </div>
                    </td>
                    <td>${UI.getPriorityBadge(grv.priority)}</td>
                    <td>${UI.getStatusBadge(grv.status)}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="openUpdateGrievanceModal(${grv.id})">
                            🛠️ Action / Resolve
                        </button>
                    </td>
                </tr>
            `;
        }).join("");

    } catch (error) {
        container.innerHTML = `<tr><td colspan="6" style="text-align:center; color: var(--rose); padding: 20px;">Error: ${error.message}</td></tr>`;
    }
}

function onGrievanceStatusFilter() {
    State.grievances.status = document.getElementById("grv-status-filter").value;
    loadGrievances();
}

function onGrievancePriorityFilter() {
    State.grievances.priority = document.getElementById("grv-priority-filter").value;
    loadGrievances();
}

function openFileGrievanceModal() {
    document.getElementById("form-file-grievance").reset();
    UI.openModal("modal-file-grievance");
}

async function handleCreateGrievance(e) {
    e.preventDefault();
    const payload = {
        full_name: document.getElementById("grv-form-name").value.trim(),
        phone: document.getElementById("grv-form-phone").value.trim(),
        email: document.getElementById("grv-form-email").value.trim() || null,
        address: document.getElementById("grv-form-address").value.trim(),
        category: document.getElementById("grv-form-category").value,
        priority: document.getElementById("grv-form-priority").value,
        description: document.getElementById("grv-form-desc").value.trim(),
        meter_serial_number: document.getElementById("grv-form-meter").value.trim() || null
    };

    try {
        const created = await API.createGrievance(payload);
        UI.closeModal("modal-file-grievance");
        UI.showToast(`Grievance ${created.grievance_number} logged! Field crew notified.`, "success");
        loadGrievances();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Failed: ${error.message}`, "error");
    }
}

function openUpdateGrievanceModal(grvId) {
    const grv = State.grievances.items.find(g => g.id === grvId);
    if (!grv) return;

    document.getElementById("edit-grv-id").value = grv.id;
    document.getElementById("edit-grv-num-display").textContent = grv.grievance_number;
    document.getElementById("edit-grv-status").value = grv.status;
    document.getElementById("edit-grv-lineman").value = grv.assigned_lineman || "";
    document.getElementById("edit-grv-notes").value = grv.resolution_notes || "";

    UI.openModal("modal-update-grievance");
}

async function handleUpdateGrievance(e) {
    e.preventDefault();
    const grvId = document.getElementById("edit-grv-id").value;
    const payload = {
        status: document.getElementById("edit-grv-status").value,
        assigned_lineman: document.getElementById("edit-grv-lineman").value.trim() || null,
        resolution_notes: document.getElementById("edit-grv-notes").value.trim() || null
    };

    try {
        await API.updateGrievance(grvId, payload);
        UI.closeModal("modal-update-grievance");
        UI.showToast("Grievance updated!", "success");
        loadGrievances();
        loadDashboard();
    } catch (error) {
        UI.showToast(`Update failed: ${error.message}`, "error");
    }
}

// =============================================================================
// 6. TRACK APPLICATION
// =============================================================================
async function searchTrackApplication(appNum) {
    const resultContainer = document.getElementById("track-result-container");
    resultContainer.innerHTML = `<div style="text-align:center; padding: 30px;"><div class="spinner" style="margin:0 auto 8px;"></div>Fetching application...</div>`;

    try {
        const app = await API.getApplication(appNum);

        const stages = [
            "Submitted",
            "Document_Verified",
            "Field_Inspection_Scheduled",
            "Inspection_Approved",
            "Payment_Pending",
            "Meter_Assigned_Active"
        ];
        const currentIdx = stages.indexOf(app.status);
        const stepperHtml = stages.map((stg, i) => {
            let cls = "";
            if (app.status === "Rejected") {
                cls = i === 0 ? "completed" : "";
            } else if (i < currentIdx) {
                cls = "completed";
            } else if (i === currentIdx) {
                cls = "active";
            }
            const labels = ["Submitted", "Doc Verified", "Inspection", "Approved", "Payment", "Active Meter"];
            return `
                <div class="step-item ${cls}">
                    <div class="step-circle">${cls === "completed" ? "✓" : (i + 1)}</div>
                    <div class="step-label">${labels[i]}</div>
                </div>
            `;
        }).join("");

        const c = app.consumer || {};

        resultContainer.innerHTML = `
            <div class="panel-card" style="margin-top: 16px;">
                <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 14px; margin-bottom: 14px;">
                    <div>
                        <h3 style="font-size: 1.25rem;">Application: ${app.application_number}</h3>
                        <p style="color: var(--text-muted); font-size: 0.8rem;">Submitted on ${UI.formatDateTime(app.created_at)}</p>
                    </div>
                    <div>
                        ${UI.getStatusBadge(app.status)}
                    </div>
                </div>

                <div class="stepper-container">
                    ${stepperHtml}
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px;">
                    <div style="background: rgba(0,0,0,0.2); padding: 14px; border-radius: var(--radius-md);">
                        <h4 style="font-size: 0.88rem; margin-bottom: 8px; color: var(--cyan-light);">Applicant & Premises</h4>
                        <p style="font-size: 0.84rem;"><strong>Name:</strong> ${c.full_name || "—"}</p>
                        <p style="font-size: 0.84rem;"><strong>Phone:</strong> ${c.phone || "—"}</p>
                        <p style="font-size: 0.84rem;"><strong>Address:</strong> ${c.address || "—"}, ${c.city || ""}</p>
                        <p style="font-size: 0.84rem;"><strong>Premises:</strong> ${app.premises_type}</p>
                    </div>

                    <div style="background: rgba(0,0,0,0.2); padding: 14px; border-radius: var(--radius-md);">
                        <h4 style="font-size: 0.88rem; margin-bottom: 8px; color: var(--amber-light);">Power Demand Note</h4>
                        <p style="font-size: 0.84rem;"><strong>Tariff:</strong> ${app.category}</p>
                        <p style="font-size: 0.84rem;"><strong>Load:</strong> ${app.requested_load_kw} kW (${app.phase})</p>
                        <p style="font-size: 0.84rem;"><strong>Substation:</strong> ${app.substation_name}</p>
                        <p style="font-size: 0.95rem; font-weight: 700; color: #38bdf8; margin-top: 4px;">
                            Quotation: ${UI.formatCurrency(app.quotation_amount)} 
                            <span style="font-size: 0.72rem; color: ${app.payment_status === 'Paid' ? '#34d399' : '#f59e0b'};">(${app.payment_status.toUpperCase()})</span>
                        </p>
                    </div>
                </div>

                ${app.meter ? `
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 14px; border-radius: var(--radius-md); margin-top: 14px;">
                        <h4 style="color: #34d399; font-size: 0.9rem; margin-bottom: 6px;">⚡ Energized Smart Meter</h4>
                        <p style="font-size: 0.84rem;"><strong>Serial:</strong> <span style="font-family: monospace;">${app.meter.meter_serial_number}</span> (${app.meter.meter_type})</p>
                        <p style="font-size: 0.84rem;"><strong>Feeder:</strong> ${app.meter.feeder_line}</p>
                        <p style="font-size: 0.84rem;"><strong>Reading:</strong> ${app.meter.current_reading_kwh} kWh</p>
                    </div>
                ` : ''}

                <div style="margin-top: 16px; display: flex; justify-content: flex-end; gap: 8px;">
                    <button class="btn btn-secondary" onclick="window.print()">🖨️ Print Application</button>
                </div>
            </div>
        `;

    } catch (error) {
        resultContainer.innerHTML = `
            <div class="panel-card" style="margin-top: 16px; text-align: center; padding: 30px;">
                <div style="color: var(--rose); font-size: 1.1rem; font-weight: 700; margin-bottom: 6px;">Application Not Found</div>
                <p style="color: var(--text-muted); font-size: 0.84rem;">No application matches '${appNum}'. Verify the number (e.g. APP-2026-1001).</p>
            </div>
        `;
    }
}

// Global Window Bindings
window.switchView = switchView;
window.loadDashboard = loadDashboard;
window.loadApplications = loadApplications;
window.loadInspections = loadInspections;
window.loadMeters = loadMeters;
window.loadGrievances = loadGrievances;
window.openNewApplicationModal = openNewApplicationModal;
window.openDossierById = openDossierById;
window.openEditAppModal = openEditAppModal;
window.promptDeleteApplication = promptDeleteApplication;
window.openScheduleInspectionModal = openScheduleInspectionModal;
window.openRecordInspectionModal = openRecordInspectionModal;
window.openAllocateMeterModal = openAllocateMeterModal;
window.openUpdateMeterModal = openUpdateMeterModal;
window.openFileGrievanceModal = openFileGrievanceModal;
window.openUpdateGrievanceModal = openUpdateGrievanceModal;
window.searchTrackApplication = searchTrackApplication;
window.onAppSearchChange = onAppSearchChange;
window.onAppStatusFilterChange = onAppStatusFilterChange;
window.onAppCategoryFilterChange = onAppCategoryFilterChange;
window.onAppSubstationFilterChange = onAppSubstationFilterChange;
window.changeAppPage = changeAppPage;
window.onGrievanceStatusFilter = onGrievanceStatusFilter;
window.onGrievancePriorityFilter = onGrievancePriorityFilter;
