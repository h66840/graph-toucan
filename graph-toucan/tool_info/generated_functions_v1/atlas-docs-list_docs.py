from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation sets.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - doc_0_name (str): Name of the first documentation set
        - doc_0_description (str): Description of the first documentation set
        - doc_0_sourceUrl (str): Source URL of the first documentation set
        - doc_1_name (str): Name of the second documentation set
        - doc_1_description (str): Description of the second documentation set
        - doc_1_sourceUrl (str): Source URL of the second documentation set
    """
    return {
        "doc_0_name": "React",
        "doc_0_description": "A JavaScript library for building user interfaces.",
        "doc_0_sourceUrl": "https://react.dev",
        "doc_1_name": "Django",
        "doc_1_description": "A high-level Python web framework that encourages rapid development and clean design.",
        "doc_1_sourceUrl": "https://docs.djangoproject.com",
    }


def atlas_docs_list_docs() -> List[Dict[str, Optional[str]]]:
    """
    Lists all available documentation libraries and frameworks.

    This function retrieves a list of documentation sets including their name,
    description, and source URL. It should be used as the first step to discover
    available documentation before using other documentation tools.

    Returns:
        List[Dict[str, Optional[str]]]: A list of documentation sets, each containing:
            - name (str): The name of the documentation set
            - description (str or None): A brief description of the documentation set
            - sourceUrl (str): The URL where the documentation is hosted
    """
    try:
        api_data = call_external_api("atlas-docs-list_docs")

        docs: List[Dict[str, Optional[str]]] = [
            {
                "name": api_data["doc_0_name"],
                "description": api_data["doc_0_description"],
                "sourceUrl": api_data["doc_0_sourceUrl"],
            },
            {
                "name": api_data["doc_1_name"],
                "description": api_data["doc_1_description"],
                "sourceUrl": api_data["doc_1_sourceUrl"],
            },
        ]

        return docs

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while listing documentation sets: {e}")