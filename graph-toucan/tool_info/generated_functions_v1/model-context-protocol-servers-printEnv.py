from typing import Dict, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching environment variables from an external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - env_VAR_0_key (str): First environment variable name
        - env_VAR_0_value (str): First environment variable value
        - env_VAR_1_key (str): Second environment variable name
        - env_VAR_1_value (str): Second environment variable value
    """
    return {
        "env_VAR_0_key": "PATH",
        "env_VAR_0_value": "/usr/local/bin:/usr/bin:/bin",
        "env_VAR_1_key": "HOME",
        "env_VAR_1_value": "/home/user"
    }


def model_context_protocol_servers_printEnv() -> Dict[str, Dict[str, str]]:
    """
    Prints all environment variables, helpful for debugging MCP server configuration.

    This function retrieves environment variables from the system and returns them
    as a dictionary mapping variable names to their string values.

    Returns:
        Dict[str, str]: A dictionary where keys are environment variable names
                       and values are their corresponding string values.
    """
    try:
        # Use call_external_api as per instructions and reconstruct the output
        api_data = call_external_api("model-context-protocol-servers-printEnv")

        # Construct the environment_variables dict from the flattened API response
        reconstructed_env = {}
        for i in range(2):  # We expect 2 items as per instructions
            key_field = f"env_VAR_{i}_key"
            value_field = f"env_VAR_{i}_value"
            if key_field in api_data and value_field in api_data:
                reconstructed_env[api_data[key_field]] = api_data[value_field]

        return {"environment_variables": reconstructed_env}

    except Exception as e:
        # In case of any error, return at least an empty dict
        return {"environment_variables": {}}