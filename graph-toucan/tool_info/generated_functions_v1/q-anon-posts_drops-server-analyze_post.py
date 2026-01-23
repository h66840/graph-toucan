from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for post analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - basic_info_author (str): Author name of the post
        - basic_info_author_id (int): Author ID
        - basic_info_date (str): Post date in ISO format
        - basic_info_source (str): Source platform of the post
        - basic_info_original_link (str): Original URL of the post
        - post_content (str): Full text content of the post
        - images_0_file_hash (str): File hash of first image
        - images_0_filename (str): Filename of first image
        - images_1_file_hash (str): File hash of second image
        - images_1_filename (str): Filename of second image
        - context_total_posts_in_dataset (int): Total number of posts in dataset
        - context_chronological_position (int): Chronological position of this post
        - context_previous_post_id (int): ID of previous post
        - context_previous_post_date (str): Date of previous post in ISO format
        - context_next_post_id (int): ID of next post
        - context_next_post_date (str): Date of next post in ISO format
    """
    return {
        "basic_info_author": "AnonymousUser42",
        "basic_info_author_id": 1001,
        "basic_info_date": "2023-10-05T14:30:00Z",
        "basic_info_source": "QAnonForums.net",
        "basic_info_original_link": "https://qanonforums.net/post/12345",
        "post_content": "This is a detailed drop containing important information about upcoming events. Trust the plan. The storm is coming. Follow the white rabbit.",
        "images_0_file_hash": "a1b2c3d4e5f67890",
        "images_0_filename": "drop_image_1.png",
        "images_1_file_hash": "f0e9d8c7b6a54321",
        "images_1_filename": "drop_image_2.jpg",
        "context_total_posts_in_dataset": 5420,
        "context_chronological_position": 3421,
        "context_previous_post_id": 12344,
        "context_previous_post_date": "2023-10-05T14:25:00Z",
        "context_next_post_id": 12346,
        "context_next_post_date": "2023-10-05T14:35:00Z"
    }

def q_anon_posts_drops_server_analyze_post(post_id: int) -> Dict[str, Any]:
    """
    Get detailed analysis of a specific post/drop including references and context.
    
    Args:
        post_id (int): The ID of the post to analyze
        
    Returns:
        Dict containing:
        - basic_info (Dict): contains 'author', 'author_id', 'date', 'source', 'original_link' fields
        - post_content (str): full text content of the post/drop
        - images (List[Dict]): list of image attachments, each with 'file_hash', 'filename' fields
        - context (Dict): contains 'total_posts_in_dataset', 'chronological_position', 
                         'previous_post_id', 'previous_post_date', 'next_post_id', 'next_post_date' fields
                         
    Raises:
        ValueError: If post_id is not a positive integer
    """
    # Input validation
    if not isinstance(post_id, int) or post_id <= 0:
        raise ValueError("post_id must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("q-anon-posts/drops-server-analyze_post")
    
    # Construct nested output structure
    result = {
        "basic_info": {
            "author": api_data["basic_info_author"],
            "author_id": api_data["basic_info_author_id"],
            "date": api_data["basic_info_date"],
            "source": api_data["basic_info_source"],
            "original_link": api_data["basic_info_original_link"]
        },
        "post_content": api_data["post_content"],
        "images": [
            {
                "file_hash": api_data["images_0_file_hash"],
                "filename": api_data["images_0_filename"]
            },
            {
                "file_hash": api_data["images_1_file_hash"],
                "filename": api_data["images_1_filename"]
            }
        ],
        "context": {
            "total_posts_in_dataset": api_data["context_total_posts_in_dataset"],
            "chronological_position": api_data["context_chronological_position"],
            "previous_post_id": api_data["context_previous_post_id"],
            "previous_post_date": api_data["context_previous_post_date"],
            "next_post_id": api_data["context_next_post_id"],
            "next_post_date": api_data["context_next_post_date"]
        }
    }
    
    return result