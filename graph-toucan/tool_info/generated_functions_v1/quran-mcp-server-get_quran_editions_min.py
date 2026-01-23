from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran editions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - edition_0_identifier (str): Identifier of the first Quran edition
        - edition_0_language (str): Language of the first edition
        - edition_0_name (str): Native name of the first edition
        - edition_0_english_name (str): English name of the first edition
        - edition_0_format (str): Format of the first edition (e.g., text, audio)
        - edition_1_identifier (str): Identifier of the second Quran edition
        - edition_1_language (str): Language of the second edition
        - edition_1_name (str): Native name of the second edition
        - edition_1_english_name (str): English name of the second edition
        - edition_1_format (str): Format of the second edition (e.g., text, audio)
        - count (int): Total number of available Quran editions returned
        - retrieved_at (str): ISO format timestamp when data was retrieved
        - version (str): API version
        - source (str): Data source identifier
    """
    return {
        "edition_0_identifier": "quran-simple",
        "edition_0_language": "ar",
        "edition_0_name": "القرآن الكريم - مبسط",
        "edition_0_english_name": "Simple Arabic",
        "edition_0_format": "text",
        "edition_1_identifier": "quran-english-sahih-international",
        "edition_1_language": "en",
        "edition_1_name": "Sahih International",
        "edition_1_english_name": "Sahih International",
        "edition_1_format": "text",
        "count": 2,
        "retrieved_at": datetime.utcnow().isoformat() + "Z",
        "version": "1.0",
        "source": "quran-mcp-server"
    }


def quran_mcp_server_get_quran_editions_min() -> Dict[str, Any]:
    """
    Mevcut tüm Kuran sürümlerinin küçültülmüş versiyonunu getirir.
    Lists all available Quran editions in minified JSON format.

    Returns:
        Dict containing:
        - editions (List[Dict]): List of available Quran editions with minimal metadata.
          Each dictionary contains 'identifier', 'language', 'name', 'english_name', and 'format'.
        - count (int): Total number of available Quran editions returned.
        - metadata (Dict): Additional contextual information including 'retrieved_at', 'version', 'source'.
    """
    try:
        api_data = call_external_api("quran-mcp-server-get_quran_editions_min")

        # Construct editions list from flattened API response
        editions = [
            {
                "identifier": api_data["edition_0_identifier"],
                "language": api_data["edition_0_language"],
                "name": api_data["edition_0_name"],
                "english_name": api_data["edition_0_english_name"],
                "format": api_data["edition_0_format"]
            },
            {
                "identifier": api_data["edition_1_identifier"],
                "language": api_data["edition_1_language"],
                "name": api_data["edition_1_name"],
                "english_name": api_data["edition_1_english_name"],
                "format": api_data["edition_1_format"]
            }
        ]

        # Construct metadata
        metadata = {
            "retrieved_at": api_data["retrieved_at"],
            "version": api_data["version"],
            "source": api_data["source"]
        }

        # Final result structure
        result = {
            "editions": editions,
            "count": api_data["count"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching Quran editions: {str(e)}")