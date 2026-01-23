from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play reviews.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - review_0_id (str): First review ID
        - review_0_userName (str): First reviewer's name
        - review_0_userImage (str): First reviewer's profile image URL
        - review_0_date (str): First review date in ISO format
        - review_0_score (int): First review score (1-5)
        - review_0_scoreText (str): First review score display text
        - review_0_title (str): First review title
        - review_0_text (str): First review content
        - review_0_url (str): First review URL
        - review_0_version (str): App version reviewed in first review
        - review_0_thumbsUp (int): Number of thumbs up for first review
        - review_0_replyDate (str): Developer reply date for first review (ISO) or empty string if none
        - review_0_replyText (str): Developer reply content for first review or empty string if none
        - review_1_id (str): Second review ID
        - review_1_userName (str): Second reviewer's name
        - review_1_userImage (str): Second reviewer's profile image URL
        - review_1_date (str): Second review date in ISO format
        - review_1_score (int): Second review score (1-5)
        - review_1_scoreText (str): Second review score display text
        - review_1_title (str): Second review title
        - review_1_text (str): Second review content
        - review_1_url (str): Second review URL
        - review_1_version (str): App version reviewed in second review
        - review_1_thumbsUp (int): Number of thumbs up for second review
        - review_1_replyDate (str): Developer reply date for second review (ISO) or empty string if none
        - review_1_replyText (str): Developer reply content for second review or empty string if none
        - total_count (int): Estimated total number of written reviews
        - pagination_token (str): Token to retrieve next page of reviews
        - has_next_page (bool): Whether more reviews are available
        - metadata_appId (str): App ID used in request
        - metadata_country (str): Country code used in request
        - metadata_lang (str): Language code used in request
        - metadata_sort (str): Sort order used in request
        - metadata_retrieved_at (str): ISO timestamp when request was made
        - criteria_0_0_name (str): First criteria name for first review
        - criteria_0_0_score (int): First criteria score for first review
        - criteria_0_1_name (str): Second criteria name for first review
        - criteria_0_1_score (int): Second criteria score for first review
        - criteria_1_0_name (str): First criteria name for second review
        - criteria_1_0_score (int): First criteria score for second review
        - criteria_1_1_name (str): Second criteria name for second review
        - criteria_1_1_score (int): Second criteria score for second review
    """
    now_iso = datetime.datetime.now().isoformat()
    return {
        "review_0_id": "rev12345",
        "review_0_userName": "John Doe",
        "review_0_userImage": "https://example.com/images/user1.jpg",
        "review_0_date": "2023-10-05T14:48:00Z",
        "review_0_score": 5,
        "review_0_scoreText": "5 stars",
        "review_0_title": "Great app!",
        "review_0_text": "I love this app. It works perfectly and has great features.",
        "review_0_url": "https://play.google.com/review1",
        "review_0_version": "2.3.1",
        "review_0_thumbsUp": 42,
        "review_0_replyDate": "2023-10-06T09:15:00Z",
        "review_0_replyText": "Thank you for your feedback!",
        "review_1_id": "rev67890",
        "review_1_userName": "Jane Smith",
        "review_1_userImage": "https://example.com/images/user2.jpg",
        "review_1_date": "2023-10-04T11:20:00Z",
        "review_1_score": 4,
        "review_1_scoreText": "4 stars",
        "review_1_title": "Very good",
        "review_1_text": "Solid app with minor bugs.",
        "review_1_url": "https://play.google.com/review2",
        "review_1_version": "2.3.0",
        "review_1_thumbsUp": 15,
        "review_1_replyDate": "",
        "review_1_replyText": "",
        "total_count": 1250,
        "pagination_token": "nextPage123",
        "has_next_page": True,
        "metadata_appId": "com.example.app",
        "metadata_country": "us",
        "metadata_lang": "en",
        "metadata_sort": "newest",
        "metadata_retrieved_at": now_iso,
        "criteria_0_0_name": "Performance",
        "criteria_0_0_score": 5,
        "criteria_0_1_name": "Usability",
        "criteria_0_1_score": 5,
        "criteria_1_0_name": "Design",
        "criteria_1_0_score": 4,
        "criteria_1_1_name": "Features",
        "criteria_1_1_score": 4
    }

def app_market_intelligence_google_play_reviews(
    appId: str,
    country: Optional[str] = "us",
    lang: Optional[str] = "en",
    nextPaginationToken: Optional[str] = None,
    num: Optional[int] = 100,
    paginate: Optional[bool] = False,
    sort: Optional[str] = "newest"
) -> Dict[str, Any]:
    """
    Get reviews for a Google Play app.
    
    Args:
        appId (str): Package name of the app (e.g., 'com.mojang.minecraftpe')
        country (str, optional): Country code (default: us)
        lang (str, optional): Language code for reviews (default: en)
        nextPaginationToken (str, optional): Token for fetching next page of reviews
        num (int, optional): Number of reviews to retrieve (default: 100). Ignored if paginate is true.
        paginate (bool, optional): Enable pagination with 150 reviews per page
        sort (str, optional): Sort order: newest, rating, or helpfulness (default: newest)
    
    Returns:
        Dict containing:
        - reviews (List[Dict]): List of review objects with detailed information
        - total_count (int): Estimated total number of written reviews
        - pagination_token (str): Token to retrieve next page of reviews
        - has_next_page (bool): Whether more reviews are available
        - metadata (Dict): Additional context about the response
    """
    # Input validation
    if not appId:
        raise ValueError("appId is required")
    
    if sort not in ["newest", "rating", "helpfulness"]:
        raise ValueError("sort must be one of: newest, rating, helpfulness")
    
    if num is not None and num <= 0:
        raise ValueError("num must be a positive integer")
    
    # Call external API (simulated)
    api_data = call_external_api("app-market-intelligence-google-play-reviews")
    
    # Construct reviews list
    reviews = []
    
    # Process first review
    review_0_criterias = [
        {"name": api_data["criteria_0_0_name"], "score": api_data["criteria_0_0_score"]},
        {"name": api_data["criteria_0_1_name"], "score": api_data["criteria_0_1_score"]}
    ]
    
    review_0 = {
        "id": api_data["review_0_id"],
        "userName": api_data["review_0_userName"],
        "userImage": api_data["review_0_userImage"],
        "date": api_data["review_0_date"],
        "score": api_data["review_0_score"],
        "scoreText": api_data["review_0_scoreText"],
        "title": api_data["review_0_title"],
        "text": api_data["review_0_text"],
        "url": api_data["review_0_url"],
        "version": api_data["review_0_version"],
        "thumbsUp": api_data["review_0_thumbsUp"],
        "replyDate": api_data["review_0_replyDate"] if api_data["review_0_replyDate"] else None,
        "replyText": api_data["review_0_replyText"] if api_data["review_0_replyText"] else None,
        "criterias": [c for c in review_0_criterias if c["name"]]
    }
    reviews.append(review_0)
    
    # Process second review
    review_1_criterias = [
        {"name": api_data["criteria_1_0_name"], "score": api_data["criteria_1_0_score"]},
        {"name": api_data["criteria_1_1_name"], "score": api_data["criteria_1_1_score"]}
    ]
    
    review_1 = {
        "id": api_data["review_1_id"],
        "userName": api_data["review_1_userName"],
        "userImage": api_data["review_1_userImage"],
        "date": api_data["review_1_date"],
        "score": api_data["review_1_score"],
        "scoreText": api_data["review_1_scoreText"],
        "title": api_data["review_1_title"],
        "text": api_data["review_1_text"],
        "url": api_data["review_1_url"],
        "version": api_data["review_1_version"],
        "thumbsUp": api_data["review_1_thumbsUp"],
        "replyDate": api_data["review_1_replyDate"] if api_data["review_1_replyDate"] else None,
        "replyText": api_data["review_1_replyText"] if api_data["review_1_replyText"] else None,
        "criterias": [c for c in review_1_criterias if c["name"]]
    }
    reviews.append(review_1)
    
    # Construct metadata
    metadata = {
        "appId": api_data["metadata_appId"],
        "country": api_data["metadata_country"],
        "lang": api_data["metadata_lang"],
        "sort": api_data["metadata_sort"],
        "retrievedAt": api_data["metadata_retrieved_at"]
    }
    
    # Return structured response
    return {
        "reviews": reviews,
        "total_count": api_data["total_count"],
        "pagination_token": api_data["pagination_token"],
        "has_next_page": api_data["has_next_page"],
        "metadata": metadata
    }