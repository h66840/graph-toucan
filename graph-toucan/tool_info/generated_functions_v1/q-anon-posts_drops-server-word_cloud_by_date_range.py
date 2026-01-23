from typing import Dict, List, Any, Optional
from datetime import datetime
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for word cloud analysis by date range.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - date_range_start (str): Start date in YYYY-MM-DD format
        - date_range_end (str): End date in YYYY-MM-DD format
        - post_id_range_min (int): Minimum post ID analyzed
        - post_id_range_max (int): Maximum post ID analyzed
        - total_posts_analyzed (int): Total number of posts processed
        - total_filtered_words (int): Total unique words after filtering
        - top_words_count (int): Number of words included in result
        - word_0_word (str): First most frequent word
        - word_0_count (int): Frequency count of first word
        - word_0_percentage (float): Percentage of first word usage
        - word_0_bar_representation (str): Bar representation string for first word
        - word_1_word (str): Second most frequent word
        - word_1_count (int): Frequency count of second word
        - word_1_percentage (float): Percentage of second word usage
        - word_1_bar_representation (str): Bar representation string for second word
    """
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    min_post_id = random.randint(1000, 5000)
    max_post_id = min_post_id + random.randint(50, 200)
    total_posts = random.randint(50, 150)
    total_filtered = random.randint(200, 500)
    top_words = random.randint(50, 100)
    
    # Generate realistic common words
    common_words = [
        "crypto", "blockchain", "nft", "market", "price", "trading", 
        "digital", "wallet", "security", "privacy", "decentralized",
        "ethereum", "bitcoin", "token", "smart", "contract"
    ]
    
    # Sample two distinct words
    selected_words = random.sample(common_words, 2)
    
    # Generate counts and percentages
    count1 = random.randint(80, 200)
    count2 = random.randint(50, 120)
    total_count = count1 + count2 + random.randint(100, 300)  # simulate other words
    
    percentage1 = round((count1 / total_count) * 100, 2)
    percentage2 = round((count2 / total_count) * 100, 2)
    
    # Create bar representations (simple text bars)
    bar1 = "█" * int(percentage1 // 2)  # scale down for display
    bar2 = "█" * int(percentage2 // 2)
    
    return {
        "date_range_start": start_date,
        "date_range_end": end_date,
        "post_id_range_min": min_post_id,
        "post_id_range_max": max_post_id,
        "total_posts_analyzed": total_posts,
        "total_filtered_words": total_filtered,
        "top_words_count": top_words,
        "word_0_word": selected_words[0],
        "word_0_count": count1,
        "word_0_percentage": percentage1,
        "word_0_bar_representation": bar1,
        "word_1_word": selected_words[1],
        "word_1_count": count2,
        "word_1_percentage": percentage2,
        "word_1_bar_representation": bar2
    }

def q_anon_posts_drops_server_word_cloud_by_date_range(
    start_date: str,
    end_date: str,
    min_word_length: Optional[int] = 3,
    max_words: Optional[int] = 100
) -> Dict[str, Any]:
    """
    Generate a word cloud analysis showing the most common words used in posts within a specified date range.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        min_word_length (Optional[int]): Minimum length of words to include (default: 3)
        max_words (Optional[int]): Maximum number of words to return (default: 100)
    
    Returns:
        Dict containing:
        - date_range (Dict): contains 'start' and 'end' date strings in YYYY-MM-DD format
        - post_id_range (Dict): contains 'min' and 'max' post IDs analyzed as integers
        - total_posts_analyzed (int): total number of posts processed
        - word_frequencies (List[Dict]): list of word frequency entries with 'word', 'count', 'percentage', 'bar_representation'
        - total_filtered_words (int): total number of unique words after filtering
        - top_words_count (int): number of words included in the returned word cloud
    
    Raises:
        ValueError: If date format is invalid or start_date > end_date
    """
    # Input validation
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}")
    
    if start_dt > end_dt:
        raise ValueError("start_date must be less than or equal to end_date")
    
    # Validate min_word_length and max_words
    if min_word_length is not None and min_word_length < 1:
        raise ValueError("min_word_length must be at least 1")
    
    if max_words is not None and max_words < 1:
        raise ValueError("max_words must be at least 1")
    
    # Get data from external API (simulated)
    api_data = call_external_api("q-anon-posts/drops-server-word_cloud_by_date_range")
    
    # Construct the nested output structure
    result = {
        "date_range": {
            "start": api_data["date_range_start"],
            "end": api_data["date_range_end"]
        },
        "post_id_range": {
            "min": api_data["post_id_range_min"],
            "max": api_data["post_id_range_max"]
        },
        "total_posts_analyzed": api_data["total_posts_analyzed"],
        "total_filtered_words": api_data["total_filtered_words"],
        "top_words_count": api_data["top_words_count"],
        "word_frequencies": [
            {
                "word": api_data["word_0_word"],
                "count": api_data["word_0_count"],
                "percentage": api_data["word_0_percentage"],
                "bar_representation": api_data["word_0_bar_representation"]
            },
            {
                "word": api_data["word_1_word"],
                "count": api_data["word_1_count"],
                "percentage": api_data["word_1_percentage"],
                "bar_representation": api_data["word_1_bar_representation"]
            }
        ]
    }
    
    # Apply max_words limit (ensure we don't return more than requested)
    if max_words is not None and max_words < len(result["word_frequencies"]):
        result["word_frequencies"] = result["word_frequencies"][:max_words]
        result["top_words_count"] = len(result["word_frequencies"])
    
    # In a real implementation, we would filter words by min_word_length here
    # For this simulation, we assume the API already applied filtering
    
    return result