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
    Simulates fetching motion component data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - component_0_name (str): Name of first component
        - component_0_animation_type (str): Animation type of first component
        - component_0_config_options (str): JSON string of config options for first component
        - component_0_code_snippet (str): Code snippet for first component
        - component_0_supported_properties (str): JSON string of supported properties for first component
        - component_1_name (str): Name of second component
        - component_1_animation_type (str): Animation type of second component
        - component_1_config_options (str): JSON string of config options for second component
        - component_1_code_snippet (str): Code snippet for second component
        - component_1_supported_properties (str): JSON string of supported properties for second component
        - total_components (int): Total number of components returned
        - metadata_timestamp (str): Timestamp of response in ISO format
        - metadata_version (str): API version
        - metadata_categories_scroll (bool): Whether scroll effects are available
        - metadata_categories_fade (bool): Whether fade effects are available
        - metadata_categories_orbit (bool): Whether orbit effects are available
    """
    return {
        "component_0_name": "blur-fade",
        "component_0_animation_type": "fade",
        "component_0_config_options": '{"duration": 0.5, "delay": 0.1, "easing": "easeInOut"}',
        "component_0_code_snippet": "const BlurFade = ({ children }) => <motion.div animate={{ opacity: 1 }} initial={{ opacity: 0 }} >{children}</motion.div>;",
        "component_0_supported_properties": '["opacity", "blur", "scale"]',
        "component_1_name": "scroll-progress",
        "component_1_animation_type": "scroll",
        "component_1_config_options": '{"triggerOffset": 100, "duration": 1.0}',
        "component_1_code_snippet": "const ScrollProgress = () => <ProgressBar value={scrollYProgress} />;",
        "component_1_supported_properties": '["progress", "position", "velocity"]',
        "total_components": 2,
        "metadata_timestamp": "2024-01-15T10:30:00Z",
        "metadata_version": "1.2.0",
        "metadata_categories_scroll": True,
        "metadata_categories_fade": True,
        "metadata_categories_orbit": False
    }

def magic_ui_component_server_getMotion() -> Dict[str, Any]:
    """
    Provides implementation details for various UI motion components.
    
    Returns:
        Dict containing:
        - components (List[Dict]): List of component objects with implementation details
        - total_components (int): Number of components returned
        - metadata (Dict): Additional information about the response including timestamp, version, and available categories
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("magic-ui-component-server-getMotion", **locals())
        
        # Construct components list from indexed fields
        components: List[Dict[str, Any]] = [
            {
                "name": api_data["component_0_name"],
                "animation_type": api_data["component_0_animation_type"],
                "config_options": api_data["component_0_config_options"],
                "code_snippet": api_data["component_0_code_snippet"],
                "supported_properties": api_data["component_0_supported_properties"]
            },
            {
                "name": api_data["component_1_name"],
                "animation_type": api_data["component_1_animation_type"],
                "config_options": api_data["component_1_config_options"],
                "code_snippet": api_data["component_1_code_snippet"],
                "supported_properties": api_data["component_1_supported_properties"]
            }
        ]
        
        # Construct metadata
        metadata: Dict[str, Any] = {
            "timestamp": api_data["metadata_timestamp"],
            "version": api_data["metadata_version"],
            "available_categories": {
                "scroll": api_data["metadata_categories_scroll"],
                "fade": api_data["metadata_categories_fade"],
                "orbit": api_data["metadata_categories_orbit"]
            }
        }
        
        # Build final result
        result = {
            "components": components,
            "total_components": api_data["total_components"],
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve motion components: {str(e)}")

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
