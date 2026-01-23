from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran page retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - page_content_0_verse_number (int): Verse number of first verse
        - page_content_0_text (str): Text of first verse
        - page_content_1_verse_number (int): Verse number of second verse
        - page_content_1_text (str): Text of second verse
        - page_number (int): The requested page number returned
        - edition_metadata_name (str): Name of the Quran edition
        - edition_metadata_language (str): Language of the edition
        - edition_metadata_type (str): Type of edition (e.g., translation, transliteration)
        - edition_metadata_author (str): Author of the edition
        - script_type_used (str): Script type applied ('', 'la', 'lad')
        - total_verses_on_page (int): Total number of verses on the page
        - surah_info_0_surah_name (str): Name of first surah on page
        - surah_info_0_surah_number (int): Number of first surah
        - surah_info_0_starting_verse (int): Starting verse number in first surah
        - surah_info_0_ending_verse (int): Ending verse number in first surah
        - surah_info_1_surah_name (str): Name of second surah on page
        - surah_info_1_surah_number (int): Number of second surah
        - surah_info_1_starting_verse (int): Starting verse number in second surah
        - surah_info_1_ending_verse (int): Ending verse number in second surah
        - metadata_revelation_place (str): Revelation place (Meccan/Medinan)
        - metadata_timestamp (str): Timestamp of response
        - metadata_source_api (str): Source API identifier
    """
    return {
        "page_content_0_verse_number": 1,
        "page_content_0_text": "Bismillahirrahmanirrahim.",
        "page_content_1_verse_number": 2,
        "page_content_1_text": "Alhamdulillahi rabbil alemin.",
        "page_number": 1,
        "edition_metadata_name": "Turkish Translation by Y. N. O.",
        "edition_metadata_language": "tr",
        "edition_metadata_type": "translation",
        "edition_metadata_author": "Yusuf Nabi Öztürk",
        "script_type_used": "",
        "total_verses_on_page": 2,
        "surah_info_0_surah_name": "Al-Fatiha",
        "surah_info_0_surah_number": 1,
        "surah_info_0_starting_verse": 1,
        "surah_info_0_ending_verse": 7,
        "surah_info_1_surah_name": "Al-Baqarah",
        "surah_info_1_surah_number": 2,
        "surah_info_1_starting_verse": 1,
        "surah_info_1_ending_verse": 10,
        "metadata_revelation_place": "Meccan",
        "metadata_timestamp": "2023-10-05T12:00:00Z",
        "metadata_source_api": "quran.api.kuranikerim.com"
    }

def kuran_ı_kerim_quran_api_server_get_quran_page(
    edition_name: str,
    page_no: int,
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Retrieves the specified Quran page based on edition, page number, and script type.
    
    Args:
        edition_name (str): Name of the Quran edition (e.g., translation or transliteration version)
        page_no (int): Page number to retrieve
        script_type (Optional[str]): Script type for rendering ('' = normal, 'la' = latin, 'lad' = latin with diacritics)
    
    Returns:
        Dict containing:
        - page_content (List[Dict]): List of verses on the requested page with verse details
        - page_number (int): The page number returned
        - edition_metadata (Dict): Information about the Quran edition used
        - script_type_used (str): The script type applied to the text
        - total_verses_on_page (int): Number of verses on the page
        - surah_info (List[Dict]): List of surahs appearing on this page with relevant details
        - metadata (Dict): Additional metadata including revelation place, timestamp, and source info
    
    Raises:
        ValueError: If page_no is not a positive integer
    """
    if not isinstance(page_no, int) or page_no <= 0:
        raise ValueError("page_no must be a positive integer")
    
    if not edition_name.strip():
        raise ValueError("edition_name cannot be empty")
    
    # Normalize script_type
    script_type = script_type if script_type in ["la", "lad"] else ""
    
    # Fetch simulated external data
    api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_page")
    
    # Construct page_content list from indexed fields
    page_content = [
        {
            "verse_number": api_data["page_content_0_verse_number"],
            "text": api_data["page_content_0_text"]
        },
        {
            "verse_number": api_data["page_content_1_verse_number"],
            "text": api_data["page_content_1_text"]
        }
    ]
    
    # Construct surah_info list
    surah_info = [
        {
            "surah_name": api_data["surah_info_0_surah_name"],
            "surah_number": api_data["surah_info_0_surah_number"],
            "starting_verse": api_data["surah_info_0_starting_verse"],
            "ending_verse": api_data["surah_info_0_ending_verse"]
        },
        {
            "surah_name": api_data["surah_info_1_surah_name"],
            "surah_number": api_data["surah_info_1_surah_number"],
            "starting_verse": api_data["surah_info_1_starting_verse"],
            "ending_verse": api_data["surah_info_1_ending_verse"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "page_content": page_content,
        "page_number": api_data["page_number"],
        "edition_metadata": {
            "name": api_data["edition_metadata_name"],
            "language": api_data["edition_metadata_language"],
            "type": api_data["edition_metadata_type"],
            "author": api_data["edition_metadata_author"]
        },
        "script_type_used": api_data["script_type_used"],
        "total_verses_on_page": api_data["total_verses_on_page"],
        "surah_info": surah_info,
        "metadata": {
            "revelation_place": api_data["metadata_revelation_place"],
            "timestamp": api_data["metadata_timestamp"],
            "source_api": api_data["metadata_source_api"]
        }
    }
    
    return result