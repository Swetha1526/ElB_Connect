// frontend/js/config.js
/**
 * VoltFlow Global Configuration
 */
const CONFIG = {
    APP_NAME: "VoltFlow",
    VERSION: "1.0.0",
    
    // Automatically resolve API Base URL
    get API_BASE_URL() {
        if (window.location.port === "8000" || window.location.pathname.startsWith("/static")) {
            return "/api/v1";
        }
        return "http://127.0.0.1:8000/api/v1";
    },

    CATEGORIES: [
        { id: "Domestic", label: "Domestic (LT-1)", ratePerKw: 600, baseFee: 1200 },
        { id: "Commercial", label: "Commercial (LT-2)", ratePerKw: 1200, baseFee: 2500 },
        { id: "Industrial", label: "Industrial (HT-1)", ratePerKw: 2500, baseFee: 8000 },
        { id: "Agricultural", label: "Agricultural (LT-4)", ratePerKw: 200, baseFee: 800 }
    ],

    SUBSTATIONS: [
        "Central Substation 33/11kV",
        "Tech Park Substation 66/11kV",
        "Industrial Substation 110/33kV",
        "Rural Feeder Substation 33/11kV",
        "East Substation 33/11kV",
        "West Substation 33/11kV",
        "North Substation 66/11kV"
    ],

    STATUSES: [
        { id: "Submitted", label: "Submitted", badge: "badge-info" },
        { id: "Document_Verified", label: "Document Verified", badge: "badge-primary" },
        { id: "Field_Inspection_Scheduled", label: "Inspection Scheduled", badge: "badge-warning" },
        { id: "Inspection_Approved", label: "Inspection Approved", badge: "badge-accent" },
        { id: "Payment_Pending", label: "Payment Pending", badge: "badge-amber" },
        { id: "Meter_Assigned_Active", label: "Active Meter", badge: "badge-success" },
        { id: "Rejected", label: "Rejected", badge: "badge-danger" }
    ]
};
