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
    Simulates fetching data from external API for UI component layout information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - component_0_name (str): Name of the first component
        - component_0_type (str): Type of the first component
        - component_0_layout_config (str): Layout configuration of the first component in JSON string format
        - component_0_properties (str): Available properties of the first component in JSON string format
        - component_1_name (str): Name of the second component
        - component_1_type (str): Type of the second component
        - component_1_layout_config (str): Layout configuration of the second component in JSON string format
        - component_1_properties (str): Available properties of the second component in JSON string format
        - total_components (int): Total number of components returned
        - supported_type_0 (str): First supported component type
        - supported_type_1 (str): Second supported component type
        - layout_schema_version (str): Version identifier for the layout schema format
        - metadata_timestamp (str): Generation timestamp in ISO format
        - metadata_server_version (str): Server version string
        - metadata_docs_url (str): Documentation URL
    """
    return {
        "component_0_name": "MainDashboardGrid",
        "component_0_type": "bento-grid",
        "component_0_layout_config": '{"rows": 3, "columns": 4, "gap": 12}',
        "component_0_properties": '{"items": ["chart1", "chart2", "table1"], "autoResize": true}',
        "component_1_name": "FileExplorer",
        "component_1_type": "file-tree",
        "component_1_layout_config": '{"orientation": "vertical", "width": 280}',
        "component_1_properties": '{"showIcons": true, "draggable": true, "contextMenu": true}',
        "total_components": 2,
        "supported_type_0": "bento-grid",
        "supported_type_1": "file-tree",
        "layout_schema_version": "1.2.0",
        "metadata_timestamp": "2023-12-05T10:30:00Z",
        "metadata_server_version": "2.5.1",
        "metadata_docs_url": "https://docs.magicui.dev/components"
    }

def magic_ui_component_server_getLayout() -> Dict[str, Any]:
    """
    Provides implementation details for various UI components including bento-grid, dock, file-tree, 
    grid-pattern, interactive-grid-pattern, and dot-pattern components.
    
    This function retrieves layout and configuration data for supported UI components by querying 
    an external API (simulated) and transforming the flat response into a structured nested format.
    
    Returns:
        Dict containing:
        - components (List[Dict]): List of component implementation details with name, type, 
          layout configuration, and available properties
        - total_components (int): Total number of components returned
        - supported_types (List[str]): List of supported component types
        - layout_schema_version (str): Version identifier for the layout schema format
        - metadata (Dict): Additional metadata including timestamp, server version, and docs URL
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("magic-ui-component-server-getLayout", **locals())
        
        # Construct components list from indexed fields
        components = [
            {
                "name": api_data["component_0_name"],
                "type": api_data["component_0_type"],
                "layout_configuration": api_data["component_0_layout_config"],
                "properties": api_data["component_0_properties"]
            },
            {
                "name": api_data["component_1_name"],
                "type": api_data["component_1_type"],
                "layout_configuration": api_data["component_1_layout_config"],
                "properties": api_data["component_1_properties"]
            }
        ]
        
        # Construct supported types list
        supported_types = [
            api_data["supported_type_0"],
            api_data["supported_type_1"]
        ]
        
        # Construct metadata dictionary
        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "server_version": api_data["metadata_server_version"],
            "documentation_url": api_data["metadata_docs_url"]
        }
        
        # Build final result structure
        result = {
            "components": components,
            "total_components": api_data["total_components"],
            "supported_types": supported_types,
            "layout_schema_version": api_data["layout_schema_version"],
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"Failed to retrieve component layout data: {str(e)}")

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
