from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

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
    Simulates fetching documentation data from an external API for n8n MCP tools.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - documentation_introduction (str): Introduction section of the documentation
        - documentation_usage (str): Usage instructions
        - documentation_examples (str): Example usage code or scenarios
        - documentation_parameters (str): Description of parameters
        - topic (str): The subject of the documentation (e.g., 'search_nodes', 'overview')
        - depth (str): Level of detail ('essentials' or 'full')
        - sections_0 (str): First section name
        - sections_1 (str): Second section name
        - last_updated (str): ISO 8601 timestamp of last update
        - version (str): Version of the tool or framework
        - related_topics_0 (str): First related topic
        - related_topics_1 (str): Second related topic
        - metadata_format (str): Format of the documentation (e.g., 'markdown')
        - metadata_source_url (str): URL where source documentation is hosted
        - metadata_is_deprecated (bool): Whether the tool is deprecated
    """
    return {
        "documentation_introduction": "This guide provides an overview of the n8n MCP tools ecosystem.",
        "documentation_usage": "Call this tool with a topic to get specific documentation. Use depth='full' for detailed information.",
        "documentation_examples": "Example: {\"topic\": \"search_nodes\", \"depth\": \"essentials\"}",
        "documentation_parameters": "topic: name of the tool or 'overview'; depth: 'essentials' or 'full'",
        "topic": "overview",
        "depth": "essentials",
        "sections_0": "Introduction",
        "sections_1": "Usage",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "version": "1.5.3",
        "related_topics_0": "search_nodes",
        "related_topics_1": "execute_workflow",
        "metadata_format": "markdown",
        "metadata_source_url": "https://docs.n8n.io/mcp-tools/",
        "metadata_is_deprecated": False,
    }


def ennkaheksa_tools_documentation(
    depth: Optional[str] = "essentials", 
    topic: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get documentation for n8n MCP tools. Call without parameters for quick start guide.
    Use topic parameter to get documentation for specific tools.
    Use depth='full' for comprehensive documentation.

    Args:
        depth (Optional[str]): Level of detail. "essentials" (default) for quick reference,
                               "full" for comprehensive docs.
        topic (Optional[str]): Tool name (e.g., "search_nodes") or "overview" for general guide.
                               Leave empty for quick reference.

    Returns:
        Dict containing structured documentation with the following keys:
        - documentation (Dict): Structured content grouped by sections
        - topic (str): Subject of the returned documentation
        - depth (str): Level of detail provided
        - sections (List[str]): List of section names included
        - last_updated (str): Timestamp in ISO 8601 format
        - version (str): Version of the tool or framework
        - related_topics (List[str]): Suggested topics for further reading
        - metadata (Dict): Additional context like source, formatting, deprecation status
    """
    # Input validation
    if depth not in ["essentials", "full"]:
        raise ValueError("depth must be one of 'essentials' or 'full'")
    
    # Normalize topic
    resolved_topic = topic or "overview"
    
    # Fetch simulated external data
    api_data = call_external_api("ennkaheksa-tools_documentation", **locals())
    
    # Override with input parameters if needed (simulation)
    used_depth = depth or api_data["depth"]
    used_topic = resolved_topic
    
    # Construct nested documentation structure
    documentation_content = {}
    if "documentation_introduction" in api_data:
        documentation_content["introduction"] = api_data["documentation_introduction"]
    if "documentation_usage" in api_data:
        documentation_content["usage"] = api_data["documentation_usage"]
    if "documentation_examples" in api_data:
        documentation_content["examples"] = api_data["documentation_examples"]
    if "documentation_parameters" in api_data:
        documentation_content["parameters"] = api_data["documentation_parameters"]
    
    # Build sections list from indexed fields
    sections = []
    if "sections_0" in api_data and api_data["sections_0"]:
        sections.append(api_data["sections_0"])
    if "sections_1" in api_data and api_data["sections_1"]:
        sections.append(api_data["sections_1"])
    
    # Build related topics list
    related_topics = []
    if "related_topics_0" in api_data and api_data["related_topics_0"]:
        related_topics.append(api_data["related_topics_0"])
    if "related_topics_1" in api_data and api_data["related_topics_1"]:
        related_topics.append(api_data["related_topics_1"])
    
    # Build metadata
    metadata = {
        "format": api_data.get("metadata_format", "text"),
        "source_url": api_data.get("metadata_source_url", ""),
        "is_deprecated": api_data.get("metadata_is_deprecated", False),
    }
    
    # Assemble final result matching output schema
    result = {
        "documentation": documentation_content,
        "topic": used_topic,
        "depth": used_depth,
        "sections": sections,
        "last_updated": api_data["last_updated"],
        "version": api_data["version"],
        "related_topics": related_topics,
        "metadata": metadata,
    }
    
    return result

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
