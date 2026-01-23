from typing import Dict, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for forest fire status and evacuation information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - timestamp (str): Data generation timestamp in 'YYYY-MM-DD HH:MM:SS' format
        - fire_info_timestamp (str): Timestamp of fire data update
        - fire_info_summary (str): Brief summary of current fire status
        - fire_info_warnings (str): Active fire warnings
        - fire_info_details (str): Detailed fire information
        - fire_info_formatted_message (str): Human-readable fire message
        - fire_info_raw_data (str): Raw fire data as JSON string
        - evacuation_info_success (bool): Whether evacuation search was successful
        - evacuation_info_error (str): Error message if evacuation search failed
        - evacuation_info_message (str): Message about evacuation shelters
        - evacuation_info_location (str): Searched location for shelters
    """
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fire_info_timestamp": "2023-04-05 14:30:00",
        "fire_info_summary": "산불 3건 발생, 2건 진화 완료",
        "fire_info_warnings": "강원도 삼척시 산불 주의보 발령",
        "fire_info_details": "삼척시 신기면 일대에서 산불 발생, 10ha 소실",
        "fire_info_formatted_message": "🔥 산불 발생: 강원도 삼척시\n진화율: 70%\n대피 권고 지역 존재",
        "fire_info_raw_data": '{"fires": [{"location": "삼척시 신기면", "size_ha": 10, "status": "진화중"}]}',
        "evacuation_info_success": True,
        "evacuation_info_error": "",
        "evacuation_info_message": "근처 대피소 3개소 발견",
        "evacuation_info_location": "강원도 삼척시"
    }


def current_forest_fire_status_in_korea_get_comprehensive_fire_info(location: Optional[str] = None) -> Dict[str, Any]:
    """
    산불 정보와 지정된 위치의 대피소 정보를 함께 제공합니다.

    Args:
        location (str, optional): 대피소를 검색할 지역명. 지정하지 않으면 대피소 정보는 제외됩니다.

    Returns:
        dict: 산불 정보와 대피소 정보를 포함한 딕셔너리 with keys:
            - timestamp (str): 데이터 생성 시간 ('YYYY-MM-DD HH:MM:SS')
            - fire_info (Dict): 산불 상태 정보 (요약, 경고, 세부 정보 등)
            - evacuation_info (Dict or None): 대피소 검색 결과 (성공 여부, 메시지 등)
            - message (str): 산불 및 대피 정보를 포함한 가독성 높은 메시지
    """
    # Fetch simulated external data
    api_data = call_external_api("current-forest-fire-status-in-korea-get_comprehensive_fire_info")

    # Construct fire_info dictionary
    fire_info = {
        "timestamp": api_data["fire_info_timestamp"],
        "summary": api_data["fire_info_summary"],
        "warnings": api_data["fire_info_warnings"],
        "details": api_data["fire_info_details"],
        "formatted_message": api_data["fire_info_formatted_message"],
        "raw_data": api_data["fire_info_raw_data"]
    }

    # Construct evacuation_info if location is provided
    evacuation_info = None
    if location:
        evacuation_info = {
            "success": api_data["evacuation_info_success"],
            "message": api_data["evacuation_info_message"]
        }
        # Add error only if present
        if api_data["evacuation_info_error"]:
            evacuation_info["error"] = api_data["evacuation_info_error"]
    else:
        evacuation_info = None

    # Construct final message
    message_parts = [fire_info["formatted_message"]]
    if evacuation_info:
        message_parts.append(f"📍 대피소 정보 ({location or api_data['evacuation_info_location']}): {evacuation_info['message']}")

    message = "\n".join(message_parts)

    # Build final result
    result = {
        "timestamp": api_data["timestamp"],
        "fire_info": fire_info,
        "evacuation_info": evacuation_info,
        "message": message
    }

    return result