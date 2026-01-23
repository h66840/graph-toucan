from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching video danmaku data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - danmaku_0_content (str): Content of the first danmaku
        - danmaku_0_time_in_video (float): Appearance time of first danmaku in seconds
        - danmaku_0_color (str): Color code of first danmaku in hex
        - danmaku_0_style (str): Style type of first danmaku (e.g., 'scroll', 'top', 'bottom')
        - danmaku_0_sender_id (str): Sender UID of first danmaku
        - danmaku_0_send_time (str): Send timestamp of first danmaku in ISO format
        - danmaku_1_content (str): Content of the second danmaku
        - danmaku_1_time_in_video (float): Appearance time of second danmaku in seconds
        - danmaku_1_color (str): Color code of second danmaku in hex
        - danmaku_1_style (str): Style type of second danmaku
        - danmaku_1_sender_id (str): Sender UID of second danmaku
        - danmaku_1_send_time (str): Send timestamp of second danmaku in ISO format
        - video_bv_id (str): BV ID of the video
        - total_count (int): Total number of danmaku retrieved
        - segment_info_start_time (float): Start time of the segment in seconds
        - segment_info_end_time (float): End time of the segment in seconds
        - metadata_request_time (str): ISO formatted request timestamp
        - metadata_complete (bool): Whether the response contains all danmaku
        - metadata_encoding (str): Encoding format of the danmaku data
        - metadata_version (str): API version used
    """
    return {
        "danmaku_0_content": "这是一条测试弹幕",
        "danmaku_0_time_in_video": 12.34,
        "danmaku_0_color": "#FFFFFF",
        "danmaku_0_style": "scroll",
        "danmaku_0_sender_id": "12345678",
        "danmaku_0_send_time": "2023-10-01T12:00:00Z",
        "danmaku_1_content": "前方高能",
        "danmaku_1_time_in_video": 45.67,
        "danmaku_1_color": "#FFFF00",
        "danmaku_1_style": "top",
        "danmaku_1_sender_id": "87654321",
        "danmaku_1_send_time": "2023-10-01T12:01:30Z",
        "video_bv_id": "BV1Xx411c7mD",
        "total_count": 256,
        "segment_info_start_time": 0.0,
        "segment_info_end_time": 60.0,
        "metadata_request_time": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_complete": True,
        "metadata_encoding": "UTF-8",
        "metadata_version": "1.0.0"
    }

def bilibili_api_server_get_video_danmaku(bv_id: str) -> Dict[str, Any]:
    """
    获取视频的弹幕数据。
    
    Args:
        bv_id (str): 视频的BV号
        
    Returns:
        Dict containing:
        - danmaku_list (List[Dict]): 每条弹幕的详细信息
        - video_bv_id (str): 当前视频的BV号
        - total_count (int): 弹幕总数
        - segment_info (Dict): 分段信息，包含开始时间和结束时间
        - metadata (Dict): 元数据，包括请求时间、完整性、编码格式和版本
    
    Raises:
        ValueError: If bv_id is empty or invalid
    """
    if not bv_id or not isinstance(bv_id, str) or not bv_id.strip():
        raise ValueError("bv_id must be a non-empty string")
    
    bv_id = bv_id.strip()
    
    # Call external API to get flattened data
    api_data = call_external_api("bilibili-api-server-get_video_danmaku")
    
    # Construct danmaku list from indexed fields
    danmaku_list = [
        {
            "content": api_data["danmaku_0_content"],
            "time_in_video": api_data["danmaku_0_time_in_video"],
            "color": api_data["danmaku_0_color"],
            "style": api_data["danmaku_0_style"],
            "sender": {
                "id": api_data["danmaku_0_sender_id"],
                "send_time": api_data["danmaku_0_send_time"]
            }
        },
        {
            "content": api_data["danmaku_1_content"],
            "time_in_video": api_data["danmaku_1_time_in_video"],
            "color": api_data["danmaku_1_color"],
            "style": api_data["danmaku_1_style"],
            "sender": {
                "id": api_data["danmaku_1_sender_id"],
                "send_time": api_data["danmaku_1_send_time"]
            }
        }
    ]
    
    # Construct segment info
    segment_info = {
        "start_time": api_data["segment_info_start_time"],
        "end_time": api_data["segment_info_end_time"]
    }
    
    # Construct metadata
    metadata = {
        "request_time": api_data["metadata_request_time"],
        "complete": api_data["metadata_complete"],
        "encoding": api_data["metadata_encoding"],
        "version": api_data["metadata_version"]
    }
    
    # Final result structure
    result = {
        "danmaku_list": danmaku_list,
        "video_bv_id": api_data["video_bv_id"],
        "total_count": api_data["total_count"],
        "segment_info": segment_info,
        "metadata": metadata
    }
    
    return result