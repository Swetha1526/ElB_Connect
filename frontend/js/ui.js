// frontend/js/ui.js
/**
 * VoltFlow UI Helper Utilities
 */
const UI = {
    // --- Toast Notifications ---
    showToast(message, type = "info", duration = 4000) {
        let container = document.getElementById("toast-container");
        if (!container) {
            container = document.createElement("div");
            container.id = "toast-container";
            container.className = "toast-container";
            document.body.appendChild(container);
        }

        const toast = document.createElement("div");
        toast.className = `toast toast-${type} animate-slide-in`;

        const icons = {
            success: `<svg class="toast-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>`,
            error: `<svg class="toast-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>`,
            warning: `<svg class="toast-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>`,
            info: `<svg class="toast-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>`
        };

        toast.innerHTML = `
            ${icons[type] || icons.info}
            <div class="toast-content">${message}</div>
            <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add("fade-out");
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    // --- Modal Management ---
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add("active");
            document.body.style.overflow = "hidden";
            const firstInput = modal.querySelector("input:not([type=hidden]), select, textarea");
            if (firstInput) firstInput.focus();
        }
    },

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove("active");
            document.body.style.overflow = "";
        }
    },

    closeAllModals() {
        document.querySelectorAll(".modal.active").forEach(m => m.classList.remove("active"));
        document.body.style.overflow = "";
    },

    // --- Formatters ---
    formatCurrency(amount) {
        if (amount === undefined || amount === null) return "₹ 0.00";
        return new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 2
        }).format(amount);
    },

    formatDate(dateStr) {
        if (!dateStr) return "—";
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric"
        });
    },

    formatDateTime(dateStr) {
        if (!dateStr) return "—";
        const date = new Date(dateStr);
        return date.toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        });
    },

    getStatusBadge(status) {
        const map = {
            "Submitted": { label: "Submitted", class: "badge-submitted" },
            "Document_Verified": { label: "Doc Verified", class: "badge-verified" },
            "Field_Inspection_Scheduled": { label: "Inspection Sched.", class: "badge-scheduled" },
            "Inspection_Approved": { label: "Feasible Approved", class: "badge-approved" },
            "Payment_Pending": { label: "Demand Note Pending", class: "badge-payment" },
            "Meter_Assigned_Active": { label: "Active Energized", class: "badge-active" },
            "Rejected": { label: "Rejected", class: "badge-rejected" },
            "Registered": { label: "Registered", class: "badge-submitted" },
            "Assigned": { label: "Assigned", class: "badge-scheduled" },
            "In_Progress": { label: "In Progress", class: "badge-warning" },
            "Resolved": { label: "Resolved", class: "badge-active" },
            "Closed": { label: "Closed", class: "badge-verified" }
        };

        const config = map[status] || { label: status, class: "badge-default" };
        return `<span class="badge ${config.class}">${config.label}</span>`;
    },

    getPriorityBadge(priority) {
        const map = {
            "Critical": "badge-danger",
            "High": "badge-warning",
            "Medium": "badge-primary",
            "Low": "badge-default"
        };
        const cls = map[priority] || "badge-default";
        return `<span class="badge ${cls}">${priority}</span>`;
    },

    getCategoryBadge(category) {
        const map = {
            "Domestic": "cat-domestic",
            "Commercial": "cat-commercial",
            "Industrial": "cat-industrial",
            "Agricultural": "cat-agricultural"
        };
        const cls = map[category] || "cat-default";
        return `<span class="cat-pill ${cls}">${category}</span>`;
    }
};
