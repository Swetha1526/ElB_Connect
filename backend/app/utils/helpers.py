# backend/app/utils/helpers.py
import random
from datetime import datetime, timezone

def calculate_quotation(category: str, requested_load_kw: float, phase: str) -> float:
    """
    Calculate electricity connection quotation charges based on DISCOM tariff schedule:
    - Security Deposit per kW
    - Service Line & Connection Charges
    - Meter and Processing Charges
    """
    load = max(0.5, float(requested_load_kw))
    category_lower = category.strip().lower()

    if "domestic" in category_lower:
        deposit_per_kw = 600.0
        base_service_fee = 1200.0
        phase_multiplier = 1.0 if "single" in phase.lower() else 1.8
        meter_charge = 1500.0
    elif "commercial" in category_lower:
        deposit_per_kw = 1200.0
        base_service_fee = 2500.0
        phase_multiplier = 1.0 if "single" in phase.lower() else 1.7
        meter_charge = 3000.0
    elif "industrial" in category_lower:
        deposit_per_kw = 2500.0
        base_service_fee = 8000.0
        phase_multiplier = 2.5
        meter_charge = 7500.0
    elif "agri" in category_lower:
        deposit_per_kw = 200.0
        base_service_fee = 800.0
        phase_multiplier = 1.0 if "single" in phase.lower() else 1.2
        meter_charge = 1000.0
    else:
        deposit_per_kw = 800.0
        base_service_fee = 1500.0
        phase_multiplier = 1.2
        meter_charge = 2000.0

    security_deposit = load * deposit_per_kw
    connection_charge = base_service_fee * phase_multiplier
    total = security_deposit + connection_charge + meter_charge
    return round(total, 2)

def generate_application_number() -> str:
    """Generate a unique tracking application ID, e.g., APP-2026-4821"""
    year = datetime.now(timezone.utc).year
    rand_suffix = random.randint(1000, 9999)
    return f"APP-{year}-{rand_suffix}"

def generate_meter_serial() -> str:
    """Generate a unique smart meter serial number, e.g., MTR-2026-7241"""
    year = datetime.now(timezone.utc).year
    rand_suffix = random.randint(1000, 9999)
    return f"MTR-{year}-{rand_suffix}"

def generate_grievance_number() -> str:
    """Generate a unique grievance ticket number, e.g., GRV-2026-3109"""
    year = datetime.now(timezone.utc).year
    rand_suffix = random.randint(1000, 9999)
    return f"GRV-{year}-{rand_suffix}"
