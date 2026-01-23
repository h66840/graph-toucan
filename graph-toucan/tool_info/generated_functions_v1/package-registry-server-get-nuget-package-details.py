from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NuGet package details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the NuGet package
        - description (str): Description of the package functionality and purpose
        - latestVersion (str): Version string of the most recent release
        - title (str): Display title of the package
        - authors_0 (str): First author name
        - authors_1 (str): Second author name
        - license (str): License type under which the package is distributed
        - projectUrl (str): URL to the project's official website or repository
        - iconUrl (str): URL to the package icon image
        - tags_0 (str): First tag associated with the package
        - tags_1 (str): Second tag associated with the package
        - published (str): ISO 8601 timestamp of when the latest version was published
        - listed (bool): Indicates whether the package is publicly listed in the registry
        - requireLicenseAcceptance (bool): Indicates if license acceptance is required before installation
        - minClientVersion (str): Minimum NuGet client version required to use this package
        - dependencies_0_targetFramework (str): Target framework for first dependency group
        - dependencies_0_dependency_0_id (str): First dependency ID in first group
        - dependencies_0_dependency_0_range (str): Version range for first dependency in first group
        - dependencies_0_dependency_1_id (str): Second dependency ID in first group
        - dependencies_0_dependency_1_range (str): Version range for second dependency in first group
        - dependencies_1_targetFramework (str): Target framework for second dependency group
        - dependencies_1_dependency_0_id (str): First dependency ID in second group
        - dependencies_1_dependency_0_range (str): Version range for first dependency in second group
        - dependencies_1_dependency_1_id (str): Second dependency ID in second group
        - dependencies_1_dependency_1_range (str): Version range for second dependency in second group
        - versions_0 (str): First available version string
        - versions_1 (str): Second available version string
        - totalVersions (int): Total number of versions available for the package
    """
    return {
        "name": "Newtonsoft.Json",
        "description": "A popular high-performance JSON framework for .NET",
        "latestVersion": "13.0.3",
        "title": "Json.NET",
        "authors_0": "James Newton-King",
        "authors_1": "Newtonsoft",
        "license": "MIT",
        "projectUrl": "https://www.newtonsoft.com/json",
        "iconUrl": "https://www.newtonsoft.com/content/images/nuget-icon.png",
        "tags_0": "json",
        "tags_1": "serialization",
        "published": "2023-02-15T10:30:00Z",
        "listed": True,
        "requireLicenseAcceptance": False,
        "minClientVersion": "2.12",
        "dependencies_0_targetFramework": ".NETFramework4.5",
        "dependencies_0_dependency_0_id": "Microsoft.CSharp",
        "dependencies_0_dependency_0_range": "[4.0.0, )",
        "dependencies_0_dependency_1_id": "System.Runtime.Serialization.Formatters",
        "dependencies_0_dependency_1_range": "[4.3.0, )",
        "dependencies_1_targetFramework": ".NETStandard2.0",
        "dependencies_1_dependency_0_id": "System.Runtime.InteropServices",
        "dependencies_1_dependency_0_range": "[4.3.0, )",
        "dependencies_1_dependency_1_id": "System.Text.Encoding.Extensions",
        "dependencies_1_dependency_1_range": "[4.3.0, )",
        "versions_0": "13.0.1",
        "versions_1": "13.0.3",
        "totalVersions": 250
    }

def package_registry_server_get_nuget_package_details(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific NuGet package.
    
    Args:
        name (str): Name of the NuGet package to retrieve details for
        
    Returns:
        Dict containing detailed information about the NuGet package with the following structure:
        - name (str): name of the NuGet package
        - description (str): description of the package functionality and purpose
        - latestVersion (str): version string of the most recent release
        - title (str): display title of the package
        - authors (List[str]): list of author names
        - license (str): license type under which the package is distributed
        - projectUrl (str): URL to the project's official website or repository
        - iconUrl (str): URL to the package icon image
        - tags (List[str]): list of tags associated with the package
        - published (str): ISO 8601 timestamp of when the latest version was published
        - listed (bool): indicates whether the package is publicly listed in the registry
        - requireLicenseAcceptance (bool): indicates if license acceptance is required before installation
        - minClientVersion (str): minimum NuGet client version required to use this package
        - dependencies (List[Dict]): list of dependency objects, each containing 'targetFramework' and 'dependencies' 
          which is a list of packages with 'id' and 'range'
        - versions (List[str]): list of all available version strings for the package
        - totalVersions (int): total number of versions available for the package
        
    Raises:
        ValueError: If name is empty or None
    """
    if not name:
        raise ValueError("Package name is required")
        
    # Call external API to get data (simulated)
    api_data = call_external_api("package_registry_server_get_nuget_package_details")
    
    # Construct authors list
    authors = []
    if "authors_0" in api_data and api_data["authors_0"]:
        authors.append(api_data["authors_0"])
    if "authors_1" in api_data and api_data["authors_1"]:
        authors.append(api_data["authors_1"])
    
    # Construct tags list
    tags = []
    if "tags_0" in api_data and api_data["tags_0"]:
        tags.append(api_data["tags_0"])
    if "tags_1" in api_data and api_data["tags_1"]:
        tags.append(api_data["tags_1"])
    
    # Construct versions list
    versions = []
    if "versions_0" in api_data and api_data["versions_0"]:
        versions.append(api_data["versions_0"])
    if "versions_1" in api_data and api_data["versions_1"]:
        versions.append(api_data["versions_1"])
    
    # Construct dependencies structure
    dependencies = []
    
    # First dependency group
    if "dependencies_0_targetFramework" in api_data and api_data["dependencies_0_targetFramework"]:
        dep_group_0 = {
            "targetFramework": api_data["dependencies_0_targetFramework"],
            "dependencies": []
        }
        if "dependencies_0_dependency_0_id" in api_data and api_data["dependencies_0_dependency_0_id"]:
            dep_group_0["dependencies"].append({
                "id": api_data["dependencies_0_dependency_0_id"],
                "range": api_data["dependencies_0_dependency_0_range"]
            })
        if "dependencies_0_dependency_1_id" in api_data and api_data["dependencies_0_dependency_1_id"]:
            dep_group_0["dependencies"].append({
                "id": api_data["dependencies_0_dependency_1_id"],
                "range": api_data["dependencies_0_dependency_1_range"]
            })
        dependencies.append(dep_group_0)
    
    # Second dependency group
    if "dependencies_1_targetFramework" in api_data and api_data["dependencies_1_targetFramework"]:
        dep_group_1 = {
            "targetFramework": api_data["dependencies_1_targetFramework"],
            "dependencies": []
        }
        if "dependencies_1_dependency_0_id" in api_data and api_data["dependencies_1_dependency_0_id"]:
            dep_group_1["dependencies"].append({
                "id": api_data["dependencies_1_dependency_0_id"],
                "range": api_data["dependencies_1_dependency_0_range"]
            })
        if "dependencies_1_dependency_1_id" in api_data and api_data["dependencies_1_dependency_1_id"]:
            dep_group_1["dependencies"].append({
                "id": api_data["dependencies_1_dependency_1_id"],
                "range": api_data["dependencies_1_dependency_1_range"]
            })
        dependencies.append(dep_group_1)
    
    # Construct final result matching output schema
    result = {
        "name": api_data["name"],
        "description": api_data["description"],
        "latestVersion": api_data["latestVersion"],
        "title": api_data["title"],
        "authors": authors,
        "license": api_data["license"],
        "projectUrl": api_data["projectUrl"],
        "iconUrl": api_data["iconUrl"],
        "tags": tags,
        "published": api_data["published"],
        "listed": api_data["listed"],
        "requireLicenseAcceptance": api_data["requireLicenseAcceptance"],
        "minClientVersion": api_data["minClientVersion"],
        "dependencies": dependencies,
        "versions": versions,
        "totalVersions": api_data["totalVersions"]
    }
    
    return result