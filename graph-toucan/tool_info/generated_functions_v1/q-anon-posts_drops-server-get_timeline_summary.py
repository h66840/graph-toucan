from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for QAnon posts timeline summary.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - timeline_title (str): Title of the timeline summary
        - months_0_month_year (str): First month in "Month YYYY" format
        - months_0_post_count (int): Number of posts in first month
        - months_0_posts_0_date (str): Date of first post in first month (DD)
        - months_0_posts_0_post_id (str): Post ID of first post in first month
        - months_0_posts_0_content (str): Content of first post in first month
        - months_0_posts_0_truncated (bool): Whether first post content is truncated
        - months_0_posts_1_date (str): Date of second post in first month (DD)
        - months_0_posts_1_post_id (str): Post ID of second post in first month
        - months_0_posts_1_content (str): Content of second post in first month
        - months_0_posts_1_truncated (bool): Whether second post content is truncated
        - months_1_month_year (str): Second month in "Month YYYY" format
        - months_1_post_count (int): Number of posts in second month
        - months_1_posts_0_date (str): Date of first post in second month (DD)
        - months_1_posts_0_post_id (str): Post ID of first post in second month
        - months_1_posts_0_content (str): Content of first post in second month
        - months_1_posts_0_truncated (bool): Whether first post content is truncated
        - months_1_posts_1_date (str): Date of second post in second month (DD)
        - months_1_posts_1_post_id (str): Post ID of second post in second month
        - months_1_posts_1_content (str): Content of second post in second month
        - months_1_posts_1_truncated (bool): Whether second post content is truncated
    """
    return {
        "timeline_title": "QAnon Posts Timeline",
        "months_0_month_year": "November 2017",
        "months_0_post_count": 3,
        "months_0_posts_0_date": "04",
        "months_0_posts_0_post_id": "#1234",
        "months_0_posts_0_content": "The plan is in motion. Trust the plan. Many will be arrested soon...",
        "months_0_posts_0_truncated": True,
        "months_0_posts_1_date": "05",
        "months_0_posts_1_post_id": "#1235",
        "months_0_posts_1_content": "Patriots are in control. The deep state is crumbling. Stay vigilant.",
        "months_0_posts_1_truncated": False,
        "months_1_month_year": "December 2017",
        "months_1_post_count": 2,
        "months_1_posts_0_date": "01",
        "months_1_posts_0_post_id": "#1236",
        "months_1_posts_0_content": "Big moves happening behind the scenes. The truth will come out soon...",
        "months_1_posts_0_truncated": True,
        "months_1_posts_1_date": "03",
        "months_1_posts_1_post_id": "#1237",
        "months_1_posts_1_content": "Trust the plan. The storm is coming. Patriots will prevail.",
        "months_1_posts_1_truncated": False,
    }

def q_anon_posts_drops_server_get_timeline_summary(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a timeline summary of QAnon posts/drops, optionally within a date range.
    
    Args:
        start_date (Optional[str]): Optional start date in YYYY-MM-DD format
        end_date (Optional[str]): Optional end date in YYYY-MM-DD format
    
    Returns:
        Dict containing:
        - timeline_title (str): title of the timeline summary
        - months (List[Dict]): list of monthly post summaries with month_year, post_count, and posts
          - Each month dict contains:
            - month_year (str): month and year in "Month YYYY" format
            - post_count (int): total number of posts in that month
            - posts (List[Dict]): list of individual posts with date, post_id, content, truncated
              - Each post dict contains:
                - date (str): day of the month in DD format
                - post_id (str): unique identifier in format "#XXXX"
                - content (str): full or partial text of the post
                - truncated (bool): whether the content was cut off with ellipsis
    
    Raises:
        ValueError: If date format is invalid
    """
    # Validate date formats if provided
    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("start_date must be in YYYY-MM-DD format")
    
    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("end_date must be in YYYY-MM-DD format")
    
    # Call external API to get data (with only simple fields)
    api_data = call_external_api("q-anon-posts/drops-server-get_timeline_summary")
    
    # Construct the nested structure from flat API data
    months = []
    
    # Process first month
    month_0_posts = [
        {
            "date": api_data["months_0_posts_0_date"],
            "post_id": api_data["months_0_posts_0_post_id"],
            "content": api_data["months_0_posts_0_content"],
            "truncated": api_data["months_0_posts_0_truncated"]
        },
        {
            "date": api_data["months_0_posts_1_date"],
            "post_id": api_data["months_0_posts_1_post_id"],
            "content": api_data["months_0_posts_1_content"],
            "truncated": api_data["months_0_posts_1_truncated"]
        }
    ]
    
    months.append({
        "month_year": api_data["months_0_month_year"],
        "post_count": api_data["months_0_post_count"],
        "posts": month_0_posts
    })
    
    # Process second month
    month_1_posts = [
        {
            "date": api_data["months_1_posts_0_date"],
            "post_id": api_data["months_1_posts_0_post_id"],
            "content": api_data["months_1_posts_0_content"],
            "truncated": api_data["months_1_posts_0_truncated"]
        },
        {
            "date": api_data["months_1_posts_1_date"],
            "post_id": api_data["months_1_posts_1_post_id"],
            "content": api_data["months_1_posts_1_content"],
            "truncated": api_data["months_1_posts_1_truncated"]
        }
    ]
    
    months.append({
        "month_year": api_data["months_1_month_year"],
        "post_count": api_data["months_1_post_count"],
        "posts": month_1_posts
    })
    
    # Apply date filtering if start_date or end_date is provided
    if start_date or end_date:
        filtered_months = []
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        
        for month_data in months:
            # Parse month_year string to datetime (first day of the month)
            month_year_dt = datetime.strptime(month_data["month_year"], "%B %Y")
            
            # Check if within range
            within_range = True
            if start_dt and month_year_dt < start_dt:
                within_range = False
            if end_dt and month_year_dt > end_dt:
                within_range = False
            
            if within_range:
                filtered_months.append(month_data)
        
        months = filtered_months
    
    # Construct final result
    result = {
        "timeline_title": api_data["timeline_title"],
        "months": months
    }
    
    return result