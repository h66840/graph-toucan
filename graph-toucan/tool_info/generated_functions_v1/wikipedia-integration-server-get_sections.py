from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia sections.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article
        - section_0_title (str): Title of the first section
        - section_0_level (int): Level (depth) of the first section
        - section_0_text (str): Text content of the first section
        - section_0_section_0_title (str): Title of the first subsection under section 0
        - section_0_section_0_level (int): Level of the first subsection under section 0
        - section_0_section_0_text (str): Text of the first subsection under section 0
        - section_1_title (str): Title of the second section
        - section_1_level (int): Level (depth) of the second section
        - section_1_text (str): Text content of the second section
        - section_1_section_0_title (str): Title of the first subsection under section 1
        - section_1_section_0_level (int): Level of the first subsection under section 1
        - section_1_section_0_text (str): Text of the first subsection under section 1
    """
    return {
        "title": "Python (programming language)",
        "section_0_title": "Overview",
        "section_0_level": 1,
        "section_0_text": "Python is a high-level programming language...",
        "section_0_section_0_title": "History",
        "section_0_section_0_level": 2,
        "section_0_section_0_text": "Python was created in the late 1980s...",
        "section_1_title": "Syntax and semantics",
        "section_1_level": 1,
        "section_1_text": "Python uses indentation to define code blocks...",
        "section_1_section_0_title": "Indentation",
        "section_1_section_0_level": 2,
        "section_1_section_0_text": "Python uses whitespace indentation..."
    }

def wikipedia_integration_server_get_sections(title: str) -> Dict[str, Any]:
    """
    Get the sections of a Wikipedia article.

    Args:
        title (str): The title of the Wikipedia article.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - title (str): Title of the Wikipedia article
            - sections (List[Dict]): List of section objects with keys:
                - title (str): Section title
                - level (int): Section level (1 for top-level, 2 for subsection, etc.)
                - text (str): Section text content
                - sections (List[Dict]): Nested subsections (same structure)
    """
    if not title or not title.strip():
        raise ValueError("Title must be a non-empty string.")
    
    # Call the external API to get flat data
    api_data = call_external_api("wikipedia-integration-server-get_sections")
    
    # Construct nested subsections for section 0
    subsection_0_0 = {
        "title": api_data["section_0_section_0_title"],
        "level": api_data["section_0_section_0_level"],
        "text": api_data["section_0_section_0_text"],
        "sections": []
    }
    
    # Construct nested subsections for section 1
    subsection_1_0 = {
        "title": api_data["section_1_section_0_title"],
        "level": api_data["section_1_section_0_level"],
        "text": api_data["section_1_section_0_text"],
        "sections": []
    }
    
    # Construct top-level sections
    section_0 = {
        "title": api_data["section_0_title"],
        "level": api_data["section_0_level"],
        "text": api_data["section_0_text"],
        "sections": [subsection_0_0]
    }
    
    section_1 = {
        "title": api_data["section_1_title"],
        "level": api_data["section_1_level"],
        "text": api_data["section_1_text"],
        "sections": [subsection_1_0]
    }
    
    # Construct final result
    result = {
        "title": api_data["title"],
        "sections": [section_0, section_1]
    }
    
    return result