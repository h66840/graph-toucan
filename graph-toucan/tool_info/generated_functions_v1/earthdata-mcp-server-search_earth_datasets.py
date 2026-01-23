from typing import Dict, List, Any, Optional
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching dataset search results from NASA Earthdata API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - dataset_0_Title (str): Title of the first dataset
        - dataset_0_ShortName (str): Short name of the first dataset
        - dataset_0_Abstract (str): Abstract/description of the first dataset
        - dataset_0_Data_Type (str): Data type of the first dataset
        - dataset_0_DOI (str): DOI of the first dataset
        - dataset_0_LandingPage (str): Landing page URL of the first dataset
        - dataset_0_DatasetViz (str): Visualization URL of the first dataset
        - dataset_0_DatasetURL (str): Data access URL of the first dataset
        - dataset_1_Title (str): Title of the second dataset
        - dataset_1_ShortName (str): Short name of the second dataset
        - dataset_1_Abstract (str): Abstract/description of the second dataset
        - dataset_1_Data_Type (str): Data type of the second dataset
        - dataset_1_DOI (str): DOI of the second dataset
        - dataset_1_LandingPage (str): Landing page URL of the second dataset
        - dataset_1_DatasetViz (str): Visualization URL of the second dataset
        - dataset_1_DatasetURL (str): Data access URL of the second dataset
    """
    return {
        "dataset_0_Title": "MODIS Terra Vegetation Indices Monthly L3 Global 1km SIN Grid",
        "dataset_0_ShortName": "MOD13A3",
        "dataset_0_Abstract": "The MODIS Vegetation Indices product is a level-3 product generated using inputs from the best available pixels over a month to provide consistent space-time composites for terrestrial applications.",
        "dataset_0_Data_Type": "SCIENCE_QUALITY",
        "dataset_0_DOI": "10.5067/MODIS/MOD13A3.061",
        "dataset_0_LandingPage": "https://doi.org/10.5067/MODIS/MOD13A3.061",
        "dataset_0_DatasetViz": "https://earthdata.nasa.gov/visualize?dataset=MOD13A3",
        "dataset_0_DatasetURL": "https://n5eil01u.ecs.nsidc.org/MODIS/MOD13A3.061/",
        
        "dataset_1_Title": "GRACE Monthly Mass Grids from JPL RL06M.1",
        "dataset_1_ShortName": "GRCTellus.LND.RL06M_1.MSCNv03",
        "dataset_1_Abstract": "These data represent terrestrial water storage variations observed by the GRACE satellite mission, processed by JPL using the mascon solution approach.",
        "dataset_1_Data_Type": "SCIENCE_QUALITY",
        "dataset_1_DOI": "10.5067/GRACE/GFZ/LND/RL06M_1",
        "dataset_1_LandingPage": "https://doi.org/10.5067/GRACE/GFZ/LND/RL06M_1",
        "dataset_1_DatasetViz": "https://earthdata.nasa.gov/visualize?dataset=GRCTellus",
        "dataset_1_DatasetURL": "https://grace.jpl.nasa.gov/data/get-data/monthly-mass-grids-land/"
    }

def earthdata_mcp_server_search_earth_datasets(
    search_keywords: str,
    count: int,
    temporal: Optional[str] = None,
    bounding_box: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Search for datasets on NASA Earthdata based on keywords, temporal range, and spatial bounding box.
    
    Args:
        search_keywords (str): Keywords to search for in the dataset titles.
        count (int): Number of datasets to return.
        temporal (Optional[str]): Temporal range in the format (date_from, date_to) as string.
        bounding_box (Optional[str]): Bounding box in the format (lower_left_lon, lower_left_lat, upper_right_lon, upper_right_lat) as string.
    
    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary containing a list of dataset objects with fields including 
        'Title', 'ShortName', 'Abstract', 'Data Type', 'DOI', 'LandingPage', 'DatasetViz', and 'DatasetURL'.
    
    Raises:
        ValueError: If count is less than 1 or search_keywords is empty.
    """
    # Input validation
    if not search_keywords or not search_keywords.strip():
        raise ValueError("search_keywords is required and cannot be empty")
    
    if count < 1:
        raise ValueError("count must be at least 1")
    
    # Call external API to get simulated data
    api_data = call_external_api("earthdata-mcp-server-search_earth_datasets")
    
    # Construct the datasets list by mapping flat API fields to nested structure
    datasets = []
    
    # Process up to 'count' datasets (maximum 2 available in simulation)
    max_available = 2
    actual_count = min(count, max_available)
    
    for i in range(actual_count):
        dataset = {
            "Title": api_data.get(f"dataset_{i}_Title", f"Simulated Dataset {i+1}"),
            "ShortName": api_data.get(f"dataset_{i}_ShortName", f"SIMULATED_{i+1}"),
            "Abstract": api_data.get(f"dataset_{i}_Abstract", f"Simulated abstract for dataset {i+1} based on keywords: {search_keywords}"),
            "Data Type": api_data.get(f"dataset_{i}_Data_Type", "SIMULATED"),
            "DOI": api_data.get(f"dataset_{i}_DOI", f"10.1234/simulated.doi.{i+1}"),
            "LandingPage": api_data.get(f"dataset_{i}_LandingPage", f"https://example.com/landing/{i+1}"),
            "DatasetViz": api_data.get(f"dataset_{i}_DatasetViz", f"https://example.com/visualize/{i+1}"),
            "DatasetURL": api_data.get(f"dataset_{i}_DatasetURL", f"https://example.com/data/{i+1}")
        }
        datasets.append(dataset)
    
    return {"datasets": datasets}