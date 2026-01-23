from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - quran_verses_0_surah_number (int): Surah number of first verse
        - quran_verses_0_verse_number (int): Verse number of first verse
        - quran_verses_0_verse_text (str): Text of first verse
        - quran_verses_0_edition_name (str): Edition name of first verse
        - quran_verses_1_surah_number (int): Surah number of second verse
        - quran_verses_1_verse_number (int): Verse number of second verse
        - quran_verses_1_verse_text (str): Text of second verse
        - quran_verses_1_edition_name (str): Edition name of second verse
        - metadata_edition_name (str): Name of the Quran edition
        - metadata_language (str): Language of the edition
        - metadata_script_type (str): Script type (normal, la, lad)
        - metadata_total_surahs (int): Total number of surahs
        - metadata_total_verses (int): Total number of verses
        - metadata_revelation_period_meccan (int): Number of Meccan surahs
        - metadata_revelation_period_medinan (int): Number of Medinan surahs
        - success (bool): Whether the request was successful
        - error_message (str): Error message if any, otherwise empty string
    """
    return {
        "quran_verses_0_surah_number": 1,
        "quran_verses_0_verse_number": 1,
        "quran_verses_0_verse_text": "Bismillahirrahmanirrahim. Alif Lam Mim.",
        "quran_verses_0_edition_name": "ben-muhiuddinkhan",
        "quran_verses_1_surah_number": 1,
        "quran_verses_1_verse_number": 2,
        "quran_verses_1_verse_text": "Dhalika alkitabu la rayba feehi hudan lilmuttaqin.",
        "quran_verses_1_edition_name": "ben-muhiuddinkhan",
        "metadata_edition_name": "ben-muhiuddinkhan",
        "metadata_language": "tr",
        "metadata_script_type": "la",
        "metadata_total_surahs": 114,
        "metadata_total_verses": 6236,
        "metadata_revelation_period_meccan": 86,
        "metadata_revelation_period_medinan": 28,
        "success": True,
        "error_message": ""
    }

def kuran_ı_kerim_quran_api_server_get_quran_full(edition_name: str, script_type: Optional[str] = "") -> Dict[str, Any]:
    """
    Tüm Kuran'ı/Kuran tercümesini getirir.
    
    Args:
        edition_name (str): Sürüm adı (örn: "ben-muhiuddinkhan")
        script_type (str, optional): Yazı tipi ("" = normal, "la" = latin, "lad" = latin diakritikli)
    
    Returns:
        Dict containing:
        - quran_verses (List[Dict]): List of dictionaries, each representing a verse with keys like 
          'surah_number', 'verse_number', 'verse_text', and 'edition_name'.
        - metadata (Dict): Information about the retrieved Quran edition, including 'edition_name', 
          'language', 'script_type', 'total_surahs', 'total_verses', and 'revelation_period'.
        - success (bool): Indicates whether the request was successful.
        - error_message (str): Error details if the request failed; null otherwise.
    """
    # Input validation
    if not edition_name:
        return {
            "quran_verses": [],
            "metadata": {},
            "success": False,
            "error_message": "edition_name is required"
        }

    try:
        # Call external API simulation
        api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_full")
        
        # Construct quran_verses list from indexed fields
        quran_verses = [
            {
                "surah_number": api_data["quran_verses_0_surah_number"],
                "verse_number": api_data["quran_verses_0_verse_number"],
                "verse_text": api_data["quran_verses_0_verse_text"],
                "edition_name": api_data["quran_verses_0_edition_name"]
            },
            {
                "surah_number": api_data["quran_verses_1_surah_number"],
                "verse_number": api_data["quran_verses_1_verse_number"],
                "verse_text": api_data["quran_verses_1_verse_text"],
                "edition_name": api_data["quran_verses_1_edition_name"]
            }
        ]
        
        # Construct metadata dictionary
        metadata = {
            "edition_name": api_data["metadata_edition_name"],
            "language": api_data["metadata_language"],
            "script_type": api_data["metadata_script_type"],
            "total_surahs": api_data["metadata_total_surahs"],
            "total_verses": api_data["metadata_total_verses"],
            "revelation_period": {
                "meccan": api_data["metadata_revelation_period_meccan"],
                "medinan": api_data["metadata_revelation_period_medinan"]
            }
        }
        
        # Return final structured response
        return {
            "quran_verses": quran_verses,
            "metadata": metadata,
            "success": api_data["success"],
            "error_message": api_data["error_message"] if api_data["error_message"] else None
        }
        
    except Exception as e:
        return {
            "quran_verses": [],
            "metadata": {},
            "success": False,
            "error_message": str(e)
        }