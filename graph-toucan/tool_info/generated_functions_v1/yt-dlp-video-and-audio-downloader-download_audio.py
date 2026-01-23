from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for audio download operation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - file_path (str): Local file system path where the audio was saved
        - format (str): Audio format of the downloaded file (e.g., 'm4a', 'mp3')
        - file_size_bytes (int): Size of the downloaded audio file in bytes
        - download_status (str): Status of the download operation ('success', 'failed', etc.)
        - url (str): Original URL of the video that was processed
        - title (str): Title of the video/audio content as extracted from the source
        - duration_seconds (float): Duration of the audio in seconds
        - bitrate (int): Bitrate of the audio stream in kbps, if available
        - metadata_uploader (str): Uploader of the video
        - metadata_upload_date (str): Upload date in YYYYMMDD format
        - metadata_thumbnail_url (str): URL to the thumbnail image
        - error_message (str): Error description if download failed; null otherwise
    """
    return {
        "file_path": "/Users/test/Downloads/sample_audio.m4a",
        "format": "m4a",
        "file_size_bytes": 4194304,
        "download_status": "success",
        "url": "https://www.youtube.com/watch?v=example",
        "title": "Sample Music Track - Official Audio",
        "duration_seconds": 245.75,
        "bitrate": 128,
        "metadata_uploader": "OfficialArtistChannel",
        "metadata_upload_date": "20231201",
        "metadata_thumbnail_url": "https://i.ytimg.com/vi/example/maxresdefault.jpg",
        "error_message": None
    }

def yt_dlp_video_and_audio_downloader_download_audio(url: str) -> Dict[str, Any]:
    """
    Download audio in best available quality (usually m4a/mp3 format) to the user's default Downloads folder.
    
    Args:
        url (str): URL of the video
        
    Returns:
        Dict containing the following fields:
        - file_path (str): Local file system path where the audio was saved
        - format (str): Audio format of the downloaded file (e.g., 'm4a', 'mp3')
        - file_size_bytes (int): Size of the downloaded audio file in bytes
        - download_status (str): Status of the download operation ('success', 'failed', etc.)
        - url (str): Original URL of the video that was processed
        - title (str): Title of the video/audio content as extracted from the source
        - duration_seconds (float): Duration of the audio in seconds
        - bitrate (int): Bitrate of the audio stream in kbps, if available
        - metadata (Dict): Additional metadata extracted during download (e.g., uploader, upload_date, thumbnail_url)
        - error_message (Optional[str]): Error description if download failed; None otherwise
    """
    # Input validation
    if not url or not isinstance(url, str):
        return {
            "file_path": "",
            "format": "",
            "file_size_bytes": 0,
            "download_status": "failed",
            "url": url or "",
            "title": "",
            "duration_seconds": 0.0,
            "bitrate": 0,
            "metadata": {},
            "error_message": "Invalid URL provided"
        }
    
    try:
        # Call external API to get the data
        api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_audio")
        
        # Construct the metadata dictionary from flattened fields
        metadata = {
            "uploader": api_data["metadata_uploader"],
            "upload_date": api_data["metadata_upload_date"],
            "thumbnail_url": api_data["metadata_thumbnail_url"]
        }
        
        # Build the final result structure
        result = {
            "file_path": api_data["file_path"],
            "format": api_data["format"],
            "file_size_bytes": api_data["file_size_bytes"],
            "download_status": api_data["download_status"],
            "url": api_data["url"],
            "title": api_data["title"],
            "duration_seconds": api_data["duration_seconds"],
            "bitrate": api_data["bitrate"],
            "metadata": metadata,
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except Exception as e:
        return {
            "file_path": "",
            "format": "",
            "file_size_bytes": 0,
            "download_status": "failed",
            "url": url,
            "title": "",
            "duration_seconds": 0.0,
            "bitrate": 0,
            "metadata": {},
            "error_message": str(e)
        }