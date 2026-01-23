from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching ChEMBL release data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - release_0_version (str): Version of the first ChEMBL release
        - release_0_release_date (str): Release date of the first ChEMBL release
        - release_0_compound_count (int): Number of compounds in the first release
        - release_0_assay_count (int): Number of assays in the first release
        - release_0_download_link (str): Download link for the first release
        - release_1_version (str): Version of the second ChEMBL release
        - release_1_release_date (str): Release date of the second ChEMBL release
        - release_1_compound_count (int): Number of compounds in the second release
        - release_1_assay_count (int): Number of assays in the second release
        - release_1_download_link (str): Download link for the second release
        - total_count (int): Total number of ChEMBL releases returned
        - latest_release_version (str): Version of the most recent ChEMBL release
        - latest_release_release_date (str): Release date of the most recent ChEMBL release
        - latest_release_compound_count (int): Number of compounds in the latest release
        - latest_release_assay_count (int): Number of assays in the latest release
        - latest_release_download_link (str): Download link for the latest release
    """
    return {
        "release_0_version": "30",
        "release_0_release_date": "2023-04-10",
        "release_0_compound_count": 2150000,
        "release_0_assay_count": 1750000,
        "release_0_download_link": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_30",
        "release_1_version": "29",
        "release_1_release_date": "2022-03-15",
        "release_1_compound_count": 2100000,
        "release_1_assay_count": 1700000,
        "release_1_download_link": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_29",
        "total_count": 2,
        "latest_release_version": "30",
        "latest_release_release_date": "2023-04-10",
        "latest_release_compound_count": 2150000,
        "latest_release_assay_count": 1750000,
        "latest_release_download_link": "https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_30"
    }

def chembl_server_example_chembl_release() -> Dict[str, Any]:
    """
    Get all ChEMBL release information.
    
    This function retrieves ChEMBL database release details including version history,
    release dates, data statistics, and download links by querying an external API.
    
    Returns:
        Dict containing:
        - releases (List[Dict]): List of ChEMBL release entries with version, release date,
          compound count, assay count, and download link
        - total_count (int): Total number of ChEMBL releases returned
        - latest_release (Dict): Information about the most recent ChEMBL release
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("chembl-server-example_chembl_release")
        
        # Construct releases list from indexed fields
        releases = [
            {
                "version": api_data["release_0_version"],
                "release_date": api_data["release_0_release_date"],
                "compound_count": api_data["release_0_compound_count"],
                "assay_count": api_data["release_0_assay_count"],
                "download_link": api_data["release_0_download_link"]
            },
            {
                "version": api_data["release_1_version"],
                "release_date": api_data["release_1_release_date"],
                "compound_count": api_data["release_1_compound_count"],
                "assay_count": api_data["release_1_assay_count"],
                "download_link": api_data["release_1_download_link"]
            }
        ]
        
        # Construct latest release info
        latest_release = {
            "version": api_data["latest_release_version"],
            "release_date": api_data["latest_release_release_date"],
            "compound_count": api_data["latest_release_compound_count"],
            "assay_count": api_data["latest_release_assay_count"],
            "download_link": api_data["latest_release_download_link"]
        }
        
        # Return structured response matching output schema
        return {
            "releases": releases,
            "total_count": api_data["total_count"],
            "latest_release": latest_release
        }
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve ChEMBL release information: {str(e)}")