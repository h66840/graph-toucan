from typing import Dict, List, Any
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching forest fire status data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - timestamp (str): Timestamp of when the forest fire status was recorded
        - summary_total (int): Total number of forest fires
        - summary_in_progress (int): Number of ongoing forest fires
        - summary_completed (int): Number of completed forest fires
        - summary_other_ended (int): Number of fires ended by other means
        - warning_0_location (str): Location of first active warning
        - warning_0_level (str): Warning level of first active warning
        - warning_0_message (str): Message for first active warning
        - warning_1_location (str): Location of second active warning
        - warning_1_level (str): Warning level of second active warning
        - warning_1_message (str): Message for second active warning
        - fire_0_location (str): Location of first fire incident
        - fire_0_status (str): Status of first fire incident
        - fire_0_start_time (str): Start time of first fire incident
        - fire_0_response_team (str): Response team assigned to first fire
        - fire_0_cause (str): Suspected cause of first fire
        - fire_1_location (str): Location of second fire incident
        - fire_1_status (str): Status of second fire incident
        - fire_1_start_time (str): Start time of second fire incident
        - fire_1_response_team (str): Response team assigned to second fire
        - fire_1_cause (str): Suspected cause of second fire
    """
    now = datetime.now()
    start_time_1 = (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    start_time_2 = (now - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "summary_total": random.randint(5, 15),
        "summary_in_progress": random.randint(1, 5),
        "summary_completed": random.randint(2, 8),
        "summary_other_ended": random.randint(0, 3),
        "warning_0_location": "Gangwon-do, Pyeongchang",
        "warning_0_level": "High",
        "warning_0_message": "High risk of forest fire due to dry weather and strong winds.",
        "warning_1_location": "Gyeongsangbuk-do, Andong",
        "warning_1_level": "Moderate",
        "warning_1_message": "Moderate fire risk observed. Public caution advised.",
        "fire_0_location": "Gangwon-do, Inje-gun",
        "fire_0_status": "In Progress",
        "fire_0_start_time": start_time_1,
        "fire_0_response_team": "National Forest Fire Brigade #3",
        "fire_0_cause": "Suspected human activity",
        "fire_1_location": "Chungcheongbuk-do, Danyang-gun",
        "fire_1_status": "Under Control",
        "fire_1_start_time": start_time_2,
        "fire_1_response_team": "Local Fire Department & Aerial Unit",
        "fire_1_cause": "Lightning strike",
    }


def current_forest_fire_status_in_korea_get_forest_fire_info() -> Dict[str, Any]:
    """
    산림청에서 산불 현황 정보를 가져옵니다.

    Returns:
        dict: 산불 발생 현황 및 경보 정보를 포함한 딕셔너리
        - timestamp (str): timestamp of when the forest fire status was recorded, in 'YYYY-MM-DD HH:MM:SS' format
        - summary (Dict): contains summary counts of forest fires with keys 'total', 'in_progress', 'completed', 'other_ended'
        - warnings (List[Dict]): list of active forest fire warnings, each containing details such as location, level, and message if available
        - fires (List[Dict]): list of current or recent forest fire incidents, each including details like location, status, start time, and response information
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("current-forest-fire-status-in-korea-get_forest_fire_info")

        # Construct summary dictionary
        summary = {
            "total": api_data["summary_total"],
            "in_progress": api_data["summary_in_progress"],
            "completed": api_data["summary_completed"],
            "other_ended": api_data["summary_other_ended"],
        }

        # Construct warnings list
        warnings = [
            {
                "location": api_data["warning_0_location"],
                "level": api_data["warning_0_level"],
                "message": api_data["warning_0_message"],
            },
            {
                "location": api_data["warning_1_location"],
                "level": api_data["warning_1_level"],
                "message": api_data["warning_1_message"],
            },
        ]

        # Construct fires list
        fires = [
            {
                "location": api_data["fire_0_location"],
                "status": api_data["fire_0_status"],
                "start_time": api_data["fire_0_start_time"],
                "response_team": api_data["fire_0_response_team"],
                "cause": api_data["fire_0_cause"],
            },
            {
                "location": api_data["fire_1_location"],
                "status": api_data["fire_1_status"],
                "start_time": api_data["fire_1_start_time"],
                "response_team": api_data["fire_1_response_team"],
                "cause": api_data["fire_1_cause"],
            },
        ]

        # Assemble final result
        result = {
            "timestamp": api_data["timestamp"],
            "summary": summary,
            "warnings": warnings,
            "fires": fires,
        }

        return result

    except KeyError as e:
        # Handle missing keys in API response
        raise KeyError(f"Missing expected data field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve forest fire information: {str(e)}")