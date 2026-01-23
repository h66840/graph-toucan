from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching package information from PyPI via an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - author (str): Name of the package author
        - author_email (str): Email address of the package author
        - classifier_0 (str): First classifier string
        - classifier_1 (str): Second classifier string
        - description (str): Full description of the package
        - description_content_type (str): MIME type of the description content
        - home_page (str): Official homepage URL of the project
        - keywords (str): Keywords associated with the package
        - license (str): License under which the package is distributed
        - license_expression (str): SPDX license expression
        - license_file_0 (str): First license file name
        - license_file_1 (str): Second license file name
        - maintainer (str): Name of the current maintainer
        - maintainer_email (str): Email of the maintainer
        - name (str): Canonical name of the package on PyPI
        - version (str): Current version string of the package
        - summary (str): Short one-line summary of the package functionality
        - requires_python (str): Python version requirement specifier
        - requires_dist_0 (str): First distribution requirement
        - requires_dist_1 (str): Second distribution requirement
        - provides_extra_0 (str): First optional feature group
        - provides_extra_1 (str): Second optional feature group
        - project_url_documentation (str): Documentation URL
        - project_url_source (str): Source code URL
        - package_url (str): URL to the package listing on PyPI
        - release_url (str): Direct URL to this specific release on PyPI
        - downloads_last_day (int): Download count in the last day
        - downloads_last_month (int): Download count in the last month
        - downloads_last_week (int): Download count in the last week
        - yanked (bool): Whether this release has been yanked
        - yanked_reason (str): Reason given for yanking the release
        - dynamic_0 (str): First dynamically generated metadata field
        - dynamic_1 (str): Second dynamically generated metadata field
        - platform (str): Platform compatibility specification
        - bugtrack_url (str): URL to the issue tracker
        - docs_url (str): URL to the package documentation
        - download_url (str): Direct download link for the distribution
        - project_url (str): Alias for package_url; project page on PyPI
    """
    return {
        "author": "Example Author",
        "author_email": "author@example.com",
        "classifier_0": "Development Status :: 5 - Production/Stable",
        "classifier_1": "Intended Audience :: Developers",
        "description": "This is a sample package for demonstration purposes.",
        "description_content_type": "text/markdown",
        "home_page": "https://example.com/home",
        "keywords": "sample demo example",
        "license": "MIT",
        "license_expression": "MIT",
        "license_file_0": "LICENSE.txt",
        "license_file_1": "NOTICE.txt",
        "maintainer": "Example Maintainer",
        "maintainer_email": "maintainer@example.com",
        "name": "sample-package",
        "version": "1.0.0",
        "summary": "A sample Python package for testing",
        "requires_python": ">=3.7",
        "requires_dist_0": "requests>=2.25.0",
        "requires_dist_1": "click>=7.0; extra == 'cli'",
        "provides_extra_0": "cli",
        "provides_extra_1": "test",
        "project_url_documentation": "https://docs.sample-package.org",
        "project_url_source": "https://github.com/example/sample-package",
        "package_url": "https://pypi.org/project/sample-package/",
        "release_url": "https://pypi.org/project/sample-package/1.0.0/",
        "downloads_last_day": 1500,
        "downloads_last_month": 45000,
        "downloads_last_week": 10500,
        "yanked": False,
        "yanked_reason": "",
        "dynamic_0": "Version",
        "dynamic_1": "Description",
        "platform": "any",
        "bugtrack_url": "https://github.com/example/sample-package/issues",
        "docs_url": "https://docs.sample-package.org",
        "download_url": "https://files.pythonhosted.org/packages/source/s/sample-package/sample-package-1.0.0.tar.gz",
        "project_url": "https://pypi.org/project/sample-package/"
    }

def pypi_mcp_server_get_package_info(package_name: str, version: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves detailed metadata information about a Python package from PyPI.
    
    Args:
        package_name (str): The name of the package on PyPI (required)
        version (Optional[str]): Specific version of the package to retrieve info for (optional)
    
    Returns:
        Dict containing comprehensive package metadata with the following structure:
        - author (str): name of the package author
        - author_email (str): email address of the package author
        - classifiers (List[str]): list of PyPI trove classifiers
        - description (str): full description of the package
        - description_content_type (str): MIME type of the description content
        - home_page (str): official homepage URL of the project
        - keywords (str or None): keywords associated with the package
        - license (str): license under which the package is distributed
        - license_expression (str or None): SPDX license expression if available
        - license_files (List[str] or None): list of license file names
        - maintainer (str or None): name of the current maintainer
        - maintainer_email (str or None): email of the maintainer
        - name (str): canonical name of the package on PyPI
        - version (str): current version string of the package
        - summary (str): short one-line summary of the package functionality
        - requires_python (str): Python version requirement specifier
        - requires_dist (List[str]): list of distribution requirements
        - provides_extra (List[str] or None): list of optional feature groups
        - project_urls (Dict): mapping of label to URL for project-related links
        - package_url (str): URL to the package listing on PyPI
        - release_url (str): direct URL to this specific release on PyPI
        - downloads (Dict): contains 'last_day', 'last_month', 'last_week' download counts
        - yanked (bool): indicates whether this release has been yanked
        - yanked_reason (str or None): reason given for yanking the release
        - dynamic (List[str] or None): list of metadata fields marked as dynamically generated
        - platform (str or None): platform compatibility specification
        - bugtrack_url (str or None): URL to the issue tracker
        - docs_url (str or None): URL to the package documentation
        - download_url (str or None): direct download link for the distribution
        - project_url (str): alias for package_url; URL of the project page on PyPI
    
    Raises:
        ValueError: If package_name is empty or None
    """
    if not package_name or not package_name.strip():
        raise ValueError("package_name is required and cannot be empty")
    
    # Call the simulated external API to get flattened data
    api_data = call_external_api("pypi_mcp_server_get_package_info")
    
    # Construct nested output structure from flattened API data
    result = {
        "author": api_data["author"],
        "author_email": api_data["author_email"],
        "classifiers": [
            api_data["classifier_0"],
            api_data["classifier_1"]
        ],
        "description": api_data["description"],
        "description_content_type": api_data["description_content_type"],
        "home_page": api_data["home_page"],
        "keywords": api_data["keywords"] if api_data["keywords"] else None,
        "license": api_data["license"],
        "license_expression": api_data["license_expression"] if api_data["license_expression"] else None,
        "license_files": [
            api_data["license_file_0"],
            api_data["license_file_1"]
        ],
        "maintainer": api_data["maintainer"] if api_data["maintainer"] else None,
        "maintainer_email": api_data["maintainer_email"] if api_data["maintainer_email"] else None,
        "name": api_data["name"],
        "version": api_data["version"],
        "summary": api_data["summary"],
        "requires_python": api_data["requires_python"],
        "requires_dist": [
            api_data["requires_dist_0"],
            api_data["requires_dist_1"]
        ],
        "provides_extra": [
            api_data["provides_extra_0"],
            api_data["provides_extra_1"]
        ],
        "project_urls": {
            "Documentation": api_data["project_url_documentation"],
            "Source": api_data["project_url_source"]
        },
        "package_url": api_data["package_url"],
        "release_url": api_data["release_url"],
        "downloads": {
            "last_day": api_data["downloads_last_day"],
            "last_month": api_data["downloads_last_month"],
            "last_week": api_data["downloads_last_week"]
        },
        "yanked": api_data["yanked"],
        "yanked_reason": api_data["yanked_reason"] if api_data["yanked_reason"] else None,
        "dynamic": [
            api_data["dynamic_0"],
            api_data["dynamic_1"]
        ] if api_data["dynamic_0"] or api_data["dynamic_1"] else None,
        "platform": api_data["platform"] if api_data["platform"] else None,
        "bugtrack_url": api_data["bugtrack_url"] if api_data["bugtrack_url"] else None,
        "docs_url": api_data["docs_url"] if api_data["docs_url"] else None,
        "download_url": api_data["download_url"] if api_data["download_url"] else None,
        "project_url": api_data["project_url"]
    }
    
    return result