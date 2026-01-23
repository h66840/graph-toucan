def weather_server_ping() -> dict:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.
    
    Returns:
        dict: A dictionary containing the server's response to the ping request,
              indicating its operational status.
        - response (str): The server's response message indicating operational status.
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - response (str): Server response message indicating status ('OK' or similar).
        """
        return {
            "response": "OK"
        }

    try:
        # Validate tool name input for safety even though no external input is used
        if not isinstance("weather-server-ping", str):
            raise ValueError("Tool name must be a string.")

        # Fetch simulated external data
        api_data = call_external_api("weather-server-ping")

        # Construct result according to output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except Exception as e:
        # Handle any unexpected errors during execution
        return {
            "response": f"Error: {str(e)}"
        }