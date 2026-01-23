from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for word cloud analysis by post IDs.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - analysis_title (str): Title of the word cloud analysis
        - date_range_start (str): Start date in YYYY-MM-DD format
        - date_range_end (str): End date in YYYY-MM-DD format
        - total_posts_analyzed (int): Number of posts analyzed
        - total_filtered_words (int): Total count of filtered words
        - max_words (int): Maximum number of words returned
        - min_word_length (int): Minimum word length included
        - word_0_word (str): First most frequent word
        - word_0_count (int): Frequency of first word
        - word_0_percentage (float): Percentage of first word
        - word_0_bar (str): Bar representation for first word
        - word_1_word (str): Second most frequent word
        - word_1_count (int): Frequency of second word
        - word_1_percentage (float): Percentage of second word
        - word_1_bar (str): Bar representation for second word
    """
    # Generate realistic mock data based on input range
    start_date = (datetime.now() - timedelta(days=random.randint(30, 100))).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    return {
        "analysis_title": f"Word Cloud Analysis: Posts {1001} to {1100}",
        "date_range_start": start_date,
        "date_range_end": end_date,
        "total_posts_analyzed": random.randint(80, 120),
        "total_filtered_words": random.randint(5000, 15000),
        "max_words": 100,
        "min_word_length": 3,
        "word_0_word": "digital",
        "word_0_count": 142,
        "word_0_percentage": 8.7,
        "word_0_bar": "█" * 17,
        "word_1_word": "future",
        "word_1_count": 128,
        "word_1_percentage": 7.9,
        "word_1_bar": "█" * 15
    }

def q_anon_posts_drops_server_word_cloud_by_post_ids(
    start_id: int,
    end_id: int,
    min_word_length: Optional[int] = 3,
    max_words: Optional[int] = 100
) -> Dict[str, Any]:
    """
    Generate a word cloud analysis showing the most common words used in posts within a specified ID range.
    
    Args:
        start_id (int): Starting post ID (required)
        end_id (int): Ending post ID (required)
        min_word_length (Optional[int]): Minimum length of words to include (default: 3)
        max_words (Optional[int]): Maximum number of words to return (default: 100)
    
    Returns:
        Dict containing:
        - analysis_title (str): title of the word cloud analysis indicating the post ID range
        - date_range (Dict): contains 'start' and 'end' dates as strings in YYYY-MM-DD format
        - total_posts_analyzed (int): total number of posts included in the analysis
        - total_filtered_words (int): total count of words after filtering before ranking
        - max_words (int): maximum number of top words returned
        - min_word_length (int): minimum character length of words included
        - word_frequencies (List[Dict]): list of top words with 'word', 'count', 'percentage', 'bar'
    
    Raises:
        ValueError: If start_id > end_id or if any parameter is invalid
    """
    # Input validation
    if start_id <= 0:
        raise ValueError("start_id must be a positive integer")
    if end_id <= 0:
        raise ValueError("end_id must be a positive integer")
    if start_id > end_id:
        raise ValueError("start_id cannot be greater than end_id")
    if min_word_length is not None and min_word_length < 1:
        raise ValueError("min_word_length must be at least 1")
    if max_words is not None and max_words < 1:
        raise ValueError("max_words must be at least 1")
    
    # Set defaults if not provided
    min_word_length = min_word_length if min_word_length is not None else 3
    max_words = max_words if max_words is not None else 100
    
    # Call external API to get data (simulated)
    api_data = call_external_api("q-anon-posts/drops-server-word_cloud_by_post_ids")
    
    # Construct nested output structure matching schema
    result = {
        "analysis_title": api_data["analysis_title"],
        "date_range": {
            "start": api_data["date_range_start"],
            "end": api_data["date_range_end"]
        },
        "total_posts_analyzed": api_data["total_posts_analyzed"],
        "total_filtered_words": api_data["total_filtered_words"],
        "max_words": api_data["max_words"],
        "min_word_length": api_data["min_word_length"],
        "word_frequencies": [
            {
                "word": api_data["word_0_word"],
                "count": api_data["word_0_count"],
                "percentage": api_data["word_0_percentage"],
                "bar": api_data["word_0_bar"]
            },
            {
                "word": api_data["word_1_word"],
                "count": api_data["word_1_count"],
                "percentage": api_data["word_1_percentage"],
                "bar": api_data["word_1_bar"]
            }
        ]
    }
    
    return result