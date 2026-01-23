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
    Simulates fetching data from external API for listing GitHub repository structure.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - repository (str): Name of the GitHub repository in "owner/repo" format
        - url (str): URL to the GitHub repository
        - root_files_0_name (str): Name of first file at root level
        - root_files_0_path (str): Path of first file at root level
        - root_files_1_name (str): Name of second file at root level
        - root_files_1_path (str): Path of second file at root level
        - root_directories_0_name (str): Name of first directory at root level
        - root_directories_0_path (str): Path of first directory at root level
        - root_directories_1_name (str): Name of second directory at root level
        - root_directories_1_path (str): Path of second directory at root level
        - directories_a_files_0_name (str): Name of first file in directory 'a'
        - directories_a_files_0_path (str): Path of first file in directory 'a'
        - directories_a_files_0_extension (str): Extension of first file in directory 'a'
        - directories_a_files_1_name (str): Name of second file in directory 'a'
        - directories_a_files_1_path (str): Path of second file in directory 'a'
        - directories_a_files_1_extension (str): Extension of second file in directory 'a'
        - directories_a_directories_0_name (str): Name of first subdirectory in directory 'a'
        - directories_a_directories_0_path (str): Path of first subdirectory in directory 'a'
        - directories_a_directories_1_name (str): Name of second subdirectory in directory 'a'
        - directories_a_directories_1_path (str): Path of second subdirectory in directory 'a'
        - directories_a_path (str): Full path of directory 'a'
        - directories_b_files_0_name (str): Name of first file in directory 'b'
        - directories_b_files_0_path (str): Path of first file in directory 'b'
        - directories_b_files_0_extension (str): Extension of first file in directory 'b'
        - directories_b_files_1_name (str): Name of second file in directory 'b'
        - directories_b_files_1_path (str): Path of second file in directory 'b'
        - directories_b_files_1_extension (str): Extension of second file in directory 'b'
        - directories_b_directories_0_name (str): Name of first subdirectory in directory 'b'
        - directories_b_directories_0_path (str): Path of first subdirectory in directory 'b'
        - directories_b_directories_1_name (str): Name of second subdirectory in directory 'b'
        - directories_b_directories_1_path (str): Path of second subdirectory in directory 'b'
        - directories_b_path (str): Full path of directory 'b'
        - summary_total_root_files (int): Total number of files at root level
        - summary_total_root_directories (int): Total number of directories at root level
        - summary_explored_directories_0 (str): First explored directory path
        - summary_explored_directories_1 (str): Second explored directory path
    """
    return {
        "repository": "openai/agent-library",
        "url": "https://github.com/openai/agent-library",
        "root_files_0_name": "README.md",
        "root_files_0_path": "/README.md",
        "root_files_1_name": "LICENSE",
        "root_files_1_path": "/LICENSE",
        "root_directories_0_name": "src",
        "root_directories_0_path": "/src",
        "root_directories_1_name": "tests",
        "root_directories_1_path": "/tests",
        "directories_a_files_0_name": "main.py",
        "directories_a_files_0_path": "/src/main.py",
        "directories_a_files_0_extension": "py",
        "directories_a_files_1_name": "utils.py",
        "directories_a_files_1_path": "/src/utils.py",
        "directories_a_files_1_extension": "py",
        "directories_a_directories_0_name": "helpers",
        "directories_a_directories_0_path": "/src/helpers",
        "directories_a_directories_1_name": "config",
        "directories_a_directories_1_path": "/src/config",
        "directories_a_path": "/src",
        "directories_b_files_0_name": "test_main.py",
        "directories_b_files_0_path": "/tests/test_main.py",
        "directories_b_files_0_extension": "py",
        "directories_b_files_1_name": "test_utils.py",
        "directories_b_files_1_path": "/tests/test_utils.py",
        "directories_b_files_1_extension": "py",
        "directories_b_directories_0_name": "fixtures",
        "directories_b_directories_0_path": "/tests/fixtures",
        "directories_b_directories_1_name": "unit",
        "directories_b_directories_1_path": "/tests/unit",
        "directories_b_path": "/tests",
        "summary_total_root_files": 2,
        "summary_total_root_directories": 2,
        "summary_explored_directories_0": "/src",
        "summary_explored_directories_1": "/tests"
    }

def openai_agent_library_list_github_structure() -> Dict[str, Any]:
    """
    List the structure of the GitHub repository.
    
    Returns:
        Dict containing the full structure of the GitHub repository with nested fields:
        - repository (str): name of the GitHub repository in "owner/repo" format
        - url (str): URL to the GitHub repository
        - root (Dict): contains 'files' and 'directories' lists for root-level items
        - root.files (List[Dict]): list of files in the repository root, each with 'name' and 'path' fields
        - root.directories (List[Dict]): list of directories in the repository root, each with 'name' and 'path' fields
        - directories (Dict): mapping of directory paths to their contents
        - directories.*.files (List[Dict]): list of files in the given directory
        - directories.*.directories (List[Dict]): list of subdirectories in the given directory
        - directories.*.path (str): full path of the directory
        - summary (Dict): summary statistics about the repository structure
        - summary.total_root_files (int): total number of files at the root level
        - summary.total_root_directories (int): total number of directories at the root level
        - summary.explored_directories (List[str]): list of directory paths that were fully explored
    """
    try:
        api_data = call_external_api("openai-agent-library-list_github_structure", **locals())
        
        # Construct root.files
        root_files = [
            {
                "name": api_data["root_files_0_name"],
                "path": api_data["root_files_0_path"]
            },
            {
                "name": api_data["root_files_1_name"],
                "path": api_data["root_files_1_path"]
            }
        ]
        
        # Construct root.directories
        root_directories = [
            {
                "name": api_data["root_directories_0_name"],
                "path": api_data["root_directories_0_path"]
            },
            {
                "name": api_data["root_directories_1_name"],
                "path": api_data["root_directories_1_path"]
            }
        ]
        
        # Construct directories dictionary
        directories = {}
        
        # Add /src directory
        src_path = api_data["directories_a_path"]
        directories[src_path] = {
            "files": [
                {
                    "name": api_data["directories_a_files_0_name"],
                    "path": api_data["directories_a_files_0_path"],
                    "extension": api_data["directories_a_files_0_extension"]
                },
                {
                    "name": api_data["directories_a_files_1_name"],
                    "path": api_data["directories_a_files_1_path"],
                    "extension": api_data["directories_a_files_1_extension"]
                }
            ],
            "directories": [
                {
                    "name": api_data["directories_a_directories_0_name"],
                    "path": api_data["directories_a_directories_0_path"]
                },
                {
                    "name": api_data["directories_a_directories_1_name"],
                    "path": api_data["directories_a_directories_1_path"]
                }
            ],
            "path": src_path
        }
        
        # Add /tests directory
        tests_path = api_data["directories_b_path"]
        directories[tests_path] = {
            "files": [
                {
                    "name": api_data["directories_b_files_0_name"],
                    "path": api_data["directories_b_files_0_path"],
                    "extension": api_data["directories_b_files_0_extension"]
                },
                {
                    "name": api_data["directories_b_files_1_name"],
                    "path": api_data["directories_b_files_1_path"],
                    "extension": api_data["directories_b_files_1_extension"]
                }
            ],
            "directories": [
                {
                    "name": api_data["directories_b_directories_0_name"],
                    "path": api_data["directories_b_directories_0_path"]
                },
                {
                    "name": api_data["directories_b_directories_1_name"],
                    "path": api_data["directories_b_directories_1_path"]
                }
            ],
            "path": tests_path
        }
        
        # Construct summary
        summary = {
            "total_root_files": api_data["summary_total_root_files"],
            "total_root_directories": api_data["summary_total_root_directories"],
            "explored_directories": [
                api_data["summary_explored_directories_0"],
                api_data["summary_explored_directories_1"]
            ]
        }
        
        # Construct final result
        result = {
            "repository": api_data["repository"],
            "url": api_data["url"],
            "root": {
                "files": root_files,
                "directories": root_directories
            },
            "directories": directories,
            "summary": summary
        }
        
        return result
        
    except Exception as e:
        # In case of any error, return empty structure
        return {
            "repository": "",
            "url": "",
            "root": {
                "files": [],
                "directories": []
            },
            "directories": {},
            "summary": {
                "total_root_files": 0,
                "total_root_directories": 0,
                "explored_directories": []
            }
        }

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
