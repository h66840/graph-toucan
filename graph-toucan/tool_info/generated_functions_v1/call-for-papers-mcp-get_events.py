from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for conference events.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - status (str): Status of the response, e.g., "success"
        - count (int): Total number of events returned
        - event_0_id (str): Unique identifier for the first event
        - event_0_name (str): Short name or acronym of the first conference
        - event_0_title (str): Full title of the first conference
        - event_0_when (str): Date range of the first event
        - event_0_where (str): Location of the first event
        - event_0_submission_deadline (str): Submission deadline for the first event
        - event_0_notification_due (str): Notification date for the first event
        - event_0_wikicfp_link (str): WikiCFP URL for the first event
        - event_0_description (str): Description of the first event
        - event_0_external_link (str): Official website URL for the first event
        - event_0_related_resource_0_name (str): Name of first related resource for event 0
        - event_0_related_resource_0_title (str): Title of first related resource for event 0
        - event_0_related_resource_0_url (str): URL of first related resource for event 0
        - event_0_related_resource_1_name (str): Name of second related resource for event 0
        - event_0_related_resource_1_title (str): Title of second related resource for event 0
        - event_0_related_resource_1_url (str): URL of second related resource for event 0
        - event_1_id (str): Unique identifier for the second event
        - event_1_name (str): Short name or acronym of the second conference
        - event_1_title (str): Full title of the second conference
        - event_1_when (str): Date range of the second event
        - event_1_where (str): Location of the second event
        - event_1_submission_deadline (str): Submission deadline for the second event
        - event_1_notification_due (str): Notification date for the second event
        - event_1_wikicfp_link (str): WikiCFP URL for the second event
        - event_1_description (str): Description of the second event
        - event_1_external_link (str): Official website URL for the second event
        - event_1_related_resource_0_name (str): Name of first related resource for event 1
        - event_1_related_resource_0_title (str): Title of first related resource for event 1
        - event_1_related_resource_0_url (str): URL of first related resource for event 1
        - event_1_related_resource_1_name (str): Name of second related resource for event 1
        - event_1_related_resource_1_title (str): Title of second related resource for event 1
        - event_1_related_resource_1_url (str): URL of second related resource for event 1
    """
    return {
        "status": "success",
        "count": 2,
        "event_0_id": "conf123",
        "event_0_name": "ICML",
        "event_0_title": "International Conference on Machine Learning",
        "event_0_when": "July 20-25, 2025",
        "event_0_where": "Vienna, Austria",
        "event_0_submission_deadline": "February 15, 2025",
        "event_0_notification_due": "April 30, 2025",
        "event_0_wikicfp_link": "https://www.wikicfp.com/cfp/somepage1",
        "event_0_description": "A premier conference on machine learning research and applications.",
        "event_0_external_link": "https://icml.cc/2025",
        "event_0_related_resource_0_name": "NeurIPS",
        "event_0_related_resource_0_title": "Conference on Neural Information Processing Systems",
        "event_0_related_resource_0_url": "https://neurips.cc",
        "event_0_related_resource_1_name": "ICLR",
        "event_0_related_resource_1_title": "International Conference on Learning Representations",
        "event_0_related_resource_1_url": "https://iclr.cc",
        "event_1_id": "conf456",
        "event_1_name": "ACL",
        "event_1_title": "Annual Meeting of the Association for Computational Linguistics",
        "event_1_when": "August 5-10, 2025",
        "event_1_where": "Dublin, Ireland",
        "event_1_submission_deadline": "March 1, 2025",
        "event_1_notification_due": "May 15, 2025",
        "event_1_wikicfp_link": "https://www.wikicfp.com/cfp/somepage2",
        "event_1_description": "Top-tier conference on computational linguistics and natural language processing.",
        "event_1_external_link": "https://acl2025.org",
        "event_1_related_resource_0_name": "EMNLP",
        "event_1_related_resource_0_title": "Conference on Empirical Methods in Natural Language Processing",
        "event_1_related_resource_0_url": "https://emnlp2025.org",
        "event_1_related_resource_1_name": "NAACL",
        "event_1_related_resource_1_title": "North American Chapter of the ACL",
        "event_1_related_resource_1_url": "https://naacl.org/2025",
    }

def call_for_papers_mcp_get_events(keywords: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search for conferences matching specific keywords.

    Args:
        keywords (str): Keywords to search for in conference titles, descriptions, or topics.
        limit (Optional[int]): Maximum number of events to return. Defaults to None (no limit).

    Returns:
        Dict containing:
        - status (str): Status of the response (e.g., "success")
        - count (int): Total number of events returned
        - events (List[Dict]): List of conference/event objects with detailed information

        Each event dict contains:
        - id (str): Unique identifier for the event
        - name (str): Short name or acronym of the conference
        - title (str): Full title of the conference
        - when (str): Date range of the event
        - where (str): Location of the event
        - submission_deadline (str): Deadline for paper submission
        - notification_due (str): Date when authors will be notified
        - wikicfp_link (str): URL to the event page on WikiCFP
        - description (str): Detailed description of the conference
        - external_link (str): Official website URL
        - related_resources (List[Dict]): List of related conferences/resources with 'name', 'title', 'url'
    """
    if not keywords or not keywords.strip():
        return {
            "status": "error",
            "count": 0,
            "events": []
        }

    api_data = call_external_api("call-for-papers-mcp-get_events")
    
    # Extract events from flat API data
    events = []
    
    for i in range(2):
        prefix = f"event_{i}"
        if f"{prefix}_id" not in api_data:
            continue
            
        # Build related_resources list
        related_resources = []
        for j in range(2):
            res_prefix = f"{prefix}_related_resource_{j}"
            if f"{res_prefix}_name" in api_data:
                related_resources.append({
                    "name": api_data[f"{res_prefix}_name"],
                    "title": api_data[f"{res_prefix}_title"],
                    "url": api_data[f"{res_prefix}_url"]
                })
        
        event = {
            "id": api_data[f"{prefix}_id"],
            "name": api_data[f"{prefix}_name"],
            "title": api_data[f"{prefix}_title"],
            "when": api_data[f"{prefix}_when"],
            "where": api_data[f"{prefix}_where"],
            "submission_deadline": api_data[f"{prefix}_submission_deadline"],
            "notification_due": api_data[f"{prefix}_notification_due"],
            "wikicfp_link": api_data[f"{prefix}_wikicfp_link"],
            "description": api_data[f"{prefix}_description"],
            "external_link": api_data[f"{prefix}_external_link"],
            "related_resources": related_resources
        }
        events.append(event)
        
        # Apply limit if specified
        if limit is not None and len(events) >= limit:
            break

    result_count = len(events)
    if limit is not None:
        events = events[:limit]
        result_count = len(events)

    return {
        "status": api_data["status"],
        "count": result_count,
        "events": events
    }