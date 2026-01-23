from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for school meal information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_education_office (str): Education office for first result
        - results_0_school_name (str): School name for first result
        - results_0_date (str): Date of meal for first result in YYYYMMDD
        - results_0_has_meal (bool): Whether meal exists for first result
        - results_1_education_office (str): Education office for second result
        - results_1_school_name (str): School name for second result
        - results_1_date (str): Date of meal for second result in YYYYMMDD
        - results_1_has_meal (bool): Whether meal exists for second result
        - error (str): Error message if any
        - suggestions_0 (str): First suggested school name
        - suggestions_1 (str): Second suggested school name
    """
    return {
        "results_0_education_office": "경기도교육청",
        "results_0_school_name": "의정부고등학교",
        "results_0_date": "20231015",
        "results_0_has_meal": True,
        "results_1_education_office": "서울특별시교육청",
        "results_1_school_name": "서울고등학교",
        "results_1_date": "20231015",
        "results_1_has_meal": False,
        "error": "",
        "suggestions_0": "의정부중학교",
        "suggestions_1": "의정부여자고등학교",
    }


def schoolfoods_get_school_meal(date: Optional[str] = None, school_name: Optional[str] = None) -> Dict[str, Any]:
    """
    학교명과 날짜를 입력받아 급식 정보를 제공합니다.
    
    날짜는 YYYYMMDD 형식이나 '오늘', '내일', '모레'와 같은 상대적인 표현도 사용 가능합니다.
    날짜를 생략하면 오늘 급식 정보를 조회합니다.

    Args:
        date (Optional[str]): 급식 조회 날짜 (YYYYMMDD 형식, '오늘', '내일' 등)
        school_name (str): 학교 이름 (예: 의정부고등학교)

    Returns:
        Dict containing:
        - results (List[Dict]): list of result entries with 'education_office', 'school_name', 'date', 'has_meal'
        - error (str): error message if school lookup failed
        - suggestions (List[str]): list of similar or suggested school names

    Raises:
        ValueError: If school_name is not provided
    """
    # Input validation
    if not school_name:
        return {
            "results": [],
            "error": "학교 이름이 제공되지 않았습니다.",
            "suggestions": []
        }

    # Process date
    if not date or date == "오늘":
        target_date = datetime.now().strftime("%Y%m%d")
    elif date == "내일":
        target_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    elif date == "모레":
        target_date = (datetime.now() + timedelta(days=2)).strftime("%Y%m%d")
    elif re.match(r"^\d{8}$", date):
        target_date = date
    else:
        return {
            "results": [],
            "error": f"잘못된 날짜 형식: {date}. YYYYMMDD 형식이나 '오늘', '내일', '모레'를 사용하세요.",
            "suggestions": []
        }

    # Call external API (simulated)
    api_data = call_external_api("schoolfoods-get_school_meal")

    # Construct results list from flattened API response
    results = [
        {
            "education_office": api_data["results_0_education_office"],
            "school_name": api_data["results_0_school_name"],
            "date": api_data["results_0_date"],
            "has_meal": api_data["results_0_has_meal"]
        },
        {
            "education_office": api_data["results_1_education_office"],
            "school_name": api_data["results_1_school_name"],
            "date": api_data["results_1_date"],
            "has_meal": api_data["results_1_has_meal"]
        }
    ]

    # Filter results by school_name (case-insensitive partial match)
    filtered_results = [
        r for r in results
        if school_name.lower() in r["school_name"].lower()
    ]

    # If no match found, return suggestions
    if not filtered_results:
        suggestions = [
            api_data["suggestions_0"],
            api_data["suggestions_1"]
        ]
        return {
            "results": [],
            "error": f"'{school_name}'에 해당하는 학교를 찾을 수 없습니다.",
            "suggestions": suggestions
        }

    # Update date in results to requested date
    for r in filtered_results:
        r["date"] = target_date

    # Prepare suggestions if needed
    suggestions = []
    if api_data["suggestions_0"] and api_data["suggestions_1"]:
        suggestions = [api_data["suggestions_0"], api_data["suggestions_1"]]

    return {
        "results": filtered_results,
        "error": api_data["error"] if api_data["error"] else "",
        "suggestions": suggestions
    }