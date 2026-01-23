from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for conference search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the search operation
        - count (int): Total number of events returned
        - event_0_event_name (str): Name of the first event
        - event_0_event_description (str): Description of the first event
        - event_0_event_time (str): Time of the first event
        - event_0_event_location (str): Location of the first event
        - event_0_deadline (str): Deadline of the first event
        - event_0_description (str): Additional description of the first event
        - event_0_event_link (str): Link to the first event
        - event_1_event_name (str): Name of the second event
        - event_1_event_description (str): Description of the second event
        - event_1_event_time (str): Time of the second event
        - event_1_event_location (str): Location of the second event
        - event_1_deadline (str): Deadline of the second event
        - event_1_description (str): Additional description of the second event
        - event_1_event_link (str): Link to the second event
    """
    return {
        "status": "success",
        "count": 2,
        "event_0_event_name": "International Conference on Machine Learning",
        "event_0_event_description": "A premier conference on machine learning research.",
        "event_0_event_time": "2024-07-21T09:00:00Z",
        "event_0_event_location": "Vienna, Austria",
        "event_0_deadline": "2024-03-15",
        "event_0_description": "ICML is the leading conference for machine learning research.",
        "event_0_event_link": "https://icml.cc/2024",
        "event_1_event_name": "Conference on Computer Vision and Pattern Recognition",
        "event_1_event_description": "Top-tier conference on computer vision and pattern recognition.",
        "event_1_event_time": "2024-06-18T08:30:00Z",
        "event_1_event_location": "Seattle, WA, USA",
        "event_1_deadline": "2024-02-20",
        "event_1_description": "CVPR is a premier annual conference in computer vision.",
        "event_1_event_link": "https://cvpr2024.thecvf.com"
    }


def conferencesearcher_get_events(keywords: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search for conferences matching specific keywords.

    Args:
        keywords (str): Keywords to search for in conference events.
        limit (Optional[int]): Maximum number of events to return. Defaults to None (no limit).

    Returns:
        Dict containing:
            - status (str): Status of the search operation (e.g., "success").
            - count (int): Total number of events returned.
            - events (List[Dict]): List of conference/event items, each containing:
                - event_name (str)
                - event_description (str)
                - event_time (str)
                - event_location (str)
                - deadline (str)
                - description (str)
                - event_link (str)

    Raises:
        ValueError: If keywords is empty or not a string.
    """
    if not keywords or not isinstance(keywords, str):
        raise ValueError("Keywords must be a non-empty string.")

    # Fetch data from simulated external API
    api_data = call_external_api("conferencesearcher-get_events")

    # Construct events list from flattened API response
    events = []
    for i in range(api_data["count"]):
        event_key_prefix = f"event_{i}"
        event = {
            "event_name": api_data.get(f"{event_key_prefix}_event_name", ""),
            "event_description": api_data.get(f"{event_key_prefix}_event_description", ""),
            "event_time": api_data.get(f"{event_key_prefix}_event_time", ""),
            "event_location": api_data.get(f"{event_key_prefix}_event_location", ""),
            "deadline": api_data.get(f"{event_key_prefix}_deadline", ""),
            "description": api_data.get(f"{event_key_prefix}_description", ""),
            "event_link": api_data.get(f"{event_key_prefix}_event_link", "")
        }
        events.append(event)

    # Apply limit if specified
    if limit is not None and limit > 0:
        events = events[:limit]
        count = len(events)
    else:
        count = api_data["count"]

    return {
        "status": api_data["status"],
        "count": count,
        "events": events
    }