from typing import Dict, List, Any, Optional

def ennkaheksa_validate_node_operation(config: Dict[str, Any], nodeType: str, profile: Optional[str] = "ai-friendly") -> Dict[str, Any]:
    """
    Validates a node configuration based on the specified node type and validation profile.
    
    Args:
        config (Dict[str, Any]): The node configuration to validate. Must include operation fields if applicable.
        nodeType (str): The type of node being validated (e.g., "nodes-base.slack").
        profile (Optional[str]): Validation profile to use. Options: 'minimal', 'runtime', 'ai-friendly', 'strict'.
                                Defaults to 'ai-friendly'.
    
    Returns:
        Dict[str, Any]: A dictionary containing validation results including:
            - nodeType (str): Type of the node being validated
            - displayName (str): User-friendly name of the node
            - valid (bool): Whether the configuration is valid
            - errors (List[Dict]): List of validation errors with type, property, message, and fix
            - warnings (List[Dict]): List of warnings with type, property, message, and suggestion
            - suggestions (List[str]): General suggestions for improvement
            - visibleProperties (List[str]): Properties currently visible and active
            - hiddenProperties (List[str]): Properties hidden due to current settings
            - mode (str): Validation mode used (e.g., "operation")
            - profile (str): Validation profile applied
            - operation (Dict): Operation context (resource, operation, etc.)
            - examples (List[Dict]): Working configuration examples
            - nextSteps (List[str]): Recommended actions
            - summary (Dict): Summary of results with hasErrors, errorCount, warningCount, suggestionCount
    """
    # Default validation result structure
    result = {
        "nodeType": nodeType,
        "displayName": nodeType.split('.')[-1].replace('-', ' ').title(),
        "valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": [],
        "visibleProperties": [],
        "hiddenProperties": [],
        "mode": "operation",
        "profile": profile or "ai-friendly",
        "operation": {},
        "examples": [],
        "nextSteps": [],
        "summary": {
            "hasErrors": False,
            "errorCount": 0,
            "warningCount": 0,
            "suggestionCount": 0
        }
    }

    # Extract operation context if present
    resource = config.get("resource")
    operation = config.get("operation") or config.get("action")
    if resource or operation:
        result["operation"] = {"resource": resource, "operation": operation}

    # Determine visible and hidden properties based on conditional logic in config
    # This is a simplified simulation - real implementation would inspect node schema
    all_properties = list(config.keys())
    result["visibleProperties"] = [p for p in all_properties if p not in ["credentials", "authentication"]]
    result["hiddenProperties"] = [p for p in all_properties if p in ["credentials", "authentication"]]

    # Validate required fields based on node type and operation
    required_fields = []
    if nodeType == "nodes-base.slack":
        if operation == "send":
            required_fields = ["channel"]
        elif operation == "postMessage":
            required_fields = ["channel", "message"]
    elif nodeType == "n8n-nodes-base.google-sheets":
        required_fields = ["sheetName", "range"]
    elif nodeType == "n8n-nodes-base.mongodb":
        required_fields = ["collection", "operation"]
    elif nodeType == "n8n-nodes-base.openai":
        required_fields = ["resource", "operation", "model"]

    for field in required_fields:
        if field not in config:
            result["valid"] = False
            result["errors"].append({
                "type": "required",
                "property": field,
                "message": f"{field.replace('-', ' ').title()} is required for this operation.",
                "fix": f"Add '{field}' to your configuration."
            })

    # Type and format validation (simplified)
    for key, value in config.items():
        if key.endswith("Id") and not isinstance(value, str):
            result["valid"] = False
            result["errors"].append({
                "type": "type",
                "property": key,
                "message": f"{key} must be a string.",
                "fix": f"Ensure {key} is a string value."
            })
        elif key == "timeout" and not isinstance(value, (int, float)):
            result["valid"] = False
            result["errors"].append({
                "type": "type",
                "property": key,
                "message": f"{key} must be a number.",
                "fix": f"Set {key} to a numeric value."
            })

    # Operation-specific rules
    if nodeType == "nodes-base.slack" and operation == "send":
        if "channel" in config and not config["channel"].startswith(("#", "@")):
            result["valid"] = False
            result["errors"].append({
                "type": "format",
                "property": "channel",
                "message": "Slack channel must start with # or @.",
                "fix": "Use '#general' for channels or '@user' for mentions."
            })

    # Warnings for common issues
    if "credentials" not in config and "apiKey" not in config:
        result["warnings"].append({
            "type": "security",
            "property": "authentication",
            "message": "No authentication method configured.",
            "suggestion": "Add credentials or API key for secure access."
        })

    if "timeout" in config and config["timeout"] > 30000:
        result["warnings"].append({
            "type": "performance",
            "property": "timeout",
            "message": "High timeout value may cause delays.",
            "suggestion": "Consider reducing timeout to 30 seconds or less."
        })

    # Suggestions for improvement
    if "description" not in config:
        result["suggestions"].append("Add a description to document this node's purpose.")

    if "rateLimit" not in config and nodeType in ["nodes-base.slack", "n8n-nodes-base.google-sheets"]:
        result["suggestions"].append("Consider adding rate limiting to avoid API throttling.")

    # Examples based on node type
    if nodeType == "nodes-base.slack" and operation == "send":
        result["examples"].append({
            "description": "Send message to #general channel",
            "config": {
                "resource": "message",
                "operation": "send",
                "channel": "#general",
                "message": "Hello from n8n!"
            }
        })

    # Next steps
    if not result["valid"]:
        result["nextSteps"].append("Fix all validation errors before deploying.")
        if result["suggestions"]:
            result["nextSteps"].append("Apply suggestions to improve configuration quality.")
    else:
        result["nextSteps"].append("Configuration is valid. You can now use this node in your workflow.")

    # Update summary
    result["summary"]["hasErrors"] = not result["valid"]
    result["summary"]["errorCount"] = len(result["errors"])
    result["summary"]["warningCount"] = len(result["warnings"])
    result["summary"]["suggestionCount"] = len(result["suggestions"])

    return result