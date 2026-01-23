from typing import Dict, Any, Optional
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for image generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_url (str): URL of the generated image
        - prompt (str): the text prompt used to generate the image
        - width (int): width of the generated image in pixels
        - height (int): height of the generated image in pixels
        - model (str): name of the model used for image generation
        - seed (int): random seed used for reproducible image generation
        - enhance (bool): whether the prompt was enhanced using an LLM before generation
        - private (bool): whether the generated image is marked as private
        - nologo (bool): whether the image was generated with no logo overlay
        - safe (bool): whether content filtering was applied during generation
        - transparent (bool): whether the image background is transparent
    """
    return {
        "image_url": "https://images.pollinations.ai/prompt/a%20beautiful%20sunset%20over%20the%20ocean",
        "prompt": "a beautiful sunset over the ocean",
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "seed": random.randint(1, 100000),
        "enhance": True,
        "private": False,
        "nologo": True,
        "safe": False,
        "transparent": False,
    }


def mcpollinations_multimodal_server_generateImageUrl(
    prompt: str,
    enhance: Optional[bool] = True,
    height: Optional[int] = 1024,
    model: Optional[str] = "flux",
    safe: Optional[bool] = False,
    seed: Optional[int] = None,
    width: Optional[int] = 1024,
) -> Dict[str, Any]:
    """
    Generate an image URL from a text prompt using a multimodal server.

    Args:
        prompt (str): The text description of the image to generate (required).
        enhance (bool, optional): Whether to enhance the prompt using an LLM before generating. Defaults to True.
        height (int, optional): Height of the generated image. Defaults to 1024.
        model (str, optional): Model name to use for generation. Options: "flux", "sdxl", "sd3", "sd15", "flux-schnell", "flux-dev". Defaults to "flux".
        safe (bool, optional): Whether to apply content filtering. Defaults to False.
        seed (int, optional): Seed for reproducible results. If not provided, a random seed is used.
        width (int, optional): Width of the generated image. Defaults to 1024.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - imageUrl (str): URL of the generated image
            - prompt (str): the text prompt used to generate the image
            - width (int): width of the generated image in pixels
            - height (int): height of the generated image in pixels
            - model (str): name of the model used for image generation
            - seed (int): random seed used for reproducible image generation
            - enhance (bool): whether the prompt was enhanced using an LLM before generation
            - private (bool): whether the generated image is marked as private
            - nologo (bool): whether the image was generated with no logo overlay
            - safe (bool): whether content filtering was applied during generation
            - transparent (bool): whether the image background is transparent

    Raises:
        ValueError: If prompt is empty or None.
        ValueError: If width or height is not a positive integer.
        ValueError: If model is not one of the allowed values.
    """
    # Input validation
    if not prompt:
        raise ValueError("Prompt is required and cannot be empty.")

    if not isinstance(width, int) or width <= 0:
        raise ValueError("Width must be a positive integer.")

    if not isinstance(height, int) or height <= 0:
        raise ValueError("Height must be a positive integer.")

    allowed_models = ["flux", "sdxl", "sd3", "sd15", "flux-schnell", "flux-dev"]
    if model not in allowed_models:
        raise ValueError(f"Model must be one of {allowed_models}.")

    # Use provided seed or generate a random one
    final_seed = seed if seed is not None else random.randint(1, 100000)

    # Call external API (simulation)
    api_data = call_external_api("mcpollinations-multimodal-server-generateImageUrl")

    # Construct result dictionary matching output schema
    result = {
        "imageUrl": api_data["image_url"],
        "prompt": prompt,  # Use original prompt (could be enhanced in real API)
        "width": width,
        "height": height,
        "model": model,
        "seed": final_seed,
        "enhance": enhance if enhance is not None else True,
        "private": api_data["private"],
        "nologo": api_data["nologo"],
        "safe": safe,
        "transparent": api_data["transparent"],
    }

    return result