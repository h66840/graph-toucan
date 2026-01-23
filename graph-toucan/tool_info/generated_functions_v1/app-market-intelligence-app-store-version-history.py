from typing import Dict, List, Any
from datetime import datetime, timedelta
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching version history data from external App Store API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - app_id (int): The numeric App Store ID
        - total_versions (int): Total number of version entries
        - latest_version (str): Most recent version number
        - earliest_version (str): Earliest recorded version number
        - version_0_versionDisplay (str): Version number for first entry
        - version_0_releaseNotes (str): Release notes for first entry
        - version_0_releaseDate (str): Release date (YYYY-MM-DD) for first entry
        - version_0_releaseTimestamp (str): ISO timestamp for first entry
        - version_1_versionDisplay (str): Version number for second entry
        - version_1_releaseNotes (str): Release notes for second entry
        - version_1_releaseDate (str): Release date (YYYY-MM-DD) for second entry
        - version_1_releaseTimestamp (str): ISO timestamp for second entry
    """
    app_id = 444934666
    base_date = datetime.now() - timedelta(days=365)
    
    # Generate two realistic version entries
    version_0_date = base_date
    version_1_date = base_date + timedelta(days=180)
    
    # Sort so latest is first
    versions = [
        {
            'versionDisplay': '2.1.0',
            'releaseNotes': 'Improved performance and fixed critical bugs.',
            'releaseDate': version_1_date.strftime('%Y-%m-%d'),
            'releaseTimestamp': version_1_date.isoformat() + 'Z'
        },
        {
            'versionDisplay': '1.5.3',
            'releaseNotes': 'Initial public release with core features.',
            'releaseDate': version_0_date.strftime('%Y-%m-%d'),
            'releaseTimestamp': version_0_date.isoformat() + 'Z'
        }
    ]
    
    return {
        "app_id": app_id,
        "total_versions": 2,
        "latest_version": versions[0]['versionDisplay'],
        "earliest_version": versions[1]['versionDisplay'],
        "version_0_versionDisplay": versions[0]['versionDisplay'],
        "version_0_releaseNotes": versions[0]['releaseNotes'],
        "version_0_releaseDate": versions[0]['releaseDate'],
        "version_0_releaseTimestamp": versions[0]['releaseTimestamp'],
        "version_1_versionDisplay": versions[1]['versionDisplay'],
        "version_1_releaseNotes": versions[1]['releaseNotes'],
        "version_1_releaseDate": versions[1]['releaseDate'],
        "version_1_releaseTimestamp": versions[1]['releaseTimestamp']
    }

def app_market_intelligence_app_store_version_history(id: int) -> Dict[str, Any]:
    """
    Get version history for an App Store app.
    
    Args:
        id (int): Numeric App ID (e.g., 444934666)
    
    Returns:
        Dict containing:
        - versions (List[Dict]): List of version entries with versionDisplay, releaseNotes, releaseDate, releaseTimestamp
        - app_id (int): The numeric App Store ID
        - total_versions (int): Total number of version entries returned
        - latest_version (str): The most recent version number string
        - earliest_version (str): The earliest recorded version number string
    
    Raises:
        ValueError: If id is not a positive integer
    """
    if not isinstance(id, int) or id <= 0:
        raise ValueError("App ID must be a positive integer")
    
    # Call external API to get flattened data
    api_data = call_external_api("app-market-intelligence-app-store-version-history")
    
    # Construct versions list from indexed fields
    versions = [
        {
            'versionDisplay': api_data['version_0_versionDisplay'],
            'releaseNotes': api_data['version_0_releaseNotes'],
            'releaseDate': api_data['version_0_releaseDate'],
            'releaseTimestamp': api_data['version_0_releaseTimestamp']
        },
        {
            'versionDisplay': api_data['version_1_versionDisplay'],
            'releaseNotes': api_data['version_1_releaseNotes'],
            'releaseDate': api_data['version_1_releaseDate'],
            'releaseTimestamp': api_data['version_1_releaseTimestamp']
        }
    ]
    
    # Construct final result matching output schema
    result = {
        'versions': versions,
        'app_id': api_data['app_id'],
        'total_versions': api_data['total_versions'],
        'latest_version': api_data['latest_version'],
        'earliest_version': api_data['earliest_version']
    }
    
    return result