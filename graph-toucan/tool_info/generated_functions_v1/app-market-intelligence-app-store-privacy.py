from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching privacy data for an App Store app from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - managePrivacyChoicesUrl (str): URL where users can manage privacy choices
        - privacyType_0 (str): Name of the first privacy category
        - identifier_0 (str): Unique identifier for the first privacy type
        - description_0 (str): Description of how the first privacy data is used
        - dataCategory_0_0 (str): First data category name for first privacy type
        - dataCategoryIdentifier_0_0 (str): Identifier for first data category of first privacy type
        - dataType_0_0_0 (str): First data type collected in first data category of first privacy type
        - dataType_0_0_1 (str): Second data type collected in first data category of first privacy type
        - dataCategory_0_1 (str): Second data category name for first privacy type
        - dataCategoryIdentifier_0_1 (str): Identifier for second data category of first privacy type
        - dataType_0_1_0 (str): First data type collected in second data category of first privacy type
        - dataType_0_1_1 (str): Second data type collected in second data category of first privacy type
        - purpose_0_0 (str): First purpose for data collection in first privacy type
        - purpose_0_1 (str): Second purpose for data collection in first privacy type
        - privacyType_1 (str): Name of the second privacy category
        - identifier_1 (str): Unique identifier for the second privacy type
        - description_1 (str): Description of how the second privacy data is used
        - dataCategory_1_0 (str): First data category name for second privacy type
        - dataCategoryIdentifier_1_0 (str): Identifier for first data category of second privacy type
        - dataType_1_0_0 (str): First data type collected in first data category of second privacy type
        - dataType_1_0_1 (str): Second data type collected in first data category of second privacy type
        - dataCategory_1_1 (str): Second data category name for second privacy type
        - dataCategoryIdentifier_1_1 (str): Identifier for second data category of second privacy type
        - dataType_1_1_0 (str): First data type collected in second data category of second privacy type
        - dataType_1_1_1 (str): Second data type collected in second data category of second privacy type
        - purpose_1_0 (str): First purpose for data collection in second privacy type
        - purpose_1_1 (str): Second purpose for data collection in second privacy type
    """
    return {
        "managePrivacyChoicesUrl": "https://privacy.example.com/manage",
        "privacyType_0": "Tracking",
        "identifier_0": "tracking_data",
        "description_0": "Data used to track user activity across apps and websites.",
        "dataCategory_0_0": "Device ID",
        "dataCategoryIdentifier_0_0": "device_id",
        "dataType_0_0_0": "Advertising ID",
        "dataType_0_0_1": "Hardware ID",
        "dataCategory_0_1": "Usage Data",
        "dataCategoryIdentifier_0_1": "usage_data",
        "dataType_0_1_0": "App Function Usage",
        "dataType_0_1_1": "Crash Logs",
        "purpose_0_0": "Advertising",
        "purpose_0_1": "Analytics",
        "privacyType_1": "Contact Information",
        "identifier_1": "contact_info",
        "description_1": "Personal information provided by the user for account creation.",
        "dataCategory_1_0": "Email",
        "dataCategoryIdentifier_1_0": "email_address",
        "dataType_1_0_0": "Primary Email",
        "dataType_1_0_1": "Backup Email",
        "dataCategory_1_1": "Phone Number",
        "dataCategoryIdentifier_1_1": "phone_number",
        "dataType_1_1_0": "Mobile Number",
        "dataType_1_1_1": "Home Number",
        "purpose_1_0": "Account Management",
        "purpose_1_1": "Customer Support"
    }

def app_market_intelligence_app_store_privacy(id: int) -> Dict[str, Any]:
    """
    Get privacy details for an App Store app by its numeric App ID.
    
    Args:
        id (int): Numeric App ID (e.g., 553834731). Required.
    
    Returns:
        Dict containing:
        - managePrivacyChoicesUrl (Optional[str]): URL where users can manage their privacy choices
        - privacyTypes (List[Dict]): List of privacy data types with:
            - privacyType (str): Name of the privacy category
            - identifier (str): Unique identifier for the privacy type
            - description (str): Detailed description of how data is used
            - dataCategories (List[Dict]): List of data categories with:
                - dataCategory (str): Category name
                - identifier (str): Category identifier
                - dataTypes (List[str]): List of specific data types collected
            - purposes (List[str]): List of purposes for data collection
    
    Note:
        Currently only available for US App Store.
    """
    if not isinstance(id, int) or id <= 0:
        raise ValueError("App ID must be a positive integer.")
    
    api_data = call_external_api("app-market-intelligence-app-store-privacy")
    
    # Construct dataCategories for first privacy type
    data_categories_0 = [
        {
            "dataCategory": api_data["dataCategory_0_0"],
            "identifier": api_data["dataCategoryIdentifier_0_0"],
            "dataTypes": [
                api_data["dataType_0_0_0"],
                api_data["dataType_0_0_1"]
            ]
        },
        {
            "dataCategory": api_data["dataCategory_0_1"],
            "identifier": api_data["dataCategoryIdentifier_0_1"],
            "dataTypes": [
                api_data["dataType_0_1_0"],
                api_data["dataType_0_1_1"]
            ]
        }
    ]
    
    # Construct purposes for first privacy type
    purposes_0 = [
        api_data["purpose_0_0"],
        api_data["purpose_0_1"]
    ]
    
    # Construct first privacy type
    privacy_type_0 = {
        "privacyType": api_data["privacyType_0"],
        "identifier": api_data["identifier_0"],
        "description": api_data["description_0"],
        "dataCategories": data_categories_0,
        "purposes": purposes_0
    }
    
    # Construct dataCategories for second privacy type
    data_categories_1 = [
        {
            "dataCategory": api_data["dataCategory_1_0"],
            "identifier": api_data["dataCategoryIdentifier_1_0"],
            "dataTypes": [
                api_data["dataType_1_0_0"],
                api_data["dataType_1_0_1"]
            ]
        },
        {
            "dataCategory": api_data["dataCategory_1_1"],
            "identifier": api_data["dataCategoryIdentifier_1_1"],
            "dataTypes": [
                api_data["dataType_1_1_0"],
                api_data["dataType_1_1_1"]
            ]
        }
    ]
    
    # Construct purposes for second privacy type
    purposes_1 = [
        api_data["purpose_1_0"],
        api_data["purpose_1_1"]
    ]
    
    # Construct second privacy type
    privacy_type_1 = {
        "privacyType": api_data["privacyType_1"],
        "identifier": api_data["identifier_1"],
        "description": api_data["description_1"],
        "dataCategories": data_categories_1,
        "purposes": purposes_1
    }
    
    # Construct final result
    result = {
        "managePrivacyChoicesUrl": api_data["managePrivacyChoicesUrl"],
        "privacyTypes": [
            privacy_type_0,
            privacy_type_1
        ]
    }
    
    return result