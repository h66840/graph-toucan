from typing import Dict, List, Any, Optional
import datetime
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing data files.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - files_0_name (str): Name of the first file
        - files_0_type (str): Type/extension of the first file
        - files_0_size_bytes (int): Size in bytes of the first file
        - files_0_last_modified (str): ISO 8601 timestamp of last modification for first file
        - files_0_url (str): Direct URL to access the first file
        - files_1_name (str): Name of the second file
        - files_1_type (str): Type/extension of the second file
        - files_1_size_bytes (int): Size in bytes of the second file
        - files_1_last_modified (str): ISO 8601 timestamp of last modification for second file
        - files_1_url (str): Direct URL to access the second file
        - total_count (int): Total number of files returned
        - filters_applied_fileType (str): File type filter applied, if any
        - directory_path (str): Path of the directory from which files were listed
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    two_days_ago = now - datetime.timedelta(days=2)
    one_week_ago = now - datetime.timedelta(weeks=1)

    return {
        "files_0_name": "highscores_data.json",
        "files_0_type": "json",
        "files_0_size_bytes": 2048000,
        "files_0_last_modified": two_days_ago.isoformat(),
        "files_0_url": "https://data.osrs.wiki/files/highscores_data.json",

        "files_1_name": "npc_definitions.txt",
        "files_1_type": "txt",
        "files_1_size_bytes": 512000,
        "files_1_last_modified": one_week_ago.isoformat(),
        "files_1_url": "https://data.osrs.wiki/files/npc_definitions.txt",

        "total_count": 2,
        "filters_applied_fileType": "txt",
        "directory_path": "/data/osrs/"
    }


def old_school_runescape_wiki_and_data_server_list_data_files(fileType: Optional[str] = None) -> Dict[str, Any]:
    """
    List available data files in the data directory.

    Args:
        fileType (Optional[str]): Optional filter for file type (e.g., 'txt'). If provided,
                                  only files matching this extension will be returned.

    Returns:
        Dict containing:
        - files (List[Dict]): List of file objects with name, type, size_bytes, last_modified, and url
        - total_count (int): Total number of files returned
        - filters_applied (Dict): Dictionary indicating any filters applied
        - directory_path (str): The path of the directory from which files were listed
    """
    # Fetch simulated external data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-list_data_files")

    # Construct list of files from flattened API response
    files = [
        {
            "name": api_data["files_0_name"],
            "type": api_data["files_0_type"],
            "size_bytes": api_data["files_0_size_bytes"],
            "last_modified": api_data["files_0_last_modified"],
            "url": api_data["files_0_url"]
        },
        {
            "name": api_data["files_1_name"],
            "type": api_data["files_1_type"],
            "size_bytes": api_data["files_1_size_bytes"],
            "last_modified": api_data["files_1_last_modified"],
            "url": api_data["files_1_url"]
        }
    ]

    # Apply fileType filter if specified
    applied_filters = {}
    if fileType is not None:
        applied_filters["fileType"] = fileType
        files = [f for f in files if f["type"] == fileType]
    else:
        applied_filters["fileType"] = None

    total_count = len(files)
    directory_path = api_data["directory_path"]

    return {
        "files": files,
        "total_count": total_count,
        "filters_applied": applied_filters,
        "directory_path": directory_path
    }