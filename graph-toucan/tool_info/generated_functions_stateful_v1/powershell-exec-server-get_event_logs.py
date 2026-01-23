from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

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
    Simulates fetching data from external API for event log retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - event_0_event_id (int): First event's ID
        - event_0_level (int): First event's level (1-4)
        - event_0_timestamp (str): First event's timestamp in ISO format
        - event_0_message (str): First event's message
        - event_0_source (str): First event's source
        - event_1_event_id (int): Second event's ID
        - event_1_level (int): Second event's level (1-4)
        - event_1_timestamp (str): Second event's timestamp in ISO format
        - event_1_message (str): Second event's message
        - event_1_source (str): Second event's source
        - total_count (int): Total number of events returned
        - log_name (str): Name of the event log
        - filtered_by_level (int): Level filter applied (1-4), null if none
        - retrieval_duration_sec (float): Duration of retrieval in seconds
        - oldest_timestamp (str): Oldest event timestamp in ISO format
        - newest_timestamp (str): Newest event timestamp in ISO format
        - success (bool): Whether operation succeeded
        - error_message (str): Error message if failed, empty otherwise
    """
    now = datetime.now()
    level = random.randint(1, 4)
    
    return {
        "event_0_event_id": random.randint(1000, 9999),
        "event_0_level": level,
        "event_0_timestamp": (now - timedelta(minutes=5)).isoformat(),
        "event_0_message": f"Sample event message for event ID {random.randint(1000, 9999)}",
        "event_0_source": f"SampleSource{random.randint(1, 10)}",
        "event_1_event_id": random.randint(1000, 9999),
        "event_1_level": random.randint(1, 4),
        "event_1_timestamp": now.isoformat(),
        "event_1_message": f"Another sample event message for event ID {random.randint(1000, 9999)}",
        "event_1_source": f"SampleSource{random.randint(1, 10)}",
        "total_count": 2,
        "log_name": "Application",
        "filtered_by_level": level,
        "retrieval_duration_sec": round(random.uniform(0.1, 2.0), 3),
        "oldest_timestamp": (now - timedelta(minutes=5)).isoformat(),
        "newest_timestamp": now.isoformat(),
        "success": True,
        "error_message": ""
    }

def powershell_exec_server_get_event_logs(
    logname: str,
    newest: Optional[int] = 10,
    level: Optional[int] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Get Windows event logs from a server using PowerShell.
    
    Args:
        logname (str): Name of the event log (System, Application, Security, etc.)
        newest (Optional[int]): Number of most recent events to retrieve (default 10)
        level (Optional[int]): Filter by event level (1: Critical, 2: Error, 3: Warning, 4: Information)
        timeout (Optional[int]): Command timeout in seconds (1-300, default 60)
    
    Returns:
        Dict containing:
        - events (List[Dict]): List of event log entries with details
        - total_count (int): Total number of events returned
        - log_name (str): Name of the event log
        - query_metadata (Dict): Information about query execution
        - success (bool): Whether operation completed successfully
        - error_message (str): Error description if failed, None otherwise
    """
    # Input validation
    if not logname:
        return {
            "events": [],
            "total_count": 0,
            "log_name": "",
            "query_metadata": {
                "filtered_by_level": level,
                "retrieval_duration_sec": 0,
                "oldest_timestamp": "",
                "newest_timestamp": ""
            },
            "success": False,
            "error_message": "logname is required"
        }
    
    if timeout and (timeout < 1 or timeout > 300):
        return {
            "events": [],
            "total_count": 0,
            "log_name": "",
            "query_metadata": {
                "filtered_by_level": level,
                "retrieval_duration_sec": 0,
                "oldest_timestamp": "",
                "newest_timestamp": ""
            },
            "success": False,
            "error_message": "timeout must be between 1 and 300 seconds"
        }
    
    # Use default values if not provided
    newest = newest or 10
    
    try:
        # Call external API to get data
        api_data = call_external_api("powershell-exec-server-get_event_logs", **locals())
        
        # Construct events list from flattened data
        events = [
            {
                "event_id": api_data["event_0_event_id"],
                "level": api_data["event_0_level"],
                "timestamp": api_data["event_0_timestamp"],
                "message": api_data["event_0_message"],
                "source": api_data["event_0_source"]
            },
            {
                "event_id": api_data["event_1_event_id"],
                "level": api_data["event_1_level"],
                "timestamp": api_data["event_1_timestamp"],
                "message": api_data["event_1_message"],
                "source": api_data["event_1_source"]
            }
        ]
        
        # Apply level filter if specified
        if level is not None:
            events = [event for event in events if event["level"] == level]
        
        # Apply newest limit
        events = events[:newest]
        
        # Construct result following output schema
        result = {
            "events": events,
            "total_count": len(events),
            "log_name": api_data["log_name"],
            "query_metadata": {
                "filtered_by_level": api_data["filtered_by_level"] if level is not None else None,
                "retrieval_duration_sec": api_data["retrieval_duration_sec"],
                "oldest_timestamp": api_data["oldest_timestamp"],
                "newest_timestamp": api_data["newest_timestamp"]
            },
            "success": api_data["success"],
            "error_message": api_data["error_message"] if api_data["error_message"] else None
        }
        
        return result
        
    except Exception as e:
        return {
            "events": [],
            "total_count": 0,
            "log_name": logname,
            "query_metadata": {
                "filtered_by_level": level,
                "retrieval_duration_sec": 0,
                "oldest_timestamp": "",
                "newest_timestamp": ""
            },
            "success": False,
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
