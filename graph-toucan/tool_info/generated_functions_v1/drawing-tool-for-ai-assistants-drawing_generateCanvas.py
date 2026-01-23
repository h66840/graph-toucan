def drawing_tool_for_ai_assistants_drawing_generateCanvas(height: float, width: float) -> dict:
    """
    Generate a new drawing canvas with specified width and height.

    This function creates a canvas representation based on the provided dimensions.
    It validates the input parameters to ensure they are positive numbers and returns
    a dictionary containing the canvas properties including width, height, and status.

    Args:
        height (float): Height of the canvas in pixels. Must be a positive number.
        width (float): Width of the canvas in pixels. Must be a positive number.

    Returns:
        dict: A dictionary containing:
            - width (int): Width of the generated canvas in pixels
            - height (int): Height of the generated canvas in pixels
            - status (str): Status message indicating success, e.g., "Canvas generated"

    Raises:
        ValueError: If height or width is not a positive number
        TypeError: If height or width is not a number
    """
    # Input validation
    if not isinstance(width, (int, float)):
        raise TypeError("Width must be a number")
    if not isinstance(height, (int, float)):
        raise TypeError("Height must be a number")
    
    if width <= 0:
        raise ValueError("Width must be a positive number")
    if height <= 0:
        raise ValueError("Height must be a positive number")
    
    # Convert to integers (pixel values must be whole numbers)
    canvas_width = int(width)
    canvas_height = int(height)
    
    # Return the canvas data structure
    return {
        "width": canvas_width,
        "height": canvas_height,
        "status": "Canvas generated"
    }