from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran ruku retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ruku_number (int): The unique identifier of the ruku in the Quran
        - edition_name (str): Name of the Quranic edition or translation used
        - script_type (str): Script format of the text
        - revelation_place (str): The location where the ruku was revealed (Mecca/Medina)
        - total_verses (int): Number of verses in this ruku
        - start_position (str): First verse of the ruku in "chapter:verse" form
        - end_position (str): Last verse of the ruku in "chapter:verse" form
        - verse_0_key (str): Unique identifier for the first verse in "chapter.verse" format
        - verse_0_chapter_number (int): Chapter number of the first verse
        - verse_0_verse_number (int): Verse number within the chapter for the first verse
        - verse_0_text (str): Text of the first verse in requested script
        - verse_1_key (str): Unique identifier for the second verse in "chapter.verse" format
        - verse_1_chapter_number (int): Chapter number of the second verse
        - verse_1_verse_number (int): Verse number within the chapter for the second verse
        - verse_1_text (str): Text of the second verse in requested script
        - verse_0_word_0_text (str): Text of the first word in the first verse
        - verse_0_word_0_transliteration (str): Transliteration of the first word in the first verse
        - verse_0_word_0_translation (str): Translation of the first word in the first verse
        - verse_0_word_1_text (str): Text of the second word in the first verse
        - verse_0_word_1_transliteration (str): Transliteration of the second word in the first verse
        - verse_0_word_1_translation (str): Translation of the second word in the first verse
        - success (bool): Whether the request was successful
        - error_message (str): Error description if success is False
    """
    return {
        "ruku_number": 1,
        "edition_name": "en.asad",
        "script_type": "la",
        "revelation_place": "Mecca",
        "total_verses": 2,
        "start_position": "1:1",
        "end_position": "1:7",
        "verse_0_key": "1.1",
        "verse_0_chapter_number": 1,
        "verse_0_verse_number": 1,
        "verse_0_text": "Bismillah ir-Rahman ir-Rahim",
        "verse_1_key": "1.2",
        "verse_1_chapter_number": 1,
        "verse_1_verse_number": 2,
        "verse_1_text": "Alhamdu lillahi Rabbil 'alamin",
        "verse_0_word_0_text": "بِسْمِ",
        "verse_0_word_0_transliteration": "bismi",
        "verse_0_word_0_translation": "In the name of",
        "verse_0_word_1_text": "اللَّهِ",
        "verse_0_word_1_transliteration": "Allahi",
        "verse_0_word_1_translation": "God",
        "success": True,
        "error_message": ""
    }

def quran_mcp_server_get_quran_ruku(
    edition_name: str, 
    ruku_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Belirtilen rükuyu getirir.
    Gets the specified ruku.

    Args:
        edition_name (str): Sürüm adı / Edition name
        ruku_no (int): Rüku numarası / Ruku number
        script_type (str, optional): Yazı tipi ("" = normal, "la" = latin, "lad" = latin diakritikli) 
                                    / Script type ("" = normal, "la" = latin, "lad" = latin with diacritics)

    Returns:
        Dict containing:
        - ruku_data (Dict): Detailed information about the requested ruku
        - success (bool): Whether the request was processed successfully
        - error_message (str): Description of any error (only if success is False)

        ruku_data structure:
        - ruku_number (int): Unique identifier of the ruku
        - edition_name (str): Quranic edition name
        - script_type (str): Script format used
        - revelation_place (str): Revelation location (Mecca/Medina)
        - verses (List[Dict]): List of verses in the ruku
            - verse_key (str): "chapter.verse" identifier
            - chapter_number (int): Surah number
            - verse_number (int): Verse number in surah
            - text (str): Verse text
            - words (List[Dict]): Breakdown of words
                - word_text (str): Original word text
                - transliteration (str): Phonetic rendering
                - translation (str): Meaning in target language
        - metadata (Dict):
            - total_verses (int): Number of verses in ruku
            - start_position (str): First verse in "chapter:verse" format
            - end_position (str): Last verse in "chapter:verse" format
    """
    # Input validation
    if not edition_name:
        return {
            "success": False,
            "error_message": "Edition name is required"
        }
    
    if ruku_no <= 0:
        return {
            "success": False,
            "error_message": "Ruku number must be a positive integer"
        }
    
    try:
        # Call external API to get flat data
        api_data = call_external_api("quran-mcp-server-get_quran_ruku")
        
        # Check if external call was successful
        if not api_data.get("success", False):
            return {
                "success": False,
                "error_message": api_data.get("error_message", "Unknown error occurred")
            }
        
        # Construct words list for first verse
        words_0 = [
            {
                "word_text": api_data["verse_0_word_0_text"],
                "transliteration": api_data["verse_0_word_0_transliteration"],
                "translation": api_data["verse_0_word_0_translation"]
            },
            {
                "word_text": api_data["verse_0_word_1_text"],
                "transliteration": api_data["verse_0_word_1_transliteration"],
                "translation": api_data["verse_0_word_1_translation"]
            }
        ]
        
        # Construct verses list
        verses = [
            {
                "verse_key": api_data["verse_0_key"],
                "chapter_number": api_data["verse_0_chapter_number"],
                "verse_number": api_data["verse_0_verse_number"],
                "text": api_data["verse_0_text"],
                "words": words_0
            },
            {
                "verse_key": api_data["verse_1_key"],
                "chapter_number": api_data["verse_1_chapter_number"],
                "verse_number": api_data["verse_1_verse_number"],
                "text": api_data["verse_1_text"]
                # Words not included for second verse to reflect optional nature
            }
        ]
        
        # Construct metadata
        metadata = {
            "total_verses": api_data["total_verses"],
            "start_position": api_data["start_position"],
            "end_position": api_data["end_position"]
        }
        
        # Construct final ruku_data
        ruku_data = {
            "ruku_number": api_data["ruku_number"],
            "edition_name": api_data["edition_name"],
            "script_type": api_data["script_type"],
            "revelation_place": api_data["revelation_place"],
            "verses": verses,
            "metadata": metadata
        }
        
        return {
            "ruku_data": ruku_data,
            "success": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}"
        }