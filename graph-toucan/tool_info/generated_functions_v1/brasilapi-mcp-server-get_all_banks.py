from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian banks.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - bank_0_code (int): First bank's code
        - bank_0_name (str): First bank's name
        - bank_0_ispb (str): First bank's ISPB
        - bank_1_code (int): Second bank's code
        - bank_1_name (str): Second bank's name
        - bank_1_ispb (str): Second bank's ISPB
        - total_count (int): Total number of banks returned
        - last_updated (str): ISO 8601 timestamp of last update
        - metadata_source (str): Data source identifier
        - metadata_api_version (str): API version used
        - metadata_data_freshness (str): Data freshness status
    """
    return {
        "bank_0_code": 1,
        "bank_0_name": "Banco do Brasil S.A.",
        "bank_0_ispb": "00000000",
        "bank_1_code": 237,
        "bank_1_name": "Banco Bradesco S.A.",
        "bank_1_ispb": "60746948",
        "total_count": 2,
        "last_updated": "2023-10-10T08:00:00Z",
        "metadata_source": "brasilapi",
        "metadata_api_version": "1.0",
        "metadata_data_freshness": "up-to-date"
    }


def brasilapi_mcp_server_get_all_banks() -> Dict[str, Any]:
    """
    Retrieve information about all banks in Brazil.

    Returns:
        Dict containing:
        - banks (List[Dict]): List of bank objects with code, name, and ISPB
        - total_count (int): Total number of banks returned
        - last_updated (str): ISO 8601 timestamp indicating when the data was last updated
        - metadata (Dict): Additional contextual information including source, API version, and data freshness

    Example:
        {
            "banks": [
                {"code": 1, "name": "Banco do Brasil S.A.", "ispb": "00000000"},
                {"code": 237, "name": "Banco Bradesco S.A.", "ispb": "60746948"}
            ],
            "total_count": 2,
            "last_updated": "2023-10-10T08:00:00Z",
            "metadata": {
                "source": "brasilapi",
                "api_version": "1.0",
                "data_freshness": "up-to-date"
            }
        }
    """
    try:
        api_data = call_external_api("brasilapi-mcp-server-get_all_banks")

        banks = [
            {
                "code": api_data["bank_0_code"],
                "name": api_data["bank_0_name"],
                "ispb": api_data["bank_0_ispb"]
            },
            {
                "code": api_data["bank_1_code"],
                "name": api_data["bank_1_name"],
                "ispb": api_data["bank_1_ispb"]
            }
        ]

        metadata = {
            "source": api_data["metadata_source"],
            "api_version": api_data["metadata_api_version"],
            "data_freshness": api_data["metadata_data_freshness"]
        }

        result = {
            "banks": banks,
            "total_count": api_data["total_count"],
            "last_updated": api_data["last_updated"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve bank data: {str(e)}") from e