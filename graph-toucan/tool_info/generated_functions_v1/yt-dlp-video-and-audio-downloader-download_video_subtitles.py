from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for video subtitles download.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - subtitles_content (str): Raw subtitle content in WEBVTT format with timing and captions
        - format (str): Format of subtitles, always 'webvtt'
        - language (str): Language code of the subtitles, e.g., 'en'
        - kind (str): Type of captions, e.g., 'captions'
    """
    return {
        "subtitles_content": "WEBVTT\n\n1\n00:00:01.000 --> 00:00:04.000\nHello, welcome to the video.\n\n2\n00:00:05.000 --> 00:00:08.000\nThis is an example of subtitles.",
        "format": "webvtt",
        "language": "en",
        "kind": "captions"
    }

def yt_dlp_video_and_audio_downloader_download_video_subtitles(url: str, language: Optional[str] = None) -> Dict[str, Any]:
    """
    Download video subtitles in WEBVTT format from a given video URL.
    
    This function simulates downloading subtitles using yt-dlp, supporting both regular
    and auto-generated subtitles in various languages. The output is always in WEBVTT format.
    
    Args:
        url (str): URL of the video (required)
        language (Optional[str]): Language code (e.g., 'en', 'zh-Hant', 'ja'). If not available,
                                 attempts to retrieve auto-generated subtitles.
    
    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - subtitles_content (str): Raw subtitle content in WEBVTT format including timing metadata and caption text
            - format (str): Format of the returned subtitles, always "webvtt"
            - language (str): Language code of the subtitles as provided in the response metadata
            - kind (str): Type of captions, extracted from the WEBVTT metadata (e.g., 'captions')
    
    Raises:
        ValueError: If the URL is empty or invalid
    """
    if not url or not url.strip():
        raise ValueError("URL is required and cannot be empty")
    
    # Simulate calling external API to get subtitle data
    api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_video_subtitles")
    
    # Construct result matching the expected output schema
    result = {
        "subtitles_content": api_data["subtitles_content"],
        "format": api_data["format"],
        "language": api_data["language"],
        "kind": api_data["kind"]
    }
    
    return result