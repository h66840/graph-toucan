from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching package release data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - package_name (str): Name of the package
        - total_releases (int): Total number of releases
        - latest_release (str): Most recent version number
        - created_at (str): ISO 8601 timestamp of first release
        - updated_at (str): ISO 8601 timestamp of latest release
        - releases_0_version (str): Version of first release
        - releases_0_published_at (str): Publication timestamp of first release
        - releases_0_url (str): File URL of first release
        - releases_0_sha256 (str): SHA256 digest of first release
        - releases_1_version (str): Version of second release
        - releases_1_published_at (str): Publication timestamp of second release
        - releases_1_url (str): File URL of second release
        - releases_1_sha256 (str): SHA256 digest of second release
    """
    # Generate deterministic but realistic mock data based on tool name
    base_time = datetime.now() - timedelta(days=365)  # One year ago
    package = "example-package"

    return {
        "package_name": package,
        "total_releases": 42,
        "latest_release": "2.1.5",
        "created_at": (base_time).isoformat(),
        "updated_at": (base_time + timedelta(days=350)).isoformat(),
        "releases_0_version": "1.0.0",
        "releases_0_published_at": (base_time).isoformat(),
        "releases_0_url": f"https://pypi.org/packages/source/{package[0]}/{package}/{package}-1.0.0.tar.gz",
        "releases_0_sha256": "".join(random.choices(string.hexdigits.lower(), k=64)),
        "releases_1_version": "2.1.5",
        "releases_1_published_at": (base_time + timedelta(days=350)).isoformat(),
        "releases_1_url": f"https://pypi.org/packages/source/{package[0]}/{package}/{package}-2.1.5.tar.gz",
        "releases_1_sha256": "".join(random.choices(string.hexdigits.lower(), k=64)),
    }


def pypi_mcp_server_get_package_releases(package_name: str) -> Dict[str, Any]:
    """
    Retrieves release information for a given Python package from PyPI.

    Args:
        package_name (str): Name of the package to retrieve releases for. Required.

    Returns:
        Dict containing:
        - releases (List[Dict]): List of release objects with version, publication timestamp, and metadata
        - package_name (str): Name of the package
        - total_releases (int): Total number of releases available
        - latest_release (str): Most recent version number
        - created_at (str): ISO 8601 timestamp of first release
        - updated_at (str): ISO 8601 timestamp of latest release

    Raises:
        ValueError: If package_name is empty or None
    """
    if not package_name or not package_name.strip():
        raise ValueError("package_name is required and cannot be empty")

    package_name = package_name.strip()

    # Fetch data from external API (simulated)
    api_data = call_external_api("pypi-mcp-server-get_package_releases")

    # Construct releases list from indexed fields
    releases = [
        {
            "version": api_data["releases_0_version"],
            "published_at": api_data["releases_0_published_at"],
            "url": api_data["releases_0_url"],
            "sha256": api_data["releases_0_sha256"],
        },
        {
            "version": api_data["releases_1_version"],
            "published_at": api_data["releases_1_published_at"],
            "url": api_data["releases_1_url"],
            "sha256": api_data["releases_1_sha256"],
        },
    ]

    # Build final result structure matching output schema
    result = {
        "releases": releases,
        "package_name": api_data["package_name"],
        "total_releases": api_data["total_releases"],
        "latest_release": api_data["latest_release"],
        "created_at": api_data["created_at"],
        "updated_at": api_data["updated_at"],
    }

    return result