from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Macrostrat stratigraphic columns.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success_v (int): API version number indicating the response format version
        - success_license (str): license type for the data (e.g., "CC-BY 4.0")
        - success_data_0_col_id (int): unique identifier for the stratigraphic column
        - success_data_0_col_name (str): name of the stratigraphic column
        - success_data_0_col_group (str): geological group to which the column belongs
        - success_data_0_col_group_id (int): identifier for the geological group
        - success_data_0_group_col_id (str): group-specific column identifier
        - success_data_0_lat (str): latitude of the column in decimal degrees
        - success_data_0_lng (str): longitude of the column in decimal degrees
        - success_data_0_col_area (float): area of the column in square kilometers
        - success_data_0_project_id (int): associated project identifier
        - success_data_0_col_type (str): type of column (e.g., "column")
        - success_data_0_refs_0 (int): first reference identifier linked to this column
        - success_data_0_max_thick (int): maximum thickness of the column in meters
        - success_data_0_max_min_thick (int): maximum of minimum estimated thickness
        - success_data_0_min_min_thick (int): minimum of minimum estimated thickness
        - success_data_0_b_age (float): bottom age in millions of years before present
        - success_data_0_t_age (float): top age in millions of years before present
        - success_data_0_b_int_name (str): name of the geologic time interval at the base
        - success_data_0_t_int_name (str): name of the geologic time interval at the top
        - success_data_0_pbdb_collections (int): number of Paleobiology Database collections
        - success_data_0_lith_0_name (str): name of the lithology type
        - success_data_0_lith_0_type (str): broader lithologic type
        - success_data_0_lith_0_class (str): main class of rock
        - success_data_0_lith_0_prop (float): proportion of this lithology in the column
        - success_data_0_lith_0_lith_id (int): unique identifier for the lithology type
        - success_data_0_environ_0_name (str): name of the environment
        - success_data_0_environ_0_type (str): subtype of environment
        - success_data_0_environ_0_class (str): broad environmental class
        - success_data_0_environ_0_prop (float): proportion of this environment interpretation
        - success_data_0_environ_0_environ_id (int): unique identifier for the environment type
        - success_data_0_econ_0_name (str): name of the economic resource
        - success_data_0_econ_0_type (str): type of resource
        - success_data_0_econ_0_class (str): resource category
        - success_data_0_econ_0_prop (float): proportion or significance of the resource
        - success_data_0_econ_0_econ_id (int): unique identifier for the economic resource
        - success_data_0_t_units (int): total number of time units in the column
        - success_data_0_t_sections (int): total number of stratigraphic sections
        - success_refs_0 (str): bibliographic citation for reference ID 0
    """
    return {
        "success_v": 2,
        "success_license": "CC-BY 4.0",
        "success_data_0_col_id": 12345,
        "success_data_0_col_name": "Grand Canyon Stratigraphic Column",
        "success_data_0_col_group": "Colorado Plateau",
        "success_data_0_col_group_id": 678,
        "success_data_0_group_col_id": "GC-001",
        "success_data_0_lat": "36.1069",
        "success_data_0_lng": "-112.1126",
        "success_data_0_col_area": 49.2,
        "success_data_0_project_id": 99,
        "success_data_0_col_type": "column",
        "success_data_0_refs_0": 1001,
        "success_data_0_max_thick": 1800,
        "success_data_0_max_min_thick": 1500,
        "success_data_0_min_min_thick": 1200,
        "success_data_0_b_age": 1000.0,
        "success_data_0_t_age": 250.0,
        "success_data_0_b_int_name": "Mesoproterozoic",
        "success_data_0_t_int_name": "Pennsylvanian",
        "success_data_0_pbdb_collections": 45,
        "success_data_0_lith_0_name": "sandstone",
        "success_data_0_lith_0_type": "siliciclastic",
        "success_data_0_lith_0_class": "sedimentary",
        "success_data_0_lith_0_prop": 0.45,
        "success_data_0_lith_0_lith_id": 23,
        "success_data_0_environ_0_name": "marine",
        "success_data_0_environ_0_type": "",
        "success_data_0_environ_0_class": "marine",
        "success_data_0_environ_0_prop": 0.6,
        "success_data_0_environ_0_environ_id": 7,
        "success_data_0_econ_0_name": "uranium",
        "success_data_0_econ_0_type": "uranium",
        "success_data_0_econ_0_class": "mineral",
        "success_data_0_econ_0_prop": 0.1,
        "success_data_0_econ_0_econ_id": 5,
        "success_data_0_t_units": 12,
        "success_data_0_t_sections": 8,
        "success_refs_0": "Smith et al., 2020, Journal of Geology"
    }

def macrostrat_api_server_find_columns(lat: float, lng: float, responseType: str, adjacents: Optional[bool] = None) -> Dict[str, Any]:
    """
    Query Macrostrat stratigraphic columns based on geographic coordinates and response type.
    
    Args:
        lat (float): A valid latitude in decimal degrees (required)
        lng (float): A valid longitude in decimal degrees (required)
        responseType (str): The length of response, either "long" or "short" (required)
        adjacents (Optional[bool]): Include adjacent columns if True
        
    Returns:
        Dict containing:
        - success (Dict): contains version, license, data, and references from the response
            - v (int): API version number
            - license (str): license type for the data
            - data (List[Dict]): list of stratigraphic columns with detailed geological properties
                - col_id (int): unique identifier for the stratigraphic column
                - col_name (str): name of the column
                - col_group (str): geological group
                - col_group_id (int): identifier for the geological group
                - group_col_id (str): group-specific column identifier
                - lat (str): latitude in decimal degrees
                - lng (str): longitude in decimal degrees
                - col_area (float): area in square kilometers
                - project_id (int): associated project identifier
                - col_type (str): type of column
                - refs (List[int]): list of reference identifiers
                - max_thick (int): maximum thickness in meters
                - max_min_thick (int): maximum of minimum estimated thickness
                - min_min_thick (int): minimum of minimum estimated thickness
                - b_age (float): bottom age in millions of years
                - t_age (float): top age in millions of years
                - b_int_name (str): geologic time interval at base
                - t_int_name (str): geologic time interval at top
                - pbdb_collections (int): number of PBDB collections
                - lith (List[Dict]): list of lithology components
                    - name (str): lithology type name
                    - type (str): broader lithologic type
                    - class (str): main rock class
                    - prop (float): proportion in column
                    - lith_id (int): unique identifier
                - environ (List[Dict]): list of paleoenvironmental interpretations
                    - name (str): environment name
                    - type (str): environment subtype
                    - class (str): broad environmental class
                    - prop (float): proportion
                    - environ_id (int): unique identifier
                - econ (List[Dict]): list of economic resources
                    - name (str): resource name
                    - type (str): resource type
                    - class (str): resource category
                    - prop (float): proportion/significance
                    - econ_id (int): unique identifier
                - t_units (int): total number of time units
                - t_sections (int): total number of stratigraphic sections
            - refs (Dict): mapping of reference IDs to full bibliographic citations
    
    Raises:
        ValueError: If latitude or longitude are not within valid ranges, or if responseType is invalid
    """
    # Input validation
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= lng <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    if responseType not in ["long", "short"]:
        raise ValueError("responseType must be either 'long' or 'short'")
    
    # Call external API (simulated)
    api_data = call_external_api("macrostrat-api-server-find-columns")
    
    # Construct the nested data structure for the single column
    column_data = {
        "col_id": api_data["success_data_0_col_id"],
        "col_name": api_data["success_data_0_col_name"],
        "col_group": api_data["success_data_0_col_group"],
        "col_group_id": api_data["success_data_0_col_group_id"],
        "group_col_id": api_data["success_data_0_group_col_id"],
        "lat": api_data["success_data_0_lat"],
        "lng": api_data["success_data_0_lng"],
        "col_area": api_data["success_data_0_col_area"],
        "project_id": api_data["success_data_0_project_id"],
        "col_type": api_data["success_data_0_col_type"],
        "refs": [api_data["success_data_0_refs_0"]],
        "max_thick": api_data["success_data_0_max_thick"],
        "max_min_thick": api_data["success_data_0_max_min_thick"],
        "min_min_thick": api_data["success_data_0_min_min_thick"],
        "b_age": api_data["success_data_0_b_age"],
        "t_age": api_data["success_data_0_t_age"],
        "b_int_name": api_data["success_data_0_b_int_name"],
        "t_int_name": api_data["success_data_0_t_int_name"],
        "pbdb_collections": api_data["success_data_0_pbdb_collections"],
        "lith": [
            {
                "name": api_data["success_data_0_lith_0_name"],
                "type": api_data["success_data_0_lith_0_type"],
                "class": api_data["success_data_0_lith_0_class"],
                "prop": api_data["success_data_0_lith_0_prop"],
                "lith_id": api_data["success_data_0_lith_0_lith_id"]
            }
        ],
        "environ": [
            {
                "name": api_data["success_data_0_environ_0_name"],
                "type": api_data["success_data_0_environ_0_type"],
                "class": api_data["success_data_0_environ_0_class"],
                "prop": api_data["success_data_0_environ_0_prop"],
                "environ_id": api_data["success_data_0_environ_0_environ_id"]
            }
        ],
        "econ": [
            {
                "name": api_data["success_data_0_econ_0_name"],
                "type": api_data["success_data_0_econ_0_type"],
                "class": api_data["success_data_0_econ_0_class"],
                "prop": api_data["success_data_0_econ_0_prop"],
                "econ_id": api_data["success_data_0_econ_0_econ_id"]
            }
        ],
        "t_units": api_data["success_data_0_t_units"],
        "t_sections": api_data["success_data_0_t_sections"]
    }
    
    # Construct references dictionary
    references = {
        api_data["success_data_0_refs_0"]: api_data["success_refs_0"]
    }
    
    # Build the final success object
    success_result = {
        "v": api_data["success_v"],
        "license": api_data["success_license"],
        "data": [column_data],
        "refs": references
    }
    
    return {"success": success_result}