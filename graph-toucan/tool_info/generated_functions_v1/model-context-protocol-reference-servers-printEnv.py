from typing import Dict, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching environment variables from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - env_0_key (str): First environment variable name
        - env_0_value (str): First environment variable value
        - env_1_key (str): Second environment variable name
        - env_1_value (str): Second environment variable value
    """
    return {
        "env_0_key": "PATH",
        "env_0_value": "/usr/local/bin:/usr/bin:/bin",
        "env_1_key": "HOME",
        "env_1_value": "/home/user"
    }


def model_context_protocol_reference_servers_printEnv() -> Dict[str, Dict[str, str]]:
    """
    Prints all environment variables, helpful for debugging MCP server configuration.

    Returns:
        Dict containing a single key 'environment_variables' mapping environment variable names to their string values.
    """
    try:
        # Use the external API simulation to get environment variables instead of os.environ
        api_data = call_external_api("model-context-protocol-reference-servers-printEnv")
        env_vars = {
            api_data["env_0_key"]: api_data["env_0_value"],
            api_data["env_1_key"]: api_data["env_1_value"]
        }

        return {
            "environment_variables": env_vars
        }

    except Exception as e:
        # In case of any error, return empty environment variables dict
        return {
            "environment_variables": {}
        }