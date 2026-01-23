from typing import Dict, Any

def medical_calculation_server_child_pugh_score(
    albumin: float,
    ascites: str,
    bilirubin: float,
    encephalopathy_grade: int,
    inr: float
) -> Dict[str, Any]:
    """
    Calculates the Child-Pugh Score for cirrhosis mortality assessment.

    Parameters:
    -----------
    bilirubin : float
        Total bilirubin in mg/dL.
    albumin : float
        Albumin in g/dL.
    inr : float
        International Normalized Ratio (INR) for prothrombin time.
    ascites : str
        One of: "absent", "slight", "moderate".
    encephalopathy_grade : int
        Hepatic encephalopathy grade: 0 (none), 1-2 (mild), 3-4 (severe).

    Returns:
    --------
    Dict with the following keys:
        - score (int): Total Child-Pugh score (5–15).
        - class (str): Child-Pugh class (A, B, or C).
        - components (Dict): Breakdown of individual component scores.
        - interpretation (str): Clinical interpretation of the score and class.
        - mortality_risk_1_year (str): Estimated one-year survival probability.
    """
    # Validate inputs
    if not isinstance(albumin, (float, int)):
        raise ValueError("Albumin must be a number.")
    if ascites not in ["absent", "slight", "moderate"]:
        raise ValueError("Ascites must be one of: 'absent', 'slight', 'moderate'.")
    if not isinstance(bilirubin, (float, int)) or bilirubin < 0:
        raise ValueError("Bilirubin must be a non-negative number.")
    if not isinstance(encephalopathy_grade, int) or encephalopathy_grade < 0 or encephalopathy_grade > 4:
        raise ValueError("Encephalopathy grade must be an integer between 0 and 4.")
    if not isinstance(inr, (float, int)) or inr < 0:
        raise ValueError("INR must be a non-negative number.")

    # Helper function to assign points based on thresholds
    def get_bilirubin_points(bilirubin: float) -> int:
        if bilirubin < 2.0:
            return 1
        elif bilirubin <= 3.0:
            return 2
        else:
            return 3

    def get_albumin_points(albumin: float) -> int:
        if albumin >= 3.5:
            return 1
        elif albumin >= 2.8:
            return 2
        else:
            return 3

    def get_inr_points(inr: float) -> int:
        if inr < 1.7:
            return 1
        elif inr <= 2.3:
            return 2
        else:
            return 3

    def get_ascites_points(ascites: str) -> int:
        if ascites == "absent":
            return 1
        elif ascites == "slight":
            return 2
        else:  # moderate
            return 3

    def get_encephalopathy_points(grade: int) -> int:
        if grade == 0:
            return 1
        elif grade in [1, 2]:
            return 2
        else:  # 3 or 4
            return 3

    # Calculate individual component points
    bilirubin_points = get_bilirubin_points(bilirubin)
    albumin_points = get_albumin_points(albumin)
    inr_points = get_inr_points(inr)
    ascites_points = get_ascites_points(ascites)
    encephalopathy_points = get_encephalopathy_points(encephalopathy_grade)

    # Total score
    total_score = (
        bilirubin_points +
        albumin_points +
        inr_points +
        ascites_points +
        encephalopathy_points
    )

    # Determine Child-Pugh class
    if total_score <= 6:
        child_pugh_class = "A"
        interpretation = "Mild liver dysfunction"
        mortality_risk = "Excellent (>80%)"
    elif total_score <= 9:
        child_pugh_class = "B"
        interpretation = "Moderate liver dysfunction"
        mortality_risk = "Good (60-80%)"
    else:
        child_pugh_class = "C"
        interpretation = "Severe cirrhosis with high mortality risk"
        mortality_risk = "Poor (<45%)"

    # Component breakdown
    components = {
        "bilirubin": {
            "points": bilirubin_points,
            "interpretation": f"Bilirubin = {bilirubin} mg/dL"
        },
        "albumin": {
            "points": albumin_points,
            "interpretation": f"Albumin = {albumin} g/dL"
        },
        "inr": {
            "points": inr_points,
            "interpretation": f"INR = {inr}"
        },
        "ascites": {
            "points": ascites_points,
            "interpretation": f"Ascites = {ascites}"
        },
        "encephalopathy": {
            "points": encephalopathy_points,
            "interpretation": f"Encephalopathy grade = {encephalopathy_grade}"
        }
    }

    return {
        "score": total_score,
        "class": child_pugh_class,
        "components": components,
        "interpretation": interpretation,
        "mortality_risk_1_year": mortality_risk
    }