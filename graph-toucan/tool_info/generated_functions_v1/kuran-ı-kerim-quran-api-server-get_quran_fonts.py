from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran fonts.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - font_0_name (str): Internal name of the first Quranic font
        - font_0_display_name (str): Display name of the first font
        - font_0_language (str): Language of the first font
        - font_0_script (str): Script type of the first font
        - font_0_is_default (bool): Whether the first font is default
        - font_1_name (str): Internal name of the second Quranic font
        - font_1_display_name (str): Display name of the second font
        - font_1_language (str): Language of the second font
        - font_1_script (str): Script type of the second font
        - font_1_is_default (bool): Whether the second font is default
        - total_count (int): Total number of available Quranic fonts
        - metadata_timestamp (str): Timestamp when data was retrieved
        - metadata_source (str): Source of the data
    """
    return {
        "font_0_name": "uthmanic-hafs",
        "font_0_display_name": "Uthmanic Script - Hafs",
        "font_0_language": "Arabic",
        "font_0_script": "Naskh",
        "font_0_is_default": True,
        "font_1_name": "indopak",
        "font_1_display_name": "IndoPak Script",
        "font_1_language": "Arabic",
        "font_1_script": "Nasta'liq",
        "font_1_is_default": False,
        "total_count": 2,
        "metadata_timestamp": "2023-11-15T10:30:00Z",
        "metadata_source": "Kuran-API Server v2.1"
    }

def kuran_ı_kerim_quran_api_server_get_quran_fonts() -> Dict[str, Any]:
    """
    Retrieves a list of available Quranic Arabic fonts from the API server.

    Returns:
        Dict containing:
        - fonts (List[Dict]): List of font objects with keys 'name', 'display_name',
          'language', 'script', and 'is_default'.
        - total_count (int): Total number of fonts returned.
        - metadata (Dict): Additional info including timestamp and source.

    Raises:
        Exception: If there is an error in retrieving or parsing the data.
    """
    try:
        api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_fonts")

        fonts = [
            {
                "name": api_data["font_0_name"],
                "display_name": api_data["font_0_display_name"],
                "language": api_data["font_0_language"],
                "script": api_data["font_0_script"],
                "is_default": api_data["font_0_is_default"]
            },
            {
                "name": api_data["font_1_name"],
                "display_name": api_data["font_1_display_name"],
                "language": api_data["font_1_language"],
                "script": api_data["font_1_script"],
                "is_default": api_data["font_1_is_default"]
            }
        ]

        result = {
            "fonts": fonts,
            "total_count": api_data["total_count"],
            "metadata": {
                "timestamp": api_data["metadata_timestamp"],
                "source": api_data["metadata_source"]
            }
        }

        return result

    except KeyError as e:
        raise Exception(f"Missing expected data field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve Quran fonts: {str(e)}")