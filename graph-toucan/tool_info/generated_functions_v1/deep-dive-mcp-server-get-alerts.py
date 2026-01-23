def deep_dive_mcp_server_get_alerts(state: str) -> dict:
    """
    Get weather alerts for a given state.

    Args:
        state (str): Two-letter state code (e.g., 'CA', 'NY'). Must be a valid U.S. state code.

    Returns:
        dict: A dictionary containing a list of weather alerts. Each alert includes:
            - event (str): Type of weather event (e.g., 'Severe Thunderstorm Warning')
            - area (str): Affected geographic area
            - severity (str): Severity level ('Minor', 'Moderate', 'Severe', 'Extreme')
            - status (str): Current status ('Active', 'Expired', 'Test')
            - headline (str): Brief summary of the alert

    Raises:
        ValueError: If the state code is not a valid two-letter string.
    """
    # Input validation
    if not isinstance(state, str) or len(state) != 2 or not state.isalpha():
        raise ValueError("State must be a valid two-letter string (e.g., 'CA', 'NY')")

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple scalar fields only (str, int, float, bool):
            - alert_0_event (str): Event name for first alert
            - alert_0_area (str): Area affected by first alert
            - alert_0_severity (str): Severity level of first alert
            - alert_0_status (str): Status of first alert
            - alert_0_headline (str): Headline description of first alert
            - alert_1_event (str): Event name for second alert
            - alert_1_area (str): Area affected by second alert
            - alert_1_severity (str): Severity level of second alert
            - alert_1_status (str): Status of second alert
            - alert_1_headline (str): Headline description of second alert
        """
        return {
            "alert_0_event": "Severe Thunderstorm Warning",
            "alert_0_area": f"Central {state.upper()}",
            "alert_0_severity": "Severe",
            "alert_0_status": "Active",
            "alert_0_headline": f"Severe thunderstorms are expected in central {state.upper()} this evening.",
            "alert_1_event": "Flash Flood Watch",
            "alert_1_area": f"Southern {state.upper()}",
            "alert_1_severity": "Moderate",
            "alert_1_status": "Active",
            "alert_1_headline": f"Heavy rains may cause flash flooding in southern {state.upper()} through tomorrow morning."
        }

    try:
        api_data = call_external_api("deep-dive-mcp-server-get-alerts")

        # Construct list of alerts from flattened API response
        alerts = [
            {
                "event": api_data["alert_0_event"],
                "area": api_data["alert_0_area"],
                "severity": api_data["alert_0_severity"],
                "status": api_data["alert_0_status"],
                "headline": api_data["alert_0_headline"]
            },
            {
                "event": api_data["alert_1_event"],
                "area": api_data["alert_1_area"],
                "severity": api_data["alert_1_severity"],
                "status": api_data["alert_1_status"],
                "headline": api_data["alert_1_headline"]
            }
        ]

        return {"alerts": alerts}

    except KeyError as e:
        raise RuntimeError(f"Missing expected data field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process weather alerts: {str(e)}") from e