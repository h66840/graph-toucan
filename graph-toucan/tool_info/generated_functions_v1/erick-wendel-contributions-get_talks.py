from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Erick Wendel's talks.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_count (int): Total number of talks matching the query
        - retrieved (int): Number of talks returned in this response
        - processed_in (int): Processing time in milliseconds
        - talk_0__id (str): ID of the first talk
        - talk_0_title (str): Title of the first talk
        - talk_0_abstract (str): Abstract of the first talk
        - talk_0_type (str): Type of the first talk
        - talk_0_event_name (str): Event name of the first talk
        - talk_0_event_link (str): Event link of the first talk
        - talk_0_slides (str): Slides URL of the first talk
        - talk_0_video (str): Video URL of the first talk
        - talk_0_tags_0 (str): First tag of the first talk
        - talk_0_tags_1 (str): Second tag of the first talk
        - talk_0_location_country (str): Country of the first talk location
        - talk_0_location_city (str): City of the first talk location
        - talk_0_language (str): Language of the first talk
        - talk_0_date (str): Date of the first talk
        - talk_1__id (str): ID of the second talk
        - talk_1_title (str): Title of the second talk
        - talk_1_abstract (str): Abstract of the second talk
        - talk_1_type (str): Type of the second talk
        - talk_1_event_name (str): Event name of the second talk
        - talk_1_event_link (str): Event link of the second talk
        - talk_1_slides (str): Slides URL of the second talk
        - talk_1_video (str): Video URL of the second talk
        - talk_1_tags_0 (str): First tag of the second talk
        - talk_1_tags_1 (str): Second tag of the second talk
        - talk_1_location_country (str): Country of the second talk location
        - talk_1_location_city (str): City of the second talk location
        - talk_1_language (str): Language of the second talk
        - talk_1_date (str): Date of the second talk
    """
    return {
        "total_count": 42,
        "retrieved": 2,
        "processed_in": 15,
        "talk_0__id": "t1001",
        "talk_0_title": "Mastering Node.js",
        "talk_0_abstract": "Deep dive into Node.js internals and performance optimization.",
        "talk_0_type": "keynote",
        "talk_0_event_name": "NodeConf",
        "talk_0_event_link": "https://nodeconf.com/talks/1001",
        "talk_0_slides": "https://slides.com/erickwendel/nodejs-mastering",
        "talk_0_video": "https://youtube.com/watch?v=node1001",
        "talk_0_tags_0": "nodejs",
        "talk_0_tags_1": "performance",
        "talk_0_location_country": "Brazil",
        "talk_0_location_city": "São Paulo",
        "talk_0_language": "en",
        "talk_0_date": "2023-05-15",
        "talk_1__id": "t1002",
        "talk_1_title": "Advanced JavaScript Patterns",
        "talk_1_abstract": "Exploring advanced design patterns in modern JavaScript.",
        "talk_1_type": "workshop",
        "talk_1_event_name": "JS Summit",
        "talk_1_event_link": "https://jssummit.com/talks/1002",
        "talk_1_slides": "https://slides.com/erickwendel/js-patterns",
        "talk_1_video": "https://youtube.com/watch?v=js1002",
        "talk_1_tags_0": "javascript",
        "talk_1_tags_1": "design-patterns",
        "talk_1_location_country": "United States",
        "talk_1_location_city": "San Francisco",
        "talk_1_language": "en",
        "talk_1_date": "2023-06-20"
    }

def erick_wendel_contributions_get_talks(
    city: Optional[str] = None,
    count_only: Optional[bool] = None,
    country: Optional[str] = None,
    group_by: Optional[str] = None,
    id: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    title: Optional[str] = None,
    year: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get a list of talks with optional filtering and pagination.

    Args:
        city (Optional[str]): Filter talks by city
        count_only (Optional[bool]): If true, returns only the count without talk details
        country (Optional[str]): Filter talks by country
        group_by (Optional[str]): Group counts by a specific field (language, country, city)
        id (Optional[str]): Filter talks by ID
        language (Optional[str]): Filter talks by language (e.g., 'spanish', 'english', 'portuguese' or direct codes like 'es', 'en', 'pt-br')
        limit (Optional[int]): Maximum number of talks to return
        skip (Optional[int]): Number of talks to skip
        title (Optional[str]): Filter talks by title
        year (Optional[int]): Filter talks by year

    Returns:
        Dict containing:
        - totalCount (int): total number of talks matching the query
        - retrieved (int): number of talks actually returned in this response
        - processedIn (int): processing time in milliseconds
        - talks (List[Dict]): list of talk objects with fields: '_id', 'title', 'abstract', 'type', 'event', 
          'slides', 'video', 'tags', 'location', 'language', and 'date'
    """
    # Call external API to get flat data
    api_data = call_external_api("erick-wendel-contributions-get_talks")
    
    # Apply filtering logic based on input parameters (simulated)
    # In a real implementation, this would filter the actual data
    # Here we just simulate that the filtering has been applied
    
    result = {
        "totalCount": api_data["total_count"],
        "retrieved": api_data["retrieved"],
        "processedIn": api_data["processed_in"]
    }
    
    # If count_only is True, don't include talks in the response
    if count_only:
        return result
    
    # Construct the talks list from flattened API data
    talks = []
    
    for i in range(2):  # We have 2 talks in our simulated data
        talk_key_prefix = f"talk_{i}"
        
        # Only add talk if it passes our (simulated) filters
        should_include = True
        
        # Simulate filtering logic
        if id and api_data.get(f"{talk_key_prefix}__id") != id:
            should_include = False
        if title and title.lower() not in api_data.get(f"{talk_key_prefix}_title", "").lower():
            should_include = False
        if city and api_data.get(f"{talk_key_prefix}_location_city") != city:
            should_include = False
        if country and api_data.get(f"{talk_key_prefix}_location_country") != country:
            should_include = False
        if language and api_data.get(f"{talk_key_prefix}_language") != language:
            should_include = False
        if year:
            talk_date = api_data.get(f"{talk_key_prefix}_date", "")
            talk_year = int(talk_date.split("-")[0]) if talk_date else 0
            if talk_year != year:
                should_include = False
        
        if not should_include:
            continue
            
        # Build the talk object with nested structures
        talk = {
            "_id": api_data[f"{talk_key_prefix}__id"],
            "title": api_data[f"{talk_key_prefix}_title"],
            "abstract": api_data[f"{talk_key_prefix}_abstract"],
            "type": api_data[f"{talk_key_prefix}_type"],
            "event": {
                "name": api_data[f"{talk_key_prefix}_event_name"],
                "link": api_data[f"{talk_key_prefix}_event_link"]
            },
            "slides": api_data[f"{talk_key_prefix}_slides"],
            "video": api_data[f"{talk_key_prefix}_video"],
            "tags": [
                api_data[f"{talk_key_prefix}_tags_0"],
                api_data[f"{talk_key_prefix}_tags_1"]
            ],
            "location": {
                "country": api_data[f"{talk_key_prefix}_location_country"],
                "city": api_data[f"{talk_key_prefix}_location_city"]
            },
            "language": api_data[f"{talk_key_prefix}_language"],
            "date": api_data[f"{talk_key_prefix}_date"]
        }
        talks.append(talk)
    
    result["talks"] = talks
    return result