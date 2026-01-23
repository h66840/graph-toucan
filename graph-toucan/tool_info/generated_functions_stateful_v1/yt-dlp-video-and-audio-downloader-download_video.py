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
    Simulates fetching data from external API for video download operation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - file_name (str): Name of the downloaded video file
        - file_size (str): Size of the downloaded file in human-readable format
        - download_path (str): Full path to the directory where the file was saved
        - status (str): Status of the download operation ("success" or "failed")
    """
    return {
        "file_name": "example_video_720p.mp4",
        "file_size": "150MB",
        "download_path": "/home/user/Downloads",
        "status": "success"
    }

def yt_dlp_video_and_audio_downloader_download_video(url: str, resolution: Optional[str] = "720p") -> Dict[str, Any]:
    """
    Download video to the user's default Downloads folder.
    
    Args:
        url (str): URL of the video (required)
        resolution (str, optional): Preferred video resolution. For YouTube: '480p', '720p', '1080p', 'best'. 
                                   For other platforms: '480p' for low quality, '720p'/'1080p' for HD, 
                                   'best' for highest quality. Defaults to '720p'.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - file_name (str): name of the downloaded video file
            - file_size (str): size of the downloaded file in human-readable format (e.g., "11MB")
            - download_path (str): full path to the directory where the file was saved
            - status (str): status of the download operation, typically "success" or "failed"
    
    Raises:
        ValueError: If url is not provided
    """
    if not url:
        raise ValueError("URL is required")
        
    # Validate resolution if provided
    if resolution:
        valid_resolutions = ['480p', '720p', '1080p', 'best']
        if resolution not in valid_resolutions:
            # Use default if invalid
            resolution = '720p'
    
    # Call external API to simulate download
    api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_video", **locals())
    
    # Construct result matching output schema
    result = {
        "file_name": api_data["file_name"],
        "file_size": api_data["file_size"],
        "download_path": api_data["download_path"],
        "status": api_data["status"]
    }
    
    return result

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
