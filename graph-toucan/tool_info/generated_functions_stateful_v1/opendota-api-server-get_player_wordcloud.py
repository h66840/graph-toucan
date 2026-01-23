from typing import Dict, List, Any
from datetime import datetime

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
    Simulates fetching data from external API for player wordcloud.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - word_0_word (str): Most frequent word used by player
        - word_0_count (int): Frequency count of the most frequent word
        - word_1_word (str): Second most frequent word used by player
        - word_1_count (int): Frequency count of the second most frequent word
        - total_word_count (int): Total number of chat words analyzed
        - player_account_id (int): Steam32 account ID of the player
        - sample_size (int): Number of matches or chat samples used in analysis
        - generated_at (str): ISO 8601 timestamp when the wordcloud was generated
    """
    return {
        "word_0_word": "gg",
        "word_0_count": 156,
        "word_1_word": "push",
        "word_1_count": 132,
        "total_word_count": 2450,
        "player_account_id": 123456789,
        "sample_size": 45,
        "generated_at": "2023-10-05T14:32:18Z"
    }

def opendota_api_server_get_player_wordcloud(account_id: int) -> Dict[str, Any]:
    """
    Get most common words used by a player in chat.

    Args:
        account_id (int): Steam32 account ID of the player

    Returns:
        Dict containing:
        - words (List[Dict]): List of dictionaries with keys 'word' (str) and 'count' (int)
        - total_word_count (int): Total number of chat words analyzed
        - player_account_id (int): The Steam32 account ID of the player
        - sample_size (int): Number of matches or chat samples used in analysis
        - generated_at (str): ISO 8601 timestamp indicating when the data was generated

    Raises:
        ValueError: If account_id is not a positive integer
    """
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")

    # Call external API to get flattened data
    api_data = call_external_api("opendota-api-server-get_player_wordcloud", **locals())

    # Construct the words list from indexed fields
    words = [
        {"word": api_data["word_0_word"], "count": api_data["word_0_count"]},
        {"word": api_data["word_1_word"], "count": api_data["word_1_count"]}
    ]

    # Build final result structure matching output schema
    result = {
        "words": words,
        "total_word_count": api_data["total_word_count"],
        "player_account_id": api_data["player_account_id"],
        "sample_size": api_data["sample_size"],
        "generated_at": api_data["generated_at"]
    }

    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # POST
        if "post" in tool_name or "send" in tool_name:
            content = kwargs.get("content") or kwargs.get("text") or kwargs.get("message")
            if content:
                sys_state.post_content(content)
                
        # FEED
        if "get" in tool_name or "feed" in tool_name or "timeline" in tool_name:
            posts = sys_state.get_feed()
            if posts:
                 result["content"] = posts
    except Exception:
        pass
    return result
