from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran maqra retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - maqra_no (int): The unique identifier of the maqra
        - edition_name (str): Name of the Quranic edition
        - script_type (str): Type of script used (normal, latin, latin with diacritics)
        - text (str): Full textual content of the maqra
        - verse_0_verse_no (int): First verse number
        - verse_0_verse_text (str): Text of the first verse
        - verse_0_surah_name (str): Surah name for first verse
        - verse_0_surah_number (int): Surah number for first verse
        - verse_0_juz (int): Juz number for first verse
        - verse_0_position_in_quran (int): Position in Quran for first verse
        - verse_1_verse_no (int): Second verse number
        - verse_1_verse_text (str): Text of the second verse
        - verse_1_surah_name (str): Surah name for second verse
        - verse_1_surah_number (int): Surah number for second verse
        - verse_1_juz (int): Juz number for second verse
        - verse_1_position_in_quran (int): Position in Quran for second verse
        - metadata_retrieved_at (str): ISO 8601 timestamp when data was fetched
        - metadata_success (bool): Whether retrieval was successful
        - metadata_error_message (str): Error message if any occurred
    """
    return {
        "maqra_no": 1,
        "edition_name": "quran-uthmani",
        "script_type": "la",
        "text": "Bismillah ir-Rahman ir-Rahim",
        "verse_0_verse_no": 1,
        "verse_0_verse_text": "Bismillah ir-Rahman ir-Rahim",
        "verse_0_surah_name": "Al-Fatiha",
        "verse_0_surah_number": 1,
        "verse_0_juz": 1,
        "verse_0_position_in_quran": 1,
        "verse_1_verse_no": 2,
        "verse_1_verse_text": "Alhamdu lillahi rabbil 'alamin",
        "verse_1_surah_name": "Al-Fatiha",
        "verse_1_surah_number": 1,
        "verse_1_juz": 1,
        "verse_1_position_in_quran": 2,
        "metadata_retrieved_at": datetime.utcnow().isoformat() + "Z",
        "metadata_success": True,
        "metadata_error_message": ""
    }

def quran_mcp_server_get_quran_maqra(
    edition_name: str, 
    maqra_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Gets the specified maqra from the Quran based on edition, maqra number, and script type.
    
    Args:
        edition_name (str): Name of the Quranic edition (e.g., 'quran-uthmani')
        maqra_no (int): The maqra number to retrieve
        script_type (str, optional): Script type for text rendering:
            "" = normal Arabic script,
            "la" = Latin transliteration,
            "lad" = Latin with diacritics
            Defaults to "" (normal).

    Returns:
        Dict[str, Any]: A dictionary containing:
            - maqra (dict): Detailed information about the requested maqra including:
                - maqra_no (int)
                - edition_name (str)
                - script_type (str)
                - text (str)
                - verses (List[Dict]): List of verse details including verse_no, verse_text,
                  surah_name, surah_number, juz, position_in_quran
            - metadata (dict): Contextual information:
                - retrieved_at (str): ISO 8601 timestamp
                - success (bool)
                - error_message (str, optional)
    
    Example:
        >>> result = quran_mcp_server_get_quran_maqra("quran-uthmani", 1, "la")
        >>> print(result["maqra"]["text"])
        "Bismillah ir-Rahman ir-Rahim"
    """
    # Input validation
    if not edition_name:
        return {
            "maqra": None,
            "metadata": {
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "success": False,
                "error_message": "Edition name is required"
            }
        }
    
    if maqra_no < 1:
        return {
            "maqra": None,
            "metadata": {
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "success": False,
                "error_message": "Maqra number must be a positive integer"
            }
        }

    # Normalize script_type
    if script_type not in ["", "la", "lad"]:
        script_type = ""

    try:
        # Call external API (simulated)
        api_data = call_external_api("quran-mcp-server-get_quran_maqra")
        
        # Construct the nested output structure
        maqra_data = {
            "maqra_no": api_data["maqra_no"],
            "edition_name": api_data["edition_name"],
            "script_type": api_data["script_type"],
            "text": api_data["text"],
            "verses": [
                {
                    "verse_no": api_data["verse_0_verse_no"],
                    "verse_text": api_data["verse_0_verse_text"],
                    "surah_name": api_data["verse_0_surah_name"],
                    "surah_number": api_data["verse_0_surah_number"],
                    "juz": api_data["verse_0_juz"],
                    "position_in_quran": api_data["verse_0_position_in_quran"]
                },
                {
                    "verse_no": api_data["verse_1_verse_no"],
                    "verse_text": api_data["verse_1_verse_text"],
                    "surah_name": api_data["verse_1_surah_name"],
                    "surah_number": api_data["verse_1_surah_number"],
                    "juz": api_data["verse_1_juz"],
                    "position_in_quran": api_data["verse_1_position_in_quran"]
                }
            ]
        }
        
        metadata = {
            "retrieved_at": api_data["metadata_retrieved_at"],
            "success": api_data["metadata_success"]
        }
        
        if not api_data["metadata_success"]:
            metadata["error_message"] = api_data["metadata_error_message"]
        
        return {
            "maqra": maqra_data,
            "metadata": metadata
        }
        
    except Exception as e:
        return {
            "maqra": None,
            "metadata": {
                "retrieved_at": datetime.utcnow().isoformat() + "Z",
                "success": False,
                "error_message": f"Failed to retrieve maqra: {str(e)}"
            }
        }