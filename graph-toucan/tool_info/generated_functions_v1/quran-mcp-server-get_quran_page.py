from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran page retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page_number (int): The page number of the Quran as per the specified edition
        - edition_name (str): Name of the Quran edition returned
        - script_type (str): Script type used in the response ('' = Arabic, 'la' = Latin, 'lad' = Latin with diacritics)
        - verses_0_verse_key (str): Verse key for first verse (e.g., '1:1')
        - verses_0_text (str): Text of the first verse
        - verses_0_surah_number (int): Surah number of the first verse
        - verses_0_surah_name (str): Surah name of the first verse
        - verses_1_verse_key (str): Verse key for second verse
        - verses_1_text (str): Text of the second verse
        - verses_1_surah_number (int): Surah number of the second verse
        - verses_1_surah_name (str): Surah name of the second verse
        - surahs_covered_0_number (int): Surah number for first surah covered
        - surahs_covered_0_name_arabic (str): Arabic name of first surah
        - surahs_covered_0_name_english (str): English name of first surah
        - surahs_covered_0_revelation_place (str): Revelation place of first surah
        - surahs_covered_1_number (int): Surah number for second surah covered
        - surahs_covered_1_name_arabic (str): Arabic name of second surah
        - surahs_covered_1_name_english (str): English name of second surah
        - surahs_covered_1_revelation_place (str): Revelation place of second surah
        - page_image_url (str): URL to an image of the Quran page in Arabic script
        - metadata_edition_language (str): Language of the edition
        - metadata_text_direction (str): Text direction ('rtl' or 'ltr')
        - metadata_total_pages_in_edition (int): Total pages in the edition
        - metadata_timestamp (str): Timestamp of retrieval in ISO format
    """
    return {
        "page_number": 1,
        "edition_name": "quran-simple",
        "script_type": "",
        "verses_0_verse_key": "1:1",
        "verses_0_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verses_0_surah_number": 1,
        "verses_0_surah_name": "Al-Fatiha",
        "verses_1_verse_key": "1:2",
        "verses_1_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "verses_1_surah_number": 1,
        "verses_1_surah_name": "Al-Fatiha",
        "surahs_covered_0_number": 1,
        "surahs_covered_0_name_arabic": "الفاتحة",
        "surahs_covered_0_name_english": "Al-Fatiha",
        "surahs_covered_0_revelation_place": "Mecca",
        "surahs_covered_1_number": 2,
        "surahs_covered_1_name_arabic": "البقرة",
        "surahs_covered_1_name_english": "Al-Baqarah",
        "surahs_covered_1_revelation_place": "Medina",
        "page_image_url": "https://example.com/quran/page1.png",
        "metadata_edition_language": "ar",
        "metadata_text_direction": "rtl",
        "metadata_total_pages_in_edition": 604,
        "metadata_timestamp": "2023-10-05T12:00:00Z"
    }

def quran_mcp_server_get_quran_page(
    edition_name: str, 
    page_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Gets the specified page of the Quran based on edition, page number, and script type.
    
    Args:
        edition_name (str): Name of the Quran edition (e.g., 'quran-simple', 'quran-uthmani')
        page_no (int): Page number to retrieve (1-based indexing)
        script_type (str, optional): Script type for text rendering:
            - "" = Arabic script (default)
            - "la" = Latin transliteration
            - "lad" = Latin with diacritics
    
    Returns:
        Dict containing:
        - page_number (int): The page number of the Quran as per the specified edition
        - edition_name (str): Name of the Quran edition returned
        - script_type (str): Script type used in the response
        - verses (List[Dict]): List of verses on the page with keys:
            - verse_key (str): Unique identifier (e.g., '1:1')
            - text (str): Verse text in requested script
            - surah (Dict, optional): Surah info with number and name
        - surahs_covered (List[Dict]): List of Surahs appearing on this page with:
            - number (int)
            - name_arabic (str)
            - name_english (str)
            - revelation_place (str)
        - page_image_url (str): URL to original Arabic script page image
        - metadata (Dict): Additional info including:
            - edition_language (str)
            - text_direction (str): 'rtl' or 'ltr'
            - total_pages_in_edition (int)
            - timestamp (str): ISO format timestamp
    
    Raises:
        ValueError: If page_no is less than 1 or edition_name is empty
    """
    if not edition_name:
        raise ValueError("edition_name is required")
    if page_no < 1:
        raise ValueError("page_no must be a positive integer")
    
    # Normalize script_type
    if script_type not in ["", "la", "lad"]:
        script_type = ""
    
    # Call external API (simulated)
    api_data = call_external_api("quran-mcp-server-get_quran_page")
    
    # Construct verses list
    verses = [
        {
            "verse_key": api_data["verses_0_verse_key"],
            "text": api_data["verses_0_text"],
            "surah": {
                "number": api_data["verses_0_surah_number"],
                "name": api_data["verses_0_surah_name"]
            }
        },
        {
            "verse_key": api_data["verses_1_verse_key"],
            "text": api_data["verses_1_text"],
            "surah": {
                "number": api_data["verses_1_surah_number"],
                "name": api_data["verses_1_surah_name"]
            }
        }
    ]
    
    # Construct surahs_covered list
    surahs_covered = [
        {
            "number": api_data["surahs_covered_0_number"],
            "name_arabic": api_data["surahs_covered_0_name_arabic"],
            "name_english": api_data["surahs_covered_0_name_english"],
            "revelation_place": api_data["surahs_covered_0_revelation_place"]
        },
        {
            "number": api_data["surahs_covered_1_number"],
            "name_arabic": api_data["surahs_covered_1_name_arabic"],
            "name_english": api_data["surahs_covered_1_name_english"],
            "revelation_place": api_data["surahs_covered_1_revelation_place"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "edition_language": api_data["metadata_edition_language"],
        "text_direction": api_data["metadata_text_direction"],
        "total_pages_in_edition": api_data["metadata_total_pages_in_edition"],
        "timestamp": api_data["metadata_timestamp"]
    }
    
    # Build final result
    result = {
        "page_number": api_data["page_number"],
        "edition_name": api_data["edition_name"],
        "script_type": api_data["script_type"],
        "verses": verses,
        "surahs_covered": surahs_covered,
        "page_image_url": api_data["page_image_url"],
        "metadata": metadata
    }
    
    return result