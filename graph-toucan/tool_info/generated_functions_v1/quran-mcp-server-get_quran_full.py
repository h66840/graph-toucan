from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Quran full text retrieval.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - quran_edition_name (str): Name of the Quran edition
        - quran_edition_language (str): Language code of the edition (e.g., 'en', 'tr', 'ar')
        - quran_edition_script_type (str): Script type used ('arabic', 'latin', 'latin-diacritics')
        - quran_edition_source (str): Source or publisher of the edition
        - surah_0_number (int): Chapter number of the first surah
        - surah_0_name (str): Name of the first surah
        - surah_0_english_name (str): English name of the first surah
        - surah_0_revelation_type (str): Revelation type (Meccan/Medinan)
        - surah_0_verse_count (int): Number of verses in the first surah
        - surah_0_verse_0_text (str): Text of the first verse in the first surah
        - surah_0_verse_1_text (str): Text of the second verse in the first surah
        - surah_1_number (int): Chapter number of the second surah
        - surah_1_name (str): Name of the second surah
        - surah_1_english_name (str): English name of the second surah
        - surah_1_revelation_type (str): Revelation type (Meccan/Medinan)
        - surah_1_verse_count (int): Number of verses in the second surah
        - surah_1_verse_0_text (str): Text of the first verse in the second surah
        - surah_1_verse_1_text (str): Text of the second verse in the second surah
        - total_verses (int): Total number of verses in the Quran
        - language (str): Language of the translation or original text
        - script_type (str): Script used in the output
        - metadata_timestamp (str): ISO format timestamp of data retrieval
        - metadata_version (str): Version of the edition
        - metadata_status (str): Processing status (e.g., 'success')
    """
    return {
        "quran_edition_name": "Quran English Translation by Muhiuddin Khan",
        "quran_edition_language": "en",
        "quran_edition_script_type": "latin",
        "quran_edition_source": "https://quran.com",
        "surah_0_number": 1,
        "surah_0_name": "Al-Fatiha",
        "surah_0_english_name": "The Opening",
        "surah_0_revelation_type": "Meccan",
        "surah_0_verse_count": 7,
        "surah_0_verse_0_text": "In the name of Allah, the Most Gracious, the Most Merciful.",
        "surah_0_verse_1_text": "Praise be to Allah, the Lord of all the worlds.",
        "surah_1_number": 2,
        "surah_1_name": "Al-Baqarah",
        "surah_1_english_name": "The Cow",
        "surah_1_revelation_type": "Medinan",
        "surah_1_verse_count": 286,
        "surah_1_verse_0_text": "Alif-Lam-Mim.",
        "surah_1_verse_1_text": "This is the Book; in it is guidance sure, without doubt, to those who fear Allah.",
        "total_verses": 6236,
        "language": "en",
        "script_type": "latin",
        "metadata_timestamp": "2023-10-05T12:00:00Z",
        "metadata_version": "1.0.0",
        "metadata_status": "success"
    }

def quran_mcp_server_get_quran_full(edition_name: str, script_type: Optional[str] = "") -> Dict[str, Any]:
    """
    Gets the full Quran or translation based on the specified edition and script type.

    Args:
        edition_name (str): The name of the Quran edition (e.g., "ben-muhiuddinkhan")
        script_type (str, optional): The script type to use:
            - "" = Arabic script
            - "la" = Latin script
            - "lad" = Latin script with diacritics
            Defaults to "" (Arabic).

    Returns:
        Dict containing:
        - quran_edition (Dict): Metadata about the Quran edition
        - surahs (List[Dict]): List of all chapters (surahs) with verses and metadata
        - total_verses (int): Total number of verses in the Quran
        - language (str): Language code of the edition
        - script_type (str): Script type used
        - metadata (Dict): Additional metadata including timestamp, version, and status
    """
    if not edition_name:
        raise ValueError("edition_name is required and cannot be empty")

    # Normalize script_type
    script_map = {
        "": "arabic",
        "la": "latin",
        "lad": "latin-diacritics"
    }
    normalized_script = script_map.get(script_type, "arabic")

    # Fetch simulated external data
    api_data = call_external_api("quran-mcp-server-get_quran_full")

    # Construct quran_edition
    quran_edition = {
        "name": api_data["quran_edition_name"],
        "language": api_data["quran_edition_language"],
        "script_type": api_data["quran_edition_script_type"],
        "source": api_data["quran_edition_source"]
    }

    # Construct surahs list
    surahs = [
        {
            "number": api_data["surah_0_number"],
            "name": api_data["surah_0_name"],
            "english_name": api_data["surah_0_english_name"],
            "revelation_type": api_data["surah_0_revelation_type"],
            "verse_count": api_data["surah_0_verse_count"],
            "verses": [
                {"text": api_data["surah_0_verse_0_text"]},
                {"text": api_data["surah_0_verse_1_text"]}
            ]
        },
        {
            "number": api_data["surah_1_number"],
            "name": api_data["surah_1_name"],
            "english_name": api_data["surah_1_english_name"],
            "revelation_type": api_data["surah_1_revelation_type"],
            "verse_count": api_data["surah_1_verse_count"],
            "verses": [
                {"text": api_data["surah_1_verse_0_text"]},
                {"text": api_data["surah_1_verse_1_text"]}
            ]
        }
    ]

    # Construct final result
    result = {
        "quran_edition": quran_edition,
        "surahs": surahs,
        "total_verses": api_data["total_verses"],
        "language": api_data["language"],
        "script_type": normalized_script,
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "version": api_data["metadata_version"],
            "status": api_data["metadata_status"]
        }
    }

    return result