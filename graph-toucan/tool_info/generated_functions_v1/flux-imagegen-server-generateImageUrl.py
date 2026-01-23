from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for image generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_url (str): URL of the generated image
        - prompt (str): Original text prompt used for image generation
        - width (int): Width of the generated image in pixels
        - height (int): Height of the generated image in pixels
        - model (str): Model name used for image generation
        - seed (int): Random seed used for reproducible image generation
        - enhance (bool): Whether the prompt was enhanced using an LLM before generation
        - private (bool): Whether the image is marked as private
        - nologo (bool): Whether the image is generated without a logo overlay
        - safe (bool): Whether content filtering was applied during generation
    """
    return {
        "image_url": "https://example.com/generated-image.png",
        "prompt": "a beautiful sunset over mountains",
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "seed": 123456789,
        "enhance": True,
        "private": False,
        "nologo": True,
        "safe": False
    }

def flux_imagegen_server_generateImageUrl(
    prompt: str,
    enhance: Optional[bool] = None,
    height: Optional[int] = None,
    model: Optional[str] = None,
    safe: Optional[bool] = None,
    seed: Optional[int] = None,
    width: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate an image URL from a text prompt using a specified model and parameters.

    Args:
        prompt (str): The text description of the image to generate. Required.
        enhance (bool, optional): Whether to enhance the prompt using an LLM before generating. Default: True.
        height (int, optional): Height of the generated image. Default: 1024.
        model (str, optional): Model name to use for generation. Options: "flux", "sdxl", "sd3", "sd15", "flux-schnell", "flux-dev". Default: "flux".
        safe (bool, optional): Whether to apply content filtering. Default: False.
        seed (int, optional): Seed for reproducible results. Default: random.
        width (int, optional): Width of the generated image. Default: 1024.

    Returns:
        Dict containing:
            - imageUrl (str): URL of the generated image
            - prompt (str): Original text prompt used for image generation
            - width (int): Width of the generated image in pixels
            - height (int): Height of the generated image in pixels
            - model (str): Model name used for image generation
            - seed (int): Random seed used for reproducible image generation
            - enhance (bool): Whether the prompt was enhanced using an LLM before generation
            - private (bool): Whether the image is marked as private
            - nologo (bool): Whether the image is generated without a logo overlay
            - safe (bool): Whether content filtering was applied during generation

    Raises:
        ValueError: If required prompt is not provided or if invalid model is specified.
    """
    # Input validation
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string.")

    valid_models = ["flux", "sdxl", "sd3", "sd15", "flux-schnell", "flux-dev"]
    if model and model not in valid_models:
        raise ValueError(f"Invalid model '{model}'. Must be one of {valid_models}.")

    # Set default values
    enhance = True if enhance is None else enhance
    height = 1024 if height is None else height
    model = "flux" if model is None else model
    safe = False if safe is None else safe
    width = 1024 if width is None else width

    # Call external API simulation
    api_data = call_external_api("flux-imagegen-server-generateImageUrl")

    # Construct result matching output schema exactly
    result = {
        "imageUrl": api_data["image_url"],
        "prompt": prompt,  # Use actual input prompt
        "width": width,   # Use input or default width
        "height": height, # Use input or default height
        "model": model,   # Use input or default model
        "seed": api_data["seed"] if seed is None else seed,
        "enhance": enhance,
        "private": api_data["private"],
        "nologo": api_data["nologo"],
        "safe": safe
    }

    return result