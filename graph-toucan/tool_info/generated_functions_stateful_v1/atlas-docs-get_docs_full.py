from typing import Dict, Any
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
    Simulates fetching data from external API for documentation retrieval.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): The complete consolidated documentation content as a single string
        - docName (str): Name of the documentation set that was retrieved
        - format (str): Format of the returned documentation (e.g., 'markdown', 'plaintext', 'html')
        - size (int): Total number of characters in the documentation content
        - retrieval_timestamp (str): ISO 8601 timestamp indicating when the documentation was retrieved
        - metadata_version (str): Version of the documentation set
        - metadata_source (str): Source of the documentation
        - metadata_last_updated (str): Last updated date of the documentation in ISO 8601
    """
    return {
        "content": "# Atlas Documentation\n\nThis is the full documentation for the Atlas system...\n\n## Features\n- Feature 1\n- Feature 2\n\n## API Reference\n...",
        "docName": "Atlas System Docs",
        "format": "markdown",
        "size": 12345,
        "retrieval_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_version": "1.5.2",
        "metadata_source": "internal-knowledge-base",
        "metadata_last_updated": "2023-10-05T08:45:00Z"
    }


def atlas_docs_get_docs_full(docName: str) -> Dict[str, Any]:
    """
    Retrieves the complete documentation content in a single consolidated file.

    Use this when you need comprehensive knowledge or need to analyze the full documentation context.
    Returns a large volume of text - consider using get_docs_page or search_docs for targeted information.

    Args:
        docName (str): Name of the documentation set

    Returns:
        Dict with the following keys:
        - content (str): The complete consolidated documentation content as a single string
        - docName (str): Name of the documentation set that was retrieved
        - format (str): Format of the returned documentation (e.g., 'markdown', 'plaintext', 'html')
        - size (int): Total number of characters in the documentation content
        - retrieval_timestamp (str): ISO 8601 timestamp indicating when the documentation was retrieved
        - metadata (Dict): Additional metadata about the documentation set, such as version, source, or last updated date
    """
    if not docName or not isinstance(docName, str):
        raise ValueError("docName must be a non-empty string")

    api_data = call_external_api("atlas-docs-get_docs_full", **locals())

    result = {
        "content": api_data["content"],
        "docName": docName,
        "format": api_data["format"],
        "size": api_data["size"],
        "retrieval_timestamp": api_data["retrieval_timestamp"],
        "metadata": {
            "version": api_data["metadata_version"],
            "source": api_data["metadata_source"],
            "last_updated": api_data["metadata_last_updated"]
        }
    }

    return result

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
