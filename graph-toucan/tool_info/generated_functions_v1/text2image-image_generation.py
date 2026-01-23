from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for image generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_url (str): URL of the generated image
        - prompt_description (str): Detailed textual description used to generate the image
    """
    return {
        "image_url": "https://example.com/generated-image.png",
        "prompt_description": "A beautiful sunset over a calm ocean with golden reflections on the water, seagulls flying in the sky, and a silhouette of a lighthouse on a rocky shore."
    }

def text2image_image_generation(
    image_prompt: str, 
    width: Optional[int] = 1024, 
    height: Optional[int] = 1024
) -> Dict[str, Any]:
    """
    Generates an image based on a detailed description derived from the input prompt.
    The function simulates calling an external image generation service and returns the image URL
    along with the detailed description used for generation.
    
    :param image_prompt: A short English description of the desired image (required)
    :param width: Width of the generated image in pixels (optional, default 1024)
    :param height: Height of the generated image in pixels (optional, default 1024)
    :return: Dictionary containing the image URL and the detailed prompt description used
    """
    if not image_prompt.strip():
        raise ValueError("image_prompt is required and cannot be empty or whitespace only.")
    
    if width is not None and (width <= 0 or width > 4096):
        raise ValueError("width must be a positive integer and less than or equal to 4096.")
    
    if height is not None and (height <= 0 or height > 4096):
        raise ValueError("height must be a positive integer and less than or equal to 4096.")
    
    # Simulate calling external API
    api_data = call_external_api("text2image-image_generation")
    
    # Construct result matching output schema
    result = {
        "image_url": api_data["image_url"],
        "prompt_description": api_data["prompt_description"]
    }
    
    return result