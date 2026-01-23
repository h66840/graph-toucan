from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran information.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - juz_count (int): Total number of juz in the Quran
        - sajda_count (int): Total number of sajda occurrences
        - ruku_count (int): Total number of ruku in the Quran
        - surah_count (int): Total number of surahs in the Quran
        - verse_count (int): Total number of verses in the Quran
        - word_count (int): Total number of words in the Quran
        - character_count (int): Total number of characters in the Quran
        - sajda_0_verse_key (str): Verse key of first sajda verse
        - sajda_0_verse_number (int): Verse number of first sajda verse
        - sajda_0_surah_name (str): Surah name of first sajda verse
        - sajda_0_type (str): Type of first sajda (obligatory or recommended)
        - sajda_1_verse_key (str): Verse key of second sajda verse
        - sajda_1_verse_number (int): Verse number of second sajda verse
        - sajda_1_surah_name (str): Surah name of second sajda verse
        - sajda_1_type (str): Type of second sajda (obligatory or recommended)
        - ruku_0_ruku_number (int): Ruku number of first ruku
        - ruku_0_start_verse (str): Start verse of first ruku
        - ruku_0_end_verse (str): End verse of first ruku
        - ruku_0_surah (str): Surah name of first ruku
        - ruku_1_ruku_number (int): Ruku number of second ruku
        - ruku_1_start_verse (str): Start verse of second ruku
        - ruku_1_end_verse (str): End verse of second ruku
        - ruku_1_surah (str): Surah name of second ruku
    """
    return {
        "juz_count": 30,
        "sajda_count": 14,
        "ruku_count": 540,
        "surah_count": 114,
        "verse_count": 6236,
        "word_count": 77439,
        "character_count": 323015,
        "sajda_0_verse_key": "32:15",
        "sajda_0_verse_number": 15,
        "sajda_0_surah_name": "As-Sajdah",
        "sajda_0_type": "obligatory",
        "sajda_1_verse_key": "41:38",
        "sajda_1_verse_number": 38,
        "sajda_1_surah_name": "Fussilat",
        "sajda_1_type": "obligatory",
        "ruku_0_ruku_number": 1,
        "ruku_0_start_verse": "1:1",
        "ruku_0_end_verse": "1:7",
        "ruku_0_surah": "Al-Fatiha",
        "ruku_1_ruku_number": 2,
        "ruku_1_start_verse": "2:1",
        "ruku_1_end_verse": "2:39",
        "ruku_1_surah": "Al-Baqarah"
    }

def quran_mcp_server_get_quran_info() -> Dict[str, Any]:
    """
    Gets all details about the Quran such as number of juz, sajdas, rukus, etc.

    Returns:
        Dict containing Quran metadata with the following structure:
        - juz_count (int): total number of juz (sections) in the Quran
        - sajda_verses (List[Dict]): list of verses with prostration (sajda), each containing:
            - 'verse_key' (str)
            - 'verse_number' (int)
            - 'surah_name' (str)
            - 'type' (str): obligatory or recommended
        - ruku_count (int): total number of ruku (sub-sections) in the Quran
        - surah_count (int): total number of surahs (chapters) in the Quran
        - verse_count (int): total number of verses (ayat) in the Quran
        - word_count (int): total number of words in the Quran
        - character_count (int): total number of characters in the Quran
        - sajda_count (int): total number of sajda (prostration) occurrences in the Quran
        - rukus (List[Dict]): detailed list of all rukus with:
            - 'ruku_number' (int)
            - 'start_verse' (str)
            - 'end_verse' (str)
            - 'surah' (str)
    """
    try:
        api_data = call_external_api("quran-mcp-server-get_quran_info")

        sajda_verses = [
            {
                "verse_key": api_data["sajda_0_verse_key"],
                "verse_number": api_data["sajda_0_verse_number"],
                "surah_name": api_data["sajda_0_surah_name"],
                "type": api_data["sajda_0_type"]
            },
            {
                "verse_key": api_data["sajda_1_verse_key"],
                "verse_number": api_data["sajda_1_verse_number"],
                "surah_name": api_data["sajda_1_surah_name"],
                "type": api_data["sajda_1_type"]
            }
        ]

        rukus = [
            {
                "ruku_number": api_data["ruku_0_ruku_number"],
                "start_verse": api_data["ruku_0_start_verse"],
                "end_verse": api_data["ruku_0_end_verse"],
                "surah": api_data["ruku_0_surah"]
            },
            {
                "ruku_number": api_data["ruku_1_ruku_number"],
                "start_verse": api_data["ruku_1_start_verse"],
                "end_verse": api_data["ruku_1_end_verse"],
                "surah": api_data["ruku_1_surah"]
            }
        ]

        result = {
            "juz_count": api_data["juz_count"],
            "sajda_verses": sajda_verses,
            "ruku_count": api_data["ruku_count"],
            "surah_count": api_data["surah_count"],
            "verse_count": api_data["verse_count"],
            "word_count": api_data["word_count"],
            "character_count": api_data["character_count"],
            "sajda_count": api_data["sajda_count"],
            "rukus": rukus
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve Quran information: {str(e)}")