from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching forest fire status data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - timestamp (str): Data generation timestamp in 'YYYY-MM-DD HH:MM:SS' format
        - summary_total (int): Total number of fire incidents
        - summary_in_progress (int): Number of fires currently in progress
        - summary_completed (int): Number of fires that have been completed
        - summary_other_ended (int): Number of fires ended by other means
        - warning_0_level (str): Level of first active fire warning
        - warning_0_region (str): Region of first active fire warning
        - warning_0_issued_at (str): Issue time of first warning in 'YYYY-MM-DD HH:MM:SS' format
        - warning_0_message (str): Message of first warning (can be empty)
        - warning_1_level (str): Level of second active fire warning
        - warning_1_region (str): Region of second active fire warning
        - warning_1_issued_at (str): Issue time of second warning in 'YYYY-MM-DD HH:MM:SS' format
        - warning_1_message (str): Message of second warning (can be empty)
        - fire_0_id (str): ID of first fire incident
        - fire_0_location (str): Location of first fire incident
        - fire_0_status (str): Status of first fire incident
        - fire_0_start_time (str): Start time of first fire in 'YYYY-MM-DD HH:MM:SS' format
        - fire_0_area_affected (float): Area affected by first fire in hectares
        - fire_0_response_level (str): Response level of first fire
        - fire_0_updated_at (str): Last update time of first fire in 'YYYY-MM-DD HH:MM:SS' format
        - fire_1_id (str): ID of second fire incident
        - fire_1_location (str): Location of second fire incident
        - fire_1_status (str): Status of second fire incident
        - fire_1_start_time (str): Start time of second fire in 'YYYY-MM-DD HH:MM:SS' format
        - fire_1_area_affected (float): Area affected by second fire in hectares
        - fire_1_response_level (str): Response level of second fire
        - fire_1_updated_at (str): Last update time of second fire in 'YYYY-MM-DD HH:MM:SS' format
    """
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary_total": 5,
        "summary_in_progress": 2,
        "summary_completed": 2,
        "summary_other_ended": 1,
        "warning_0_level": "High",
        "warning_0_region": "Gangwon-do",
        "warning_0_issued_at": "2023-04-05 10:30:00",
        "warning_0_message": "High risk of fire spread due to dry conditions and strong winds.",
        "warning_1_level": "Moderate",
        "warning_1_region": "Gyeongsangbuk-do",
        "warning_1_issued_at": "2023-04-05 12:15:00",
        "warning_1_message": "Caution advised during outdoor activities.",
        "fire_0_id": "FIRE-KR-20230405-001",
        "fire_0_location": "Mount Seorak, Gangwon Province",
        "fire_0_status": "In Progress",
        "fire_0_start_time": "2023-04-05 08:45:00",
        "fire_0_area_affected": 12.5,
        "fire_0_response_level": "Level 3",
        "fire_0_updated_at": "2023-04-05 14:20:00",
        "fire_1_id": "FIRE-KR-20230405-002",
        "fire_1_location": "Andong, Gyeongsangbuk-do",
        "fire_1_status": "Containment Phase",
        "fire_1_start_time": "2023-04-04 16:20:00",
        "fire_1_area_affected": 8.3,
        "fire_1_response_level": "Level 2",
        "fire_1_updated_at": "2023-04-05 13:45:00"
    }

def current_forest_fire_status_in_korea_get_formatted_fire_info() -> Dict[str, Any]:
    """
    산불 정보를 조회하고 사람이 읽기 쉬운 형태로 포맷팅합니다.
    
    Returns:
        dict: 포맷팅된 산불 정보를 포함한 딕셔너리, 다음 키를 포함:
            - timestamp (str): 데이터 생성 시간 ('YYYY-MM-DD HH:MM:SS' 형식)
            - summary (Dict): 총합, 진행 중, 완료, 기타 종료된 화재 건수를 포함
            - warnings (List[Dict]): 활성 경고 목록 (각 항목은 level, region, issued_at, message 포함)
            - fires (List[Dict]): 진행 중 또는 최근 화재 상세 정보 (id, location, status, start_time, 
              area_affected, response_level, updated_at 포함)
            - formatted_message (str): 전체 화재 상태 및 경고 요약을 사람이 읽기 쉽게 정리한 문자열
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("current-forest-fire-status-in-korea-get_formatted_fire_info")
        
        # Construct summary
        summary = {
            "total": api_data["summary_total"],
            "in_progress": api_data["summary_in_progress"],
            "completed": api_data["summary_completed"],
            "other_ended": api_data["summary_other_ended"]
        }
        
        # Construct warnings list
        warnings = []
        if summary["in_progress"] > 0:
            warnings.append({
                "level": api_data["warning_0_level"],
                "region": api_data["warning_0_region"],
                "issued_at": api_data["warning_0_issued_at"],
                "message": api_data["warning_0_message"]
            })
            warnings.append({
                "level": api_data["warning_1_level"],
                "region": api_data["warning_1_region"],
                "issued_at": api_data["warning_1_issued_at"],
                "message": api_data["warning_1_message"]
            })
        
        # Construct fires list
        fires = []
        if summary["in_progress"] > 0:
            fires.append({
                "id": api_data["fire_0_id"],
                "location": api_data["fire_0_location"],
                "status": api_data["fire_0_status"],
                "start_time": api_data["fire_0_start_time"],
                "area_affected": api_data["fire_0_area_affected"],
                "response_level": api_data["fire_0_response_level"],
                "updated_at": api_data["fire_0_updated_at"]
            })
            fires.append({
                "id": api_data["fire_1_id"],
                "location": api_data["fire_1_location"],
                "status": api_data["fire_1_status"],
                "start_time": api_data["fire_1_start_time"],
                "area_affected": api_data["fire_1_area_affected"],
                "response_level": api_data["fire_1_response_level"],
                "updated_at": api_data["fire_1_updated_at"]
            })
        
        # Generate human-readable formatted message
        message_lines = [
            f"산불 현황 요약 ({api_data['timestamp']})",
            "=" * 50,
            f"총 화재 건수: {summary['total']}건",
            f"진행 중: {summary['in_progress']}건",
            f"완료: {summary['completed']}건",
            f"기타 종료: {summary['other_ended']}건"
        ]
        
        if warnings:
            message_lines.append("\n⚠️  활성 경고:")
            for warning in warnings:
                message_lines.append(f"  - [{warning['level']}] {warning['region']} ({warning['issued_at']})")
                if warning['message']:
                    message_lines.append(f"    {warning['message']}")
        
        if fires:
            message_lines.append("\n🔥 화재 상세 정보:")
            for fire in fires:
                message_lines.append(f"  - ID: {fire['id']}")
                message_lines.append(f"    위치: {fire['location']}")
                message_lines.append(f"    상태: {fire['status']} (응답 레벨: {fire['response_level']})")
                message_lines.append(f"    시작 시간: {fire['start_time']}, 최종 업데이트: {fire['updated_at']}")
                message_lines.append(f"    피해 면적: {fire['area_affected']}ha")
        
        # Combine all lines into a single formatted message
        formatted_message = "\n".join(message_lines)
        
        return {
            "timestamp": api_data["timestamp"],
            "summary": summary,
            "warnings": warnings,
            "fires": fires,
            "formatted_message": formatted_message
        }
        
    except Exception as e:
        # In case of any error, return a minimal error response
        error_msg = f"산불 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {"total": 0, "in_progress": 0, "completed": 0, "other_ended": 0},
            "warnings": [],
            "fires": [],
            "formatted_message": error_msg
        }