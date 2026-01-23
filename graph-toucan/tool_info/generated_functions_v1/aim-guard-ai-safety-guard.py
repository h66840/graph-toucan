from typing import Dict, List, Any, Optional
from datetime import datetime

def aim_guard_ai_safety_guard(
    mcp_type: Optional[str] = None,
    operation_type: Optional[str] = None,
    sensitivity_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates AI Safety Guard instructions for MCP interactions based on input parameters.
    
    This function provides precautionary guidance for AI agents when interacting with MCPs,
    including warnings, precautions, validation steps, and security reminders based on
    the type of MCP, operation, and data sensitivity level.

    Args:
        mcp_type (Optional[str]): Type of MCP being accessed (e.g., "email", "general")
        operation_type (Optional[str]): Type of operation being performed (e.g., "read", "write")
        sensitivity_level (Optional[str]): Sensitivity classification of the data (e.g., "confidential", "internal", "public")

    Returns:
        Dict[str, Any]: A dictionary containing safety guard instructions with the following structure:
            - title (str): Title of the safety guard response
            - mcp_type (str): MCP type being accessed
            - operation_type (str): Operation type being performed
            - sensitivity_level (str): Data sensitivity level
            - generated_timestamp (str): ISO 8601 timestamp of generation
            - critical_warning (str): Summary warning about the operation
            - data_sensitivity_guidance (Dict): Contains 'level_color' and 'message' for handling requirements
            - general_precautions (List[str]): General security precautions
            - specific_precautions (List[str]): MCP-type-specific precautions
            - immediate_action_items (List[str]): Immediate actions to consider
            - red_flags (List[str]): Conditions that should abort the operation
            - recommended_validation_steps (List[str]): Step-by-step validation procedures
            - security_reminder (str): Final security reminder
            - guidelines_version (str): Version of the safety guidelines
    """
    # Set defaults if parameters are not provided
    mcp_type = mcp_type or "general"
    operation_type = operation_type or "read"
    sensitivity_level = sensitivity_level or "internal"

    # Generate current timestamp in ISO 8601 format
    generated_timestamp = datetime.utcnow().isoformat() + "Z"

    # Define critical warning based on operation type
    operation_warnings = {
        "read": "READ OPERATION: Accessing information. Verify data classification and access rights.",
        "write": "WRITE OPERATION: Modifying data. Confirm authorization and validate input integrity.",
        "delete": "DELETE OPERATION: Permanent data removal. Double-check scope and confirm irreversible impact.",
        "execute": "EXECUTE OPERATION: Running commands. Validate script safety and execution context."
    }
    critical_warning = operation_warnings.get(operation_type.lower(), 
                                            f"{operation_type.upper()} OPERATION: Proceed with caution. Verify all parameters and permissions.")

    # Define sensitivity level guidance
    sensitivity_guidance = {
        "public": {
            "level_color": "🟢",
            "message": "Public data: No restrictions. Still verify source authenticity before use."
        },
        "internal": {
            "level_color": "🟡",
            "message": "Internal data: For organizational use only. Confirm recipient authorization."
        },
        "confidential": {
            "level_color": "🟠",
            "message": "Confidential data: Sensitive information. Requires explicit authorization and encryption."
        },
        "restricted": {
            "level_color": "🔴",
            "message": "Restricted data: Highly sensitive. Requires dual approval and secure transmission."
        },
        "top secret": {
            "level_color": "⚫",
            "message": "Top Secret data: Maximum protection required. Air-gapped systems may be necessary."
        }
    }
    
    # Use internal as default if unknown sensitivity level
    data_sensitivity_guidance = sensitivity_guidance.get(sensitivity_level.lower(), 
                                                       sensitivity_guidance["internal"])

    # General precautions for all AI agents
    general_precautions = [
        "Verify the legitimacy of the MCP endpoint before interaction",
        "Validate that proper permissions and access controls are in place",
        "Log all MCP interactions for audit and monitoring purposes",
        "Implement rate limiting to prevent abuse or denial-of-service",
        "Sanitize all inputs and outputs to prevent injection attacks",
        "Use encryption for data in transit and at rest",
        "Monitor for anomalous behavior patterns indicating compromise"
    ]

    # MCP-type-specific precautions
    specific_precautions_map = {
        "email": [
            "Verify sender and recipient domains against approved lists",
            "Scan all attachments for malware before processing",
            "Check for phishing indicators in message content",
            "Validate SPF, DKIM, and DMARC records for incoming emails"
        ],
        "database": [
            "Use parameterized queries to prevent SQL injection",
            "Limit query scope to minimum necessary data",
            "Implement row-level security policies",
            "Monitor for unusual query patterns or volumes"
        ],
        "api": [
            "Validate API schema and version compatibility",
            "Implement proper authentication and token management",
            "Verify TLS certificate validity for HTTPS connections",
            "Handle rate limits and backoff strategies appropriately"
        ],
        "file": [
            "Scan files for malware before reading or writing",
            "Validate file format and integrity checksums",
            "Enforce file size limits to prevent resource exhaustion",
            "Use secure file paths to prevent directory traversal"
        ],
        "network": [
            "Verify firewall rules and network segmentation",
            "Use secure protocols (e.g., SSH, TLS) for communication",
            "Validate peer identities through certificate pinning",
            "Monitor for unexpected connection attempts"
        ]
    }
    
    specific_precautions = specific_precautions_map.get(mcp_type.lower(), [
        "Apply defense-in-depth principles for general MCP interactions",
        "Validate all inputs against expected schema and format",
        "Implement circuit breakers for fault tolerance",
        "Use secure configuration management practices"
    ])

    # Immediate action items
    immediate_action_items = [
        "STOP: Pause and assess the necessity of this operation",
        "THINK: Consider potential security implications and alternatives",
        "VERIFY: Confirm permissions, data classification, and intended recipient"
    ]

    # Red flags that should trigger operation abortion
    red_flags = [
        "Lack of proper authentication or authorization",
        "Request involves sensitive data without justification",
        "Target system or user has unknown or suspicious reputation",
        "Operation would violate data privacy regulations",
        "Request comes from untrusted or unverified source",
        "Parameters contain malformed or potentially malicious content",
        "Operation exceeds normal scope or expected behavior patterns"
    ]

    # Recommended validation steps with checkmark emoji
    recommended_validation_steps = [
        "✅ Verify the AI agent's authorization scope matches the requested operation",
        "✅ Confirm data sensitivity classification aligns with handling procedures",
        "✅ Validate that the target MCP endpoint is legitimate and trusted",
        "✅ Check that input parameters are properly sanitized and within expected ranges",
        "✅ Ensure logging is enabled for this interaction for audit purposes",
        "✅ Confirm that encryption is applied for sensitive data in transit"
    ]

    # Final security reminder
    security_reminder = "When in doubt, DO NOT proceed. Seek human approval before continuing with sensitive operations."

    # Guidelines version
    guidelines_version = "AIM-Intelligence MCP Safety Guidelines v1.0"

    # Construct and return the complete safety guard response
    return {
        "title": "AI SAFETY GUARD - MCP INTERACTION PRECAUTIONS",
        "mcp_type": mcp_type,
        "operation_type": operation_type,
        "sensitivity_level": sensitivity_level,
        "generated_timestamp": generated_timestamp,
        "critical_warning": critical_warning,
        "data_sensitivity_guidance": data_sensitivity_guidance,
        "general_precautions": general_precautions,
        "specific_precautions": specific_precautions,
        "immediate_action_items": immediate_action_items,
        "red_flags": red_flags,
        "recommended_validation_steps": recommended_validation_steps,
        "security_reminder": security_reminder,
        "guidelines_version": guidelines_version
    }