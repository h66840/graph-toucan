from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAI Agents SDK documentation index.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - doc_index_0_title (str): Title of the first documentation page
        - doc_index_0_url (str): URL of the first documentation page
        - doc_index_0_section (str): Section of the first documentation page
        - doc_index_1_title (str): Title of the second documentation page
        - doc_index_1_url (str): URL of the second documentation page
        - doc_index_1_section (str): Section of the second documentation page
    """
    return {
        "doc_index_0_title": "Getting Started with OpenAI Agents SDK",
        "doc_index_0_url": "https://docs.openai.com/agents/getting-started",
        "doc_index_0_section": "Introduction",
        "doc_index_1_title": "Creating Custom Agent Workflows",
        "doc_index_1_url": "https://docs.openai.com/agents/workflows",
        "doc_index_1_section": "Advanced Usage"
    }


def openai_agent_library_get_doc_index() -> List[Dict[str, str]]:
    """
    Get the index of all OpenAI Agents SDK documentation pages.

    Returns:
        List[Dict]: A list of documentation page objects, each containing:
            - title (str): The title of the documentation page
            - url (str): The URL of the documentation page
            - section (str): The section/category the page belongs to
    """
    try:
        api_data = call_external_api("openai-agent-library-get_doc_index")

        doc_index = [
            {
                "title": api_data["doc_index_0_title"],
                "url": api_data["doc_index_0_url"],
                "section": api_data["doc_index_0_section"]
            },
            {
                "title": api_data["doc_index_1_title"],
                "url": api_data["doc_index_1_url"],
                "section": api_data["doc_index_1_section"]
            }
        ]

        return doc_index

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve documentation index: {e}")