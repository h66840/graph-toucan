from typing import Dict, List, Any
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for TabNews status.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Current operational status of the TabNews API
        - last_updated (str): Timestamp when status was last updated in ISO 8601
        - components_0_name (str): Name of first system component
        - components_0_status (str): Status of first component
        - components_0_incident_title (str): Incident title for first component if applicable
        - components_0_incident_description (str): Incident description for first component
        - components_1_name (str): Name of second system component
        - components_1_status (str): Status of second component
        - components_1_incident_title (str): Incident title for second component if applicable
        - components_1_incident_description (str): Incident description for second component
        - incidents_0_title (str): Title of first active incident
        - incidents_0_impact_level (str): Impact level of first incident
        - incidents_0_description (str): Description of first incident
        - incidents_0_start_time (str): Start time of first incident in ISO 8601
        - incidents_0_status (str): Current status of first incident
        - incidents_1_title (str): Title of second active incident
        - incidents_1_impact_level (str): Impact level of second incident
        - incidents_1_description (str): Description of second incident
        - incidents_1_start_time (str): Start time of second incident in ISO 8601
        - incidents_1_status (str): Current status of second incident
        - maintenance_0_title (str): Title of first maintenance activity
        - maintenance_0_start_time (str): Start time of first maintenance in ISO 8601
        - maintenance_0_end_time (str): End time of first maintenance in ISO 8601
        - maintenance_0_description (str): Description of first maintenance
        - maintenance_0_status (str): Status of first maintenance
        - maintenance_1_title (str): Title of second maintenance activity
        - maintenance_1_start_time (str): Start time of second maintenance in ISO 8601
        - maintenance_1_end_time (str): End time of second maintenance in ISO 8601
        - maintenance_1_description (str): Description of second maintenance
        - maintenance_1_status (str): Status of second maintenance
        - response_time_ms (float): Latest measured response time in milliseconds
        - uptime_24h (float): Uptime percentage over last 24 hours
        - message (str): Human-readable message summarizing current state
    """
    now = datetime.utcnow()
    past_hour = (now - timedelta(hours=1)).isoformat() + "Z"
    future_time = (now + timedelta(hours=2)).isoformat() + "Z"
    current_status = random.choice(["operational", "degraded", "down"])
    
    return {
        "status": current_status,
        "last_updated": now.isoformat() + "Z",
        "components_0_name": "API Gateway",
        "components_0_status": random.choice(["operational", "degraded"]),
        "components_0_incident_title": "High Latency in API Gateway" if current_status == "degraded" else "",
        "components_0_incident_description": "Experiencing higher than normal response times" if current_status == "degraded" else "",
        "components_1_name": "Database Cluster",
        "components_1_status": "operational",
        "components_1_incident_title": "",
        "components_1_incident_description": "",
        "incidents_0_title": "API Rate Limiting Issue" if current_status == "degraded" else "",
        "incidents_0_impact_level": "medium" if current_status == "degraded" else "",
        "incidents_0_description": "Some users are experiencing rate limiting errors" if current_status == "degraded" else "",
        "incidents_0_start_time": past_hour if current_status == "degraded" else "",
        "incidents_0_status": "investigating" if current_status == "degraded" else "",
        "incidents_1_title": "Authentication Service Outage" if current_status == "down" else "",
        "incidents_1_impact_level": "high" if current_status == "down" else "",
        "incidents_1_description": "Users unable to log in due to authentication service failure" if current_status == "down" else "",
        "incidents_1_start_time": past_hour if current_status == "down" else "",
        "incidents_1_status": "identified" if current_status == "down" else "",
        "maintenance_0_title": "Database Maintenance",
        "maintenance_0_start_time": future_time,
        "maintenance_0_end_time": (now + timedelta(hours=4)).isoformat() + "Z",
        "maintenance_0_description": "Routine database optimization and backup",
        "maintenance_0_status": "scheduled",
        "maintenance_1_title": "",
        "maintenance_1_start_time": "",
        "maintenance_1_end_time": "",
        "maintenance_1_description": "",
        "maintenance_1_status": "",
        "response_time_ms": round(random.uniform(50, 800), 2),
        "uptime_24h": round(random.uniform(95, 100), 2),
        "message": f"TabNews API is currently {current_status}. Please monitor for updates." if current_status != "operational" else "TabNews API is operating normally."
    }


def tabnews_integration_get_status() -> Dict[str, Any]:
    """
    Get status from TabNews API.

    Returns:
        Dict containing the current operational status and related information:
        - status (str): Current operational status of the TabNews API
        - last_updated (str): Timestamp indicating when the status was last updated (ISO 8601)
        - components (List[Dict]): List of system components with their statuses and incident details
        - incidents (List[Dict]): List of active incidents affecting the service
        - maintenance (List[Dict]): List of scheduled or ongoing maintenance activities
        - response_time_ms (float): Latest measured response time in milliseconds
        - uptime_24h (float): Uptime percentage over the last 24 hours
        - message (str): Human-readable message summarizing current state
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("tabnews-integration-get status")

        # Construct components list
        components = []
        for i in range(2):
            name_key = f"components_{i}_name"
            status_key = f"components_{i}_status"
            incident_title_key = f"components_{i}_incident_title"
            incident_description_key = f"components_{i}_incident_description"

            if api_data.get(name_key):
                component = {
                    "name": api_data[name_key],
                    "status": api_data[status_key],
                }
                # Add incident details only if they exist
                if api_data.get(incident_title_key):
                    component["incident"] = {
                        "title": api_data[incident_title_key],
                        "description": api_data[incident_description_key]
                    }
                components.append(component)

        # Construct incidents list
        incidents = []
        for i in range(2):
            title_key = f"incidents_{i}_title"
            if api_data.get(title_key):
                incident = {
                    "title": api_data[title_key],
                    "impact_level": api_data[f"incidents_{i}_impact_level"],
                    "description": api_data[f"incidents_{i}_description"],
                    "start_time": api_data[f"incidents_{i}_start_time"],
                    "status": api_data[f"incidents_{i}_status"]
                }
                incidents.append(incident)

        # Construct maintenance list
        maintenance = []
        for i in range(2):
            title_key = f"maintenance_{i}_title"
            if api_data.get(title_key):
                maintenance_activity = {
                    "title": api_data[title_key],
                    "start_time": api_data[f"maintenance_{i}_start_time"],
                    "end_time": api_data[f"maintenance_{i}_end_time"],
                    "description": api_data[f"maintenance_{i}_description"],
                    "status": api_data[f"maintenance_{i}_status"]
                }
                maintenance.append(maintenance_activity)

        # Build final result structure
        result = {
            "status": api_data["status"],
            "last_updated": api_data["last_updated"],
            "components": components,
            "incidents": incidents,
            "maintenance": maintenance,
            "response_time_ms": api_data["response_time_ms"],
            "uptime_24h": api_data["uptime_24h"],
            "message": api_data["message"]
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process TabNews API status: {str(e)}") from e