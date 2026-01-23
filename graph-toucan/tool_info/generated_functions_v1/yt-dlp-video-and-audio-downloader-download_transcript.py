from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for video transcript download.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - transcript (str): Plain text transcript content
        - language (str): Language code of the transcript
        - source_url (str): URL of the video source
        - download_success (bool): Whether download and processing succeeded
        - error_message (str): Error description if failed, else empty string
        - metadata_format (str): Format of the original subtitle file (e.g., vtt, srt)
        - metadata_auto_generated (bool): Whether subtitles were auto-generated
    """
    return {
        "transcript": "Hello world this is a sample video transcript. Welcome to the demonstration of yt-dlp transcript downloader. Today we will show how subtitles are extracted and cleaned.",
        "language": "en",
        "source_url": "https://www.youtube.com/watch?v=example123",
        "download_success": True,
        "error_message": "",
        "metadata_format": "vtt",
        "metadata_auto_generated": False
    }

def yt_dlp_video_and_audio_downloader_download_transcript(language: Optional[str] = 'en', url: str = "") -> Dict[str, Any]:
    """
    Download and clean video subtitles to produce a plain text transcript without timestamps or formatting.
    
    Args:
        language (Optional[str]): Language code (e.g., 'en', 'zh-Hant', 'ja'). Defaults to 'en'
        url (str): URL of the video (required)
    
    Returns:
        Dict containing:
        - transcript (str): Plain text transcript extracted from the video, with timestamps and formatting removed
        - language (str): Language code of the downloaded transcript, matching the requested language or auto-detected if not specified
        - source_url (str): URL of the video from which the transcript was downloaded
        - download_success (bool): Indicates whether the transcript was successfully downloaded and processed
        - error_message (Optional[str]): Error description if download or processing failed; None otherwise
        - metadata (Dict): Additional information about the transcript such as source format, availability, and extraction details
    """
    # Input validation
    if not url:
        return {
            "transcript": "",
            "language": language or "en",
            "source_url": url,
            "download_success": False,
            "error_message": "URL is required",
            "metadata": {}
        }
    
    try:
        # Call external API to get transcript data
        api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_transcript")
        
        # Construct the result using data from API
        transcript = api_data["transcript"]
        detected_language = api_data["language"]
        success = api_data["download_success"]
        error_msg = api_data["error_message"] if api_data["error_message"] else None
        
        # Build metadata dictionary from flattened API response
        metadata = {
            "format": api_data["metadata_format"],
            "auto_generated": api_data["metadata_auto_generated"]
        }
        
        result = {
            "transcript": transcript,
            "language": detected_language,
            "source_url": api_data["source_url"],
            "download_success": success,
            "error_message": error_msg,
            "metadata": metadata
        }
        
        return result
        
    except Exception as e:
        return {
            "transcript": "",
            "language": language or "en",
            "source_url": url,
            "download_success": False,
            "error_message": str(e),
            "metadata": {}
        }