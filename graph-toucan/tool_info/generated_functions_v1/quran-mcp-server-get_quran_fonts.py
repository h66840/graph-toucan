from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran fonts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - font_0_name (str): Name of the first available Arabic Quranic font
        - font_0_language (str): Language of the first font
        - font_0_script (str): Script type of the first font
        - font_0_is_quranic (bool): Whether the first font is specifically for Quranic text
        - font_0_file_format (str): File format of the first font
        - font_0_supported_features_0 (str): First supported feature of the first font
        - font_0_supported_features_1 (str): Second supported feature of the first font
        - font_1_name (str): Name of the second available Arabic Quranic font
        - font_1_language (str): Language of the second font
        - font_1_script (str): Script type of the second font
        - font_1_is_quranic (bool): Whether the second font is specifically for Quranic text
        - font_1_file_format (str): File format of the second font
        - font_1_supported_features_0 (str): First supported feature of the second font
        - font_1_supported_features_1 (str): Second supported feature of the second font
        - total_count (int): Total number of available Arabic fonts returned
        - metadata_retrieval_time_utc (str): UTC timestamp when data was retrieved
        - metadata_source (str): Source of the font data
        - metadata_note (str): Additional note about context or limitations
    """
    return {
        "font_0_name": "Uthmanic Hafs",
        "font_0_language": "Arabic",
        "font_0_script": "Arabic",
        "font_0_is_quranic": True,
        "font_0_file_format": "TTF",
        "font_0_supported_features_0": "Tajweed Rules",
        "font_0_supported_features_1": "Harakat",
        "font_1_name": "Amiri Quran",
        "font_1_language": "Arabic",
        "font_1_script": "Arabic",
        "font_1_is_quranic": True,
        "font_1_file_format": "OTF",
        "font_1_supported_features_0": "Tajweed Rules",
        "font_1_supported_features_1": "I'jaz Marks",
        "total_count": 2,
        "metadata_retrieval_time_utc": "2023-11-15T10:30:00Z",
        "metadata_source": "Quranic Typography Archive",
        "metadata_note": "Only includes fonts verified for Quranic script accuracy."
    }

def quran_mcp_server_get_quran_fonts() -> Dict[str, Any]:
    """
    Lists available Arabic Quranic fonts with detailed metadata.

    Returns:
        Dict containing:
        - fonts (List[Dict]): List of font objects with keys 'name', 'language', 'script',
          'is_quranic', 'file_format', and 'supported_features'.
        - total_count (int): Total number of fonts returned.
        - metadata (Dict): Additional info including 'retrieval_time_utc', 'source', and 'note'.
    """
    try:
        api_data = call_external_api("quran-mcp-server-get_quran_fonts")

        # Construct fonts list
        fonts = [
            {
                "name": api_data["font_0_name"],
                "language": api_data["font_0_language"],
                "script": api_data["font_0_script"],
                "is_quranic": api_data["font_0_is_quranic"],
                "file_format": api_data["font_0_file_format"],
                "supported_features": [
                    api_data["font_0_supported_features_0"],
                    api_data["font_0_supported_features_1"]
                ]
            },
            {
                "name": api_data["font_1_name"],
                "language": api_data["font_1_language"],
                "script": api_data["font_1_script"],
                "is_quranic": api_data["font_1_is_quranic"],
                "file_format": api_data["font_1_file_format"],
                "supported_features": [
                    api_data["font_1_supported_features_0"],
                    api_data["font_1_supported_features_1"]
                ]
            }
        ]

        # Construct metadata
        metadata = {
            "retrieval_time_utc": api_data["metadata_retrieval_time_utc"],
            "source": api_data["metadata_source"],
            "note": api_data["metadata_note"]
        }

        # Final result
        result = {
            "fonts": fonts,
            "total_count": api_data["total_count"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred while retrieving Quran fonts: {str(e)}") from e