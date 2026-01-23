from typing import Dict, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching transcript data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - transcript_id (int): The ID of the transcript
        - transcript_text (str): Full text of the transcript
        - segment_0_start (float): Start time of first segment in seconds
        - segment_0_end (float): End time of first segment in seconds
        - segment_0_text (str): Text of first segment
        - segment_1_start (float): Start time of second segment in seconds
        - segment_1_end (float): End time of second segment in seconds
        - segment_1_text (str): Text of second segment
        - transcript_created_at (str): Creation timestamp in ISO format
        - transcript_updated_at (str): Last update timestamp in ISO format
        - transcript_source (str): Source of the transcript (e.g., 'meeting', 'interview')
        - transcript_language (str): Language code (e.g., 'en', 'zh')
        - status (str): Operation status ('success' or 'not_found')
        - error_message (str): Error description if retrieval failed
    """
    return {
        "transcript_id": 12345,
        "transcript_text": "Hello, this is a sample transcript for demonstration purposes.",
        "segment_0_start": 0.0,
        "segment_0_end": 5.5,
        "segment_0_text": "Hello,",
        "segment_1_start": 5.5,
        "segment_1_end": 12.3,
        "segment_1_text": "this is a sample transcript for demonstration purposes.",
        "transcript_created_at": "2023-10-01T08:00:00Z",
        "transcript_updated_at": "2023-10-01T08:05:00Z",
        "transcript_source": "meeting",
        "transcript_language": "en",
        "status": "success",
        "error_message": ""
    }


def votars_mcp_Votars_fetch_a_specific_transcript(id: int) -> Dict[str, Any]:
    """
    Retrieve the transcript from the workspace by its ID.

    Args:
        id (int): Transcript ID to retrieve

    Returns:
        Dict containing:
        - transcript (Dict): Full transcript data including content, metadata, and structure.
          Keys include 'id', 'text', 'segments', 'created_at', 'updated_at', 'source', and 'language'.
        - status (str): Indicates the result of the operation, e.g., 'success' or 'not_found'.
        - error_message (Optional[str]): Present only if retrieval failed, providing details about the issue.

    Example:
        {
            "transcript": {
                "id": 12345,
                "text": "Hello, this is a sample transcript...",
                "segments": [
                    {"start": 0.0, "end": 5.5, "text": "Hello,"},
                    {"start": 5.5, "end": 12.3, "text": "this is a sample transcript..."}
                ],
                "created_at": "2023-10-01T08:00:00Z",
                "updated_at": "2023-10-01T08:05:00Z",
                "source": "meeting",
                "language": "en"
            },
            "status": "success",
            "error_message": ""
        }
    """
    # Validate input
    if not isinstance(id, int) or id <= 0:
        return {
            "transcript": None,
            "status": "not_found",
            "error_message": "Invalid transcript ID: must be a positive integer"
        }

    # Fetch data from external API (simulated)
    api_data = call_external_api("votars-mcp-Votars fetch a specific transcript")

    # Check if the operation was successful
    if api_data["status"] != "success":
        return {
            "transcript": None,
            "status": api_data["status"],
            "error_message": api_data["error_message"]
        }

    # Construct segments list from indexed fields
    segments = [
        {
            "start": api_data["segment_0_start"],
            "end": api_data["segment_0_end"],
            "text": api_data["segment_0_text"]
        },
        {
            "start": api_data["segment_1_start"],
            "end": api_data["segment_1_end"],
            "text": api_data["segment_1_text"]
        }
    ]

    # Construct the full transcript object
    transcript = {
        "id": api_data["transcript_id"],
        "text": api_data["transcript_text"],
        "segments": segments,
        "created_at": api_data["transcript_created_at"],
        "updated_at": api_data["transcript_updated_at"],
        "source": api_data["transcript_source"],
        "language": api_data["transcript_language"]
    }

    return {
        "transcript": transcript,
        "status": api_data["status"],
        "error_message": api_data["error_message"]
    }