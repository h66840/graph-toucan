from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dog breed posts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - post_0_id (str): ID of the first post
        - post_0_title (str): Title of the first post
        - post_0_price (float): Price of the first post
        - post_0_birthday (str): Birthday of the dog in the first post
        - post_0_gender_distribution (str): Gender distribution for the first post
        - post_0_location (str): Location of the first post
        - post_0_type (str): Type of the first post (e.g., "sale", "adoption")
        - post_0_external_link (str): External link for the first post
        - post_0_pictures_0 (str): First picture URL of the first post
        - post_0_pictures_1 (str): Second picture URL of the first post
        - post_1_id (str): ID of the second post
        - post_1_title (str): Title of the second post
        - post_1_price (float): Price of the second post
        - post_1_birthday (str): Birthday of the dog in the second post
        - post_1_gender_distribution (str): Gender distribution for the second post
        - post_1_location (str): Location of the second post
        - post_1_type (str): Type of the second post (e.g., "sale", "adoption")
        - post_1_external_link (str): External link for the second post
        - post_1_pictures_0 (str): First picture URL of the second post
        - post_1_pictures_1 (str): Second picture URL of the second post
        - total_count (int): Total number of posts available for the breed
    """
    return {
        "post_0_id": "post123",
        "post_0_title": "Adorable Golden Retriever Puppies for Sale",
        "post_0_price": 1200.0,
        "post_0_birthday": "2023-06-15",
        "post_0_gender_distribution": "3 males, 2 females",
        "post_0_location": "New York, NY",
        "post_0_type": "sale",
        "post_0_external_link": "https://example.com/post123",
        "post_0_pictures_0": "https://example.com/images/dog1_1.jpg",
        "post_0_pictures_1": "https://example.com/images/dog1_2.jpg",
        "post_1_id": "post124",
        "post_1_title": "Purebred Labrador Retriever Puppies",
        "post_1_price": 1500.0,
        "post_1_birthday": "2023-05-20",
        "post_1_gender_distribution": "2 males, 3 females",
        "post_1_location": "Los Angeles, CA",
        "post_1_type": "sale",
        "post_1_external_link": "https://example.com/post124",
        "post_1_pictures_0": "https://example.com/images/dog2_1.jpg",
        "post_1_pictures_1": "https://example.com/images/dog2_2.jpg",
        "total_count": 25
    }

def pote_get_breed_posts(breedId: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
    """
    Get a list of available dog posts/ads for a specific breed.

    Args:
        breedId (str): The ID of the dog breed (required)
        limit (Optional[int]): Maximum number of posts to return
        offset (Optional[int]): Number of posts to skip

    Returns:
        Dict containing:
        - posts (List[Dict]): List of dog post entries with fields:
            - id (str)
            - title (str)
            - price (float)
            - birthday (str)
            - gender_distribution (str)
            - location (str)
            - type (str)
            - external_link (str)
            - pictures (Optional[List[str]])
        - total_count (int): Total number of posts found for the breed

    Raises:
        ValueError: If breedId is empty or None
    """
    if not breedId:
        raise ValueError("breedId is required and cannot be empty")

    # Validate limit and offset
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")
    if offset is not None and offset < 0:
        raise ValueError("offset must be non-negative")

    # Fetch data from external API (simulated)
    api_data = call_external_api("pote-get-breed-posts")

    # Construct posts list from flattened API data
    posts = []

    # Process first post if available
    if all(key in api_data for key in [
        "post_0_id", "post_0_title", "post_0_price", "post_0_birthday",
        "post_0_gender_distribution", "post_0_location", "post_0_type",
        "post_0_external_link"
    ]):
        pictures_0 = []
        if "post_0_pictures_0" in api_data and api_data["post_0_pictures_0"]:
            pictures_0.append(api_data["post_0_pictures_0"])
        if "post_0_pictures_1" in api_data and api_data["post_0_pictures_1"]:
            pictures_0.append(api_data["post_0_pictures_1"])
        
        post_0 = {
            "id": api_data["post_0_id"],
            "title": api_data["post_0_title"],
            "price": api_data["post_0_price"],
            "birthday": api_data["post_0_birthday"],
            "gender_distribution": api_data["post_0_gender_distribution"],
            "location": api_data["post_0_location"],
            "type": api_data["post_0_type"],
            "external_link": api_data["post_0_external_link"]
        }
        if pictures_0:
            post_0["pictures"] = pictures_0
        posts.append(post_0)

    # Process second post if available
    if all(key in api_data for key in [
        "post_1_id", "post_1_title", "post_1_price", "post_1_birthday",
        "post_1_gender_distribution", "post_1_location", "post_1_type",
        "post_1_external_link"
    ]):
        pictures_1 = []
        if "post_1_pictures_0" in api_data and api_data["post_1_pictures_0"]:
            pictures_1.append(api_data["post_1_pictures_0"])
        if "post_1_pictures_1" in api_data and api_data["post_1_pictures_1"]:
            pictures_1.append(api_data["post_1_pictures_1"])
        
        post_1 = {
            "id": api_data["post_1_id"],
            "title": api_data["post_1_title"],
            "price": api_data["post_1_price"],
            "birthday": api_data["post_1_birthday"],
            "gender_distribution": api_data["post_1_gender_distribution"],
            "location": api_data["post_1_location"],
            "type": api_data["post_1_type"],
            "external_link": api_data["post_1_external_link"]
        }
        if pictures_1:
            post_1["pictures"] = pictures_1
        posts.append(post_1)

    # Apply limit and offset if specified
    start_idx = offset if offset is not None else 0
    end_idx = start_idx + (limit if limit is not None else len(posts))
    filtered_posts = posts[start_idx:end_idx]

    # Get total count (default to number of available posts if not in API data)
    total_count = api_data.get("total_count", len(posts))

    return {
        "posts": filtered_posts,
        "total_count": total_count
    }