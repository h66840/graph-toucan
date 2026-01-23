from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node configuration based on task.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - task (str): Task identifier
        - description (str): Description of the node's function
        - nodeType (str): Type identifier of the node
        - configuration_url (str): URL field in configuration
        - configuration_method (str): HTTP method in configuration
        - configuration_headers_content_type (str): Content-Type header
        - configuration_headers_authorization (str): Authorization header template
        - userMustProvide_0_property (str): First user-provided property name
        - userMustProvide_0_description (str): Description of first user-provided property
        - userMustProvide_0_example (str): Example value for first user-provided property
        - userMustProvide_1_property (str): Second user-provided property name
        - userMustProvide_1_description (str): Description of second user-provided property
        - userMustProvide_1_example (str): Example value for second user-provided property
        - optionalEnhancements_0_property (str): First optional enhancement property
        - optionalEnhancements_0_description (str): Description of first optional enhancement
        - optionalEnhancements_1_property (str): Second optional enhancement property
        - optionalEnhancements_1_description (str): Description of second optional enhancement
        - notes_0 (str): First note about usage
        - notes_1 (str): Second note about usage
        - example_node_type (str): Node type in example
        - example_node_parameters_url (str): URL parameter in example
        - example_node_parameters_body_json (str): Body JSON in example
        - example_userInputsNeeded_0_property (str): First user input needed in example
        - example_userInputsNeeded_0_currentValue (str): Current value of first user input
        - example_userInputsNeeded_0_description (str): Description of first user input
        - example_userInputsNeeded_0_example (str): Example value of first user input
        - example_userInputsNeeded_1_property (str): Second user input needed in example
        - example_userInputsNeeded_1_currentValue (str): Current value of second user input
        - example_userInputsNeeded_1_description (str): Description of second user input
        - example_userInputsNeeded_1_example (str): Example value of second user input
    """
    return {
        "task": "post_json_request",
        "description": "Sends a JSON payload to a specified API endpoint using POST method.",
        "nodeType": "http_request",
        "configuration_url": "https://api.example.com/data",
        "configuration_method": "POST",
        "configuration_headers_content_type": "application/json",
        "configuration_headers_authorization": "Bearer {{auth_token}}",
        "userMustProvide_0_property": "auth_token",
        "userMustProvide_0_description": "Authentication token for the API",
        "userMustProvide_0_example": "abc123xyz",
        "userMustProvide_1_property": "payload",
        "userMustProvide_1_description": "JSON data to send in the request body",
        "userMustProvide_1_example": '{"name": "John", "email": "john@example.com"}',
        "optionalEnhancements_0_property": "timeout",
        "optionalEnhancements_0_description": "Request timeout in seconds",
        "optionalEnhancements_1_property": "retry_count",
        "optionalEnhancements_1_description": "Number of times to retry on failure",
        "notes_0": "Ensure the target API accepts JSON content type.",
        "notes_1": "Use environment variables to store sensitive data like tokens.",
        "example_node_type": "http_request",
        "example_node_parameters_url": "https://api.example.com/users",
        "example_node_parameters_body_json": '{"name": "{{user_name}}", "email": "{{user_email}}"}',
        "example_userInputsNeeded_0_property": "user_name",
        "example_userInputsNeeded_0_currentValue": "Alice",
        "example_userInputsNeeded_0_description": "Name of the user to create",
        "example_userInputsNeeded_0_example": "Alice Smith",
        "example_userInputsNeeded_1_property": "user_email",
        "example_userInputsNeeded_1_currentValue": "alice@example.com",
        "example_userInputsNeeded_1_description": "Email address of the user",
        "example_userInputsNeeded_1_example": "alice@example.com"
    }

def ennkaheksa_get_node_for_task(task: str) -> Dict[str, Any]:
    """
    Get pre-configured node settings for common tasks. USE THIS to quickly configure nodes
    for specific use cases like "post_json_request", "receive_webhook", "query_database", etc.
    Returns ready-to-use configuration with clear indication of what user must provide.
    Much faster than figuring out configuration from scratch.

    Args:
        task (str): The task to accomplish. Available tasks: get_api_data, post_json_request,
                    call_api_with_auth, receive_webhook, webhook_with_response, query_postgres,
                    insert_postgres_data, chat_with_ai, ai_agent_workflow, transform_data,
                    filter_data, send_slack_message, send_email.

    Returns:
        Dict containing:
        - task (str): the task identifier for which the node is configured
        - description (str): a human-readable description of what the node does
        - nodeType (str): the type identifier of the node used in the system
        - configuration (Dict): key-value pairs representing the pre-filled configuration
        - userMustProvide (List[Dict]): list of properties that the user must supply,
          each with 'property', 'description', and 'example' fields
        - optionalEnhancements (List[Dict]): list of optional features that can be added,
          each with 'property' and 'description' fields
        - notes (List[str]): additional informational notes about usage or constraints
        - example (Dict): contains sample node configuration and user inputs; includes
          'node' (with 'type' and 'parameters') and 'userInputsNeeded' (list of dicts)
    """
    if not task:
        raise ValueError("Parameter 'task' is required.")
    
    valid_tasks = [
        "get_api_data", "post_json_request", "call_api_with_auth", "receive_webhook",
        "webhook_with_response", "query_postgres", "insert_postgres_data", "chat_with_ai",
        "ai_agent_workflow", "transform_data", "filter_data", "send_slack_message", "send_email"
    ]
    
    if task not in valid_tasks:
        raise ValueError(f"Invalid task '{task}'. Valid tasks are: {', '.join(valid_tasks)}")

    api_data = call_external_api("ennkaheksa-get_node_for_task")

    # Reconstruct nested configuration
    configuration = {
        "url": api_data["configuration_url"],
        "method": api_data["configuration_method"],
        "headers": {
            "Content-Type": api_data["configuration_headers_content_type"],
            "Authorization": api_data["configuration_headers_authorization"]
        }
    }

    userMustProvide = [
        {
            "property": api_data["userMustProvide_0_property"],
            "description": api_data["userMustProvide_0_description"],
            "example": api_data["userMustProvide_0_example"]
        },
        {
            "property": api_data["userMustProvide_1_property"],
            "description": api_data["userMustProvide_1_description"],
            "example": api_data["userMustProvide_1_example"]
        }
    ]

    optionalEnhancements = [
        {
            "property": api_data["optionalEnhancements_0_property"],
            "description": api_data["optionalEnhancements_0_description"]
        },
        {
            "property": api_data["optionalEnhancements_1_property"],
            "description": api_data["optionalEnhancements_1_description"]
        }
    ]

    notes = [
        api_data["notes_0"],
        api_data["notes_1"]
    ]

    example = {
        "node": {
            "type": api_data["example_node_type"],
            "parameters": {
                "url": api_data["example_node_parameters_url"],
                "body": {
                    "json": api_data["example_node_parameters_body_json"]
                }
            }
        },
        "userInputsNeeded": [
            {
                "property": api_data["example_userInputsNeeded_0_property"],
                "currentValue": api_data["example_userInputsNeeded_0_currentValue"],
                "description": api_data["example_userInputsNeeded_0_description"],
                "example": api_data["example_userInputsNeeded_0_example"]
            },
            {
                "property": api_data["example_userInputsNeeded_1_property"],
                "currentValue": api_data["example_userInputsNeeded_1_currentValue"],
                "description": api_data["example_userInputsNeeded_1_description"],
                "example": api_data["example_userInputsNeeded_1_example"]
            }
        ]
    }

    return {
        "task": api_data["task"],
        "description": api_data["description"],
        "nodeType": api_data["nodeType"],
        "configuration": configuration,
        "userMustProvide": userMustProvide,
        "optionalEnhancements": optionalEnhancements,
        "notes": notes,
        "example": example
    }