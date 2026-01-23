from typing import Dict, List, Any, Optional
import random
import string
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for videos.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_count (int): Total number of videos available
        - retrieved (int): Number of videos returned in this response
        - processed_in (int): Time in seconds taken to process the request
        - video_0__id (str): ID of the first video
        - video_0_title (str): Title of the first video
        - video_0_abstract (str): Abstract of the first video
        - video_0_type (str): Type of the first video
        - video_0_link (str): Link to the first video
        - video_0_additionalLinks (str): Additional links for the first video (JSON string)
        - video_0_tags (str): Tags for the first video (comma-separated string)
        - video_0_language (str): Language of the first video
        - video_0_date (str): Date of the first video (ISO format)
        - video_1__id (str): ID of the second video
        - video_1_title (str): Title of the second video
        - video_1_abstract (str): Abstract of the second video
        - video_1_type (str): Type of the second video
        - video_1_link (str): Link to the second video
        - video_1_additionalLinks (str): Additional links for the second video (JSON string)
        - video_1_tags (str): Tags for the second video (comma-separated string)
        - video_1_language (str): Language of the second video
        - video_1_date (str): Date of the second video (ISO format)
    """
    # Generate realistic mock data
    def random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_date() -> str:
        days = random.randint(0, 365)
        date = datetime.now() - timedelta(days=days)
        return date.isoformat()

    def random_tags() -> str:
        tags = ["javascript", "nodejs", "backend", "api", "docker", "kubernetes", "typescript", "aws"]
        return ",".join(random.sample(tags, random.randint(1, 4)))

    return {
        "total_count": random.randint(50, 200),
        "retrieved": 2,
        "processed_in": round(random.uniform(0.1, 0.8), 3),
        "video_0__id": random_string(24),
        "video_0_title": f"Mastering Node.js with {random_string(6)} patterns",
        "video_0_abstract": f"This video covers advanced {random_string(8)} techniques in Node.js development.",
        "video_0_type": random.choice(["live", "recorded", "workshop"]),
        "video_0_link": f"https://example.com/videos/{random_string(12)}",
        "video_0_additionalLinks": '["https://github.com/example/repo", "https://slides.com/example"]',
        "video_0_tags": random_tags(),
        "video_0_language": random.choice(["en", "pt", "es"]),
        "video_0_date": random_date(),
        "video_1__id": random_string(24),
        "video_1_title": f"Building Scalable APIs using {random_string(7)} Architecture",
        "video_1_abstract": f"Learn how to build robust APIs with {random_string(9)} methodology.",
        "video_1_type": random.choice(["recorded", "workshop", "talk"]),
        "video_1_link": f"https://example.com/videos/{random_string(12)}",
        "video_1_additionalLinks": '["https://github.com/example/api", "https://docs.example.com"]',
        "video_1_tags": random_tags(),
        "video_1_language": random.choice(["en", "pt"]),
        "video_1_date": random_date(),
    }


def erick_wendel_contributions_get_videos(
    id: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of videos with optional filtering and pagination.

    Args:
        id (Optional[str]): Filter videos by ID
        language (Optional[str]): Filter videos by language
        limit (Optional[int]): Maximum number of videos to return
        skip (Optional[int]): Number of videos to skip
        title (Optional[str]): Filter videos by title

    Returns:
        Dict containing:
        - totalCount (int): total number of videos available in the database
        - retrieved (int): number of videos returned in this response
        - processedIn (int): time in seconds taken to process the request
        - videos (List[Dict]): list of video objects with '_id', 'title', 'abstract', 'type',
          'link', 'additionalLinks', 'tags', 'language', 'date' fields
    """
    # Validate inputs
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")
    if skip is not None and skip < 0:
        raise ValueError("skip must be non-negative")

    # Call external API to get data (simulated)
    api_data = call_external_api("erick-wendel-contributions-get_videos")

    # Extract simple fields and build nested structure
    videos = []

    for i in range(2):  # We have 2 videos from the API (0 and 1)
        video_id_key = f"video_{i}__id"
        title_key = f"video_{i}_title"

        # Skip if we don't have data for this index
        if video_id_key not in api_data:
            continue

        # Apply filters
        video_id = api_data[video_id_key]
        video_title = api_data[title_key]
        video_language = api_data[f"video_{i}_language"]

        # Apply filtering logic
        if id is not None and video_id != id:
            continue
        if language is not None and video_language != language:
            continue
        if title is not None and title.lower() not in video_title.lower():
            continue

        # Only include videos that pass all filters
        video = {
            "_id": video_id,
            "title": video_title,
            "abstract": api_data[f"video_{i}_abstract"],
            "type": api_data[f"video_{i}_type"],
            "link": api_data[f"video_{i}_link"],
            "additionalLinks": api_data[f"video_{i}_additionalLinks"],
            "tags": api_data[f"video_{i}_tags"].split(","),
            "language": video_language,
            "date": api_data[f"video_{i}_date"]
        }
        videos.append(video)

    # Apply skip and limit
    start_idx = skip or 0
    end_idx = start_idx + (limit if limit is not None else len(videos))
    videos = videos[start_idx:end_idx]

    # Return final response structure
    return {
        "totalCount": api_data["total_count"],
        "retrieved": len(videos),
        "processedIn": api_data["processed_in"],
        "videos": videos
    }