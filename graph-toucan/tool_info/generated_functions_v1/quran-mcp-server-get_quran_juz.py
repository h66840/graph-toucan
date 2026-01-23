from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran juz retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - juz_number (int): The number of the juz returned (1-30)
        - edition_name (str): Name of the Quranic edition
        - edition_language (str): Language of the edition
        - script_type (str): Script type used ('' = Arabic, 'la' = Latin, 'lad' = Latin with diacritics)
        - metadata_start_surah (int): Surah number where the juz starts
        - metadata_start_verse (int): Verse number in the starting surah
        - metadata_end_surah (int): Surah number where the juz ends
        - metadata_end_verse (int): Verse number in the ending surah
        - metadata_total_verses (int): Total number of verses in the juz
        - metadata_revelation_place (str): Revelation place (Mecca or Medina)
        - verse_0_number (int): Verse number of the first verse
        - verse_0_text (str): Text of the first verse
        - verse_0_surah_number (int): Surah number of the first verse
        - verse_0_surah_name (str): Surah name of the first verse
        - verse_1_number (int): Verse number of the second verse
        - verse_1_text (str): Text of the second verse
        - verse_1_surah_number (int): Surah number of the second verse
        - verse_1_surah_name (str): Surah name of the second verse
    """
    return {
        "juz_number": 1,
        "edition_name": "Quran Simple",
        "edition_language": "ar",
        "script_type": "",
        "metadata_start_surah": 1,
        "metadata_start_verse": 1,
        "metadata_end_surah": 2,
        "metadata_end_verse": 141,
        "metadata_total_verses": 143,
        "metadata_revelation_place": "Mecca",
        "verse_0_number": 1,
        "verse_0_text": "Alif Lam Mim",
        "verse_0_surah_number": 1,
        "verse_0_surah_name": "Al-Fatiha",
        "verse_1_number": 2,
        "verse_1_text": "This is the Book; in it is guidance sure, without doubt, to those who fear Allah.",
        "verse_1_surah_number": 2,
        "verse_1_surah_name": "Al-Baqarah"
    }

def quran_mcp_server_get_quran_juz(
    edition_name: str, 
    juz_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Gets the specified juz from the Quran based on edition, juz number, and script type.
    
    Args:
        edition_name (str): Name of the Quranic edition (e.g., 'Quran Simple', 'Sahih International')
        juz_no (int): Juz number to retrieve (must be between 1 and 30)
        script_type (str, optional): Script type for the text ('' = Arabic, 'la' = Latin, 'lad' = Latin with diacritics)
    
    Returns:
        Dict containing:
        - juz_number (int): The number of the juz returned (1-30)
        - edition (Dict): Information about the Quranic edition used, including name and language
        - script_type (str): The script type used in the response
        - verses (List[Dict]): List of verses in the juz, each containing metadata and text
        - metadata (Dict): Additional metadata such as start/end surah and verse numbers, total verses, and revelation details
    
    Raises:
        ValueError: If juz_no is not between 1 and 30
        ValueError: If edition_name is empty
    """
    if not edition_name:
        raise ValueError("edition_name is required")
    if not (1 <= juz_no <= 30):
        raise ValueError("juz_no must be between 1 and 30")
    if script_type not in ["", "la", "lad"]:
        raise ValueError("script_type must be '', 'la', or 'lad'")

    # Call external API to get flat data
    api_data = call_external_api("quran-mcp-server-get_quran_juz")

    # Construct nested structure matching output schema
    result = {
        "juz_number": api_data["juz_number"],
        "edition": {
            "name": api_data["edition_name"],
            "language": api_data["edition_language"]
        },
        "script_type": api_data["script_type"],
        "verses": [
            {
                "number": api_data["verse_0_number"],
                "text": api_data["verse_0_text"],
                "surah": {
                    "number": api_data["verse_0_surah_number"],
                    "name": api_data["verse_0_surah_name"]
                }
            },
            {
                "number": api_data["verse_1_number"],
                "text": api_data["verse_1_text"],
                "surah": {
                    "number": api_data["verse_1_surah_number"],
                    "name": api_data["verse_1_surah_name"]
                }
            }
        ],
        "metadata": {
            "start": {
                "surah": api_data["metadata_start_surah"],
                "verse": api_data["metadata_start_verse"]
            },
            "end": {
                "surah": api_data["metadata_end_surah"],
                "verse": api_data["metadata_end_verse"]
            },
            "total_verses": api_data["metadata_total_verses"],
            "revelation_place": api_data["metadata_revelation_place"]
        }
    }

    return result