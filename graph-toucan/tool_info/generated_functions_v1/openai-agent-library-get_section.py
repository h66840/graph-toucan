from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for getting a section from documentation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): The full text content of the requested section
        - section_title (str): The title of the section as it appears in the documentation
        - page_title (str): The title of the overall documentation page
        - metadata_author (str): Author of the section
        - metadata_last_updated (str): Last updated timestamp of the section
        - metadata_source_url (str): Source URL of the documentation
        - toc_position (int): Position of the section in the table of contents (1-based)
        - has_subsections (bool): Whether the section contains nested subsections
        - subsection_0_title (str): Title of the first immediate subsection
        - subsection_0_content (str): Content of the first immediate subsection
        - subsection_0_anchor (str): Anchor/link of the first immediate subsection
        - subsection_1_title (str): Title of the second immediate subsection
        - subsection_1_content (str): Content of the second immediate subsection
        - subsection_1_anchor (str): Anchor/link of the second immediate subsection
    """
    return {
        "content": "This is the full content of the requested section from the documentation page.",
        "section_title": "Getting Started",
        "page_title": "OpenAI Agent Library Documentation",
        "metadata_author": "OpenAI Team",
        "metadata_last_updated": "2023-10-15T14:30:00Z",
        "metadata_source_url": "https://docs.openai.com/agent-library/getting-started",
        "toc_position": 1,
        "has_subsections": True,
        "subsection_0_title": "Installation",
        "subsection_0_content": "To install the library, run pip install openai-agent.",
        "subsection_0_anchor": "installation",
        "subsection_1_title": "Quick Start",
        "subsection_1_content": "After installation, import the library and initialize the agent.",
        "subsection_1_anchor": "quick-start"
    }

def openai_agent_library_get_section(page: str, section: str) -> Dict[str, Any]:
    """
    Get a specific section from a documentation page.

    Args:
        page (str): The name or identifier of the documentation page.
        section (str): The name or identifier of the section within the page.

    Returns:
        Dict containing:
            - content (str): The full text content of the requested section
            - section_title (str): The title of the section as it appears in the documentation
            - page_title (str): The title of the overall documentation page
            - metadata (Dict): Additional info like author, last updated, source URL
            - toc_position (int): Position in the table of contents (1-based index)
            - has_subsections (bool): Whether the section has nested subsections
            - subsections (List[Dict]): List of immediate subsections with title, content, and anchor

    Raises:
        ValueError: If page or section is empty.
    """
    if not page:
        raise ValueError("Parameter 'page' is required.")
    if not section:
        raise ValueError("Parameter 'section' is required.")

    # Fetch data from simulated external API
    api_data = call_external_api("openai-agent-library-get_section")

    # Construct metadata dictionary
    metadata = {
        "author": api_data["metadata_author"],
        "last_updated": api_data["metadata_last_updated"],
        "source_url": api_data["metadata_source_url"]
    }

    # Construct subsections list
    subsections = [
        {
            "title": api_data["subsection_0_title"],
            "content": api_data["subsection_0_content"],
            "anchor": api_data["subsection_0_anchor"]
        },
        {
            "title": api_data["subsection_1_title"],
            "content": api_data["subsection_1_content"],
            "anchor": api_data["subsection_1_anchor"]
        }
    ]

    # Build final result matching output schema
    result = {
        "content": api_data["content"],
        "section_title": api_data["section_title"],
        "page_title": api_data["page_title"],
        "metadata": metadata,
        "toc_position": api_data["toc_position"],
        "has_subsections": api_data["has_subsections"],
        "subsections": subsections
    }

    return result