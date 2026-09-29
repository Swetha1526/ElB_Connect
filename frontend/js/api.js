// frontend/js/api.js
/**
 * VoltFlow Centralized REST API Service
 */
const API = {
    async request(endpoint, options = {}) {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        const headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            ...(options.headers || {})
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json().catch(() => null);

            if (!response.ok) {
                const errorMessage = (data && (data.detail || data.message)) || `HTTP Error ${response.status}: ${response.statusText}`;
                throw new Error(typeof errorMessage === "object" ? JSON.stringify(errorMessage) : errorMessage);
            }

            return data;
        } catch (error) {
            console.error(`[API ERROR] ${options.method || "GET"} ${endpoint}:`, error);
            throw error;
        }
    },

    // --- Statistics ---
    async getDashboardStats() {
        return this.request("/stats/dashboard");
    },

    // --- Applications ---
    async getApplications(params = {}) {
        const query = new URLSearchParams();
        Object.entries(params).forEach(([key, val]) => {
            if (val !== undefined && val !== null && val !== "" && val !== "All") {
                query.append(key, val);
            }
        });
        const qs = query.toString() ? `?${query.toString()}` : "";
        return this.request(`/applications${qs}`);
    },

    async getApplication(idOrNumber) {
        return this.request(`/applications/${encodeURIComponent(idOrNumber)}`);
    },

    async createApplication(payload) {
        return this.request("/applications", {
            method: "POST",
            body: JSON.stringify(payload)
        });
    },

    async updateApplication(id, payload) {
        return this.request(`/applications/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
    },

    async deleteApplication(id) {
        return this.request(`/applications/${id}`, {
            method: "DELETE"
        });
    },

    // --- Inspections ---
    async getInspections() {
        return this.request("/inspections");
    },

    async scheduleInspection(payload) {
        return this.request("/inspections", {
            method: "POST",
            body: JSON.stringify(payload)
        });
    },

    async completeInspection(id, payload) {
        return this.request(`/inspections/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
    },

    // --- Meters ---
    async getMeters(status = null) {
        const qs = status && status !== "All" ? `?status=${encodeURIComponent(status)}` : "";
        return this.request(`/meters${qs}`);
    },

    async allocateMeter(payload) {
        return this.request("/meters", {
            method: "POST",
            body: JSON.stringify(payload)
        });
    },

    async updateMeter(id, payload) {
        return this.request(`/meters/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
    },

    // --- Grievances ---
    async getGrievances(params = {}) {
        const query = new URLSearchParams();
        Object.entries(params).forEach(([key, val]) => {
            if (val !== undefined && val !== null && val !== "" && val !== "All") {
                query.append(key, val);
            }
        });
        const qs = query.toString() ? `?${query.toString()}` : "";
        return this.request(`/grievances${qs}`);
    },

    async createGrievance(payload) {
        return this.request("/grievances/public", {
            method: "POST",
            body: JSON.stringify(payload)
        });
    },

    async updateGrievance(id, payload) {
        return this.request(`/grievances/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
    }
};
