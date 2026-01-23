from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching animation details from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - metadata_0_label (str): First metadata label
        - metadata_0_value (str): First metadata value
        - metadata_1_label (str): Second metadata label
        - metadata_1_value (str): Second metadata value
        - tools_0 (str): First tool used (empty string if none)
        - tools_1 (str): Second tool used (empty string if none)
        - tags_0_name (str): First tag name
        - tags_0_slug (str): First tag slug
        - tags_0_localizedTags_0_name (str): First localized tag name
        - tags_0_localizedTags_0_slug (str): First localized tag slug
        - tags_0_localizedTags_0_locale (str): First localized tag locale
        - tags_1_name (str): Second tag name
        - tags_1_slug (str): Second tag slug
        - tags_1_localizedTags_0_name (str): Second tag localized name
        - tags_1_localizedTags_0_slug (str): Second tag localized slug
        - tags_1_localizedTags_0_locale (str): Second tag localized locale
        - relatedTags_0 (str): First related tag name
        - relatedTags_1 (str): Second related tag name
        - fileSizeInfo_jsonSize (int): JSON file size in bytes
        - fileSizeInfo_optimizedLottieSize (int): Optimized Lottie file size in bytes
        - fileSizeInfo_optimizedPercentage (float): Compression efficiency percentage
    """
    return {
        "metadata_0_label": "Frame Rate",
        "metadata_0_value": "60 fps",
        "metadata_1_label": "Resolution",
        "metadata_1_value": "512x512",
        "tools_0": "",
        "tools_1": "",
        "tags_0_name": "animation",
        "tags_0_slug": "animation",
        "tags_0_localizedTags_0_name": "animation",
        "tags_0_localizedTags_0_slug": "animation",
        "tags_0_localizedTags_0_locale": "en",
        "tags_1_name": "lottie",
        "tags_1_slug": "lottie",
        "tags_1_localizedTags_0_name": "lottie",
        "tags_1_localizedTags_0_slug": "lottie",
        "tags_1_localizedTags_0_locale": "en",
        "relatedTags_0": "motion design",
        "relatedTags_1": "ui animation",
        "fileSizeInfo_jsonSize": 45200,
        "fileSizeInfo_optimizedLottieSize": 32100,
        "fileSizeInfo_optimizedPercentage": 29.0
    }

def lottiefiles_server_get_animation_details(id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific Lottie animation, including animation data, 
    preview images, and tags.
    
    Args:
        id (str): Unique identifier of the animation
        
    Returns:
        Dict containing detailed animation information with the following structure:
        - metadata (List[Dict]): list of metadata entries with 'label' and 'value'
        - tools (List): list of tools used in the animation (currently empty)
        - tags (List[Dict]): list of tag objects with 'name', 'slug', and 'localizedTags'
        - relatedTags (List[str]): list of tag names for discovery
        - fileSizeInfo (Dict): file size details including 'jsonSize', 'optimizedLottieSize', 
          and 'optimizedPercentage'
          
    Raises:
        ValueError: If id is empty or None
    """
    if not id:
        raise ValueError("Animation ID is required")
    
    api_data = call_external_api("lottiefiles-server-get_animation_details")
    
    # Construct metadata list
    metadata = [
        {
            "label": api_data["metadata_0_label"],
            "value": api_data["metadata_0_value"]
        },
        {
            "label": api_data["metadata_1_label"],
            "value": api_data["metadata_1_value"]
        }
    ]
    
    # Construct tools list (currently appears empty in responses)
    tools = []
    if api_data.get("tools_0") and api_data["tools_0"].strip():
        tools.append(api_data["tools_0"])
    if api_data.get("tools_1") and api_data["tools_1"].strip():
        tools.append(api_data["tools_1"])
    
    # Construct tags list
    tags = [
        {
            "name": api_data["tags_0_name"],
            "slug": api_data["tags_0_slug"],
            "localizedTags": [
                {
                    "name": api_data["tags_0_localizedTags_0_name"],
                    "slug": api_data["tags_0_localizedTags_0_slug"],
                    "locale": api_data["tags_0_localizedTags_0_locale"]
                }
            ]
        },
        {
            "name": api_data["tags_1_name"],
            "slug": api_data["tags_1_slug"],
            "localizedTags": [
                {
                    "name": api_data["tags_1_localizedTags_0_name"],
                    "slug": api_data["tags_1_localizedTags_0_slug"],
                    "locale": api_data["tags_1_localizedTags_0_locale"]
                }
            ]
        }
    ]
    
    # Construct relatedTags list
    relatedTags = [
        api_data["relatedTags_0"],
        api_data["relatedTags_1"]
    ]
    
    # Construct fileSizeInfo dict
    fileSizeInfo = {
        "jsonSize": api_data["fileSizeInfo_jsonSize"],
        "optimizedLottieSize": api_data["fileSizeInfo_optimizedLottieSize"],
        "optimizedPercentage": api_data["fileSizeInfo_optimizedPercentage"]
    }
    
    return {
        "metadata": metadata,
        "tools": tools,
        "tags": tags,
        "relatedTags": relatedTags,
        "fileSizeInfo": fileSizeInfo
    }