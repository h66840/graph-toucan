from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching vulnerability data from external API for npm packages.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_package (str): Name of the first package
        - result_0_versionQueried (str): Version queried for the first package
        - result_0_status (str): Status of vulnerability check for the first package
        - result_0_message (str): Message related to the first package check
        - result_0_vulnerabilities_0_severity (str): Severity of first vulnerability in first package
        - result_0_vulnerabilities_0_title (str): Title of first vulnerability in first package
        - result_0_vulnerabilities_0_description (str): Description of first vulnerability in first package
        - result_0_vulnerabilities_1_severity (str): Severity of second vulnerability in first package
        - result_0_vulnerabilities_1_title (str): Title of second vulnerability in first package
        - result_0_vulnerabilities_1_description (str): Description of second vulnerability in first package
        - result_1_package (str): Name of the second package
        - result_1_versionQueried (str): Version queried for the second package
        - result_1_status (str): Status of vulnerability check for the second package
        - result_1_message (str): Message related to the second package check
        - result_1_vulnerabilities_0_severity (str): Severity of first vulnerability in second package
        - result_1_vulnerabilities_0_title (str): Title of first vulnerability in second package
        - result_1_vulnerabilities_0_description (str): Description of first vulnerability in second package
        - result_1_vulnerabilities_1_severity (str): Severity of second vulnerability in second package
        - result_1_vulnerabilities_1_title (str): Title of second vulnerability in second package
        - result_1_vulnerabilities_1_description (str): Description of second vulnerability in second package
    """
    return {
        "result_0_package": "lodash",
        "result_0_versionQueried": "4.17.20",
        "result_0_status": "vulnerable",
        "result_0_message": "Multiple known vulnerabilities detected",
        "result_0_vulnerabilities_0_severity": "high",
        "result_0_vulnerabilities_0_title": "Prototype Pollution",
        "result_0_vulnerabilities_0_description": "Prototype pollution vulnerability in merge function",
        "result_0_vulnerabilities_1_severity": "moderate",
        "result_0_vulnerabilities_1_title": "Regular Expression Denial of Service",
        "result_0_vulnerabilities_1_description": " vulnerable to ReDoS attack via crafted input",
        
        "result_1_package": "express",
        "result_1_versionQueried": "4.18.1",
        "result_1_status": "safe",
        "result_1_message": "No known vulnerabilities found",
        "result_1_vulnerabilities_0_severity": "none",
        "result_1_vulnerabilities_0_title": "N/A",
        "result_1_vulnerabilities_0_description": "No vulnerability",
        "result_1_vulnerabilities_1_severity": "none",
        "result_1_vulnerabilities_1_title": "N/A",
        "result_1_vulnerabilities_1_description": "No vulnerability"
    }

def npm_sentinel_mcp_npmVulnerabilities(packages: List[str]) -> Dict[str, Any]:
    """
    Check for known vulnerabilities in the specified npm packages.
    
    Args:
        packages (List[str]): List of package names to check for vulnerabilities
        
    Returns:
        Dict containing a 'results' key with a list of vulnerability check results.
        Each result contains 'package', 'versionQueried', 'status', 'vulnerabilities', and 'message' fields.
        
    Raises:
        ValueError: If packages list is empty or contains invalid values
    """
    if not packages:
        raise ValueError("packages list cannot be empty")
    
    if not isinstance(packages, list):
        raise ValueError("packages must be a list of strings")
    
    for package in packages:
        if not isinstance(package, str) or not package.strip():
            raise ValueError("each package must be a non-empty string")
    
    # Call external API to get vulnerability data (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmVulnerabilities")
    
    # Construct results list by mapping flat API data to nested structure
    results: List[Dict[str, Any]] = []
    
    # Process first package result
    result_0_vulnerabilities = [
        {
            "severity": api_data["result_0_vulnerabilities_0_severity"],
            "title": api_data["result_0_vulnerabilities_0_title"],
            "description": api_data["result_0_vulnerabilities_0_description"]
        },
        {
            "severity": api_data["result_0_vulnerabilities_1_severity"],
            "title": api_data["result_0_vulnerabilities_1_title"],
            "description": api_data["result_0_vulnerabilities_1_description"]
        }
    ]
    
    # Process second package result
    result_1_vulnerabilities = [
        {
            "severity": api_data["result_1_vulnerabilities_0_severity"],
            "title": api_data["result_1_vulnerabilities_0_title"],
            "description": api_data["result_1_vulnerabilities_0_description"]
        },
        {
            "severity": api_data["result_1_vulnerabilities_1_severity"],
            "title": api_data["result_1_vulnerabilities_1_title"],
            "description": api_data["result_1_vulnerabilities_1_description"]
        }
    ]
    
    # Build results list with both package checks
    results.append({
        "package": api_data["result_0_package"],
        "versionQueried": api_data["result_0_versionQueried"],
        "status": api_data["result_0_status"],
        "vulnerabilities": result_0_vulnerabilities,
        "message": api_data["result_0_message"]
    })
    
    results.append({
        "package": api_data["result_1_package"],
        "versionQueried": api_data["result_1_versionQueried"],
        "status": api_data["result_1_status"],
        "vulnerabilities": result_1_vulnerabilities,
        "message": api_data["result_1_message"]
    })
    
    # If more packages were requested, repeat pattern or adjust accordingly
    # For now, return the two simulated results
    return {"results": results}