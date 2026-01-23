from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PyPI package details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - package_name (str): Name of the package
        - package_summary (str): Short summary of the package
        - package_description (str): Full description of the package
        - package_author_name (str): Author's name
        - package_author_email (str): Author's email
        - package_maintainer_name (str): Maintainer's name
        - package_maintainer_email (str): Maintainer's email
        - package_license (str): License type
        - package_home_page (str): Home page URL
        - package_documentation_url (str): Documentation URL
        - package_repository_url (str): Repository URL
        - package_bug_tracker_url (str): Bug tracker URL
        - package_requires_python (str): Required Python version
        - package_keywords (str): Comma-separated keywords
        - package_platform (str): Supported platform
        - package_downloads_last_month (int): Number of downloads in last month
        - package_yanked (bool): Whether the package is yanked
        - package_vulnerabilities_count (int): Number of known vulnerabilities
        - package_version_0 (str): First available version
        - package_version_1 (str): Second available version
        - package_total_versions (int): Total number of versions
        - package_dependency_0_name (str): First dependency name
        - package_dependency_0_version (str): First dependency version requirement
        - package_dependency_1_name (str): Second dependency name
        - package_dependency_1_version (str): Second dependency version requirement
        - package_classifier_0 (str): First classifier
        - package_classifier_1 (str): Second classifier
    """
    return {
        "package_name": "requests",
        "package_summary": "Python HTTP for Humans.",
        "package_description": "Requests is an elegant and simple HTTP library for Python, built for human beings.",
        "package_author_name": "Kenneth Reitz",
        "package_author_email": "me@kennethreitz.org",
        "package_maintainer_name": "Requests Team",
        "package_maintainer_email": "python-requests@googlegroups.com",
        "package_license": "Apache 2.0",
        "package_home_page": "https://requests.readthedocs.io",
        "package_documentation_url": "https://requests.readthedocs.io",
        "package_repository_url": "https://github.com/psf/requests",
        "package_bug_tracker_url": "https://github.com/psf/requests/issues",
        "package_requires_python": ">=3.7",
        "package_keywords": "http, requests, urllib, networking",
        "package_platform": "any",
        "package_downloads_last_month": 35000000,
        "package_yanked": False,
        "package_vulnerabilities_count": 0,
        "package_version_0": "2.31.0",
        "package_version_1": "2.30.0",
        "package_total_versions": 120,
        "package_dependency_0_name": "charset-normalizer",
        "package_dependency_0_version": ">=2.0.0,<4",
        "package_dependency_1_name": "urllib3",
        "package_dependency_1_version": ">=1.21.1,<3",
        "package_classifier_0": "Development Status :: 5 - Production/Stable",
        "package_classifier_1": "Intended Audience :: Developers"
    }

def package_registry_server_get_pypi_package_details(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific PyPI package.
    
    Args:
        name (str): The name of the PyPI package to retrieve details for.
        
    Returns:
        Dict containing detailed information about the PyPI package including:
        - name: package name
        - summary: short summary
        - description: full description
        - author: dict with name and email
        - maintainer: dict with name and email
        - license: license type
        - project_urls: dict with home_page, documentation, repository, bug_tracker
        - requires_python: required Python version
        - keywords: list of keywords
        - platform: supported platform
        - downloads: dict with last_month count
        - yanked: whether package is yanked
        - vulnerabilities: count of known vulnerabilities
        - versions: list of available versions
        - version_count: total number of versions
        - dependencies: list of dependency dicts with name and version
        - classifiers: list of classifier strings
        
    Raises:
        ValueError: If name is empty or not a string
    """
    if not name:
        raise ValueError("Package name is required")
    if not isinstance(name, str):
        raise ValueError("Package name must be a string")
    
    # Call external API to get flat data
    api_data = call_external_api("package-registry-server-get-pypi-package-details")
    
    # Construct nested structure matching output schema
    result = {
        "package": {
            "name": api_data["package_name"],
            "summary": api_data["package_summary"],
            "description": api_data["package_description"],
            "author": {
                "name": api_data["package_author_name"],
                "email": api_data["package_author_email"]
            },
            "maintainer": {
                "name": api_data["package_maintainer_name"],
                "email": api_data["package_maintainer_email"]
            },
            "license": api_data["package_license"],
            "project_urls": {
                "home_page": api_data["package_home_page"],
                "documentation": api_data["package_documentation_url"],
                "repository": api_data["package_repository_url"],
                "bug_tracker": api_data["package_bug_tracker_url"]
            },
            "requires_python": api_data["package_requires_python"],
            "keywords": api_data["package_keywords"].split(", ") if api_data["package_keywords"] else [],
            "platform": api_data["package_platform"],
            "downloads": {
                "last_month": api_data["package_downloads_last_month"]
            },
            "yanked": api_data["package_yanked"],
            "vulnerabilities": {
                "count": api_data["package_vulnerabilities_count"]
            },
            "versions": [
                api_data["package_version_0"],
                api_data["package_version_1"]
            ],
            "version_count": api_data["package_total_versions"],
            "dependencies": [
                {
                    "name": api_data["package_dependency_0_name"],
                    "version": api_data["package_dependency_0_version"]
                },
                {
                    "name": api_data["package_dependency_1_name"],
                    "version": api_data["package_dependency_1_version"]
                }
            ],
            "classifiers": [
                api_data["package_classifier_0"],
                api_data["package_classifier_1"]
            ]
        }
    }
    
    return result