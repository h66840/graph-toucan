from typing import Dict, Any, Optional
import base64
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for image generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_data (str): Base64-encoded image placeholder or actual data
        - generation_message (str): Confirmation message about image generation
        - prompt (str): The text description used to generate the image
        - width (int): Width of the generated image in pixels
        - height (int): Height of the generated image in pixels
        - model (str): Model name used for generation
        - seed (int): Random seed used for reproducible generation
        - enhance (bool): Whether prompt enhancement was applied
        - private (bool): Whether the image was marked as private
        - nologo (bool): Whether logo was excluded from the image
        - safe (bool): Whether content filtering was applied
        - transparent (bool): Whether the image background is transparent
        - file_path (str): Full path where the image was saved
    """
    # Generate a fake base64 image (PNG header + random data)
    fake_image_bytes = base64.b64encode(b'\x89PNG\r\n\x1a\n' + random.randbytes(512)).decode('utf-8')
    
    return {
        "image_data": fake_image_bytes,
        "generation_message": "Image successfully generated from prompt.",
        "prompt": "A beautiful landscape with mountains and a lake at sunset",
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "seed": random.randint(0, 1000000),
        "enhance": True,
        "private": False,
        "nologo": True,
        "safe": False,
        "transparent": False,
        "file_path": "./mcpollinations-output/landscape_mountains_lake_sunset.png"
    }


def mcpollinations_multimodal_server_generateImage(
    prompt: str,
    enhance: Optional[bool] = True,
    fileName: Optional[str] = None,
    format: Optional[str] = "png",
    height: Optional[int] = 1024,
    model: Optional[str] = "flux",
    outputPath: Optional[str] = "./mcpollinations-output",
    safe: Optional[bool] = False,
    seed: Optional[int] = None,
    width: Optional[int] = 1024
) -> Dict[str, Any]:
    """
    Generate an image based on a text prompt using a multimodal AI model.

    Args:
        prompt (str): The text description of the image to generate (required).
        enhance (bool, optional): Whether to enhance the prompt using an LLM before generating. Defaults to True.
        fileName (str, optional): Name of the file to save (without extension). Defaults to generated from prompt.
        format (str, optional): Image format to save as (png, jpeg, jpg, webp). Defaults to "png".
        height (int, optional): Height of the generated image. Defaults to 1024.
        model (str, optional): Model name to use for generation. Options: "flux", "turbo". Defaults to "flux".
        outputPath (str, optional): Directory path where to save the image. Defaults to "./mcpollinations-output".
        safe (bool, optional): Whether to apply content filtering. Defaults to False.
        seed (int, optional): Seed for reproducible results. Defaults to random.
        width (int, optional): Width of the generated image. Defaults to 1024.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - image_data (str): base64-encoded image data
            - generation_message (str): confirmation message
            - prompt (str): the text description used
            - width (int): width in pixels
            - height (int): height in pixels
            - model (str): model used
            - seed (int): random seed used
            - enhance (bool): whether enhancement was applied
            - private (bool): whether marked as private
            - nologo (bool): whether logo was excluded
            - safe (bool): whether content filtering applied
            - transparent (bool): whether background is transparent
            - file_path (str): full path where image was saved

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not prompt or not prompt.strip():
        raise ValueError("Prompt is required and cannot be empty")

    if format not in ["png", "jpeg", "jpg", "webp"]:
        raise ValueError("Format must be one of: png, jpeg, jpg, webp")

    if model not in ["flux", "turbo"]:
        raise ValueError("Model must be one of: flux, turbo")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers")

    if seed is not None and (seed < 0 or seed > 4294967295):
        raise ValueError("Seed must be a valid unsigned 32-bit integer (0-4294967295)")

    # Set default seed if not provided
    if seed is None:
        seed = random.randint(0, 4294967295)

    # Normalize format (jpg -> jpeg)
    if format == "jpg":
        format = "jpeg"

    # Generate filename from prompt if not provided
    if not fileName:
        # Clean prompt and create filename
        clean_prompt = ''.join(c if c.isalnum() else '_' for c in prompt[:50].strip())
        clean_prompt = '_'.join(filter(None, clean_prompt.split('_')))
        fileName = clean_prompt or "generated_image"

    # Validate output path to prevent directory traversal
    # Only allow relative paths that don't go up directories
    if '..' in outputPath.replace('\\', '/').split('/'):
        raise ValueError("Output path cannot contain parent directory references ('..')")

    # Create a safe file path without actually creating directories
    # We'll just construct the path string safely
    file_parts = [part for part in outputPath.replace('\\', '/').split('/') if part]
    safe_output_path = '/'.join(file_parts) if file_parts else '.'
    
    # Construct full file path
    file_path = f"{safe_output_path}/{fileName}.{format}"

    # Call external API to simulate image generation
    api_data = call_external_api("mcpollinations-multimodal-server-generateImage")

    # Construct final result using provided inputs and API data
    result = {
        "image_data": api_data["image_data"],
        "generation_message": f"Image successfully generated from prompt: '{prompt}'",
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model,
        "seed": seed,
        "enhance": enhance if enhance is not None else True,
        "private": False,  # Not in input, defaulting
        "nologo": True,    # Not in input, defaulting
        "safe": safe if safe is not None else False,
        "transparent": False,  # Not in input, defaulting
        "file_path": file_path
    }

    return result