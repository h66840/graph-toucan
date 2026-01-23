from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran verse retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - chapter (int): The chapter number (1-114) of the Quran
        - verse (int): The verse number within the chapter
        - text (str): The textual content of the Quranic verse in requested script
    """
    return {
        "chapter": 1,
        "verse": 1,
        "text": "Bismillah al-rahman al-rahim. This is a sample Quranic verse in Latin script."
    }

def quran_mcp_server_get_quran_verse(
    chapter_no: int,
    edition_name: str,
    verse_no: int,
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Gets the specified Quranic verse based on chapter, verse, edition, and script type.
    
    Args:
        chapter_no (int): Chapter number (1-114) of the Quran
        edition_name (str): Name of the Quran edition/version
        verse_no (int): Verse number within the specified chapter
        script_type (str, optional): Script type for output ("", "la", "lad"). Defaults to "" (normal).
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - chapter (int): The chapter number (1-114)
            - verse (int): The verse number
            - text (str): The verse text in the requested script and edition
    
    Raises:
        ValueError: If chapter_no is not between 1 and 114
        ValueError: If verse_no is less than 1
    """
    # Input validation
    if not (1 <= chapter_no <= 114):
        raise ValueError("chapter_no must be between 1 and 114")
    if verse_no < 1:
        raise ValueError("verse_no must be a positive integer")
    if not edition_name.strip():
        raise ValueError("edition_name cannot be empty")

    # Call external API to get the verse data
    api_data = call_external_api("quran-mcp-server-get_quran_verse")

    # Construct the result matching the output schema
    result = {
        "chapter": api_data["chapter"],
        "verse": api_data["verse"],
        "text": api_data["text"]
    }

    return result