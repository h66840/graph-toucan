from typing import Dict, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - response (str): the response message from the server indicating its availability status
    """
    return {
        "response": "Server is responsive and operational"
    }


def lyrical_mcp_ping() -> Dict[str, str]:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.

    This function simulates a ping to a server by calling an external API
    and retrieving a status message about the server's availability.

    Returns:
        Dict containing:
        - response (str): the response message from the server indicating its availability status
    """
    try:
        # Call external API to get ping response
        api_data = call_external_api("lyrical-mcp-ping")

        # Construct result matching output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except KeyError as e:
        return {
            "response": f"Error: Missing expected data field {str(e)}"
        }
    except Exception as e:
        return {
            "response": f"Error occurred during ping: {str(e)}"
        }