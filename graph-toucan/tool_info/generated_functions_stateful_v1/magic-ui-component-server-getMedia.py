from typing import Dict, List, Any
from datetime import datetime

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
    Simulates fetching data from external API for UI component details.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - components_0_type (str): Type of the first UI component
        - components_0_description (str): Description of the first component
        - components_0_code_examples_react (str): React code example for the first component
        - components_0_code_examples_html (str): HTML code example for the first component
        - components_0_assets_0 (str): First asset URL for the first component
        - components_0_assets_1 (str): Second asset URL for the first component
        - components_0_props_theme (str): Theme prop for the first component
        - components_0_props_autoplay (bool): Autoplay setting for the first component
        - components_0_dependencies_0 (str): First dependency for the first component
        - components_0_dependencies_1 (str): Second dependency for the first component
        - components_1_type (str): Type of the second UI component
        - components_1_description (str): Description of the second component
        - components_1_code_examples_react (str): React code example for the second component
        - components_1_code_examples_html (str): HTML code example for the second component
        - components_1_assets_0 (str): First asset URL for the second component
        - components_1_assets_1 (str): Second asset URL for the second component
        - components_1_props_theme (str): Theme prop for the second component
        - components_1_props_autoplay (bool): Autoplay setting for the second component
        - components_1_dependencies_0 (str): First dependency for the second component
        - components_1_dependencies_1 (str): Second dependency for the second component
        - supported_types_0 (str): First supported component type
        - supported_types_1 (str): Second supported component type
        - documentation_url (str): URL to the full documentation
        - version (str): Version identifier for the component set
        - timestamp (str): ISO 8601 timestamp of response generation
    """
    return {
        "components_0_type": "hero-video-dialog",
        "components_0_description": "A fullscreen video dialog with hero styling and smooth entrance animations.",
        "components_0_code_examples_react": "<HeroVideoDialog src=\"/videos/hero.mp4\" autoplay={true} />",
        "components_0_code_examples_html": "<div class=\"hero-video-dialog\" data-src=\"/videos/hero.mp4\" data-autoplay=\"true\"></div>",
        "components_0_assets_0": "https://cdn.example.com/videos/hero.mp4",
        "components_0_assets_1": "https://cdn.example.com/thumbnails/hero.jpg",
        "components_0_props_theme": "dark",
        "components_0_props_autoplay": True,
        "components_0_dependencies_0": "react@18.2.0",
        "components_0_dependencies_1": "video.js@7.21.0",

        "components_1_type": "terminal",
        "components_1_description": "A simulated terminal interface for displaying command-line interactions.",
        "components_1_code_examples_react": "<Terminal commands={commands} theme=\"monokai\" />",
        "components_1_code_examples_html": "<div class=\"terminal\" data-theme=\"monokai\" data-commands=\"echo 'Hello'\">$ echo 'Hello'</div>",
        "components_1_assets_0": "https://cdn.example.com/scripts/terminal.js",
        "components_1_assets_1": "https://cdn.example.com/styles/terminal.css",
        "components_1_props_theme": "monokai",
        "components_1_props_autoplay": False,
        "components_1_dependencies_0": "xterm@5.1.0",
        "components_1_dependencies_1": "prismjs@1.28.0",

        "supported_types_0": "hero-video-dialog",
        "supported_types_1": "terminal",
        "documentation_url": "https://docs.magicui.dev/components",
        "version": "1.5.3",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def magic_ui_component_server_getMedia() -> Dict[str, Any]:
    """
    Fetches implementation details for various UI components including hero-video-dialog, terminal, marquee, script-copy-btn, and code-comparison.

    Returns:
        Dict containing:
        - components (List[Dict]): List of UI component objects with type, description, code examples, assets, props, and dependencies
        - supported_types (List[str]): List of supported component types
        - documentation_url (str): URL to full documentation
        - version (str): Version of the component set
        - timestamp (str): ISO 8601 timestamp when response was generated

    Each component dict includes:
        - type (str): Component name
        - description (str): Purpose and use case
        - code_examples (Dict): Language-keyed code snippets
        - assets (List[str]): URLs to media files
        - props (Dict): Customizable configuration options
        - dependencies (List[str]): Required libraries
    """
    try:
        api_data = call_external_api("magic-ui-component-server-getMedia", **locals())

        # Construct components list
        components = [
            {
                "type": api_data["components_0_type"],
                "description": api_data["components_0_description"],
                "code_examples": {
                    "react": api_data["components_0_code_examples_react"],
                    "html": api_data["components_0_code_examples_html"]
                },
                "assets": [
                    api_data["components_0_assets_0"],
                    api_data["components_0_assets_1"]
                ],
                "props": {
                    "theme": api_data["components_0_props_theme"],
                    "autoplay": api_data["components_0_props_autoplay"]
                },
                "dependencies": [
                    api_data["components_0_dependencies_0"],
                    api_data["components_0_dependencies_1"]
                ]
            },
            {
                "type": api_data["components_1_type"],
                "description": api_data["components_1_description"],
                "code_examples": {
                    "react": api_data["components_1_code_examples_react"],
                    "html": api_data["components_1_code_examples_html"]
                },
                "assets": [
                    api_data["components_1_assets_0"],
                    api_data["components_1_assets_1"]
                ],
                "props": {
                    "theme": api_data["components_1_props_theme"],
                    "autoplay": api_data["components_1_props_autoplay"]
                },
                "dependencies": [
                    api_data["components_1_dependencies_0"],
                    api_data["components_1_dependencies_1"]
                ]
            }
        ]

        # Construct supported types
        supported_types = [
            api_data["supported_types_0"],
            api_data["supported_types_1"]
        ]

        # Final result
        result = {
            "components": components,
            "supported_types": supported_types,
            "documentation_url": api_data["documentation_url"],
            "version": api_data["version"],
            "timestamp": api_data["timestamp"]
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process UI component data: {str(e)}") from e

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
