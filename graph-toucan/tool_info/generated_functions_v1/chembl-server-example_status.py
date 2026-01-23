from typing import Dict, List, Any
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL Web Services status.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Current operational status of the ChEMBL Web Services
        - version (str): Version of the ChEMBL Web Services API currently running
        - timestamp (str): ISO 8601 timestamp indicating when the status was last updated
        - api_uptime (float): Fraction of time the API has been operational
        - database_status_connection_status (str): Connection status of the database
        - database_status_version (str): Version of the underlying database
        - database_status_latency (float): Latency of database in seconds
        - services_0_name (str): Name of the first microservice
        - services_0_status (str): Status of the first microservice
        - services_0_response_time (float): Response time of the first microservice in ms
        - services_1_name (str): Name of the second microservice
        - services_1_status (str): Status of the second microservice
        - services_1_response_time (float): Response time of the second microservice in ms
        - maintenance_mode (bool): Whether the system is in maintenance mode
        - message (str): Human-readable message about the current status
    """
    return {
        "status": random.choice(["OK", "Degraded", "Down"]),
        "version": "2.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "api_uptime": round(random.uniform(0.95, 1.0), 4),
        "database_status_connection_status": random.choice(["connected", "disconnected"]),
        "database_status_version": "ChEMBL-32",
        "database_status_latency": round(random.uniform(0.01, 0.5), 3),
        "services_0_name": "Compound Service",
        "services_0_status": random.choice(["OK", "Degraded"]),
        "services_0_response_time": round(random.uniform(10, 300), 2),
        "services_1_name": "Target Service",
        "services_1_status": random.choice(["OK", "Down"]),
        "services_1_response_time": round(random.uniform(10, 500), 2),
        "maintenance_mode": False,
        "message": "System operating normally." if random.random() > 0.2 else "Maintenance scheduled for tonight."
    }


def chembl_server_example_status() -> Dict[str, Any]:
    """
    Get status information for ChEMBL Web Services.

    Returns:
        Dictionary of status information with the following fields:
        - status (str): Current operational status of the ChEMBL Web Services (e.g., 'OK', 'Degraded', 'Down')
        - version (str): Version of the ChEMBL Web Services API currently running
        - timestamp (str): ISO 8601 timestamp indicating when the status was last updated
        - api_uptime (float): Fraction or percentage of time the API has been operational in a given period
        - database_status (Dict): Health and status information about the underlying database
        - services (List[Dict]): List of individual microservices with their statuses
        - maintenance_mode (bool): Indicates whether the system is currently in maintenance mode
        - message (str): Human-readable message providing additional context about the current status

    Raises:
        Exception: If there is an error in retrieving or parsing the status data
    """
    try:
        api_data = call_external_api("chembl-server-example_status")

        # Construct database_status as a nested dictionary
        database_status = {
            "connection_status": api_data["database_status_connection_status"],
            "version": api_data["database_status_version"],
            "latency": api_data["database_status_latency"]
        }

        # Construct services list from indexed fields
        services = [
            {
                "name": api_data["services_0_name"],
                "status": api_data["services_0_status"],
                "response_time": api_data["services_0_response_time"]
            },
            {
                "name": api_data["services_1_name"],
                "status": api_data["services_1_status"],
                "response_time": api_data["services_1_response_time"]
            }
        ]

        # Build final result dictionary matching output schema
        result = {
            "status": api_data["status"],
            "version": api_data["version"],
            "timestamp": api_data["timestamp"],
            "api_uptime": api_data["api_uptime"],
            "database_status": database_status,
            "services": services,
            "maintenance_mode": api_data["maintenance_mode"],
            "message": api_data["message"]
        }

        return result

    except KeyError as e:
        raise Exception(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve or process ChEMBL server status: {str(e)}")