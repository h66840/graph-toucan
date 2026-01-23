from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAI Agents SDK documentation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - documentation_description (str): Description of the class or function
        - documentation_parameters (str): JSON string representing parameters
        - documentation_return_value (str): Description of return value
        - documentation_examples (str): JSON string representing example usages
        - found (bool): Whether the requested item was found
        - type (str): Type of the item, either 'class' or 'function'
        - version (str): SDK version
        - related_items_0 (str): First related item name
        - related_items_1 (str): Second related item name
        - errors_0_message (str): Error message for first error
        - errors_0_code (str): Error code for first error
        - errors_1_message (str): Error message for second error
        - errors_1_code (str): Error code for second error
    """
    return {
        "documentation_description": "A helper class to manage agent conversations and tool calls.",
        "documentation_parameters": '{"agent_id": {"type": "str", "description": "Unique identifier for the agent"}, "tools": {"type": "list", "description": "List of tools available to the agent"}}',
        "documentation_return_value": "Returns an instance of AgentManager configured with the provided settings.",
        "documentation_examples": '[{"code": "agent = AgentManager(agent_id=\\"123\\")", "description": "Create a new agent manager"}]',
        "found": True,
        "type": "class",
        "version": "0.12.3",
        "related_items_0": "Agent",
        "related_items_1": "ToolExecutor",
        "errors_0_message": "",
        "errors_0_code": "",
        "errors_1_message": "",
        "errors_1_code": ""
    }

def openai_agent_library_get_api_docs(class_or_function: str) -> Dict[str, Any]:
    """
    Get API documentation for a specific class or function in the OpenAI Agents SDK.

    Args:
        class_or_function (str): The name of the class or function to retrieve documentation for.

    Returns:
        Dict containing:
            - documentation (Dict): Detailed API documentation including description, parameters, return value, and examples
            - found (bool): Whether the requested item was found
            - type (str): Type of the item ('class' or 'function')
            - version (str): SDK version
            - related_items (List[str]): List of related classes or functions
            - errors (List[Dict]): List of error objects with message and code if any issues occurred
    """
    if not class_or_function or not isinstance(class_or_function, str):
        return {
            "documentation": {
                "description": "",
                "parameters": {},
                "return_value": "",
                "examples": []
            },
            "found": False,
            "type": "",
            "version": "",
            "related_items": [],
            "errors": [
                {"message": "Invalid input: class_or_function must be a non-empty string", "code": "INVALID_INPUT"}
            ]
        }

    api_data = call_external_api("openai-agent-library-get_api_docs")

    # Construct nested documentation object
    try:
        import json
        parameters = json.loads(api_data["documentation_parameters"])
    except:
        parameters = {}

    try:
        examples = json.loads(api_data["documentation_examples"])
    except:
        examples = []

    # Build errors list from flattened fields
    errors = []
    if api_data.get("errors_0_message") or api_data.get("errors_0_code"):
        errors.append({
            "message": api_data["errors_0_message"],
            "code": api_data["errors_0_code"]
        })
    if api_data.get("errors_1_message") or api_data.get("errors_1_code"):
        errors.append({
            "message": api_data["errors_1_message"],
            "code": api_data["errors_1_code"]
        })

    # Build related items list
    related_items = []
    if api_data.get("related_items_0"):
        related_items.append(api_data["related_items_0"])
    if api_data.get("related_items_1"):
        related_items.append(api_data["related_items_1"])

    result = {
        "documentation": {
            "description": api_data["documentation_description"],
            "parameters": parameters,
            "return_value": api_data["documentation_return_value"],
            "examples": examples
        },
        "found": api_data["found"],
        "type": api_data["type"],
        "version": api_data["version"],
        "related_items": related_items,
        "errors": errors
    }

    return result