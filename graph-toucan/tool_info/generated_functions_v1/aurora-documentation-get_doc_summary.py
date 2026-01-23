from typing import Dict, List, Any
import datetime
import re


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation summary.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - file (str): Full path to the documentation file
        - name (str): Name of the documentation file without extension or path
        - size (int): Size of the file in bytes
        - last_modified (str): ISO 8601 timestamp indicating when the file was last modified
        - heading_0 (str): First markdown heading in the document
        - heading_1 (str): Second markdown heading in the document
        - first_paragraph (str): The first paragraph of the document
        - word_count (int): Total number of words in the document
    """
    return {
        "file": "/docs/user-guide.md",
        "name": "user-guide",
        "size": 2048,
        "last_modified": "2023-10-05T14:48:00Z",
        "heading_0": "# User Guide Overview",
        "heading_1": "## Getting Started",
        "first_paragraph": "This document provides a comprehensive overview of the system's user interface and core functionalities.",
        "word_count": 342
    }


def aurora_documentation_get_doc_summary(doc_path: str) -> Dict[str, Any]:
    """
    Get a summary of a specific documentation file.

    Args:
        doc_path (str): Path to the documentation file

    Returns:
        Dict containing:
        - file (str): full path to the documentation file
        - name (str): name of the documentation file without extension or path
        - size (int): size of the file in bytes
        - last_modified (str): ISO 8601 timestamp indicating when the file was last modified
        - headings (List[str]): list of all markdown headings and subheadings present in the document
        - first_paragraph (str): the first paragraph of the document; may be empty or placeholder like "---"
        - word_count (int): total number of words in the document

    Raises:
        ValueError: If doc_path is empty or invalid
        FileNotFoundError: If the file does not exist
    """
    if not doc_path:
        raise ValueError("doc_path is required")

    # In real implementation, we would read the actual file.
    # Here we simulate using external API call with mocked data.
    try:
        api_data = call_external_api("aurora-documentation-get_doc_summary")

        # Extract base name and remove extension using string operations instead of os.path
        # Handle both forward and backward slashes
        clean_path = doc_path.replace('\\', '/')
        filename = clean_path.split('/')[-1]
        if '.' in filename:
            name = filename.rsplit('.', 1)[0]
        else:
            name = filename

        # Use API data for file metadata instead of os.stat
        file_size = api_data.get("size", 0)
        last_modified = api_data.get("last_modified")

        # Construct headings list from indexed fields
        headings = []
        for i in range(2):  # We expect 2 headings as per API mock
            key = f"heading_{i}"
            if key in api_data and isinstance(api_data[key], str):
                headings.append(api_data[key])

        # Extract first paragraph
        first_paragraph = api_data.get("first_paragraph", "---")

        # Count words from first paragraph and headings for realism
        content = " ".join(headings) + " " + first_paragraph
        word_count = len(re.findall(r'\b\w+\b', content))

        result = {
            "file": doc_path,
            "name": name,
            "size": file_size,
            "last_modified": last_modified,
            "headings": headings,
            "first_paragraph": first_paragraph.strip(),
            "word_count": word_count
        }

        return result

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve documentation summary: {str(e)}")