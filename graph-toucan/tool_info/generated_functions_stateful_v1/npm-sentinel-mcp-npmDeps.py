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
    Simulates fetching data from external API for NPM package dependency analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_package (str): First package name
        - result_0_status (str): Status of first package analysis
        - result_0_error (str): Error message for first package (if any)
        - result_0_message (str): Message for first package
        - result_0_data_dependencies_0_name (str): First dependency name of first package
        - result_0_data_dependencies_0_version (str): First dependency version of first package
        - result_0_data_devDependencies_0_name (str): First devDependency name of first package
        - result_0_data_devDependencies_0_version (str): First devDependency version of first package
        - result_0_data_dependencies_1_name (str): Second dependency name of first package
        - result_0_data_dependencies_1_version (str): Second dependency version of first package
        - result_0_data_devDependencies_1_name (str): Second devDependency name of first package
        - result_0_data_devDependencies_1_version (str): Second devDependency version of first package
        - result_1_package (str): Second package name
        - result_1_status (str): Status of second package analysis
        - result_1_error (str): Error message for second package (if any)
        - result_1_message (str): Message for second package
        - result_1_data_dependencies_0_name (str): First dependency name of second package
        - result_1_data_dependencies_0_version (str): First dependency version of second package
        - result_1_data_devDependencies_0_name (str): First devDependency name of second package
        - result_1_data_devDependencies_0_version (str): First devDependency version of second package
        - result_1_data_dependencies_1_name (str): Second dependency name of second package
        - result_1_data_dependencies_1_version (str): Second dependency version of second package
        - result_1_data_devDependencies_1_name (str): Second devDependency name of second package
        - result_1_data_devDependencies_1_version (str): Second devDependency version of second package
    """
    return {
        "result_0_package": "express",
        "result_0_status": "success",
        "result_0_error": "",
        "result_0_message": "Dependencies analyzed successfully",
        "result_0_data_dependencies_0_name": "accepts",
        "result_0_data_dependencies_0_version": "^1.3.8",
        "result_0_data_dependencies_1_name": "body-parser",
        "result_0_data_dependencies_1_version": "^1.19.0",
        "result_0_data_devDependencies_0_name": "mocha",
        "result_0_data_devDependencies_0_version": "^8.0.0",
        "result_0_data_devDependencies_1_name": "nyc",
        "result_0_data_devDependencies_1_version": "^15.0.0",
        
        "result_1_package": "react",
        "result_1_status": "success",
        "result_1_error": "",
        "result_1_message": "Dependencies analyzed successfully",
        "result_1_data_dependencies_0_name": "loose-envify",
        "result_1_data_dependencies_0_version": "^1.4.0",
        "result_1_data_dependencies_1_name": "object-assign",
        "result_1_data_dependencies_1_version": "^4.1.1",
        "result_1_data_devDependencies_0_name": "jest",
        "result_1_data_devDependencies_0_version": "^26.0.0",
        "result_1_data_devDependencies_1_name": "eslint",
        "result_1_data_devDependencies_1_version": "^7.0.0"
    }

def npm_sentinel_mcp_npmDeps(packages: List[str]) -> Dict[str, Any]:
    """
    Analyze dependencies and devDependencies of an NPM package.
    
    Args:
        packages (List[str]): List of package names to analyze dependencies for
        
    Returns:
        Dict containing a list of result objects, each with 'package', 'status', 'error', 'data', and 'message' fields.
        The 'data' field contains 'dependencies' and 'devDependencies' as lists of dicts with 'name' and 'version'.
        
    Example:
        {
            "results": [
                {
                    "package": "express",
                    "status": "success",
                    "error": "",
                    "message": "Dependencies analyzed successfully",
                    "data": {
                        "dependencies": [
                            {"name": "accepts", "version": "^1.3.8"},
                            {"name": "body-parser", "version": "^1.19.0"}
                        ],
                        "devDependencies": [
                            {"name": "mocha", "version": "^8.0.0"},
                            {"name": "nyc", "version": "^15.0.0"}
                        ]
                    }
                },
                {
                    "package": "react",
                    "status": "success",
                    "error": "",
                    "message": "Dependencies analyzed successfully",
                    "data": {
                        "dependencies": [
                            {"name": "loose-envify", "version": "^1.4.0"},
                            {"name": "object-assign", "version": "^4.1.1"}
                        ],
                        "devDependencies": [
                            {"name": "jest", "version": "^26.0.0"},
                            {"name": "eslint", "version": "^7.0.0"}
                        ]
                    }
                }
            ]
        }
    """
    if not packages:
        return {"results": []}
    
    # Fetch simulated external data
    api_data = call_external_api("npm-sentinel-mcp-npmDeps", **locals())
    
    results: List[Dict[str, Any]] = []
    
    # Process first result
    if "result_0_package" in api_data:
        result_0 = {
            "package": api_data["result_0_package"],
            "status": api_data["result_0_status"],
            "error": api_data["result_0_error"],
            "message": api_data["result_0_message"],
            "data": {
                "dependencies": [
                    {
                        "name": api_data["result_0_data_dependencies_0_name"],
                        "version": api_data["result_0_data_dependencies_0_version"]
                    },
                    {
                        "name": api_data["result_0_data_dependencies_1_name"],
                        "version": api_data["result_0_data_dependencies_1_version"]
                    }
                ],
                "devDependencies": [
                    {
                        "name": api_data["result_0_data_devDependencies_0_name"],
                        "version": api_data["result_0_data_devDependencies_0_version"]
                    },
                    {
                        "name": api_data["result_0_data_devDependencies_1_name"],
                        "version": api_data["result_0_data_devDependencies_1_version"]
                    }
                ]
            }
        }
        results.append(result_0)
    
    # Process second result
    if "result_1_package" in api_data:
        result_1 = {
            "package": api_data["result_1_package"],
            "status": api_data["result_1_status"],
            "error": api_data["result_1_error"],
            "message": api_data["result_1_message"],
            "data": {
                "dependencies": [
                    {
                        "name": api_data["result_1_data_dependencies_0_name"],
                        "version": api_data["result_1_data_dependencies_0_version"]
                    },
                    {
                        "name": api_data["result_1_data_dependencies_1_name"],
                        "version": api_data["result_1_data_dependencies_1_version"]
                    }
                ],
                "devDependencies": [
                    {
                        "name": api_data["result_1_data_devDependencies_0_name"],
                        "version": api_data["result_1_data_devDependencies_0_version"]
                    },
                    {
                        "name": api_data["result_1_data_devDependencies_1_name"],
                        "version": api_data["result_1_data_devDependencies_1_version"]
                    }
                ]
            }
        }
        results.append(result_1)
    
    return {"results": results}

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
