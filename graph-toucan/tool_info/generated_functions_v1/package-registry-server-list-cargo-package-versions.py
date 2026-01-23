from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Cargo package versions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - version_0_num (str): First version number
        - version_0_published_at (str): Publication timestamp of first version (ISO format)
        - version_0_yanked (bool): Whether the first version is yanked
        - version_0_crate_size (int): Crate file size in bytes for first version
        - version_1_num (str): Second version number
        - version_1_published_at (str): Publication timestamp of second version (ISO format)
        - version_1_yanked (bool): Whether the second version is yanked
        - version_1_crate_size (int): Crate file size in bytes for second version
        - total_count (int): Total number of versions available
        - latest_version (str): Most recent non-yanked version
        - has_more (bool): Whether more versions exist beyond limit
        - registry_base_url (str): Base URL of the package registry
        - response_time (str): Timestamp when response was generated (ISO format)
        - rate_limit_remaining (int): Number of API requests remaining
        - rate_limit_reset (int): Seconds until rate limit reset
    """
    now = datetime.utcnow()
    version_0_date = (now - timedelta(days=random.randint(10, 1000))).isoformat() + "Z"
    version_1_date = (now - timedelta(days=random.randint(1, 9))).isoformat() + "Z"

    return {
        "version_0_num": f"{random.randint(0, 2)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "version_0_published_at": version_0_date,
        "version_0_yanked": random.choice([True, False]),
        "version_0_crate_size": random.randint(1024, 5 * 1024 * 1024),  # 1KB to 5MB
        "version_1_num": f"{random.randint(0, 2)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "version_1_published_at": version_1_date,
        "version_1_yanked": False,  # latest is never yanked
        "version_1_crate_size": random.randint(1024, 5 * 1024 * 1024),
        "total_count": random.randint(5, 50),
        "latest_version": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "has_more": True,
        "registry_base_url": "https://crates.io/api/v1",
        "response_time": now.isoformat() + "Z",
        "rate_limit_remaining": random.randint(100, 5000),
        "rate_limit_reset": int((now + timedelta(hours=1)).timestamp()),
    }


def package_registry_server_list_cargo_package_versions(
    name: str, limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all versions of a specific Cargo package.

    Args:
        name (str): The name of the Cargo package (required).
        limit (Optional[int]): Maximum number of versions to return (optional).

    Returns:
        Dict containing:
        - versions (List[Dict]): List of package version entries with version number,
          publication date, yanked status, and crate size.
        - total_count (int): Total number of versions available for the package.
        - latest_version (str): The most recent non-yanked version.
        - has_more (bool): Indicates if more versions are available beyond the limit.
        - registry_metadata (Dict): Additional registry-level information including
          base URL, response time, and rate limit details.

    Raises:
        ValueError: If 'name' is empty or None.
    """
    if not name:
        raise ValueError("Parameter 'name' is required and cannot be empty.")

    # Fetch simulated external API data
    api_data = call_external_api("package-registry-server-list-cargo-package-versions")

    # Construct versions list from indexed fields
    versions = [
        {
            "version": api_data["version_0_num"],
            "published_at": api_data["version_0_published_at"],
            "yanked": api_data["version_0_yanked"],
            "crate_size": api_data["version_0_crate_size"],
        },
        {
            "version": api_data["version_1_num"],
            "published_at": api_data["version_1_published_at"],
            "yanked": api_data["version_1_yanked"],
            "crate_size": api_data["version_1_crate_size"],
        },
    ]

    # Apply limit if specified
    if limit is not None and limit > 0:
        versions = versions[:limit]
        has_more = api_data["has_more"] and len(versions) < api_data["total_count"]
    else:
        has_more = api_data["has_more"]

    # Construct final result matching output schema
    result = {
        "versions": versions,
        "total_count": api_data["total_count"],
        "latest_version": api_data["latest_version"],
        "has_more": has_more,
        "registry_metadata": {
            "base_url": api_data["registry_base_url"],
            "response_time": api_data["response_time"],
            "rate_limit": {
                "remaining": api_data["rate_limit_remaining"],
                "reset": api_data["rate_limit_reset"],
            },
        },
    }

    return result