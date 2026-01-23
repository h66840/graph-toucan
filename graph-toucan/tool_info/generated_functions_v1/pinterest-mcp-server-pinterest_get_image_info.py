from typing import Dict, List, Any, Optional
import re
from datetime import datetime, timedelta
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Pinterest API for image information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - image_id (str): Unique identifier for the Pinterest image
        - title (str): Title or name of the image pin
        - description (str): Description provided with the pin
        - url (str): Direct URL to the image resource
        - original_url (str): Original source link associated with the pin
        - thumbnail_url (str): URL to a smaller thumbnail version of the image
        - domain (str): Domain where the image was originally shared or sourced from
        - created_at (str): Timestamp when the pin was created, in ISO 8601 format
        - save_count (int): Number of times this pin has been saved by users
        - share_count (int): Number of times this pin has been shared
        - comment_count (int): Number of comments on the pin
        - like_count (int): Number of likes or reactions on the pin
        - is_video (bool): Indicates whether the pin is a video instead of an image
        - video_duration (float): Duration of the video in seconds (only if is_video is true)
        - aspect_ratio (float): Aspect ratio of the image (width/height)
        - color_palette_0 (str): First dominant color as hex code
        - color_palette_1 (str): Second dominant color as hex code
        - metadata_width (int): Image width in pixels
        - metadata_height (int): Image height in pixels
        - metadata_format (str): File format of the image (e.g., 'jpg', 'png')
    """
    # Generate deterministic but realistic values based on image_url hash
    image_hash = hash(tool_name) % (10 ** 12)
    
    # Generate created_at in ISO 8601 format
    base_time = datetime(2020, 1, 1)
    time_offset = timedelta(days=abs(image_hash) % 1500)
    created_at = (base_time + time_offset).isoformat()
    
    # Generate image ID
    image_id = f"{image_hash % (10**16):016d}"
    
    # Generate title from image URL pattern
    title = f"Beautiful Landscape {image_hash % 1000}"
    
    # Random but realistic domain
    domains = ["example.com", "unsplash.com", "pexels.com", "pixabay.com", "instagram.com"]
    domain = random.choice(domains)
    
    # Random counts
    save_count = random.randint(100, 50000)
    share_count = random.randint(10, 5000)
    comment_count = random.randint(0, 200)
    like_count = random.randint(50, 10000)
    
    # Determine if video
    is_video = bool(image_hash % 2)
    video_duration = round(random.uniform(5.0, 60.0), 2) if is_video else 0.0
    
    # Aspect ratio
    aspect_ratio = round(random.uniform(0.8, 1.8), 2)
    
    # Color palette (hex codes)
    colors = [
        f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}",
        f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
    ]
    
    # Metadata
    width = random.randint(800, 4000)
    height = int(width / aspect_ratio)
    image_formats = ["jpg", "png", "jpeg", "webp"]
    image_format = random.choice(image_formats)
    
    return {
        "image_id": image_id,
        "title": title,
        "description": f"This stunning image captures the essence of nature. Generated ID: {image_hash % 10000}",
        "url": f"https://i.pinimg.com/originals/{image_hash % 1000}/{(image_hash // 1000) % 100}/{(image_hash // 100000) % 100}/image.jpg",
        "original_url": f"https://{domain}/photo/{image_hash % 10000}",
        "thumbnail_url": f"https://i.pinimg.com/236x/{image_hash % 1000}/{(image_hash // 1000) % 100}/{(image_hash // 100000) % 100}/thumb.jpg",
        "domain": domain,
        "created_at": created_at,
        "save_count": save_count,
        "share_count": share_count,
        "comment_count": comment_count,
        "like_count": like_count,
        "is_video": is_video,
        "video_duration": video_duration,
        "aspect_ratio": aspect_ratio,
        "color_palette_0": colors[0],
        "color_palette_1": colors[1],
        "metadata_width": width,
        "metadata_height": height,
        "metadata_format": image_format
    }


def pinterest_mcp_server_pinterest_get_image_info(image_url: str) -> Dict[str, Any]:
    """
    Get Pinterest image information from an image URL.
    
    This function retrieves detailed information about a Pinterest image pin
    including metadata, engagement metrics, and visual characteristics.
    
    Args:
        image_url (str): The URL of the Pinterest image. Required.
        
    Returns:
        Dict containing the following fields:
        - image_id (str): Unique identifier for the Pinterest image
        - title (str): Title or name of the image pin
        - description (str): Description provided with the pin
        - url (str): Direct URL to the image resource
        - original_url (str): Original source link associated with the pin
        - thumbnail_url (str): URL to a smaller thumbnail version of the image
        - domain (str): Domain where the image was originally shared or sourced from
        - created_at (str): Timestamp when the pin was created, in ISO 8601 format
        - save_count (int): Number of times this pin has been saved
        - share_count (int): Number of times this pin has been shared
        - comment_count (int): Number of comments on the pin
        - like_count (int): Number of likes or reactions on the pin
        - is_video (bool): Whether the pin is a video
        - video_duration (float): Duration of the video in seconds (if applicable)
        - aspect_ratio (float): Aspect ratio of the image (width/height)
        - color_palette (List[str]): Dominant colors as hex codes
        - metadata (Dict): Additional metadata including width, height, and format
        
    Raises:
        ValueError: If image_url is empty or invalid
        TypeError: If image_url is not a string
    """
    # Input validation
    if not isinstance(image_url, str):
        raise TypeError("image_url must be a string")
    
    if not image_url or not image_url.strip():
        raise ValueError("image_url is required and cannot be empty")
    
    # Validate URL format
    url_pattern = re.compile(r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$')
    if not url_pattern.match(image_url.strip()):
        raise ValueError("image_url must be a valid URL")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("pinterest-mcp-server-pinterest_get_image_info")
    
    # Construct color palette from indexed fields
    color_palette = [
        api_data["color_palette_0"],
        api_data["color_palette_1"]
    ]
    
    # Construct metadata dictionary
    metadata = {
        "width": api_data["metadata_width"],
        "height": api_data["metadata_height"],
        "format": api_data["metadata_format"]
    }
    
    # Build result dictionary matching output schema
    result = {
        "image_id": api_data["image_id"],
        "title": api_data["title"],
        "description": api_data["description"],
        "url": api_data["url"],
        "original_url": api_data["original_url"],
        "thumbnail_url": api_data["thumbnail_url"],
        "domain": api_data["domain"],
        "created_at": api_data["created_at"],
        "save_count": api_data["save_count"],
        "share_count": api_data["share_count"],
        "comment_count": api_data["comment_count"],
        "like_count": api_data["like_count"],
        "is_video": api_data["is_video"],
        "video_duration": api_data["video_duration"] if api_data["is_video"] else None,
        "aspect_ratio": api_data["aspect_ratio"],
        "color_palette": color_palette,
        "metadata": metadata
    }
    
    # Clean up video_duration if not a video
    if not api_data["is_video"]:
        result["video_duration"] = None
    
    return result