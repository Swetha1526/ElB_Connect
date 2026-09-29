# backend/app/database/seed_data.py
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure root directory is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from backend.app.database.connection import SessionLocal, init_db
from backend.app.models.consumer import Consumer
from backend.app.models.application import Application
from backend.app.models.inspection import Inspection
from backend.app.models.meter import Meter
from backend.app.models.grievance import Grievance
from backend.app.models.audit_log import AuditLog

def seed_database(force: bool = False):
    """Seed the database with initial realistic records if empty or forced."""
    init_db()
    db = SessionLocal()
    try:
        existing_apps = db.query(Application).count()
        if existing_apps > 0 and not force:
            print(f"[SEED] Database already contains {existing_apps} applications. Skipping seed.")
            return

        if force:
            print("[SEED] Purging existing database records...")
            db.query(AuditLog).delete()
            db.query(Grievance).delete()
            db.query(Meter).delete()
            db.query(Inspection).delete()
            db.query(Application).delete()
            db.query(Consumer).delete()
            db.commit()

        print("[SEED] Inserting realistic electricity board seed data...")

        # 1. Consumers
        now = datetime.now(timezone.utc)
        consumers = [
            Consumer(
                id=1,
                full_name="Aarav Sharma",
                email="aarav.sharma@example.com",
                phone="9876543210",
                national_id="AADHAAR-8912-3401",
                address="Flat 402, Green Valley Apts, Sector 14",
                city="Metro City",
                pincode="110001",
                consumer_category="Domestic",
                created_at=now - timedelta(days=20),
                updated_at=now - timedelta(days=20)
            ),
            Consumer(
                id=2,
                full_name="Priya Patel",
                email="priya.patel@apextech.in",
                phone="9845123456",
                national_id="AADHAAR-4412-9902",
                address="Plot 18, Electronic City Phase 1",
                city="Metro City",
                pincode="560100",
                consumer_category="Commercial",
                created_at=now - timedelta(days=18),
                updated_at=now - timedelta(days=18)
            ),
            Consumer(
                id=3,
                full_name="Rajeshwer Rao",
                email="rajesh.rao@agrofarm.org",
                phone="9440112233",
                national_id="AADHAAR-7711-2299",
                address="Survey No 84, Village Ramanagara",
                city="Ramanagara",
                pincode="562159",
                consumer_category="Agricultural",
                created_at=now - timedelta(days=16),
                updated_at=now - timedelta(days=16)
            ),
            Consumer(
                id=4,
                full_name="Vikramaditya Mills Ltd",
                email="accounts@vikrammills.com",
                phone="9820334455",
                national_id="PAN-AAACV1234K",
                address="Industrial Area, Phase 3, GIDC",
                city="Metro City",
                pincode="390001",
                consumer_category="Industrial",
                created_at=now - timedelta(days=15),
                updated_at=now - timedelta(days=15)
            ),
            Consumer(
                id=5,
                full_name="Sneha Mukherjee",
                email="sneha.m@outlook.com",
                phone="9734567890",
                national_id="AADHAAR-6512-8821",
                address="12B Lake View Road, Salt Lake Sector 3",
                city="Metro City",
                pincode="700091",
                consumer_category="Domestic",
                created_at=now - timedelta(days=12),
                updated_at=now - timedelta(days=12)
            ),
            Consumer(
                id=6,
                full_name="Karthik Raman",
                email="karthik.raman@bakerycafe.com",
                phone="9962012345",
                national_id="AADHAAR-9012-3341",
                address="88 Cathedral Road, Gopalapuram",
                city="Metro City",
                pincode="600086",
                consumer_category="Commercial",
                created_at=now - timedelta(days=10),
                updated_at=now - timedelta(days=10)
            ),
            Consumer(
                id=7,
                full_name="Sunita Deshmukh",
                email="sunita.deshmukh@gmail.com",
                phone="9822098765",
                national_id="AADHAAR-3114-5567",
                address="Row House 5, Sunshine Meadows, Baner",
                city="Metro City",
                pincode="411045",
                consumer_category="Domestic",
                created_at=now - timedelta(days=8),
                updated_at=now - timedelta(days=8)
            ),
            Consumer(
                id=8,
                full_name="Global Logistics Hub",
                email="ops@globallogistics.com",
                phone="9811223344",
                national_id="PAN-AABCG9876P",
                address="Warehouse Zone 4, Bypass Highway",
                city="Metro City",
                pincode="122001",
                consumer_category="Commercial",
                created_at=now - timedelta(days=5),
                updated_at=now - timedelta(days=5)
            )
        ]
        db.add_all(consumers)
        db.flush()

        # 2. Applications
        apps = [
            Application(
                id=1,
                application_number="APP-2026-1001",
                consumer_id=1,
                connection_type="New Connection",
                category="Domestic",
                requested_load_kw=5.0,
                phase="Single Phase",
                premises_type="Owned",
                substation_name="Central Substation 33/11kV",
                status="Meter_Assigned_Active",
                sanctioned_load_kw=5.0,
                quotation_amount=4200.0,
                payment_status="Paid",
                remarks="Meter successfully commissioned and activated.",
                created_at=now - timedelta(days=20),
                updated_at=now - timedelta(days=14)
            ),
            Application(
                id=2,
                application_number="APP-2026-1002",
                consumer_id=2,
                connection_type="New Connection",
                category="Commercial",
                requested_load_kw=25.0,
                phase="Three Phase",
                premises_type="Rented",
                substation_name="Tech Park Substation 66/11kV",
                status="Payment_Pending",
                sanctioned_load_kw=25.0,
                quotation_amount=32500.0,
                payment_status="Pending",
                remarks="Site inspection approved. Demand note issued to consumer.",
                created_at=now - timedelta(days=18),
                updated_at=now - timedelta(days=12)
            ),
            Application(
                id=3,
                application_number="APP-2026-1003",
                consumer_id=3,
                connection_type="New Connection",
                category="Agricultural",
                requested_load_kw=7.5,
                phase="Three Phase",
                premises_type="Owned",
                substation_name="Rural Feeder Substation 33/11kV",
                status="Field_Inspection_Scheduled",
                sanctioned_load_kw=None,
                quotation_amount=2300.0,
                payment_status="Pending",
                remarks="Junior Engineer assigned for agricultural pump feasibility.",
                created_at=now - timedelta(days=16),
                updated_at=now - timedelta(days=13)
            ),
            Application(
                id=4,
                application_number="APP-2026-1004",
                consumer_id=4,
                connection_type="Load Enhancement",
                category="Industrial",
                requested_load_kw=150.0,
                phase="Three Phase",
                premises_type="Owned",
                substation_name="Industrial Substation 110/33kV",
                status="Document_Verified",
                sanctioned_load_kw=None,
                quotation_amount=383000.0,
                payment_status="Pending",
                remarks="Factory load enhancement request submitted with load audit.",
                created_at=now - timedelta(days=15),
                updated_at=now - timedelta(days=14)
            ),
            Application(
                id=5,
                application_number="APP-2026-1005",
                consumer_id=5,
                connection_type="New Connection",
                category="Domestic",
                requested_load_kw=3.0,
                phase="Single Phase",
                premises_type="Owned",
                substation_name="East Substation 33/11kV",
                status="Submitted",
                sanctioned_load_kw=None,
                quotation_amount=3000.0,
                payment_status="Pending",
                remarks="Fresh application submitted by consumer online.",
                created_at=now - timedelta(days=12),
                updated_at=now - timedelta(days=12)
            ),
            Application(
                id=6,
                application_number="APP-2026-1006",
                consumer_id=6,
                connection_type="New Connection",
                category="Commercial",
                requested_load_kw=12.0,
                phase="Three Phase",
                premises_type="Rented",
                substation_name="Central Substation 33/11kV",
                status="Meter_Assigned_Active",
                sanctioned_load_kw=12.0,
                quotation_amount=16900.0,
                payment_status="Paid",
                remarks="Commercial digital meter commissioned for Cafe.",
                created_at=now - timedelta(days=10),
                updated_at=now - timedelta(days=4)
            ),
            Application(
                id=7,
                application_number="APP-2026-1007",
                consumer_id=7,
                connection_type="Tariff Change",
                category="Domestic",
                requested_load_kw=6.0,
                phase="Single Phase",
                premises_type="Owned",
                substation_name="West Substation 33/11kV",
                status="Inspection_Approved",
                sanctioned_load_kw=6.0,
                quotation_amount=4800.0,
                payment_status="Pending",
                remarks="Feasibility approved. Security deposit payment pending.",
                created_at=now - timedelta(days=8),
                updated_at=now - timedelta(days=5)
            ),
            Application(
                id=8,
                application_number="APP-2026-1008",
                consumer_id=8,
                connection_type="New Connection",
                category="Commercial",
                requested_load_kw=50.0,
                phase="Three Phase",
                premises_type="Owned",
                substation_name="North Substation 66/11kV",
                status="Rejected",
                sanctioned_load_kw=None,
                quotation_amount=62500.0,
                payment_status="Pending",
                remarks="Rejected due to insufficient transformer margin without dedicated substation.",
                created_at=now - timedelta(days=5),
                updated_at=now - timedelta(days=2)
            )
        ]
        db.add_all(apps)
        db.flush()

        # 3. Field Inspections
        inspections = [
            Inspection(
                id=1,
                application_id=1,
                inspector_name="Er. Ramesh Kulkarni (JE-South)",
                feasibility_status="Feasible",
                pole_distance_meters=18.5,
                transformer_id="TR-CENTRAL-04",
                transformer_capacity_kva=250.0,
                meter_box_ready=True,
                remarks="Site clear. Distribution pole within 20m. Transformer capacity adequate.",
                scheduled_date=now - timedelta(days=17),
                completed_at=now - timedelta(days=17),
                created_at=now - timedelta(days=19)
            ),
            Inspection(
                id=2,
                application_id=2,
                inspector_name="Er. Swati Naik (JE-TechPark)",
                feasibility_status="Feasible",
                pole_distance_meters=22.0,
                transformer_id="TR-TECHPARK-12",
                transformer_capacity_kva=500.0,
                meter_box_ready=True,
                remarks="Three-phase commercial line extension feasible. Adequate headroom on busbar.",
                scheduled_date=now - timedelta(days=14),
                completed_at=now - timedelta(days=14),
                created_at=now - timedelta(days=16)
            ),
            Inspection(
                id=3,
                application_id=3,
                inspector_name="Er. Mahendra Gowda (JE-Rural)",
                feasibility_status="Feasible",
                pole_distance_meters=45.0,
                transformer_id="TR-RURAL-08",
                transformer_capacity_kva=100.0,
                meter_box_ready=True,
                remarks="Scheduled inspection for agricultural pump-set energization.",
                scheduled_date=now + timedelta(days=1),
                completed_at=None,
                created_at=now - timedelta(days=13)
            ),
            Inspection(
                id=4,
                application_id=6,
                inspector_name="Er. Ramesh Kulkarni (JE-South)",
                feasibility_status="Feasible",
                pole_distance_meters=12.0,
                transformer_id="TR-CENTRAL-02",
                transformer_capacity_kva=315.0,
                meter_box_ready=True,
                remarks="Commercial line verified. CT-operated meter installation approved.",
                scheduled_date=now - timedelta(days=8),
                completed_at=now - timedelta(days=8),
                created_at=now - timedelta(days=9)
            ),
            Inspection(
                id=5,
                application_id=7,
                inspector_name="Er. Amitav Sen (JE-West)",
                feasibility_status="Feasible",
                pole_distance_meters=15.0,
                transformer_id="TR-WEST-09",
                transformer_capacity_kva=200.0,
                meter_box_ready=True,
                remarks="Domestic load upgrade from 3kW to 6kW feasible on existing service drop.",
                scheduled_date=now - timedelta(days=6),
                completed_at=now - timedelta(days=6),
                created_at=now - timedelta(days=7)
            ),
            Inspection(
                id=6,
                application_id=8,
                inspector_name="Er. Nilesh Shinde (JE-North)",
                feasibility_status="Non_Feasible",
                pole_distance_meters=120.0,
                transformer_id="TR-NORTH-15",
                transformer_capacity_kva=100.0,
                meter_box_ready=False,
                remarks="Transformer capacity saturated (94% loading). Dedicated HT transformer required.",
                scheduled_date=now - timedelta(days=3),
                completed_at=now - timedelta(days=2),
                created_at=now - timedelta(days=4)
            )
        ]
        db.add_all(inspections)
        db.flush()

        # 4. Meters
        meters = [
            Meter(
                id=1,
                application_id=1,
                meter_serial_number="MTR-2026-8801",
                meter_type="Smart Digital",
                phase="Single Phase",
                initial_reading_kwh=0.0,
                current_reading_kwh=142.5,
                substation_name="Central Substation 33/11kV",
                feeder_line="Feeder-11kV-SouthCity",
                status="Active",
                installation_date=now - timedelta(days=14),
                created_at=now - timedelta(days=14),
                updated_at=now - timedelta(days=1)
            ),
            Meter(
                id=2,
                application_id=6,
                meter_serial_number="MTR-2026-8802",
                meter_type="Smart Digital",
                phase="Three Phase",
                initial_reading_kwh=0.0,
                current_reading_kwh=680.0,
                substation_name="Central Substation 33/11kV",
                feeder_line="Feeder-11kV-CommercialZone",
                status="Active",
                installation_date=now - timedelta(days=4),
                created_at=now - timedelta(days=4),
                updated_at=now
            )
        ]
        db.add_all(meters)
        db.flush()

        # 5. Grievances
        grievances = [
            Grievance(
                id=1,
                grievance_number="GRV-2026-5001",
                consumer_id=1,
                meter_id=1,
                category="Voltage Fluctuation",
                priority="Medium",
                description="Experiencing frequent voltage drop down to 180V during evening peak hours.",
                status="In_Progress",
                assigned_lineman="Lineman Suresh Kumar (Crew 4)",
                resolution_notes="Checked phase balance at distribution pillar box. Re-crimping feeder terminal.",
                resolved_at=None,
                created_at=now - timedelta(days=3),
                updated_at=now - timedelta(days=1)
            ),
            Grievance(
                id=2,
                grievance_number="GRV-2026-5002",
                consumer_id=6,
                meter_id=2,
                category="Billing Inquiry",
                priority="Low",
                description="Need confirmation of dynamic peak-hour tariff applicability for commercial cafe.",
                status="Resolved",
                assigned_lineman="Officer Ananya Gupta",
                resolution_notes="Commercial LT-2 tariff slab schedule provided to consumer via email.",
                resolved_at=now - timedelta(days=1),
                created_at=now - timedelta(days=2),
                updated_at=now - timedelta(days=1)
            ),
            Grievance(
                id=3,
                grievance_number="GRV-2026-5003",
                consumer_id=5,
                meter_id=None,
                category="Hazardous Sparking",
                priority="Critical",
                description="Service drop wire near building terrace sparking during rain breeze.",
                status="Assigned",
                assigned_lineman="Lineman Devendra J (Emergency Crew)",
                resolution_notes="Dispatched safety crew with bucket vehicle.",
                resolved_at=None,
                created_at=now - timedelta(hours=4),
                updated_at=now - timedelta(hours=3)
            )
        ]
        db.add_all(grievances)
        db.flush()

        # 6. Audit Logs
        audit_logs = [
            AuditLog(
                application_id=1,
                action="APPLICATION_SUBMITTED",
                performed_by="Aarav Sharma (Consumer)",
                old_status=None,
                new_status="Submitted",
                notes="Application registered via web portal.",
                timestamp=now - timedelta(days=20)
            ),
            AuditLog(
                application_id=1,
                action="DOCUMENT_VERIFICATION",
                performed_by="Officer S. Verma",
                old_status="Submitted",
                new_status="Document_Verified",
                notes="Identity and property tax receipt verified.",
                timestamp=now - timedelta(days=19)
            ),
            AuditLog(
                application_id=1,
                action="INSPECTION_SCHEDULED",
                performed_by="System Dispatcher",
                old_status="Document_Verified",
                new_status="Field_Inspection_Scheduled",
                notes="Assigned Er. Ramesh Kulkarni for inspection.",
                timestamp=now - timedelta(days=19)
            ),
            AuditLog(
                application_id=1,
                action="INSPECTION_COMPLETED",
                performed_by="Er. Ramesh Kulkarni",
                old_status="Field_Inspection_Scheduled",
                new_status="Inspection_Approved",
                notes="Site is feasible. Within 20m from pole.",
                timestamp=now - timedelta(days=17)
            ),
            AuditLog(
                application_id=1,
                action="PAYMENT_RECEIVED",
                performed_by="Payment Gateway (Auto)",
                old_status="Inspection_Approved",
                new_status="Payment_Pending",
                notes="Demand note payment of INR 4,200 settled.",
                timestamp=now - timedelta(days=15)
            ),
            AuditLog(
                application_id=1,
                action="METER_ALLOCATED",
                performed_by="Supt. Engineer P. Rao",
                old_status="Payment_Pending",
                new_status="Meter_Assigned_Active",
                notes="Smart Meter MTR-2026-8801 energized.",
                timestamp=now - timedelta(days=14)
            ),
            AuditLog(
                application_id=2,
                action="INSPECTION_COMPLETED",
                performed_by="Er. Swati Naik",
                old_status="Field_Inspection_Scheduled",
                new_status="Inspection_Approved",
                notes="Three-phase commercial line approved.",
                timestamp=now - timedelta(days=14)
            ),
            AuditLog(
                application_id=2,
                action="DEMAND_NOTE_ISSUED",
                performed_by="Officer S. Verma",
                old_status="Inspection_Approved",
                new_status="Payment_Pending",
                notes="Demand note INR 32,500 issued to ApexTech.",
                timestamp=now - timedelta(days=12)
            ),
            AuditLog(
                application_id=8,
                action="INSPECTION_REJECTED",
                performed_by="Er. Nilesh Shinde",
                old_status="Field_Inspection_Scheduled",
                new_status="Rejected",
                notes="Transformer saturation prevented load grant.",
                timestamp=now - timedelta(days=2)
            )
        ]
        db.add_all(audit_logs)
        db.commit()
        print(f"[SEED] Successfully seeded database with {len(apps)} applications, {len(consumers)} consumers, {len(inspections)} inspections, {len(meters)} meters, and {len(grievances)} grievances.")

    except Exception as e:
        db.rollback()
        print(f"[SEED ERROR] Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    force_seed = "--force" in sys.argv
    seed_database(force=force_seed)
