from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran chapter retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - chapter_0_chapter (int): Chapter number for first verse
        - chapter_0_verse (int): Verse number for first verse
        - chapter_0_text (str): Text of first verse in requested script
        - chapter_1_chapter (int): Chapter number for second verse
        - chapter_1_verse (int): Verse number for second verse
        - chapter_1_text (str): Text of second verse in requested script
    """
    return {
        "chapter_0_chapter": 1,
        "chapter_0_verse": 1,
        "chapter_0_text": "Bismillah ir-Rahman ir-Rahim",
        "chapter_1_chapter": 1,
        "chapter_1_verse": 2,
        "chapter_1_text": "Alhamdu lillahi Rabbil 'alamin"
    }

def quran_mcp_server_get_quran_chapter(
    chapter_no: int,
    edition_name: str,
    minified: Optional[bool] = None,
    script_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Gets the full chapter (surah) from the Quran in the specified edition and script.
    
    Args:
        chapter_no (int): Chapter number (1-114)
        edition_name (str): Edition name
        minified (bool, optional): Whether to return minified format
        script_type (str, optional): Script type ("": normal, "la": latin, "lad": latin with diacritics)
    
    Returns:
        Dict containing a list of verses with 'chapter', 'verse', and 'text' fields.
        Structure:
        {
            "chapter": [
                {"chapter": int, "verse": int, "text": str},
                {"chapter": int, "verse": int, "text": str}
            ]
        }
    
    Raises:
        ValueError: If chapter_no is not between 1 and 114
    """
    # Input validation
    if not isinstance(chapter_no, int) or chapter_no < 1 or chapter_no > 114:
        raise ValueError("chapter_no must be an integer between 1 and 114")
    
    if not isinstance(edition_name, str) or not edition_name.strip():
        raise ValueError("edition_name must be a non-empty string")
    
    # Default values for optional parameters
    if minified is None:
        minified = False
    if script_type is None:
        script_type = ""
    
    # Validate script_type
    valid_script_types = ["", "la", "lad"]
    if script_type not in valid_script_types:
        raise ValueError(f"script_type must be one of {valid_script_types}")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("quran-mcp-server-get_quran_chapter")
    
    # Construct the chapter list from flattened API response
    chapter_verses: List[Dict[str, Any]] = [
        {
            "chapter": api_data["chapter_0_chapter"],
            "verse": api_data["chapter_0_verse"],
            "text": api_data["chapter_0_text"]
        },
        {
            "chapter": api_data["chapter_1_chapter"],
            "verse": api_data["chapter_1_verse"],
            "text": api_data["chapter_1_text"]
        }
    ]
    
    # Apply chapter_no to all verses (ensure consistency)
    for verse in chapter_verses:
        verse["chapter"] = chapter_no
    
    # Return result in expected format
    return {
        "chapter": chapter_verses
    }