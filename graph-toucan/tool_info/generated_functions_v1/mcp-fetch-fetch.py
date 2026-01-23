from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for URL content retrieval and image processing.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Extracted content of the URL in markdown format
        - image_0_urls_0 (str): First source URL of first image group
        - image_0_urls_1 (str): Second source URL of first image group
        - image_1_urls_0 (str): First source URL of second image group
        - image_1_urls_1 (str): Second source URL of second image group
        - image_0_group_index (int): Group index of first image group (0-based)
        - image_1_group_index (int): Group index of second image group (0-based)
        - image_0_total_groups (int): Total number of image groups for first group
        - image_1_total_groups (int): Total number of image groups for second group
        - image_0_height (int): Height of first merged image group in pixels
        - image_1_height (int): Height of second merged image group in pixels
        - image_0_width (int): Width of first merged image group in pixels
        - image_1_width (int): Width of second merged image group in pixels
        - image_0_file_size (int): File size of first merged image group in bytes
        - image_1_file_size (int): File size of second merged image group in bytes
        - image_0_format (str): Format of first merged image group (e.g., 'JPEG')
        - image_1_format (str): Format of second merged image group (e.g., 'PNG')
    """
    return {
        "content": "# Example Article\n\nThis is an example article fetched from a URL.\n\n![Image 1](image1.jpg)\n\nSome more text here.\n\n![Image 2](image2.png)",
        "image_0_urls_0": "https://example.com/images/1.jpg",
        "image_0_urls_1": "https://example.com/images/2.png",
        "image_1_urls_0": "https://example.com/images/3.gif",
        "image_1_urls_1": "https://example.com/images/4.jpeg",
        "image_0_group_index": 0,
        "image_1_group_index": 1,
        "image_0_total_groups": 2,
        "image_1_total_groups": 2,
        "image_0_height": 1200,
        "image_1_height": 1800,
        "image_0_width": 800,
        "image_1_width": 800,
        "image_0_file_size": 2457600,
        "image_1_file_size": 1843200,
        "image_0_format": "JPEG",
        "image_1_format": "PNG",
    }


def mcp_fetch_fetch(
    url: str,
    maxLength: Optional[int] = None,
    raw: Optional[bool] = None,
    startIndex: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Retrieves URLs from the Internet and extracts their content as markdown.
    If images are found, they are merged vertically (max 6 images per group, max height 8000px, max size 30MB per group)
    and copied to the clipboard of the user's host machine.

    Args:
        url (str): The URL to fetch content from (required).
        maxLength (Optional[int]): Maximum length of content to extract.
        raw (Optional[bool]): Whether to return raw content or processed markdown.
        startIndex (Optional[int]): Start index for content extraction.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - content (str): The extracted content of the URL converted to markdown format.
            - images (List[Dict]): List of image groups with metadata.
                Each group contains:
                    - urls (List[str]): Source URLs of images in the group.
                    - group_index (int): 0-based index of the image group.
                    - total_groups (int): Total number of image groups.
                    - height (int): Height of merged image in pixels.
                    - width (int): Width of merged image in pixels.
                    - file_size (int): Size of merged image in bytes.
                    - format (str): Image format (e.g., 'JPEG', 'PNG').

    Raises:
        ValueError: If required 'url' parameter is missing or empty.
    """
    if not url:
        raise ValueError("The 'url' parameter is required and cannot be empty.")

    # Call external API to simulate fetching data
    api_data = call_external_api("mcp-fetch-fetch")

    # Construct image groups from flattened API response
    images = []

    # Process first image group
    image_0_urls = []
    if "image_0_urls_0" in api_data and api_data["image_0_urls_0"]:
        image_0_urls.append(api_data["image_0_urls_0"])
    if "image_0_urls_1" in api_data and api_data["image_0_urls_1"]:
        image_0_urls.append(api_data["image_0_urls_1"])

    if image_0_urls:
        images.append({
            "urls": image_0_urls,
            "group_index": api_data["image_0_group_index"],
            "total_groups": api_data["image_0_total_groups"],
            "height": api_data["image_0_height"],
            "width": api_data["image_0_width"],
            "file_size": api_data["image_0_file_size"],
            "format": api_data["image_0_format"],
        })

    # Process second image group
    image_1_urls = []
    if "image_1_urls_0" in api_data and api_data["image_1_urls_0"]:
        image_1_urls.append(api_data["image_1_urls_0"])
    if "image_1_urls_1" in api_data and api_data["image_1_urls_1"]:
        image_1_urls.append(api_data["image_1_urls_1"])

    if image_1_urls:
        images.append({
            "urls": image_1_urls,
            "group_index": api_data["image_1_group_index"],
            "total_groups": api_data["image_1_total_groups"],
            "height": api_data["image_1_height"],
            "width": api_data["image_1_width"],
            "file_size": api_data["image_1_file_size"],
            "format": api_data["image_1_format"],
        })

    # Apply maxLength logic if specified
    content = api_data["content"]
    if maxLength is not None and len(content) > maxLength:
        if raw:
            content = content[:maxLength]
        else:
            # Truncate at last complete sentence before maxLength
            truncated = content[:maxLength]
            last_period = truncated.rfind('.')
            if last_period != -1 and last_period > maxLength * 0.8:
                content = truncated[:last_period + 1]
            else:
                content = truncated

    # Apply startIndex logic if specified
    if startIndex is not None:
        content = content[startIndex:]

    return {
        "content": content,
        "images": images,
    }