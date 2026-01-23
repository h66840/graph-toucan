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
    Simulates fetching data from external API for the MCP server initialization.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - instructions_0_step (str): Step identifier for first instruction
        - instructions_0_action (str): Action to perform for first instruction
        - instructions_0_description (str): Description of first instruction
        - instructions_0_required (bool): Whether first instruction is required
        - instructions_1_step (str): Step identifier for second instruction
        - instructions_1_action (str): Action to perform for second instruction
        - instructions_1_description (str): Description of second instruction
        - instructions_1_required (bool): Whether second instruction is required
        - required_tools_0 (str): First required tool name after initialization
        - required_tools_1 (str): Second required tool name after initialization
        - session_token (str): Unique session token for authentication in subsequent calls
        - expires_in (int): Number of seconds until session token expires
        - status (str): Status of the initialization request
        - metadata_server_version (str): Version of the MCP server
        - metadata_timestamp (str): ISO timestamp of the response
        - metadata_environment (str): Server environment (e.g., production, staging)
    """
    return {
        "instructions_0_step": "INIT_001",
        "instructions_0_action": "Authenticate session",
        "instructions_0_description": "Call this tool to initialize the MCP server session.",
        "instructions_0_required": True,
        "instructions_1_step": "INIT_002",
        "instructions_1_action": "Validate token",
        "instructions_1_description": "Ensure the session token is stored and used in subsequent requests.",
        "instructions_1_required": True,
        "required_tools_0": "blockscout-mcp-server-__list_contracts__",
        "required_tools_1": "blockscout-mcp-server-__get_contract_details__",
        "session_token": "sess_abc123xyz456_token",
        "expires_in": 3600,
        "status": "success",
        "metadata_server_version": "1.5.2",
        "metadata_timestamp": "2023-11-15T10:30:00Z",
        "metadata_environment": "production"
    }

def blockscout_mcp_server_get_instructions() -> Dict[str, Any]:
    """
    Initializes the MCP server session by retrieving setup instructions, required tools,
    session token, and metadata. This function must be called once before any other tool
    is used in the session.

    Returns:
        Dict containing:
        - instructions (List[Dict]): List of step-by-step setup instructions with keys:
            'step', 'action', 'description', 'required'
        - required_tools (List[str]): List of tool names that must be used after initialization
        - session_token (str): Unique token for authenticating subsequent API calls
        - expires_in (int): Time in seconds until the session token expires
        - status (str): Status of the initialization (e.g., 'success')
        - metadata (Dict): Additional context including server version, timestamp, and environment
    """
    try:
        api_data = call_external_api("blockscout-mcp-server-__get_instructions__", **locals())

        instructions = [
            {
                "step": api_data["instructions_0_step"],
                "action": api_data["instructions_0_action"],
                "description": api_data["instructions_0_description"],
                "required": api_data["instructions_0_required"]
            },
            {
                "step": api_data["instructions_1_step"],
                "action": api_data["instructions_1_action"],
                "description": api_data["instructions_1_description"],
                "required": api_data["instructions_1_required"]
            }
        ]

        required_tools = [
            api_data["required_tools_0"],
            api_data["required_tools_1"]
        ]

        metadata = {
            "server_version": api_data["metadata_server_version"],
            "timestamp": api_data["metadata_timestamp"],
            "environment": api_data["metadata_environment"]
        }

        result = {
            "instructions": instructions,
            "required_tools": required_tools,
            "session_token": api_data["session_token"],
            "expires_in": api_data["expires_in"],
            "status": api_data["status"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to initialize MCP server session: {str(e)}") from e

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
