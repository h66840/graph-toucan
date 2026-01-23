from typing import Dict, List, Any, Optional
import datetime
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Velt analytics events.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - error (str): Error message if any occurred, empty otherwise
        - events_0_id (str): ID of the first event
        - events_0_event_name (str): Name of the first event
        - events_0_event_timestamp (str): ISO timestamp of the first event
        - events_0_properties (str): JSON string of properties for the first event
        - events_1_id (str): ID of the second event
        - events_1_event_name (str): Name of the second event
        - events_1_event_timestamp (str): ISO timestamp of the second event
        - events_1_properties (str): JSON string of properties for the second event
        - nextPageToken (str): Pagination token for next page, empty if no more pages
        - timezone (str): Timezone used for filtering and timestamp conversion
    """
    # Simulate possible error
    has_error = random.choice([True, False])
    if has_error:
        return {
            "error": "Failed to authenticate with Velt API",
            "events_0_id": "",
            "events_0_event_name": "",
            "events_0_event_timestamp": "",
            "events_0_properties": "",
            "events_1_id": "",
            "events_1_event_name": "",
            "events_1_event_timestamp": "",
            "events_1_properties": "",
            "nextPageToken": "",
            "timezone": ""
        }

    # Generate two sample events
    def random_timestamp() -> str:
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = datetime.timedelta(days=random.randint(0, 30), hours=random.randint(0, 24))
        past_time = now - delta
        return past_time.isoformat()

    def random_properties() -> str:
        import json
        props = {
            "page": random.choice(["home", "product", "checkout"]),
            "duration": random.randint(10, 300),
            "source": random.choice(["organic", "paid", "referral"])
        }
        return json.dumps(props)

    def random_id() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    return {
        "error": "",
        "events_0_id": random_id(),
        "events_0_event_name": random.choice(["page_view", "click", "purchase"]),
        "events_0_event_timestamp": random_timestamp(),
        "events_0_properties": random_properties(),
        "events_1_id": random_id(),
        "events_1_event_name": random.choice(["page_view", "click", "purchase"]),
        "events_1_event_timestamp": random_timestamp(),
        "events_1_properties": random_properties(),
        "nextPageToken": ''.join(random.choices(string.ascii_letters + string.digits, k=32)) if random.choice([True, False]) else "",
        "timezone": random.choice(["America/Los_Angeles", "Europe/London", "Asia/Tokyo", "UTC"])
    }


def velt_analytics_server_get_events_analytics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get paginated events from Velt with comprehensive filtering and timezone support.
    
    Supports three filtering modes:
    1. Date range: Use startDate and endDate for a specific period
    2. Single date: Use date for events from a specific day
    3. Fallback: Use lastDaysCount for recent events (default: 30 days)
    
    Args:
        data (Dict[str, Any]): Input parameters including filtering options like
            startDate, endDate, date, lastDaysCount, eventName, userId, etc.
    
    Returns:
        Dict with the following keys:
        - error (Optional[str]): Error message if request failed
        - events (List[Dict]): List of event objects with id, event_name, event_timestamp, and properties
        - nextPageToken (str): Token for retrieving next page, empty if no more pages
        - timezone (str): Timezone context applied to filtering and timestamp conversion
    """
    # Validate input
    if not isinstance(data, dict):
        return {
            "error": "Invalid input: data must be a dictionary",
            "events": [],
            "nextPageToken": "",
            "timezone": "UTC"
        }

    try:
        # Call external API (simulated)
        api_data = call_external_api("velt_analytics_server_get_events_analytics")

        # Extract error
        error: Optional[str] = api_data.get("error", "") or None
        if error:
            return {
                "error": error,
                "events": [],
                "nextPageToken": "",
                "timezone": "UTC"
            }

        # Parse events from indexed flat fields
        events: List[Dict[str, Any]] = []
        for i in range(2):  # We expect two events (0 and 1)
            event_id_key = f"events_{i}_id"
            event_name_key = f"events_{i}_event_name"
            timestamp_key = f"events_{i}_event_timestamp"
            properties_key = f"events_{i}_properties"

            if not api_data.get(event_id_key):
                continue  # Skip if event ID is missing

            try:
                import json
                properties = json.loads(api_data.get(properties_key, "{}"))
            except (json.JSONDecodeError, TypeError):
                properties = {}

            event = {
                "id": api_data.get(event_id_key, ""),
                "event_name": api_data.get(event_name_key, "unknown"),
                "event_timestamp": api_data.get(timestamp_key, ""),
                "properties": properties
            }
            events.append(event)

        # Get pagination token and timezone
        next_page_token: str = api_data.get("nextPageToken", "")
        timezone: str = api_data.get("timezone", "UTC")

        return {
            "error": None,
            "events": events,
            "nextPageToken": next_page_token,
            "timezone": timezone
        }

    except Exception as e:
        return {
            "error": f"Unexpected error processing events: {str(e)}",
            "events": [],
            "nextPageToken": "",
            "timezone": "UTC"
        }