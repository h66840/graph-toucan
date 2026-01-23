from typing import Dict, Any, Optional
import base64
import random
import string
import re
import os


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for image generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_data (str): base64-encoded string of the generated image
        - prompt (str): the original text prompt used to generate the image
        - width (int): width of the generated image in pixels
        - height (int): height of the generated image in pixels
        - model (str): model name used for image generation
        - seed (int): random seed used for reproducible generation
        - enhance (bool): whether the prompt was enhanced using an LLM
        - safe (bool): whether content filtering was applied
        - private (bool): whether the image was generated with privacy settings
        - nologo (bool): whether logo-free output was requested and applied
        - file_path (str): full path where the image was saved on disk
        - format (str): image file format (e.g., "png", "jpeg")
    """
    # Generate a dummy base64 image (a tiny transparent PNG)
    dummy_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
    return {
        "image_data": dummy_image_b64,
        "prompt": "A beautiful landscape with mountains and a lake",
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "seed": random.randint(0, 1000000),
        "enhance": True,
        "safe": False,
        "private": False,
        "nologo": False,
        "file_path": "./mcpollinations-output/landscape_mountains_lake.png",
        "format": "png",
    }


def mcpollinations_generateImage(
    prompt: str,
    enhance: Optional[bool] = True,
    fileName: Optional[str] = None,
    format: Optional[str] = "png",
    height: Optional[int] = 1024,
    model: Optional[str] = "flux",
    outputPath: Optional[str] = "./mcpollinations-output",
    safe: Optional[bool] = False,
    seed: Optional[int] = None,
    width: Optional[int] = 1024,
) -> Dict[str, Any]:
    """
    Generate an image based on a text prompt, return base64-encoded data, and save to file.

    Args:
        prompt (str): The text description of the image to generate (required).
        enhance (bool, optional): Whether to enhance the prompt using an LLM before generating. Default: True.
        fileName (str, optional): Name of the file to save (without extension). Default: generated from prompt.
        format (str, optional): Image format to save as (png, jpeg, jpg, webp). Default: "png".
        height (int, optional): Height of the generated image. Default: 1024.
        model (str, optional): Model name to use for generation ("flux", "turbo"). Default: "flux".
        outputPath (str, optional): Directory path where to save the image. Default: "./mcpollinations-output".
        safe (bool, optional): Whether to apply content filtering. Default: False.
        seed (int, optional): Seed for reproducible results. Default: random.
        width (int, optional): Width of the generated image. Default: 1024.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - image_data (str): base64-encoded string of the generated image
            - prompt (str): the original text prompt used to generate the image
            - width (int): width of the generated image in pixels
            - height (int): height of the generated image in pixels
            - model (str): model name used for image generation
            - seed (int): random seed used for reproducible generation
            - enhance (bool): whether the prompt was enhanced using an LLM before generation
            - safe (bool): whether content filtering was applied during generation
            - private (bool): whether the image was generated with privacy settings enabled
            - nologo (bool): whether logo-free output was requested and applied
            - file_path (str): full path where the image was saved on disk
            - format (str): image file format (e.g., "png", "jpeg")
    """
    # Input validation
    if not prompt or not prompt.strip():
        raise ValueError("Prompt is required and cannot be empty.")

    if format not in ["png", "jpeg", "jpg", "webp"]:
        raise ValueError("Format must be one of: png, jpeg, jpg, webp")

    if model not in ["flux", "turbo"]:
        raise ValueError("Model must be one of: flux, turbo")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")

    if seed is not None and (seed < 0 or seed > 4294967295):
        raise ValueError("Seed must be a non-negative 32-bit integer.")

    # Normalize format (convert jpg -> jpeg)
    image_format = "jpeg" if format == "jpg" else format

    # Generate filename from prompt if not provided
    if not fileName:
        # Clean prompt to create valid filename
        clean_prompt = "".join(c if c.isalnum() or c in " _-" else "_" for c in prompt.strip())
        clean_prompt = clean_prompt.replace(" ", "_")[:50]  # Max 50 chars
        fileName = clean_prompt or "image"

    # Validate and sanitize outputPath to prevent directory traversal
    if not outputPath:
        outputPath = "./mcpollinations-output"
    
    # Normalize path and ensure it's within allowed boundaries
    normalized_output_path = os.path.normpath(outputPath)
    
    # Prevent directory traversal by ensuring path doesn't go above current directory
    if ".." in normalized_output_path.split(os.sep):
        raise ValueError("Output path cannot contain directory traversal sequences")
    
    # Ensure output directory exists - this is safe as we've validated the path
    try:
        os.makedirs(normalized_output_path, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Failed to create output directory: {e}")

    # Build full file path
    file_path = os.path.join(normalized_output_path, f"{fileName}.{image_format}")

    # Use provided seed or generate random one
    used_seed = seed if seed is not None else random.randint(0, 1000000)

    # Call external API (simulation)
    api_data = call_external_api("mcpollinations-generateImage")

    # Construct result dictionary matching output schema
    result = {
        "image_data": api_data["image_data"],
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model,
        "seed": used_seed,
        "enhance": enhance if enhance is not None else True,
        "safe": safe,
        "private": False,  # Not exposed in inputs, defaulting to False
        "nologo": False,   # Not exposed in inputs, defaulting to False
        "file_path": file_path,
        "format": image_format,
    }

    return result