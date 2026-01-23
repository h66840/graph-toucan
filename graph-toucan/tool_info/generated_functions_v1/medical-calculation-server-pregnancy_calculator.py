from typing import Dict, Any, Optional
from datetime import datetime, timedelta

def medical_calculation_server_pregnancy_calculator(
    calculation_method: str,
    date_value: str,
    cycle_length: Optional[int] = 28,
    gestational_age_weeks: Optional[int] = None,
    gestational_age_days: Optional[int] = None
) -> Dict[str, Any]:
    """
    Pregnancy Due Dates Calculator
    Calculates pregnancy dates from last period, gestational age, or date of conception.

    Parameters:
    -----------
    calculation_method : str
        Method used for calculation: "lmp" (last menstrual period), "conception", or "ultrasound"
    date_value : str
        Date in format 'YYYY-MM-DD' (date of LMP, conception, or ultrasound)
    cycle_length : int, optional
        Length of menstrual cycle in days (default: 28)
    gestational_age_weeks : int, optional
        Weeks of gestational age at ultrasound (required if calculation_method is "ultrasound")
    gestational_age_days : int, optional
        Days of gestational age at ultrasound (required if calculation_method is "ultrasound")

    Returns:
    --------
    dict
        Dictionary containing calculated pregnancy dates and information including:
        - lmp_date: first day of the last menstrual period
        - conception_date: estimated date of conception
        - due_date: estimated due date (EDD)
        - current_gestational_age: current gestational age in 'XwYd' format
        - current_trimester: current trimester of pregnancy
        - cycle_length_used: menstrual cycle length used for calculation
        - calculation_method: method used for calculation
    """
    # Input validation
    if not calculation_method:
        raise ValueError("calculation_method is required")
    if calculation_method not in ["lmp", "conception", "ultrasound"]:
        raise ValueError("calculation_method must be 'lmp', 'conception', or 'ultrasound'")
    if not date_value:
        raise ValueError("date_value is required")
    if calculation_method == "ultrasound" and (gestational_age_weeks is None or gestational_age_days is None):
        raise ValueError("gestational_age_weeks and gestational_age_days are required for ultrasound method")
    
    try:
        input_date = datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("date_value must be in 'YYYY-MM-DD' format")
    
    # Set default cycle length if not provided
    cycle_length_used = cycle_length or 28
    
    # Initialize variables
    lmp_date = None
    conception_date = None
    due_date = None
    
    # Calculate based on method
    if calculation_method == "lmp":
        lmp_date = input_date
        # Adjust conception date based on cycle length
        ovulation_days = 14 + (cycle_length_used - 28)
        conception_date = lmp_date + timedelta(days=ovulation_days)
        # EDD = LMP + 40 weeks + adjustment for cycle length
        due_date = lmp_date + timedelta(weeks=40) + timedelta(days=(cycle_length_used - 28))
        
    elif calculation_method == "conception":
        conception_date = input_date
        # Estimate LMP: conception typically occurs ~14 days after LMP (adjusted for cycle length)
        ovulation_days = 14 + (cycle_length_used - 28)
        lmp_date = conception_date - timedelta(days=ovulation_days)
        due_date = lmp_date + timedelta(weeks=40) + timedelta(days=(cycle_length_used - 28))
        
    elif calculation_method == "ultrasound":
        ultrasound_date = input_date
        # Total days from LMP to ultrasound
        total_gestational_days = (gestational_age_weeks * 7) + gestational_age_days
        # LMP is retroactively calculated
        lmp_date = ultrasound_date - timedelta(days=total_gestational_days)
        ovulation_days = 14 + (cycle_length_used - 28)
        conception_date = lmp_date + timedelta(days=ovulation_days)
        due_date = lmp_date + timedelta(weeks=40) + timedelta(days=(cycle_length_used - 28))
    
    # Calculate current gestational age
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if lmp_date:
        days_since_lmp = (today - lmp_date).days
        if days_since_lmp < 0:
            weeks = 0
            days = 0
        else:
            weeks = days_since_lmp // 7
            days = days_since_lmp % 7
        current_gestational_age = f"{weeks}w{days}d"
        
        # Determine trimester
        if weeks < 13:
            current_trimester = "First trimester"
        elif weeks < 27:
            current_trimester = "Second trimester"
        else:
            current_trimester = "Third trimester"
    else:
        current_gestational_age = "0w0d"
        current_trimester = "First trimester"
    
    # Format dates back to string
    lmp_date_str = lmp_date.strftime("%Y-%m-%d") if lmp_date else None
    conception_date_str = conception_date.strftime("%Y-%m-%d") if conception_date else None
    due_date_str = due_date.strftime("%Y-%m-%d") if due_date else None
    
    return {
        "lmp_date": lmp_date_str,
        "conception_date": conception_date_str,
        "due_date": due_date_str,
        "current_gestational_age": current_gestational_age,
        "current_trimester": current_trimester,
        "cycle_length_used": cycle_length_used,
        "calculation_method": calculation_method
    }