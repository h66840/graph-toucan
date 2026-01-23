from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching OSINT data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - overview_identity_type (str): Type of identity (e.g., email, domain, IP)
        - overview_associated_domains (str): Comma-separated domains associated with the target
        - overview_reputation_score (float): Reputation score between 0 and 100
        - overview_confidence (float): Confidence level between 0 and 1
        - intelligence_results_0_source (str): Source of first intelligence result
        - intelligence_results_0_category (str): Category of first intelligence result
        - intelligence_results_0_data (str): Data of first intelligence result
        - intelligence_results_0_timestamp (str): Timestamp of first intelligence result
        - intelligence_results_0_confidence (float): Confidence of first intelligence result
        - intelligence_results_1_source (str): Source of second intelligence result
        - intelligence_results_1_category (str): Category of second intelligence result
        - intelligence_results_1_data (str): Data of second intelligence result
        - intelligence_results_1_timestamp (str): Timestamp of second intelligence result
        - intelligence_results_1_confidence (float): Confidence of second intelligence result
        - related_entities_0_entity_name (str): Name of first related entity
        - related_entities_0_relationship_type (str): Relationship type of first entity
        - related_entities_0_source (str): Source of first related entity
        - related_entities_0_confidence (float): Confidence of first related entity
        - related_entities_1_entity_name (str): Name of second related entity
        - related_entities_1_relationship_type (str): Relationship type of second entity
        - related_entities_1_source (str): Source of second related entity
        - related_entities_1_confidence (float): Confidence of second related entity
        - threat_indicators_0_indicator_type (str): Type of first threat indicator
        - threat_indicators_0_value (str): Value of first threat indicator
        - threat_indicators_0_severity (str): Severity level of first threat indicator
        - threat_indicators_0_source (str): Source of first threat indicator
        - threat_indicators_0_first_seen (str): First seen timestamp of first threat indicator
        - threat_indicators_1_indicator_type (str): Type of second threat indicator
        - threat_indicators_1_value (str): Value of second threat indicator
        - threat_indicators_1_severity (str): Severity level of second threat indicator
        - threat_indicators_1_source (str): Source of second threat indicator
        - threat_indicators_1_first_seen (str): First seen timestamp of second threat indicator
        - metadata_query_timestamp (str): Timestamp when query was executed
        - metadata_execution_time_ms (int): Execution time in milliseconds
        - metadata_sources_used_0 (str): First source used
        - metadata_sources_used_1 (str): Second source used
        - metadata_completion_status (str): Status of completion (e.g., success, failed)
        - success (bool): Whether the operation succeeded
        - error_message (str): Error message if success is False
    """
    return {
        "overview_identity_type": "email",
        "overview_associated_domains": "example.com, user-example.net",
        "overview_reputation_score": 45.0,
        "overview_confidence": 0.87,
        "intelligence_results_0_source": "HaveIBeenPwned",
        "intelligence_results_0_category": "email",
        "intelligence_results_0_data": "Found in data breach: Collection #1",
        "intelligence_results_0_timestamp": "2023-08-15T12:30:45Z",
        "intelligence_results_0_confidence": 0.95,
        "intelligence_results_1_source": "Twitter",
        "intelligence_results_1_category": "social_media",
        "intelligence_results_1_data": "Profile found: @user123",
        "intelligence_results_1_timestamp": "2023-09-01T08:22:10Z",
        "intelligence_results_1_confidence": 0.90,
        "related_entities_0_entity_name": "John Doe",
        "related_entities_0_relationship_type": "colleague",
        "related_entities_0_source": "LinkedIn",
        "related_entities_0_confidence": 0.82,
        "related_entities_1_entity_name": "Acme Corp",
        "related_entities_1_relationship_type": "employer",
        "related_entities_1_source": "Company Registry",
        "related_entities_1_confidence": 0.93,
        "threat_indicators_0_indicator_type": "leaked_credentials",
        "threat_indicators_0_value": "user@example.com:password123",
        "threat_indicators_0_severity": "high",
        "threat_indicators_0_source": "DarkWeb Forum X",
        "threat_indicators_0_first_seen": "2023-08-15T12:30:45Z",
        "threat_indicators_1_indicator_type": "malicious_activity",
        "threat_indicators_1_value": "Suspicious login from Russia",
        "threat_indicators_1_severity": "medium",
        "threat_indicators_1_source": "SIEM System",
        "threat_indicators_1_first_seen": "2023-09-05T14:11:22Z",
        "metadata_query_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_execution_time_ms": 450,
        "metadata_sources_used_0": "HaveIBeenPwned",
        "metadata_sources_used_1": "Twitter API",
        "metadata_completion_status": "success",
        "success": True,
        "error_message": ""
    }


def osint_server_osint_overview(target: str) -> Dict[str, Any]:
    """
    Performs an OSINT overview lookup on a given target (e.g., email, domain, IP).

    Args:
        target (str): The target to investigate (e.g., email address, domain, IP address).

    Returns:
        Dict containing structured OSINT results with the following keys:
        - overview (Dict): High-level summary including identity type, associated domains,
          reputation score, and confidence.
        - intelligence_results (List[Dict]): List of OSINT findings with source, category,
          data, timestamp, and confidence.
        - related_entities (List[Dict]): Entities linked to the target with name, relationship,
          source, and confidence.
        - threat_indicators (List[Dict]): Security risks such as leaked credentials or
          malicious activity.
        - metadata (Dict): Query execution details including timestamp, execution time,
          sources used, and status.
        - success (bool): Whether the lookup completed successfully.
        - error_message (str): Description of error if success is False.

    Raises:
        ValueError: If target is empty or not a string.
    """
    if not isinstance(target, str):
        raise ValueError("Target must be a string.")
    if not target.strip():
        raise ValueError("Target cannot be empty or whitespace.")
    
    try:
        api_data = call_external_api("osint_server_osint_overview")

        # Construct overview
        overview = {
            "identity_type": api_data["overview_identity_type"],
            "associated_domains": api_data["overview_associated_domains"].split(", ") if api_data["overview_associated_domains"] else [],
            "reputation_score": api_data["overview_reputation_score"],
            "confidence": api_data["overview_confidence"]
        }

        # Construct intelligence_results
        intelligence_results = [
            {
                "source": api_data["intelligence_results_0_source"],
                "category": api_data["intelligence_results_0_category"],
                "data": api_data["intelligence_results_0_data"],
                "timestamp": api_data["intelligence_results_0_timestamp"],
                "confidence": api_data["intelligence_results_0_confidence"]
            },
            {
                "source": api_data["intelligence_results_1_source"],
                "category": api_data["intelligence_results_1_category"],
                "data": api_data["intelligence_results_1_data"],
                "timestamp": api_data["intelligence_results_1_timestamp"],
                "confidence": api_data["intelligence_results_1_confidence"]
            }
        ]

        # Construct related_entities
        related_entities = [
            {
                "entity_name": api_data["related_entities_0_entity_name"],
                "relationship_type": api_data["related_entities_0_relationship_type"],
                "source": api_data["related_entities_0_source"],
                "confidence": api_data["related_entities_0_confidence"]
            },
            {
                "entity_name": api_data["related_entities_1_entity_name"],
                "relationship_type": api_data["related_entities_1_relationship_type"],
                "source": api_data["related_entities_1_source"],
                "confidence": api_data["related_entities_1_confidence"]
            }
        ]

        # Construct threat_indicators
        threat_indicators = [
            {
                "indicator_type": api_data["threat_indicators_0_indicator_type"],
                "value": api_data["threat_indicators_0_value"],
                "severity": api_data["threat_indicators_0_severity"],
                "source": api_data["threat_indicators_0_source"],
                "first_seen": api_data["threat_indicators_0_first_seen"]
            },
            {
                "indicator_type": api_data["threat_indicators_1_indicator_type"],
                "value": api_data["threat_indicators_1_value"],
                "severity": api_data["threat_indicators_1_severity"],
                "source": api_data["threat_indicators_1_source"],
                "first_seen": api_data["threat_indicators_1_first_seen"]
            }
        ]

        # Construct metadata
        metadata = {
            "query_timestamp": api_data["metadata_query_timestamp"],
            "execution_time_ms": api_data["metadata_execution_time_ms"],
            "sources_used": [
                api_data["metadata_sources_used_0"],
                api_data["metadata_sources_used_1"]
            ],
            "completion_status": api_data["metadata_completion_status"]
        }

        return {
            "overview": overview,
            "intelligence_results": intelligence_results,
            "related_entities": related_entities,
            "threat_indicators": threat_indicators,
            "metadata": metadata,
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }

    except Exception as e:
        return {
            "overview": {},
            "intelligence_results": [],
            "related_entities": [],
            "threat_indicators": [],
            "metadata": {
                "query_timestamp": datetime.utcnow().isoformat() + "Z",
                "execution_time_ms": 0,
                "sources_used": [],
                "completion_status": "failed"
            },
            "success": False,
            "error_message": str(e)
        }