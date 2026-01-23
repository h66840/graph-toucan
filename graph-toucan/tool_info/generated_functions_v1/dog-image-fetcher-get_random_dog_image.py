from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dog image fetching.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the request, e.g., "success"
        - count (int): Total number of available images matching criteria
        - image_0_id (str): ID of the first image
        - image_0_url (str): URL of the first image
        - image_0_width (int or None): Width of the first image, null if unavailable
        - image_0_height (int or None): Height of the first image, null if unavailable
        - image_1_id (str): ID of the second image
        - image_1_url (str): URL of the second image
        - image_1_width (int or None): Width of the second image, null if unavailable
        - image_1_height (int or None): Height of the second image, null if unavailable
    """
    return {
        "status": "success",
        "count": 2,
        "image_0_id": "abc123",
        "image_0_url": "https://example.com/dogs/abc123.jpg",
        "image_0_width": 800,
        "image_0_height": 600,
        "image_1_id": "def456",
        "image_1_url": "https://example.com/dogs/def456.jpg",
        "image_1_width": 1024,
        "image_1_height": 768,
    }

def dog_image_fetcher_get_random_dog_image(
    breed_id: Optional[str] = None,
    category_ids: Optional[str] = None,
    format: Optional[str] = "json",
    limit: Optional[int] = 1
) -> Dict[str, Any]:
    """
    Get random dog images with optional breed and category filtering.

    Args:
        breed_id (Optional[str]): Optional breed ID to filter by specific breed
        category_ids (Optional[str]): Optional category IDs (comma-separated) to filter by
        format (Optional[str]): Response format ("json" or "src"). Defaults to "json".
        limit (Optional[int]): Number of images to return (1-10). Defaults to 1.

    Returns:
        Dict containing:
        - status (str): status of the request (e.g., "success")
        - count (int): total number of available images matching the criteria
        - images (List[Dict]): list of image objects, each with 'id', 'url', 'width', and 'height' fields.
          'width' and 'height' may be null if unavailable

    Raises:
        ValueError: If limit is not between 1 and 10
    """
    # Input validation
    if limit is None:
        limit = 1
    if not isinstance(limit, int) or limit < 1 or limit > 10:
        raise ValueError("Limit must be an integer between 1 and 10")

    if format not in [None, "json", "src"]:
        format = "json"

    # Fetch data from external API (simulated)
    api_data = call_external_api("dog-image-fetcher-get_random_dog_image")

    # Construct the images list from flattened API response
    images = []
    for i in range(min(limit, 2)):  # We only have 2 simulated images
        width_key = f"image_{i}_width"
        height_key = f"image_{i}_height"
        width = api_data.get(width_key)
        height = api_data.get(height_key)
        
        # Convert 0 or valid numbers; keep None if null
        width = width if width is not None else None
        height = height if height is not None else None

        images.append({
            "id": api_data[f"image_{i}_id"],
            "url": api_data[f"image_{i}_url"],
            "width": width,
            "height": height
        })

    # Construct final result
    result = {
        "status": api_data["status"],
        "count": api_data["count"],
        "images": images
    }

    return result