from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for subtitle language information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - subtitle_0_language_code (str): Language code of first subtitle (e.g., 'en')
        - subtitle_0_language_name (str): Full name of first subtitle language (e.g., 'English')
        - subtitle_0_formats (str): Comma-separated formats available for first subtitle (e.g., 'vtt,srt')
        - subtitle_1_language_code (str): Language code of second subtitle (e.g., 'es')
        - subtitle_1_language_name (str): Full name of second subtitle language (e.g., 'Spanish')
        - subtitle_1_formats (str): Comma-separated formats available for second subtitle (e.g., 'vtt')
        - has_automatic_captions (bool): Whether auto-generated captions are available
        - video_title (str): Title of the video
        - detected_language_count (int): Total number of distinct subtitle languages detected
        - metadata_video_id (str): Video ID as identified by the service
        - metadata_extractor (str): Name of the extractor used (e.g., 'youtube')
        - metadata_retrieval_timestamp (str): ISO format timestamp of data retrieval
    """
    return {
        "subtitle_0_language_code": "en",
        "subtitle_0_language_name": "English",
        "subtitle_0_formats": "vtt,srt",
        "subtitle_1_language_code": "es",
        "subtitle_1_language_name": "Spanish",
        "subtitle_1_formats": "vtt",
        "has_automatic_captions": True,
        "video_title": "Sample Educational Video - Introduction to Python",
        "detected_language_count": 2,
        "metadata_video_id": "abc123xyz",
        "metadata_extractor": "youtube",
        "metadata_retrieval_timestamp": "2023-10-15T14:30:00Z"
    }

def yt_dlp_video_and_audio_downloader_list_subtitle_languages(url: str) -> Dict[str, Any]:
    """
    List all available subtitle languages and their formats for a video (including auto-generated captions).
    
    Args:
        url (str): URL of the video
        
    Returns:
        Dict containing:
        - subtitle_languages (List[Dict]): List of available subtitle language entries with language code,
          language name, and available formats
        - has_automatic_captions (bool): Whether the video has auto-generated captions
        - video_title (str): Title of the video
        - detected_language_count (int): Total number of distinct subtitle languages
        - metadata (Dict): Additional technical metadata including video ID, extractor, and timestamp
        
    Raises:
        ValueError: If URL is empty or invalid
    """
    if not url or not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    # Call external API to get flattened data
    api_data = call_external_api("yt-dlp-video-and-audio-downloader-list_subtitle_languages")
    
    # Construct subtitle languages list from indexed fields
    subtitle_languages: List[Dict[str, Any]] = []
    
    for i in range(2):  # We expect 2 items as per implementation instructions
        code_key = f"subtitle_{i}_language_code"
        name_key = f"subtitle_{i}_language_name"
        formats_key = f"subtitle_{i}_formats"
        
        if code_key in api_data and api_data[code_key]:
            formats_str = api_data.get(formats_key, "")
            formats = [fmt.strip() for fmt in formats_str.split(",")] if formats_str else []
            
            subtitle_languages.append({
                "language_code": api_data[code_key],
                "language_name": api_data[name_key],
                "formats": formats
            })
    
    # Construct metadata dictionary
    metadata = {
        "video_id": api_data["metadata_video_id"],
        "extractor": api_data["metadata_extractor"],
        "retrieval_timestamp": api_data["metadata_retrieval_timestamp"]
    }
    
    # Build final result matching output schema
    result = {
        "subtitle_languages": subtitle_languages,
        "has_automatic_captions": api_data["has_automatic_captions"],
        "video_title": api_data["video_title"],
        "detected_language_count": api_data["detected_language_count"],
        "metadata": metadata
    }
    
    return result