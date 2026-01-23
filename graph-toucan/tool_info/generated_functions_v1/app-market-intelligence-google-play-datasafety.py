from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data safety information from external API for a Google Play app.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_shared_0_data (str): Name of the first shared data item
        - data_shared_0_optional (bool): Whether sharing the first data item is optional
        - data_shared_0_purpose (str): Comma-separated purposes for sharing the first data item
        - data_shared_0_type (str): Category of the first shared data item
        - data_shared_1_data (str): Name of the second shared data item
        - data_shared_1_optional (bool): Whether sharing the second data item is optional
        - data_shared_1_purpose (str): Comma-separated purposes for sharing the second data item
        - data_shared_1_type (str): Category of the second shared data item
        - data_collected_0_data (str): Name of the first collected data item
        - data_collected_0_optional (bool): Whether collection of the first data item is optional
        - data_collected_0_purpose (str): Comma-separated purposes for collecting the first data item
        - data_collected_0_type (str): Category of the first collected data item
        - data_collected_1_data (str): Name of the second collected data item
        - data_collected_1_optional (bool): Whether collection of the second data item is optional
        - data_collected_1_purpose (str): Comma-separated purposes for collecting the second data item
        - data_collected_1_type (str): Category of the second collected data item
        - security_practices_0_practice (str): Name of the first security practice
        - security_practices_0_description (str): Description of the first security practice
        - security_practices_1_practice (str): Name of the second security practice
        - security_practices_1_description (str): Description of the second security practice
        - privacy_policy_url (str): URL to the app's privacy policy
    """
    return {
        "data_shared_0_data": "User IDs",
        "data_shared_0_optional": True,
        "data_shared_0_purpose": "Analytics, Marketing",
        "data_shared_0_type": "Personal info",
        "data_shared_1_data": "Purchase History",
        "data_shared_1_optional": False,
        "data_shared_1_purpose": "Marketing",
        "data_shared_1_type": "Financial info",
        "data_collected_0_data": "App Usage",
        "data_collected_0_optional": False,
        "data_collected_0_purpose": "App Functionality, Analytics",
        "data_collected_0_type": "App activity",
        "data_collected_1_data": "Device ID",
        "data_collected_1_optional": True,
        "data_collected_1_purpose": "Analytics",
        "data_collected_1_type": "Device or other IDs",
        "security_practices_0_practice": "Data Encryption",
        "security_practices_0_description": "Data is encrypted in transit and at rest.",
        "security_practices_1_practice": "Security Updates",
        "security_practices_1_description": "Regular security patches are applied to protect user data.",
        "privacy_policy_url": "https://example.com/privacy-policy"
    }

def app_market_intelligence_google_play_datasafety(appId: str, lang: Optional[str] = "en") -> Dict[str, Any]:
    """
    Get data safety information for a Google Play app.
    
    Args:
        appId (str): Google Play package name (e.g., 'com.dxco.pandavszombies')
        lang (Optional[str]): Language code for data safety info (default: 'en')
    
    Returns:
        Dict containing:
        - dataShared (List[Dict]): list of data items shared with third parties, each containing
          'data', 'optional', 'purpose', and 'type'
        - dataCollected (List[Dict]): list of data items collected by the app, each with
          'data', 'optional', 'purpose', and 'type'
        - securityPractices (List[Dict]): list of security practices, each with 'practice' and 'description'
        - privacyPolicyUrl (str): URL to the app's full privacy policy
    """
    if not appId:
        raise ValueError("appId is required and cannot be empty")
    
    if not isinstance(appId, str):
        raise TypeError("appId must be a string")
    
    if lang and not isinstance(lang, str):
        raise TypeError("lang must be a string")
    
    # Call external API to get flattened data
    api_data = call_external_api("app-market-intelligence-google-play-datasafety")
    
    # Construct dataShared list from indexed fields
    data_shared = [
        {
            "data": api_data["data_shared_0_data"],
            "optional": api_data["data_shared_0_optional"],
            "purpose": api_data["data_shared_0_purpose"],
            "type": api_data["data_shared_0_type"]
        },
        {
            "data": api_data["data_shared_1_data"],
            "optional": api_data["data_shared_1_optional"],
            "purpose": api_data["data_shared_1_purpose"],
            "type": api_data["data_shared_1_type"]
        }
    ]
    
    # Construct dataCollected list from indexed fields
    data_collected = [
        {
            "data": api_data["data_collected_0_data"],
            "optional": api_data["data_collected_0_optional"],
            "purpose": api_data["data_collected_0_purpose"],
            "type": api_data["data_collected_0_type"]
        },
        {
            "data": api_data["data_collected_1_data"],
            "optional": api_data["data_collected_1_optional"],
            "purpose": api_data["data_collected_1_purpose"],
            "type": api_data["data_collected_1_type"]
        }
    ]
    
    # Construct securityPractices list from indexed fields
    security_practices = [
        {
            "practice": api_data["security_practices_0_practice"],
            "description": api_data["security_practices_0_description"]
        },
        {
            "practice": api_data["security_practices_1_practice"],
            "description": api_data["security_practices_1_description"]
        }
    ]
    
    # Build final result matching output schema
    result = {
        "dataShared": data_shared,
        "dataCollected": data_collected,
        "securityPractices": security_practices,
        "privacyPolicyUrl": api_data["privacy_policy_url"]
    }
    
    return result