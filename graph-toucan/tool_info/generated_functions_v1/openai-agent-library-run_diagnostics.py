from typing import Dict, List, Any
import datetime
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching diagnostic data from external API for OpenAI Agents SDK.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Overall diagnostic status
        - timestamp (str): ISO 8601 timestamp when diagnostics were run
        - duration_ms (int): Total time taken in milliseconds
        - errors_count (int): Number of errors encountered
        - error_0_component (str): Component name for first error
        - error_0_error_type (str): Error type for first error
        - error_0_message (str): Error message for first error
        - error_1_component (str): Component name for second error
        - error_1_error_type (str): Error type for second error
        - error_1_message (str): Error message for second error
        - documentation_reachable_status (str): Status of documentation reachability check
        - documentation_reachable_response_time_ms (int): Response time in ms for documentation
        - github_repo_accessible_status (str): Status of GitHub repo accessibility check
        - github_repo_accessible_response_time_ms (int): Response time in ms for GitHub repo
        - api_endpoint_1_status (str): Status of first API endpoint check
        - api_endpoint_1_response_time_ms (int): Response time in ms for first API endpoint
        - api_endpoint_2_status (str): Status of second API endpoint check
        - api_endpoint_2_response_time_ms (int): Response time in ms for second API endpoint
        - metadata_sdk_version (str): Version of SDK checked
        - metadata_user_agent (str): User agent string used during test
        - metadata_network_latency_ms (int): Network latency in ms during test
    """
    return {
        "status": "degraded",
        "timestamp": "2023-11-20T10:30:45.123Z",
        "duration_ms": 450,
        "errors_count": 2,
        "error_0_component": "documentation",
        "error_0_error_type": "TimeoutError",
        "error_0_message": "Documentation site timed out after 30s",
        "error_1_component": "api_endpoint_1",
        "error_1_error_type": "HTTPError",
        "error_1_message": "Received 503 from API endpoint",
        "documentation_reachable_status": "unreachable",
        "documentation_reachable_response_time_ms": 30000,
        "github_repo_accessible_status": "reachable",
        "github_repo_accessible_response_time_ms": 120,
        "api_endpoint_1_status": "unreachable",
        "api_endpoint_1_response_time_ms": 250,
        "api_endpoint_2_status": "reachable",
        "api_endpoint_2_response_time_ms": 180,
        "metadata_sdk_version": "0.1.5",
        "metadata_user_agent": "OpenAI-Agent-Diagnostics/0.1.5",
        "metadata_network_latency_ms": 45,
    }


def openai_agent_library_run_diagnostics() -> Dict[str, Any]:
    """
    Run diagnostics to check the health of the OpenAI Agents SDK documentation and GitHub repository.

    Returns:
        Dict containing diagnostic results with the following structure:
        - status (str): Overall diagnostic status ('healthy', 'degraded', 'unhealthy')
        - details (Dict): Nested object with granular check results including:
            - documentation_reachable: status and response_time_ms
            - github_repo_accessible: status and response_time_ms
            - api endpoints: status and response_time_ms for each endpoint
        - timestamp (str): ISO 8601 timestamp when diagnostics were run
        - duration_ms (int): Total time taken in milliseconds
        - errors (List[Dict]): List of error objects with component, error_type, message
        - metadata (Dict): Additional context like SDK version, user agent, network conditions
    """
    # Call external API to get raw diagnostic data
    api_data = call_external_api("openai-agent-library-run_diagnostics")

    # Construct the nested details structure
    details = {
        "documentation_reachable": {
            "status": api_data["documentation_reachable_status"],
            "response_time_ms": api_data["documentation_reachable_response_time_ms"]
        },
        "github_repo_accessible": {
            "status": api_data["github_repo_accessible_status"],
            "response_time_ms": api_data["github_repo_accessible_response_time_ms"]
        },
        "api_endpoints": {
            "api_endpoint_1": {
                "status": api_data["api_endpoint_1_status"],
                "response_time_ms": api_data["api_endpoint_1_response_time_ms"]
            },
            "api_endpoint_2": {
                "status": api_data["api_endpoint_2_status"],
                "response_time_ms": api_data["api_endpoint_2_response_time_ms"]
            }
        }
    }

    # Construct errors list from indexed fields
    errors = []
    if api_data["errors_count"] > 0:
        errors.append({
            "component": api_data["error_0_component"],
            "error_type": api_data["error_0_error_type"],
            "message": api_data["error_0_message"]
        })
    if api_data["errors_count"] > 1:
        errors.append({
            "component": api_data["error_1_component"],
            "error_type": api_data["error_1_error_type"],
            "message": api_data["error_1_message"]
        })

    # Construct metadata
    metadata = {
        "sdk_version": api_data["metadata_sdk_version"],
        "user_agent": api_data["metadata_user_agent"],
        "network_conditions": {
            "latency_ms": api_data["metadata_network_latency_ms"]
        }
    }

    # Build final result matching output schema
    result = {
        "status": api_data["status"],
        "details": details,
        "timestamp": api_data["timestamp"],
        "duration_ms": api_data["duration_ms"],
        "errors": errors,
        "metadata": metadata
    }

    return result