import base64
import json
from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates calling an external image generation API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - file_path (str): Full path where the image was saved
        - file_name (str): Name of the saved file without path
        - format (str): Image format used (e.g., png, jpeg)
        - width (int): Width of the generated image in pixels
        - height (int): Height of the generated image in pixels
        - model (str): Model name used for generation
        - prompt (str): Original text description used to generate the image
        - enhanced_prompt (str): Final prompt after optional enhancement
        - seed (int): Random seed used for reproducible results
        - enhance (bool): Whether prompt enhancement was applied
        - safe (bool): Whether content filtering was enabled
        - private (bool): Whether the image was marked as private
        - nologo (bool): Whether logo watermarking was disabled
        - metadata_prompt (str): Prompt in metadata
        - metadata_width (int): Width in metadata
        - metadata_height (int): Height in metadata
        - metadata_model (str): Model in metadata
        - metadata_seed (int): Seed in metadata
        - metadata_enhance (bool): Enhance flag in metadata
        - metadata_private (bool): Private flag in metadata
        - metadata_nologo (bool): Nologo flag in metadata
        - metadata_safe (bool): Safe flag in metadata
    """
    return {
        
        "file_path": "/home/user/mcpollinations-output/a_dog_playing_in_park.png",
        "file_name": "a_dog_playing_in_park.png",
        "format": "png",
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "prompt": "a dog playing in a park",
        "enhanced_prompt": "a happy golden retriever playing fetch in a sunny park with green grass and trees",
        "seed": 12345,
        "enhance": True,
        "safe": False,
        "private": False,
        "nologo": True,
        "metadata_prompt": "a dog playing in a park",
        "metadata_width": 1024,
        "metadata_height": 1024,
        "metadata_model": "flux",
        "metadata_seed": 12345,
        "metadata_enhance": True,
        "metadata_private": False,
        "metadata_nologo": True,
        "metadata_safe": False
    }

def flux_imagegen_server_generateImage(
    prompt: str,
    enhance: Optional[bool] = None,
    fileName: Optional[str] = None,
    format: Optional[str] = None,
    height: Optional[int] = None,
    model: Optional[str] = None,
    outputPath: Optional[str] = None,
    safe: Optional[bool] = None,
    seed: Optional[int] = None,
    width: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate an image based on a text prompt using a specified model and parameters.
    
    Args:
        prompt (str): The text description of the image to generate (required).
        enhance (bool, optional): Whether to enhance the prompt using an LLM before generating. Default: True.
        fileName (str, optional): Name of the file to save (without extension). Default: generated from prompt.
        format (str, optional): Image format to save as (png, jpeg, jpg, webp). Default: png.
        height (int, optional): Height of the generated image. Default: 1024.
        model (str, optional): Model name to use for generation ("flux", "turbo"). Default: "flux".
        outputPath (str, optional): Directory path where to save the image. Default: "./mcpollinations-output".
        safe (bool, optional): Whether to apply content filtering. Default: False.
        seed (int, optional): Seed for reproducible results. Default: random.
        width (int, optional): Width of the generated image. Default: 1024.
    
    Returns:
        Dict containing:
            - image_data (str): base64-encoded string of the generated image
            - file_path (str): full path where the image was saved, including filename and extension
            - file_name (str): name of the saved file without path
            - format (str): image format used for saving
            - width (int): width of the generated image in pixels
            - height (int): height of the generated image in pixels
            - model (str): model name used for generation
            - prompt (str): original text description used to generate the image
            - enhanced_prompt (str): final prompt used after optional LLM-based enhancement
            - seed (int): random seed used for reproducible image generation
            - enhance (bool): whether prompt enhancement was applied before generation
            - safe (bool): whether content filtering was enabled during generation
            - private (bool): whether the image was marked as private
            - nologo (bool): whether logo watermarking was disabled
            - metadata (Dict): detailed generation parameters including prompt, dimensions, model, seed, flags
    
    Raises:
        ValueError: If required prompt is not provided or invalid parameters are given.
    """
    # Input validation
    if not prompt or not isinstance(prompt, str) or len(prompt.strip()) == 0:
        raise ValueError("Prompt is required and must be a non-empty string.")
    
    # Set default values
    enhance = True if enhance is None else enhance
    format = (format or "png").lower()
    height = height or 1024
    model = model or "flux"
    outputPath = outputPath or "./mcpollinations-output"
    safe = False if safe is None else safe
    width = width or 1024
    
    # Validate format
    valid_formats = ["png", "jpeg", "jpg", "webp"]
    if format not in valid_formats:
        raise ValueError(f"Format must be one of {valid_formats}. Got '{format}'.")
    
    # Normalize jpg to jpeg
    if format == "jpg":
        format = "jpeg"
    
    # Validate model
    valid_models = ["flux", "turbo"]
    if model not in valid_models:
        raise ValueError(f"Model must be one of {valid_models}. Got '{model}'.")
    
    # Validate dimensions
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive integers.")
    
    # Generate file name if not provided
    if not fileName:
        # Clean prompt to create valid filename
        cleaned_prompt = "".join(c if c.isalnum() or c in [' ', '-', '_'] else "_" for c in prompt[:50])
        cleaned_prompt = cleaned_prompt.strip().replace(" ", "_").replace("__", "_")
        fileName = f"{cleaned_prompt}.{format}"
    elif not fileName.endswith(f".{format}"):
        fileName = f"{fileName}.{format}"
    
    # Call external API to simulate image generation
    api_data = call_external_api("flux-imagegen-server-generateImage")
    
    # Construct result dictionary by mapping flat API data to nested schema
    result = {
        "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
        "file_path": api_data["file_path"],
        "file_name": api_data["file_name"],
        "format": api_data["format"],
        "width": api_data["width"],
        "height": api_data["height"],
        "model": api_data["model"],
        "prompt": api_data["prompt"],
        "enhanced_prompt": api_data["enhanced_prompt"],
        "seed": api_data["seed"],
        "enhance": api_data["enhance"],
        "safe": api_data["safe"],
        "private": api_data["private"],
        "nologo": api_data["nologo"],
        "metadata": {
            "prompt": api_data["metadata_prompt"],
            "width": api_data["metadata_width"],
            "height": api_data["metadata_height"],
            "model": api_data["metadata_model"],
            "seed": api_data["metadata_seed"],
            "enhance": api_data["metadata_enhance"],
            "private": api_data["metadata_private"],
            "nologo": api_data["metadata_nologo"],
            "safe": api_data["metadata_safe"]
        }
    }
    
    # Override with actual input values where applicable
    result["prompt"] = prompt
    result["enhance"] = enhance
    result["format"] = format
    result["width"] = width
    result["height"] = height
    result["model"] = model
    result["safe"] = safe
    result["seed"] = seed if seed is not None else result["seed"]
    
    # Update file names based on user input
    if fileName:
        base_name = fileName.rsplit('.', 1)[0] if '.' in fileName else fileName
        full_file_name = f"{base_name}.{format}" if not fileName.lower().endswith(f".{format}") else fileName
        result["file_name"] = full_file_name
        # Use string concatenation instead of os.path.join to avoid os import
        if outputPath.endswith('/') or outputPath.endswith('\\'):
            result["file_path"] = f"{outputPath}{full_file_name}"
        else:
            result["file_path"] = f"{outputPath}/{full_file_name}"
    
    # Update metadata to reflect actual inputs
    result["metadata"]["prompt"] = result["prompt"]
    result["metadata"]["width"] = result["width"]
    result["metadata"]["height"] = result["height"]
    result["metadata"]["model"] = result["model"]
    result["metadata"]["seed"] = result["seed"]
    result["metadata"]["enhance"] = result["enhance"]
    result["metadata"]["safe"] = result["safe"]
    
    # Generate a more descriptive enhanced prompt if enhancement is enabled
    if enhance:
        result["enhanced_prompt"] = f"highly detailed, realistic, vibrant colors, {prompt}, professional photography style"
    else:
        result["enhanced_prompt"] = prompt
    
    # Update metadata enhanced prompt
    result["metadata"]["prompt"] = result["enhanced_prompt"]
    
    return result