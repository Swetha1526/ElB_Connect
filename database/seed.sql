-- =============================================================================
-- VoltFlow: Database Seed Script with Realistic Electricity Board Data
-- =============================================================================

-- 1. Insert Consumers
INSERT INTO consumers (id, full_name, email, phone, national_id, address, city, pincode, consumer_category, created_at, updated_at)
VALUES 
(1, 'Aarav Sharma', 'aarav.sharma@example.com', '9876543210', 'AADHAAR-8912-3401', 'Flat 402, Green Valley Apts, Sector 14', 'Metro City', '110001', 'Domestic', '2026-09-10 09:30:00', '2026-09-10 09:30:00'),
(2, 'Priya Patel', 'priya.patel@apextech.in', '9845123456', 'AADHAAR-4412-9902', 'Plot 18, Electronic City Phase 1', 'Metro City', '560100', 'Commercial', '2026-09-12 11:15:00', '2026-09-12 11:15:00'),
(3, 'Rajeshwer Rao', 'rajesh.rao@agrofarm.org', '9440112233', 'AADHAAR-7711-2299', 'Survey No 84, Village Ramanagara', 'Ramanagara', '562159', 'Agricultural', '2026-09-14 14:00:00', '2026-09-14 14:00:00'),
(4, 'Vikramaditya Mills Ltd', 'accounts@vikrammills.com', '9820334455', 'PAN-AAACV1234K', 'Industrial Area, Phase 3, GIDC', 'Metro City', '390001', 'Industrial', '2026-09-15 10:45:00', '2026-09-15 10:45:00'),
(5, 'Sneha Mukherjee', 'sneha.m@outlook.com', '9734567890', 'AADHAAR-6512-8821', '12B Lake View Road, Salt Lake Sector 3', 'Metro City', '700091', 'Domestic', '2026-09-18 16:20:00', '2026-09-18 16:20:00'),
(6, 'Karthik Raman', 'karthik.raman@bakerycafe.com', '9962012345', 'AADHAAR-9012-3341', '88 Cathedral Road, Gopalapuram', 'Metro City', '600086', 'Commercial', '2026-09-20 12:00:00', '2026-09-20 12:00:00'),
(7, 'Sunita Deshmukh', 'sunita.deshmukh@gmail.com', '9822098765', 'AADHAAR-3114-5567', 'Row House 5, Sunshine Meadows, Baner', 'Metro City', '411045', 'Domestic', '2026-09-22 15:10:00', '2026-09-22 15:10:00'),
(8, 'Global Logistics Hub', 'ops@globallogistics.com', '9811223344', 'PAN-AABCG9876P', 'Warehouse Zone 4, Bypass Highway', 'Metro City', '122001', 'Commercial', '2026-09-24 10:00:00', '2026-09-24 10:00:00');

-- 2. Insert Applications
INSERT INTO applications (id, application_number, consumer_id, connection_type, category, requested_load_kw, phase, premises_type, substation_name, status, sanctioned_load_kw, quotation_amount, payment_status, remarks, created_at, updated_at)
VALUES
(1, 'APP-2026-1001', 1, 'New Connection', 'Domestic', 5.0, 'Single Phase', 'Owned', 'Central Substation 33/11kV', 'Meter_Assigned_Active', 5.0, 4200.00, 'Paid', 'Meter successfully commissioned and activated.', '2026-09-10 09:35:00', '2026-09-16 14:30:00'),
(2, 'APP-2026-1002', 2, 'New Connection', 'Commercial', 25.0, 'Three Phase', 'Rented', 'Tech Park Substation 66/11kV', 'Payment_Pending', 25.0, 32500.00, 'Pending', 'Site inspection approved. Demand note issued to consumer.', '2026-09-12 11:20:00', '2026-09-18 10:00:00'),
(3, 'APP-2026-1003', 3, 'New Connection', 'Agricultural', 7.5, 'Three Phase', 'Owned', 'Rural Feeder Substation 33/11kV', 'Field_Inspection_Scheduled', NULL, 2300.00, 'Pending', 'Junior Engineer assigned for agricultural pump feasibility.', '2026-09-14 14:10:00', '2026-09-17 09:00:00'),
(4, 'APP-2026-1004', 4, 'Load Enhancement', 'Industrial', 150.0, 'Three Phase', 'Owned', 'Industrial Substation 110/33kV', 'Document_Verified', NULL, 383000.00, 'Pending', 'Factory load enhancement request submitted with load audit.', '2026-09-15 10:50:00', '2026-09-16 11:30:00'),
(5, 'APP-2026-1005', 5, 'New Connection', 'Domestic', 3.0, 'Single Phase', 'Owned', 'East Substation 33/11kV', 'Submitted', NULL, 3000.00, 'Pending', 'Fresh application submitted by consumer online.', '2026-09-18 16:25:00', '2026-09-18 16:25:00'),
(6, 'APP-2026-1006', 6, 'New Connection', 'Commercial', 12.0, 'Three Phase', 'Rented', 'Central Substation 33/11kV', 'Meter_Assigned_Active', 12.0, 16900.00, 'Paid', 'Commercial digital meter commissioned for Cafe.', '2026-09-20 12:05:00', '2026-09-26 15:40:00'),
(7, 'APP-2026-1007', 7, 'Tariff Change', 'Domestic', 6.0, 'Single Phase', 'Owned', 'West Substation 33/11kV', 'Inspection_Approved', 6.0, 4800.00, 'Pending', 'Feasibility approved. Security deposit payment pending.', '2026-09-22 15:15:00', '2026-09-25 11:00:00'),
(8, 'APP-2026-1008', 8, 'New Connection', 'Commercial', 50.0, 'Three Phase', 'Owned', 'North Substation 66/11kV', 'Rejected', NULL, 62500.00, 'Pending', 'Rejected due to insufficient transformer margin without HT substation.', '2026-09-24 10:10:00', '2026-09-27 16:00:00');

-- 3. Insert Field Inspections
INSERT INTO inspections (id, application_id, inspector_name, feasibility_status, pole_distance_meters, transformer_id, transformer_capacity_kva, meter_box_ready, remarks, scheduled_date, completed_at, created_at)
VALUES
(1, 1, 'Er. Ramesh Kulkarni (JE-South)', 'Feasible', 18.5, 'TR-CENTRAL-04', 250.0, 1, 'Site clear. Distribution pole within 20m. Transformer capacity adequate.', '2026-09-13 10:00:00', '2026-09-13 11:30:00', '2026-09-11 14:00:00'),
(2, 2, 'Er. Swati Naik (JE-TechPark)', 'Feasible', 22.0, 'TR-TECHPARK-12', 500.0, 1, 'Three-phase commercial line extension feasible. Adequate headroom on busbar.', '2026-09-16 11:00:00', '2026-09-16 12:45:00', '2026-09-14 09:30:00'),
(3, 3, 'Er. Mahendra Gowda (JE-Rural)', 'Feasible', 45.0, 'TR-RURAL-08', 100.0, 1, 'Scheduled inspection for pump-set energization.', '2026-09-28 10:00:00', NULL, '2026-09-17 09:00:00'),
(4, 6, 'Er. Ramesh Kulkarni (JE-South)', 'Feasible', 12.0, 'TR-CENTRAL-02', 315.0, 1, 'Commercial line verified. CT-operated meter installation approved.', '2026-09-22 14:00:00', '2026-09-22 15:20:00', '2026-09-21 10:00:00'),
(5, 7, 'Er. Amitav Sen (JE-West)', 'Feasible', 15.0, 'TR-WEST-09', 200.0, 1, 'Domestic load upgrade from 3kW to 6kW feasible on existing service drop.', '2026-09-24 10:30:00', '2026-09-24 11:45:00', '2026-09-23 11:00:00'),
(6, 8, 'Er. Nilesh Shinde (JE-North)', 'Non_Feasible', 120.0, 'TR-NORTH-15', 100.0, 0, 'Transformer capacity saturated (94% loading). Dedicated HT transformer required.', '2026-09-26 15:00:00', '2026-09-27 15:30:00', '2026-09-25 14:00:00');

-- 4. Insert Active Meters
INSERT INTO meters (id, application_id, meter_serial_number, meter_type, phase, initial_reading_kwh, current_reading_kwh, substation_name, feeder_line, status, installation_date, created_at, updated_at)
VALUES
(1, 1, 'MTR-2026-8801', 'Smart Digital', 'Single Phase', 0.0, 142.5, 'Central Substation 33/11kV', 'Feeder-11kV-SouthCity', 'Active', '2026-09-16 14:00:00', '2026-09-16 14:00:00', '2026-09-28 18:00:00'),
(2, 6, 'MTR-2026-8802', 'Smart Digital', 'Three Phase', 0.0, 680.0, 'Central Substation 33/11kV', 'Feeder-11kV-CommercialZone', 'Active', '2026-09-26 15:30:00', '2026-09-26 15:30:00', '2026-09-29 12:00:00');

-- 5. Insert Grievances
INSERT INTO grievances (id, grievance_number, consumer_id, meter_id, category, priority, description, status, assigned_lineman, resolution_notes, resolved_at, created_at, updated_at)
VALUES
(1, 'GRV-2026-5001', 1, 1, 'Voltage Fluctuation', 'Medium', 'Experiencing frequent voltage drop down to 180V during evening peak hours.', 'In_Progress', 'Lineman Suresh Kumar (Crew 4)', 'Checked phase balance at distribution pillar box. Re-crimping feeder terminal.', NULL, '2026-09-27 19:40:00', '2026-09-28 10:15:00'),
(2, 'GRV-2026-5002', 6, 2, 'Billing Inquiry', 'Low', 'Need confirmation of dynamic peak-hour tariff applicability for commercial cafe.', 'Resolved', 'Officer Ananya Gupta', 'Commercial LT-2 tariff slab schedule provided to consumer via email.', '2026-09-28 16:30:00', '2026-09-27 11:20:00', '2026-09-28 16:30:00'),
(3, 'GRV-2026-5003', 5, NULL, 'Hazardous Sparking', 'Critical', 'Service drop wire near building terrace sparking during rain breeze.', 'Assigned', 'Lineman Devendra J (Emergency Crew)', 'Dispatched safety crew with bucket vehicle.', NULL, '2026-09-29 18:10:00', '2026-09-29 18:25:00');

-- 6. Insert Audit Logs
INSERT INTO audit_logs (id, application_id, action, performed_by, old_status, new_status, notes, timestamp)
VALUES
(1, 1, 'APPLICATION_SUBMITTED', 'Aarav Sharma (Consumer)', NULL, 'Submitted', 'Application registered via web portal.', '2026-09-10 09:35:00'),
(2, 1, 'DOCUMENT_VERIFICATION', 'Officer S. Verma', 'Submitted', 'Document_Verified', 'Identity and property tax receipt verified.', '2026-09-11 11:00:00'),
(3, 1, 'INSPECTION_SCHEDULED', 'System Dispatcher', 'Document_Verified', 'Field_Inspection_Scheduled', 'Assigned Er. Ramesh Kulkarni for inspection.', '2026-09-11 14:00:00'),
(4, 1, 'INSPECTION_COMPLETED', 'Er. Ramesh Kulkarni', 'Field_Inspection_Scheduled', 'Inspection_Approved', 'Site is feasible. Within 20m from pole.', '2026-09-13 11:30:00'),
(5, 1, 'PAYMENT_RECEIVED', 'Payment Gateway (Auto)', 'Inspection_Approved', 'Payment_Pending', 'Demand note payment of INR 4200 settled.', '2026-09-15 16:20:00'),
(6, 1, 'METER_ALLOCATED', 'Supt. Engineer P. Rao', 'Payment_Pending', 'Meter_Assigned_Active', 'Smart Meter MTR-2026-8801 energized.', '2026-09-16 14:30:00'),
(7, 2, 'INSPECTION_COMPLETED', 'Er. Swati Naik', 'Field_Inspection_Scheduled', 'Inspection_Approved', 'Three-phase commercial line approved.', '2026-09-16 12:45:00'),
(8, 2, 'DEMAND_NOTE_ISSUED', 'Officer S. Verma', 'Inspection_Approved', 'Payment_Pending', 'Demand note INR 32,500 issued to ApexTech.', '2026-09-18 10:00:00'),
(9, 8, 'INSPECTION_REJECTED', 'Er. Nilesh Shinde', 'Field_Inspection_Scheduled', 'Rejected', 'Transformer saturation prevented load grant.', '2026-09-27 16:00:00');
