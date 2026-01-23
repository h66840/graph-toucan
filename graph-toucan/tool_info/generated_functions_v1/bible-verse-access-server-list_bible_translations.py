from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bible translations.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - translation_0_identifier (str): Identifier of the first Bible translation
        - translation_0_name (str): Name of the first Bible translation
        - translation_0_language (str): Language of the first Bible translation
        - translation_0_language_code (str): Language code of the first Bible translation
        - translation_0_license (str): License of the first Bible translation
        - translation_0_url (str): URL for more info about the first translation
        - translation_1_identifier (str): Identifier of the second Bible translation
        - translation_1_name (str): Name of the second Bible translation
        - translation_1_language (str): Language of the second Bible translation
        - translation_1_language_code (str): Language code of the second Bible translation
        - translation_1_license (str): License of the second Bible translation
        - translation_1_url (str): URL for more info about the second translation
    """
    return {
        "translation_0_identifier": "KJV",
        "translation_0_name": "King James Version",
        "translation_0_language": "English",
        "translation_0_language_code": "en",
        "translation_0_license": "Public Domain",
        "translation_0_url": "https://example.com/kjv",

        "translation_1_identifier": "ESV",
        "translation_1_name": "English Standard Version",
        "translation_1_language": "English",
        "translation_1_language_code": "en",
        "translation_1_license": "All Rights Reserved",
        "translation_1_url": "https://example.com/esv"
    }


def bible_verse_access_server_list_bible_translations() -> List[Dict[str, Any]]:
    """
    Get list of all available Bible translations.

    Returns:
        List of available translations with their identifiers and names.
        Each translation contains:
        - identifier (str): Unique identifier for the translation
        - name (str): Full name of the translation
        - language (str): Language of the translation
        - language_code (str): ISO language code
        - license (str): License information
        - url (str): URL with more information

    Example:
        [
            {
                "identifier": "KJV",
                "name": "King James Version",
                "language": "English",
                "language_code": "en",
                "license": "Public Domain",
                "url": "https://example.com/kjv"
            },
            {
                "identifier": "ESV",
                "name": "English Standard Version",
                "language": "English",
                "language_code": "en",
                "license": "All Rights Reserved",
                "url": "https://example.com/esv"
            }
        ]
    """
    try:
        api_data = call_external_api("bible-verse-access-server-list_bible_translations")

        translations = [
            {
                "identifier": api_data["translation_0_identifier"],
                "name": api_data["translation_0_name"],
                "language": api_data["translation_0_language"],
                "language_code": api_data["translation_0_language_code"],
                "license": api_data["translation_0_license"],
                "url": api_data["translation_0_url"]
            },
            {
                "identifier": api_data["translation_1_identifier"],
                "name": api_data["translation_1_name"],
                "language": api_data["translation_1_language"],
                "language_code": api_data["translation_1_language_code"],
                "license": api_data["translation_1_license"],
                "url": api_data["translation_1_url"]
            }
        ]

        return translations

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve Bible translations: {e}")