from typing import Dict, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
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
        api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_audio", **locals())
        
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

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
