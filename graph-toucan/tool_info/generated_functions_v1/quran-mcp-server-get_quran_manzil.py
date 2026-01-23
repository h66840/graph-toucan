from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran manzil retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - manzil_number (int): The number of the manzil returned (1-7)
        - edition_name (str): Name of the Quran edition used
        - edition_language (str): Language of the Quran edition
        - script_type (str): The script type applied to the text ('' = Arabic, 'la' = Latin, 'lad' = Latin with diacritics)
        - verse_0_surah_number (int): Chapter number of the first verse
        - verse_0_verse_number (int): Verse number of the first verse
        - verse_0_text (str): Text of the first verse
        - verse_1_surah_number (int): Chapter number of the second verse
        - verse_1_verse_number (int): Verse number of the second verse
        - verse_1_text (str): Text of the second verse
        - start_surah_name (str): Name of the surah where this manzil begins
        - end_surah_name (str): Name of the surah where this manzil ends
        - verse_count (int): Total number of verses in this manzil
        - metadata_revelation_order (str): Revelation order of the chapters in this manzil
        - metadata_geographical_context (str): Geographical context (Meccan/Medinan) of the chapters
        - metadata_thematic_notes (str): Thematic notes about the manzil
    """
    return {
        "manzil_number": 1,
        "edition_name": "Quran Simple",
        "edition_language": "ar",
        "script_type": "",
        "verse_0_surah_number": 1,
        "verse_0_verse_number": 1,
        "verse_0_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_1_surah_number": 1,
        "verse_1_verse_number": 2,
        "verse_1_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "start_surah_name": "Al-Fatiha",
        "end_surah_name": "An-Nisa",
        "verse_count": 450,
        "metadata_revelation_order": "Mixed",
        "metadata_geographical_context": "Meccan and Medinan",
        "metadata_thematic_notes": "Covers foundational beliefs and early legal rulings"
    }

def quran_mcp_server_get_quran_manzil(
    edition_name: str, 
    manzil_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Gets the specified manzil (one-seventh portion) of the Quran based on edition and script type.
    
    Args:
        edition_name (str): Name of the Quran edition to use
        manzil_no (int): Manzil number to retrieve (must be between 1 and 7)
        script_type (str, optional): Script type for the text ('' = Arabic, 'la' = Latin, 'lad' = Latin with diacritics)
    
    Returns:
        Dict containing:
            - manzil_number (int): The number of the manzil returned (1-7)
            - edition (Dict): Information about the Quran edition used, including name and language
            - script_type (str): The script type applied to the text
            - verses (List[Dict]): List of verses in the manzil with surah number, verse number, and text
            - start_surah_name (str): Name of the surah where this manzil begins
            - end_surah_name (str): Name of the surah where this manzil ends
            - verse_count (int): Total number of verses in this manzil
            - metadata (Dict): Additional metadata such as revelation order, geographical context, and thematic notes
    
    Raises:
        ValueError: If manzil_no is not between 1 and 7
        ValueError: If edition_name is empty
    """
    if not edition_name:
        raise ValueError("edition_name is required")
    if not (1 <= manzil_no <= 7):
        raise ValueError("manzil_no must be between 1 and 7")

    # Normalize script_type
    if script_type not in ["", "la", "lad"]:
        script_type = ""
    
    # Call external API to get data (simulated)
    api_data = call_external_api("quran-mcp-server-get_quran_manzil")
    
    # Construct the nested output structure from flat API data
    result = {
        "manzil_number": manzil_no,
        "edition": {
            "name": edition_name,
            "language": api_data["edition_language"]
        },
        "script_type": script_type,
        "verses": [
            {
                "surah_number": api_data["verse_0_surah_number"],
                "verse_number": api_data["verse_0_verse_number"],
                "text": api_data["verse_0_text"]
            },
            {
                "surah_number": api_data["verse_1_surah_number"],
                "verse_number": api_data["verse_1_verse_number"],
                "text": api_data["verse_1_text"]
            }
        ],
        "start_surah_name": api_data["start_surah_name"],
        "end_surah_name": api_data["end_surah_name"],
        "verse_count": api_data["verse_count"],
        "metadata": {
            "revelation_order": api_data["metadata_revelation_order"],
            "geographical_context": api_data["metadata_geographical_context"],
            "thematic_notes": api_data["metadata_thematic_notes"]
        }
    }
    
    return result