from typing import Dict, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for pediatric blood pressure percentile calculation.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - systolic_percentile (float): Systolic blood pressure percentile
        - diastolic_percentile (float): Diastolic blood pressure percentile
        - classification (str): Blood pressure classification category
        - percentile_category_systolic (str): Systolic percentile range category
        - percentile_category_diastolic (str): Diastolic percentile range category
        - reference_population_source (str): Source of reference population data
        - reference_population_age_months (int): Age in months used in reference
        - reference_population_height_zscore (float): Height z-score from reference population
        - is_abnormal (bool): Whether blood pressure is above normal range
    """
    # Simulated realistic response based on input parameters (not actually used in computation)
    return {
        "systolic_percentile": 75.5,
        "diastolic_percentile": 68.3,
        "classification": "정상",
        "percentile_category_systolic": "90th-95th percentile",
        "percentile_category_diastolic": "<90th percentile",
        "reference_population_source": "CDC 2000",
        "reference_population_age_months": 72,
        "reference_population_height_zscore": 0.5,
        "is_abnormal": False
    }

def medical_calculation_server_bp_children(
    years: int,
    months: int,
    height: int,
    sex: str,
    systolic: int,
    diastolic: int
) -> Dict[str, Any]:
    """
    혈압 센타일(percentile)을 계산하는 함수
    
    Parameters:
    -----------
    years : int
        나이(년)
    months : int
        나이(월)
    height : int
        키(cm)
    sex : str
        성별 ('male' 또는 'female')
    systolic : int
        수축기 혈압(mmHg)
    diastolic : int
        이완기 혈압(mmHg)
    
    Returns:
    --------
    dict
        수축기 및 이완기 혈압 센타일 결과를 포함하는 딕셔너리
        - systolic_percentile (float): 수축기 혈압의 성별 및 나이-신장 기준 센타일
        - diastolic_percentile (float): 이완기 혈압의 성별 및 나이-신장 기준 센타일
        - classification (str): 혈압 등급 분류
        - percentile_category (Dict): 수축기 및 이완기 혈압에 대한 임상적 분류 정보
        - reference_population (Dict): 참조된 표준 성장도 데이터 및 인구 기준 정보
        - is_abnormal (bool): 혈압이 정상 범위를 초과하는 경우 True
        - timestamp (str): 결과 생성 시각 (ISO 8601 형식)
    
    Raises:
    -------
    ValueError
        If inputs are out of valid ranges or invalid sex value
    """
    # Input validation
    if not isinstance(years, int) or years < 0 or years > 18:
        raise ValueError("Years must be an integer between 0 and 18")
    if not isinstance(months, int) or months < 0 or months > 11:
        raise ValueError("Months must be an integer between 0 and 11")
    if not isinstance(height, int) or height < 50 or height > 220:
        raise ValueError("Height must be an integer between 50 and 220 cm")
    if sex not in ['male', 'female']:
        raise ValueError("Sex must be 'male' or 'female'")
    if not isinstance(systolic, int) or systolic < 50 or systolic > 250:
        raise ValueError("Systolic pressure must be an integer between 50 and 250 mmHg")
    if not isinstance(diastolic, int) or diastolic < 30 or diastolic > 150:
        raise ValueError("Diastolic pressure must be an integer between 30 and 150 mmHg")

    # Total age in months
    total_months = years * 12 + months

    # Call external API (simulated)
    api_data = call_external_api("medical-calculation-server-bp_children")

    # Map flat API response to nested output structure
    # In real implementation, this would use actual calculation logic based on reference charts
    systolic_percentile = api_data["systolic_percentile"]
    diastolic_percentile = api_data["diastolic_percentile"]
    classification = api_data["classification"]
    is_abnormal = api_data["is_abnormal"]

    # Construct percentile_category object
    percentile_category = {
        "systolic": api_data["percentile_category_systolic"],
        "diastolic": api_data["percentile_category_diastolic"]
    }

    # Construct reference_population object
    reference_population = {
        "source": api_data["reference_population_source"],
        "age_months": api_data["reference_population_age_months"],
        "height_zscore": api_data["reference_population_height_zscore"]
    }

    # Generate current timestamp in ISO 8601 format
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Construct final result
    result = {
        "systolic_percentile": systolic_percentile,
        "diastolic_percentile": diastolic_percentile,
        "classification": classification,
        "percentile_category": percentile_category,
        "reference_population": reference_population,
        "is_abnormal": is_abnormal,
        "timestamp": timestamp
    }

    return result