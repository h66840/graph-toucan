from typing import Dict, List, Any

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
    Simulates fetching data from external API for documentation listing.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_docs (int): Total number of documentation files available
        - doc_0_name (str): Name of the first documentation file
        - doc_0_path (str): Path of the first documentation file
        - doc_0_last_modified (str): Last modified timestamp of the first documentation file
        - doc_0_size (int): Size in bytes of the first documentation file
        - doc_0_preview (str): Preview text of the first documentation file
        - doc_1_name (str): Name of the second documentation file
        - doc_1_path (str): Path of the second documentation file
        - doc_1_last_modified (str): Last modified timestamp of the second documentation file
        - doc_1_size (int): Size in bytes of the second documentation file
        - doc_1_preview (str): Preview text of the second documentation file
    """
    return {
        "total_docs": 2,
        "doc_0_name": "Getting Started Guide",
        "doc_0_path": "/docs/getting-started.md",
        "doc_0_last_modified": "2023-10-01T08:30:00Z",
        "doc_0_size": 2048,
        "doc_0_preview": "Welcome to Aurora! This guide will help you set up your environment...",
        
        "doc_1_name": "API Reference",
        "doc_1_path": "/docs/api-reference.md",
        "doc_1_last_modified": "2023-10-05T12:15:00Z",
        "doc_1_size": 8192,
        "doc_1_preview": "This document describes all available endpoints in the Aurora system..."
    }

def aurora_documentation_list_docs() -> Dict[str, Any]:
    """
    List all available documentation files with their paths and descriptions.
    
    Returns:
        Dict containing:
        - total_docs (int): total number of documentation files available
        - docs (List[Dict]): list of documentation file objects, each containing:
            - name (str): name of the documentation file
            - path (str): full path to the documentation file
            - last_modified (str): ISO format timestamp of last modification
            - size (int): file size in bytes
            - preview (str): short preview text of the document content
    """
    try:
        # Fetch data from external API simulation
        api_data = call_external_api("aurora-documentation-list_docs", **locals())
        
        # Construct the list of documentation files from flattened API response
        docs = [
            {
                "name": api_data["doc_0_name"],
                "path": api_data["doc_0_path"],
                "last_modified": api_data["doc_0_last_modified"],
                "size": api_data["doc_0_size"],
                "preview": api_data["doc_0_preview"]
            },
            {
                "name": api_data["doc_1_name"],
                "path": api_data["doc_1_path"],
                "last_modified": api_data["doc_1_last_modified"],
                "size": api_data["doc_1_size"],
                "preview": api_data["doc_1_preview"]
            }
        ]
        
        # Construct final result matching output schema
        result = {
            "total_docs": api_data["total_docs"],
            "docs": docs
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to list documentation files: {str(e)}")

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        pass
    except Exception:
        pass
    return result
