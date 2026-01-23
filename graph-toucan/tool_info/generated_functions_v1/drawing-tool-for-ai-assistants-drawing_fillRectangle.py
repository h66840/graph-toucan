from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for drawing fillRectangle operation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the operation ("success" or "error")
        - message (str): Human-readable description of the result or error
        - rectangle_x (float): X coordinate of the top-left corner of the rectangle
        - rectangle_y (float): Y coordinate of the top-left corner of the rectangle
        - rectangle_width (float): Width of the rectangle
        - rectangle_height (float): Height of the rectangle
        - color_r (int): Red component of the color (0-255)
        - color_g (int): Green component of the color (0-255)
        - color_b (int): Blue component of the color (0-255)
        - color_a (float): Alpha/transparency component of the color (0.0-1.0), optional
        - operation (str): Name of the operation performed
    """
    return {
        "status": "success",
        "message": "Rectangle filled successfully",
        "rectangle_x": 50.0,
        "rectangle_y": 30.0,
        "rectangle_width": 100.0,
        "rectangle_height": 80.0,
        "color_r": 255,
        "color_g": 0,
        "color_b": 0,
        "color_a": 1.0,
        "operation": "fillRectangle"
    }

def drawing_tool_for_ai_assistants_drawing_fillRectangle(
    color: Dict[str, Any], 
    height: float, 
    width: float, 
    x: float, 
    y: float
) -> Dict[str, Any]:
    """
    Fill a rectangle on the drawing canvas with a specified color and coordinates.
    
    Args:
        color (Dict[str, Any]): Color to fill the rectangle with (RGB). Must contain 'r', 'g', 'b' keys with values in range 0-255.
                               Optionally may contain 'a' for alpha (transparency) in range 0.0-1.0.
        height (float): Height of the rectangle (must be positive)
        width (float): Width of the rectangle (must be positive)
        x (float): X coordinate of the top-left corner of the rectangle
        y (float): Y coordinate of the top-left corner of the rectangle
    
    Returns:
        Dict containing:
        - status (str): status of the operation ("success" or "error")
        - message (str): human-readable description of the result or error
        - rectangle (Dict): contains details about the rectangle that was filled, with 'x', 'y', 'width', 'height' fields
        - color (Dict): contains the color used for filling, with 'r', 'g', 'b', 'a' fields (a is optional)
        - operation (str): name of the operation performed, e.g. "fillRectangle"
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not isinstance(color, dict):
        return {
            "status": "error",
            "message": "Color must be a dictionary with 'r', 'g', 'b' keys",
            "operation": "fillRectangle"
        }
    
    required_color_keys = ['r', 'g', 'b']
    for key in required_color_keys:
        if key not in color:
            return {
                "status": "error",
                "message": f"Missing required color component: {key}",
                "operation": "fillRectangle"
            }
    
    # Validate color values
    for key in required_color_keys:
        if not isinstance(color[key], (int, float)) or color[key] < 0 or color[key] > 255:
            return {
                "status": "error",
                "message": f"Color component {key} must be a number between 0 and 255",
                "operation": "fillRectangle"
            }
    
    # Validate alpha if present
    if 'a' in color and (not isinstance(color['a'], (int, float)) or color['a'] < 0.0 or color['a'] > 1.0):
        return {
            "status": "error",
            "message": "Alpha component must be a number between 0.0 and 1.0",
            "operation": "fillRectangle"
        }
    
    # Validate dimensions
    if not isinstance(width, (int, float)) or width <= 0:
        return {
            "status": "error",
            "message": "Width must be a positive number",
            "operation": "fillRectangle"
        }
    
    if not isinstance(height, (int, float)) or height <= 0:
        return {
            "status": "error",
            "message": "Height must be a positive number",
            "operation": "fillRectangle"
        }
    
    if not isinstance(x, (int, float)):
        return {
            "status": "error",
            "message": "X coordinate must be a number",
            "operation": "fillRectangle"
        }
    
    if not isinstance(y, (int, float)):
        return {
            "status": "error",
            "message": "Y coordinate must be a number",
            "operation": "fillRectangle"
        }
    
    try:
        # Call external API to simulate the drawing operation
        api_data = call_external_api("drawing-tool-for-ai-assistants-drawing_fillRectangle")
        
        # Construct the nested output structure from flat API data
        result = {
            "status": api_data["status"],
            "message": api_data["message"],
            "operation": api_data["operation"],
            "rectangle": {
                "x": float(x),
                "y": float(y),
                "width": float(width),
                "height": float(height)
            },
            "color": {
                "r": int(color["r"]),
                "g": int(color["g"]),
                "b": int(color["b"])
            }
        }
        
        # Add alpha if provided
        if 'a' in color:
            result["color"]["a"] = float(color["a"])
        elif "color_a" in api_data:
            result["color"]["a"] = api_data["color_a"]
            
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fill rectangle: {str(e)}",
            "operation": "fillRectangle"
        }