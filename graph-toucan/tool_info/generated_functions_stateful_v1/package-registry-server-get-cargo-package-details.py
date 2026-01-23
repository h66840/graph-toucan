from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Cargo package details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - package_name (str): Name of the Cargo package
        - version (str): Current or latest version of the package
        - description (str): Short description of the package functionality
        - author_0 (str): First author of the package
        - author_1 (str): Second author of the package
        - repository (str): URL to the source repository
        - documentation (str): URL to the package's documentation
        - homepage (str): URL to the package's homepage
        - keyword_0 (str): First keyword associated with the package
        - keyword_1 (str): Second keyword associated with the package
        - category_0 (str): First category the package belongs to
        - category_1 (str): Second category the package belongs to
        - license (str): SPDX license identifier
        - readme (str): Full text content of the README file
        - downloads (int): Total number of downloads
        - created_at (str): Timestamp when package was first published (ISO 8601)
        - updated_at (str): Timestamp when package was last updated (ISO 8601)
        - version_0 (str): First available version of the package
        - version_1 (str): Second available version of the package
        - dependency_0_name (str): First dependency name
        - dependency_0_required_version (str): Required version for first dependency
        - dependency_0_optional (bool): Whether first dependency is optional
        - dependency_1_name (str): Second dependency name
        - dependency_1_required_version (str): Required version for second dependency
        - dependency_1_optional (bool): Whether second dependency is optional
        - reverse_dependencies_count (int): Number of crates depending on this package
        - checksum (str): SHA256 checksum of the package archive
        - yanked (bool): Whether the latest version has been yanked
        - link_documentation (str): Documentation URL from links
        - link_repository (str): Repository URL from links
        - link_homepage (str): Homepage URL from links
        - link_issues (str): Issues tracker URL from links
    """
    return {
        "package_name": "serde",
        "version": "1.0.188",
        "description": "A generic serialization/deserialization framework",
        "author_0": "Erick Tryzelaar",
        "author_1": "David Tolnay",
        "repository": "https://github.com/serde-rs/serde",
        "documentation": "https://docs.serde.rs/serde/",
        "homepage": "https://serde.rs/",
        "keyword_0": "serialization",
        "keyword_1": "deserialization",
        "category_0": "Data structures",
        "category_1": "Parsing",
        "license": "MIT OR Apache-2.0",
        "readme": "# Serde\n\nSerde is a framework for serializing and deserializing Rust data structures.",
        "downloads": 125000000,
        "created_at": "2016-11-10T18:08:12.123Z",
        "updated_at": "2023-08-24T15:32:45.678Z",
        "version_0": "1.0.187",
        "version_1": "1.0.188",
        "dependency_0_name": "serde_derive",
        "dependency_0_required_version": "1.0",
        "dependency_0_optional": True,
        "dependency_1_name": "serde_json",
        "dependency_1_required_version": "1.0",
        "dependency_1_optional": False,
        "reverse_dependencies_count": 25000,
        "checksum": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890",
        "yanked": False,
        "link_documentation": "https://docs.serde.rs/serde/",
        "link_repository": "https://github.com/serde-rs/serde",
        "link_homepage": "https://serde.rs/",
        "link_issues": "https://github.com/serde-rs/serde/issues"
    }

def package_registry_server_get_cargo_package_details(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific Cargo package.
    
    Args:
        name (str): Name of the Cargo package to retrieve details for
        
    Returns:
        Dict containing detailed information about the Cargo package with the following structure:
        - package_name (str): Name of the Cargo package
        - version (str): Current or latest version of the package
        - description (str): Short description of the package functionality
        - authors (List[str]): List of authors or maintainers of the package
        - repository (str): URL to the source repository (e.g., GitHub)
        - documentation (str): URL to the package's documentation
        - homepage (str): URL to the package's homepage
        - keywords (List[str]): Keywords associated with the package for discoverability
        - categories (List[str]): List of categories the package belongs to in the registry
        - license (str): SPDX license identifier under which the package is distributed
        - readme (str): Full text content of the package's README file
        - downloads (int): Total number of downloads for this package
        - created_at (str): Timestamp when the package was first published (ISO 8601 format)
        - updated_at (str): Timestamp when the package was last updated (ISO 8601 format)
        - versions (List[str]): List of all available versions of the package
        - dependencies (List[Dict]): List of dependencies with fields: name (str), required_version (str), optional (bool)
        - reverse_dependencies_count (int): Number of other crates that depend on this package
        - checksum (str): SHA256 checksum of the package archive
        - yanked (bool): Indicates whether the latest version has been yanked (unpublished but still downloadable)
        - links (Dict): Additional URLs such as documentation, repository, issue tracker
    
    Raises:
        ValueError: If the name parameter is empty or None
    """
    if not name:
        raise ValueError("Parameter 'name' is required")
    
    # Call external API to get flat data
    api_data = call_external_api("package-registry-server-get-cargo-package-details", **locals())
    
    # Construct nested structure matching output schema
    result = {
        "package_name": api_data["package_name"],
        "version": api_data["version"],
        "description": api_data["description"],
        "authors": [
            api_data["author_0"],
            api_data["author_1"]
        ],
        "repository": api_data["repository"],
        "documentation": api_data["documentation"],
        "homepage": api_data["homepage"],
        "keywords": [
            api_data["keyword_0"],
            api_data["keyword_1"]
        ],
        "categories": [
            api_data["category_0"],
            api_data["category_1"]
        ],
        "license": api_data["license"],
        "readme": api_data["readme"],
        "downloads": api_data["downloads"],
        "created_at": api_data["created_at"],
        "updated_at": api_data["updated_at"],
        "versions": [
            api_data["version_0"],
            api_data["version_1"]
        ],
        "dependencies": [
            {
                "name": api_data["dependency_0_name"],
                "required_version": api_data["dependency_0_required_version"],
                "optional": api_data["dependency_0_optional"]
            },
            {
                "name": api_data["dependency_1_name"],
                "required_version": api_data["dependency_1_required_version"],
                "optional": api_data["dependency_1_optional"]
            }
        ],
        "reverse_dependencies_count": api_data["reverse_dependencies_count"],
        "checksum": api_data["checksum"],
        "yanked": api_data["yanked"],
        "links": {
            "documentation": api_data["link_documentation"],
            "repository": api_data["link_repository"],
            "homepage": api_data["link_homepage"],
            "issues": api_data["link_issues"]
        }
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
