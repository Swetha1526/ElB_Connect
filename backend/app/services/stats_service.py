# backend/app/services/stats_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from backend.app.models.application import Application
from backend.app.models.meter import Meter
from backend.app.models.grievance import Grievance
from backend.app.models.audit_log import AuditLog
from backend.app.schemas.stats import DashboardStatsResponse, CategoryCount, StatusCount, SubstationStat

class StatsService:
    @staticmethod
    def get_dashboard_stats(db: Session) -> DashboardStatsResponse:
        # Total counts
        total_apps = db.query(func.count(Application.id)).scalar() or 0
        
        pending_verifications = db.query(func.count(Application.id)).filter(
            Application.status == "Submitted"
        ).scalar() or 0

        pending_inspections = db.query(func.count(Application.id)).filter(
            Application.status == "Field_Inspection_Scheduled"
        ).scalar() or 0

        pending_payments = db.query(func.count(Application.id)).filter(
            Application.status == "Payment_Pending"
        ).scalar() or 0

        active_meters = db.query(func.count(Meter.id)).filter(
            Meter.status == "Active"
        ).scalar() or 0

        sanctioned_load_kw = db.query(func.sum(Application.sanctioned_load_kw)).filter(
            Application.status == "Meter_Assigned_Active"
        ).scalar() or 0.0

        estimated_revenue = db.query(func.sum(Application.quotation_amount)).filter(
            Application.payment_status == "Paid"
        ).scalar() or 0.0

        total_grievances = db.query(func.count(Grievance.id)).scalar() or 0
        active_grievances = db.query(func.count(Grievance.id)).filter(
            Grievance.status.in_(["Registered", "Assigned", "In_Progress"])
        ).scalar() or 0
        resolved_grievances = db.query(func.count(Grievance.id)).filter(
            Grievance.status.in_(["Resolved", "Closed"])
        ).scalar() or 0

        # Status distribution
        status_rows = db.query(
            Application.status,
            func.count(Application.id)
        ).group_by(Application.status).all()
        status_distribution = [StatusCount(status=s, count=c) for s, c in status_rows]

        # Category distribution
        category_rows = db.query(
            Application.category,
            func.count(Application.id),
            func.coalesce(func.sum(Application.requested_load_kw), 0.0)
        ).group_by(Application.category).all()
        category_distribution = [
            CategoryCount(category=cat, count=c, total_load_kw=round(float(ld), 2))
            for cat, c, ld in category_rows
        ]

        # Substation metrics
        substation_rows = db.query(
            Application.substation_name,
            func.count(Application.id),
            func.coalesce(func.sum(case((Application.status == "Meter_Assigned_Active", 1), else_=0)), 0),
            func.coalesce(func.sum(Application.requested_load_kw), 0.0)
        ).group_by(Application.substation_name).all()
        substation_metrics = [
            SubstationStat(
                substation_name=sub,
                total_applications=cnt,
                active_meters=int(mtr),
                total_load_kw=round(float(ld), 2)
            )
            for sub, cnt, mtr, ld in substation_rows
        ]

        # Recent activity audit logs
        recent_logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(10).all()
        recent_activity = [
            {
                "id": log.id,
                "application_id": log.application_id,
                "action": log.action,
                "performed_by": log.performed_by,
                "old_status": log.old_status,
                "new_status": log.new_status,
                "notes": log.notes,
                "timestamp": log.timestamp.isoformat()
            }
            for log in recent_logs
        ]

        return DashboardStatsResponse(
            total_applications=total_apps,
            pending_verifications=pending_verifications,
            pending_inspections=pending_inspections,
            pending_payments=pending_payments,
            active_meters=active_meters,
            total_sanctioned_load_kw=round(float(sanctioned_load_kw), 2),
            total_sanctioned_load_mw=round(float(sanctioned_load_kw) / 1000.0, 3),
            total_grievances=total_grievances,
            active_grievances=active_grievances,
            resolved_grievances=resolved_grievances,
            estimated_revenue_inr=round(float(estimated_revenue), 2),
            status_distribution=status_distribution,
            category_distribution=category_distribution,
            substation_metrics=substation_metrics,
            recent_activity=recent_activity
        )
