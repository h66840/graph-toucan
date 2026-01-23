from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for chart generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - chart_url (str): URL string pointing to the generated chart image on quickchart.io
    """
    return {
        "chart_url": "https://quickchart.io/chart?c=%7B%22type%22:%22bar%22,%22data%22:%7B%22labels%22:%5B%22A%22,%22B%22%5D,%22datasets%22:%5B%7B%22label%22:%22Dataset%201%22,%22data%22:%5B10,20%5D%7D%5D%7D%7D"
    }

def quickchart_server_generate_chart(
    datasets: List[Dict[str, Any]],
    labels: Optional[List[str]] = None,
    options: Optional[Dict[str, Any]] = None,
    title: Optional[str] = None,
    type: str = "bar"
) -> Dict[str, str]:
    """
    Generate a chart using QuickChart by simulating an API call.
    
    Args:
        datasets (List[Dict[str, Any]]): Required list of dataset objects containing data and metadata.
        labels (Optional[List[str]]): Optional list of labels for data points.
        options (Optional[Dict[str, Any]]): Optional configuration object for chart appearance.
        title (Optional[str]): Optional title for the chart.
        type (str): Required chart type (e.g., bar, line, pie, doughnut, radar, polarArea, scatter, bubble, radialGauge, speedometer).
    
    Returns:
        Dict[str, str]: A dictionary containing the URL to the generated chart image.
            - chart_url (str): URL string pointing to the generated chart image on quickchart.io
    
    Raises:
        ValueError: If datasets is empty or type is not one of the allowed chart types.
    """
    # Input validation
    if not datasets:
        raise ValueError("Parameter 'datasets' is required and cannot be empty.")
    
    allowed_types = {"bar", "line", "pie", "doughnut", "radar", "polarArea", "scatter", "bubble", "radialGauge", "speedometer"}
    if type not in allowed_types:
        raise ValueError(f"Chart type must be one of {allowed_types}, got '{type}' instead.")
    
    # Simulate external API call
    api_data = call_external_api("quickchart-server-generate_chart")
    
    # Construct result matching output schema
    result = {
        "chart_url": api_data["chart_url"]
    }
    
    return result