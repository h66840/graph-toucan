from typing import Dict, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - response (str): the server's response indicating its availability, typically "pong" when reachable
    """
    return {
        "response": "pong"
    }


def weather_information_server_ping() -> Dict[str, Any]:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.

    This function simulates a ping to the weather information server by calling an external API
    and returning the server's response. It is used to check if the server is reachable and responsive.

    Returns:
        Dict[str, Any]: A dictionary containing the server's response with the following structure:
            - response (str): the server's response indicating its availability, typically "pong" when reachable
    """
    try:
        # Call external API to get the response
        api_data = call_external_api("weather-information-server-ping")

        # Construct the result dictionary matching the output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except Exception as e:
        # In case of any error, return an error response
        return {
            "response": f"error: {str(e)}"
        }