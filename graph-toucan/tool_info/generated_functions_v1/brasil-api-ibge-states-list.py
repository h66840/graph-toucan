from typing import Dict, List, Any
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian states list.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - state_0_id (int): ID of the first state
        - state_0_sigla (str): Abbreviation of the first state
        - state_0_nome (str): Full name of the first state
        - state_1_id (int): ID of the second state
        - state_1_sigla (str): Abbreviation of the second state
        - state_1_nome (str): Full name of the second state
        - count (int): Total number of states (always 27)
        - source (str): Data source name or URL
        - updated_at (str): ISO 8601 timestamp of last update
        - metadata_api_version (str): API version used
        - metadata_license (str): License information
    """
    return {
        "state_0_id": 11,
        "state_0_sigla": "RO",
        "state_0_nome": "Rondônia",
        "state_1_id": 12,
        "state_1_sigla": "AC",
        "state_1_nome": "Acre",
        "count": 27,
        "source": "https://servicodados.ibge.gov.br/",
        "updated_at": "2023-10-10T00:00:00Z",
        "metadata_api_version": "1.0",
        "metadata_license": "Creative Commons Attribution 4.0 International"
    }


def brasil_api_ibge_states_list() -> Dict[str, Any]:
    """
    Fetches and returns a list of all Brazilian states with their information.

    Returns:
        Dict containing:
        - states (List[Dict]): List of dictionaries with state data including 'id', 'sigla', and 'nome'
        - count (int): Total number of states (27)
        - source (str): Origin of the data
        - updated_at (str): ISO 8601 timestamp when data was last updated
        - metadata (Dict): Additional metadata such as API version and license

    The function simulates an API call to retrieve Brazilian states data from IBGE via Brasil API,
    then constructs the proper nested structure from flat scalar values returned by the simulated API.
    """
    try:
        api_data = call_external_api("brasil-api-ibge-states-list")

        # Construct states list from indexed fields
        states = [
            {
                "id": api_data["state_0_id"],
                "sigla": api_data["state_0_sigla"],
                "nome": api_data["state_0_nome"]
            },
            {
                "id": api_data["state_1_id"],
                "sigla": api_data["state_1_sigla"],
                "nome": api_data["state_1_nome"]
            }
        ]

        # Construct metadata dictionary
        metadata = {
            "api_version": api_data["metadata_api_version"],
            "license": api_data["metadata_license"]
        }

        # Build final result structure
        result = {
            "states": states,
            "count": api_data["count"],
            "source": api_data["source"],
            "updated_at": api_data["updated_at"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process Brazilian states data: {str(e)}") from e