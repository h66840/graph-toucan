from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("yt-dlp-video-and-audio-downloader-download_video")
    
    # Construct result matching output schema
    result = {
        "file_name": api_data["file_name"],
        "file_size": api_data["file_size"],
        "download_path": api_data["download_path"],
        "status": api_data["status"]
    }
    
    return result