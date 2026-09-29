-- =============================================================================
-- VoltFlow: Electricity Board Connection & Utility Service Management System
-- Relational Database Schema (SQLite / PostgreSQL Compatible)
-- =============================================================================

PRAGMA foreign_keys = ON;

-- 1. Consumers Table
CREATE TABLE IF NOT EXISTS consumers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    national_id VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(80) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    consumer_category VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_consumers_email ON consumers(email);
CREATE INDEX IF NOT EXISTS idx_consumers_phone ON consumers(phone);

-- 2. Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_number VARCHAR(30) NOT NULL UNIQUE,
    consumer_id INTEGER NOT NULL,
    connection_type VARCHAR(40) NOT NULL,
    category VARCHAR(30) NOT NULL,
    requested_load_kw REAL NOT NULL,
    phase VARCHAR(20) NOT NULL,
    premises_type VARCHAR(20) NOT NULL,
    substation_name VARCHAR(100) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'Submitted',
    sanctioned_load_kw REAL,
    quotation_amount REAL NOT NULL DEFAULT 0.0,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    remarks TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (consumer_id) REFERENCES consumers(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_applications_app_num ON applications(application_number);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_category ON applications(category);
CREATE INDEX IF NOT EXISTS idx_applications_substation ON applications(substation_name);

-- 3. Inspections Table
CREATE TABLE IF NOT EXISTS inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL UNIQUE,
    inspector_name VARCHAR(100) NOT NULL,
    feasibility_status VARCHAR(40) NOT NULL DEFAULT 'Feasible',
    pole_distance_meters REAL NOT NULL DEFAULT 25.0,
    transformer_id VARCHAR(40) NOT NULL,
    transformer_capacity_kva REAL NOT NULL DEFAULT 100.0,
    meter_box_ready BOOLEAN NOT NULL DEFAULT 1,
    remarks TEXT,
    scheduled_date DATETIME NOT NULL,
    completed_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

-- 4. Meters Table
CREATE TABLE IF NOT EXISTS meters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL UNIQUE,
    meter_serial_number VARCHAR(40) NOT NULL UNIQUE,
    meter_type VARCHAR(40) NOT NULL,
    phase VARCHAR(20) NOT NULL,
    initial_reading_kwh REAL NOT NULL DEFAULT 0.0,
    current_reading_kwh REAL NOT NULL DEFAULT 0.0,
    substation_name VARCHAR(100) NOT NULL,
    feeder_line VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    installation_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_meters_serial ON meters(meter_serial_number);
CREATE INDEX IF NOT EXISTS idx_meters_status ON meters(status);

-- 5. Grievances Table
CREATE TABLE IF NOT EXISTS grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grievance_number VARCHAR(30) NOT NULL UNIQUE,
    consumer_id INTEGER NOT NULL,
    meter_id INTEGER,
    category VARCHAR(40) NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
    description TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Registered',
    assigned_lineman VARCHAR(100),
    resolution_notes TEXT,
    resolved_at DATETIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (consumer_id) REFERENCES consumers(id) ON DELETE CASCADE,
    FOREIGN KEY (meter_id) REFERENCES meters(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_grievances_num ON grievances(grievance_number);
CREATE INDEX IF NOT EXISTS idx_grievances_status ON grievances(status);
CREATE INDEX IF NOT EXISTS idx_grievances_priority ON grievances(priority);

-- 6. Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    action VARCHAR(60) NOT NULL,
    performed_by VARCHAR(100) NOT NULL,
    old_status VARCHAR(40),
    new_status VARCHAR(40) NOT NULL,
    notes TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_app_id ON audit_logs(application_id);
