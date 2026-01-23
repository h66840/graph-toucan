from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Go package details.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): The full module name of the Go package
        - version (str): The latest or requested version of the module
        - version_0 (str): First available version of the module
        - version_1 (str): Second available version of the module
        - time (str): Publication timestamp of the current version in ISO 8601 format
        - repository (str): URL of the source repository (e.g., GitHub)
        - description (str): Short description or README summary of the module
        - license (str): License type (e.g., MIT, Apache-2.0) if detected
        - imported_by_count (int): Number of other modules that import this package
        - direct_import_0 (str): First package that directly depends on this one
        - direct_import_1 (str): Second package that directly depends on this one
        - file_0_path (str): Path of the first file
        - file_0_size (int): Size of the first file in bytes
        - file_0_executable (bool): Whether the first file is executable
        - file_1_path (str): Path of the second file
        - file_1_size (int): Size of the second file in bytes
        - file_1_executable (bool): Whether the second file is executable
        - documentation (str): Rendered documentation (e.g., godoc content) for the current version
        - readme (str): Raw or rendered README content from the repository
        - module_path (str): Module path as declared in go.mod
        - main_package (bool): Indicates whether this is a main package (executable)
        - deprecated (bool): Whether the module is marked as deprecated
        - reason (str): Optional reason for deprecation or discontinuation
        - checksum (str): Checksum (e.g., SHA-256) of the module archive
        - go_mod (str): Content of the go.mod file for this version
    """
    return {
        "name": "github.com/example/pkg",
        "version": "v1.2.3",
        "version_0": "v1.0.0",
        "version_1": "v1.1.0",
        "time": datetime.now(timezone.utc).isoformat(),
        "repository": "https://github.com/example/pkg",
        "description": "A sample Go package for demonstration purposes",
        "license": "MIT",
        "imported_by_count": 150,
        "direct_import_0": "github.com/user/app1",
        "direct_import_1": "github.com/user/app2",
        "file_0_path": "main.go",
        "file_0_size": 1024,
        "file_0_executable": True,
        "file_1_path": "utils.go",
        "file_1_size": 2048,
        "file_1_executable": False,
        "documentation": "Package pkg provides useful utilities for Go applications.",
        "readme": "# Example Package\nThis is a sample Go package.",
        "module_path": "github.com/example/pkg",
        "main_package": True,
        "deprecated": False,
        "reason": "",
        "checksum": "sha256:abc123def456...",
        "go_mod": 'module github.com/example/pkg\ngo 1.19\nrequire github.com/other/lib v1.0.0',
    }


def package_registry_server_get_golang_package_details(module: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific Go module/package.

    Args:
        module (str): The full module name of the Go package (e.g., github.com/example/pkg)

    Returns:
        Dict containing detailed information about the Go module with the following keys:
        - name (str): The full module name of the Go package
        - version (str): The latest or requested version of the module
        - versions (List[str]): List of all available versions of the module
        - time (str): Publication timestamp of the current version in ISO 8601 format
        - repository (str): URL of the source repository (e.g., GitHub)
        - description (str): Short description or README summary of the module
        - license (str): License type (e.g., MIT, Apache-2.0) if detected
        - imported_by_count (int): Number of other modules that import this package
        - direct_imports (List[str]): List of packages/modules that directly depend on this one
        - files (Dict): Mapping of file paths to metadata (e.g., size, executable flag)
        - documentation (str): Rendered documentation (e.g., godoc content) for the current version
        - readme (str): Raw or rendered README content from the repository
        - module_path (str): Module path as declared in go.mod
        - main_package (bool): Indicates whether this is a main package (executable)
        - deprecated (bool): Whether the module is marked as deprecated
        - reason (str): Optional reason for deprecation or discontinuation
        - checksum (str): Checksum (e.g., SHA-256) of the module archive
        - go_mod (str): Content of the go.mod file for this version

    Raises:
        ValueError: If module name is empty or invalid
    """
    if not module or not isinstance(module, str) or not module.strip():
        raise ValueError("Module name is required and must be a non-empty string")

    module = module.strip()

    # Fetch data from external API (simulated)
    api_data = call_external_api("package-registry-server-get-golang-package-details")

    # Construct the nested output structure
    result = {
        "name": api_data["name"],
        "version": api_data["version"],
        "versions": [api_data["version_0"], api_data["version_1"]],
        "time": api_data["time"],
        "repository": api_data["repository"],
        "description": api_data["description"],
        "license": api_data["license"],
        "imported_by_count": api_data["imported_by_count"],
        "direct_imports": [api_data["direct_import_0"], api_data["direct_import_1"]],
        "files": {
            api_data["file_0_path"]: {
                "size": api_data["file_0_size"],
                "executable": api_data["file_0_executable"]
            },
            api_data["file_1_path"]: {
                "size": api_data["file_1_size"],
                "executable": api_data["file_1_executable"]
            }
        },
        "documentation": api_data["documentation"],
        "readme": api_data["readme"],
        "module_path": api_data["module_path"],
        "main_package": api_data["main_package"],
        "deprecated": api_data["deprecated"],
        "reason": api_data["reason"],
        "checksum": api_data["checksum"],
        "go_mod": api_data["go_mod"]
    }

    return result