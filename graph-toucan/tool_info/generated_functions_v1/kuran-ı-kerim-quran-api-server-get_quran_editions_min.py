from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran editions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - edition_0_language (str): Language of the first Quran edition
        - edition_0_name (str): Name of the first Quran edition
        - edition_0_author (str): Author of the first Quran edition
        - edition_0_identifier (str): Identifier of the first Quran edition
        - edition_1_language (str): Language of the second Quran edition
        - edition_1_name (str): Name of the second Quran edition
        - edition_1_author (str): Author of the second Quran edition
        - edition_1_identifier (str): Identifier of the second Quran edition
        - total_count (int): Total number of Quran editions returned
        - metadata_timestamp (str): Timestamp of the response
        - metadata_source (str): Source of the data
        - metadata_api_version (str): API version used
    """
    return {
        "edition_0_language": "tr",
        "edition_0_name": "Diyanet Meali",
        "edition_0_author": "Diyanet İşleri Başkanlığı",
        "edition_0_identifier": "tr.diyanet",
        "edition_1_language": "en",
        "edition_1_name": "Sahih International",
        "edition_1_author": "Sahih International",
        "edition_1_identifier": "en.sahih",
        "total_count": 2,
        "metadata_timestamp": "2023-11-15T10:00:00Z",
        "metadata_source": "Kuran-ı Kerim API Server",
        "metadata_api_version": "v1.0"
    }


def kuran_ı_kerim_quran_api_server_get_quran_editions_min() -> Dict[str, Any]:
    """
    Mevcut tüm Kuran sürümlerinin küçültülmüş versiyonunu getirir.

    Returns:
        Dict containing:
        - editions (List[Dict]): List of simplified Quran edition objects with language, name, author, and identifier
        - total_count (int): Total number of Quran editions returned
        - metadata (Dict): Additional contextual information including timestamp, source, and API version
    """
    try:
        api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_editions_min")

        # Construct editions list from flattened API response
        editions = [
            {
                "language": api_data["edition_0_language"],
                "name": api_data["edition_0_name"],
                "author": api_data["edition_0_author"],
                "identifier": api_data["edition_0_identifier"]
            },
            {
                "language": api_data["edition_1_language"],
                "name": api_data["edition_1_name"],
                "author": api_data["edition_1_author"],
                "identifier": api_data["edition_1_identifier"]
            }
        ]

        # Construct metadata
        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "source": api_data["metadata_source"],
            "api_version": api_data["metadata_api_version"]
        }

        # Build final result
        result = {
            "editions": editions,
            "total_count": api_data["total_count"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing Quran editions: {str(e)}")