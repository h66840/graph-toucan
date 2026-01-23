from typing import Dict, Any, Optional
import json

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for chart image generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the request, either "success" or "error"
        - message (str): URL link to the generated chart image from quickchart.io
    """
    return {
        "status": "success",
        "message": "https://quickchart.io/chart?c=%7B%22type%22:%22bar%22,%22data%22:%7B%22labels%22:%5B%22A%22,%22B%22,%22C%22%5D,%22datasets%22:%5B%7B%22label%22:%22Sample%20Data%22,%22data%22:%5B1,2,3%5D%7D%5D%7D%7D"
    }

def quick_chart_server_GetChartImgLink(json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generates a chart image URL using the Quick Chart API (quickchart.io) based on provided configuration.

    This function simulates the behavior of generating a chart image link by using a mock external API call.
    The input is a JSON object that conforms to the Quick Chart API format (without functions, only values).
    The output contains a status and a message with the encoded URL to the generated chart image.

    Args:
        json (Optional[Dict[str, Any]]): Configuration parameters for the chart in JSON format,
            following the Quick Chart API specification. If not provided, a default chart is generated.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): "success" if the operation was successful, "error" otherwise
            - message (str): The URL to the generated chart image, encoded with the chart configuration
    """
    try:
        # Use default chart configuration if none provided
        if json is None:
            chart_config = {
                "type": "bar",
                "data": {
                    "labels": ["A", "B", "C"],
                    "datasets": [{"label": "Sample Data", "data": [1, 2, 3]}]
                }
            }
        else:
            chart_config = json
        
        # Validate that chart_config is a dictionary
        if not isinstance(chart_config, dict):
            return {
                "status": "error",
                "message": "Chart configuration must be a JSON object"
            }
        
        # Call the external API simulation
        api_data = call_external_api("quick-chart-server-GetChartImgLink")
        
        # Construct the result using the data from the external API
        result = {
            "status": api_data["status"],
            "message": api_data["message"]
        }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }