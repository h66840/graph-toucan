from typing import Dict, List, Any, Union, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Macrostrat geologic units.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_unit_id (int): unique identifier for the geologic unit
        - data_0_section_id (int): identifier for the section where this unit is defined
        - data_0_col_id (int): collection ID associated with the unit
        - data_0_project_id (int): project ID to which the unit belongs
        - data_0_col_area (float): area in square kilometers of the column representing the unit
        - data_0_unit_name (str): short name of the geologic unit
        - data_0_strat_name_id (Optional[int]): stratigraphic name identifier; null if unnamed
        - data_0_Mbr (str): member name abbreviation; empty if not applicable
        - data_0_Fm (str): formation name abbreviation; empty if not applicable
        - data_0_Gp (str): group name abbreviation; empty if not applicable
        - data_0_SGp (str): subgroup name abbreviation; empty if not applicable
        - data_0_t_age (float): top age of the unit in million years before present
        - data_0_b_age (float): bottom age of the unit in million years before present
        - data_0_max_thick (Optional[Union[float, int]]): maximum thickness of the unit in meters; 0 if not applicable
        - data_0_min_thick (Optional[Union[float, int]]): minimum thickness of the unit in meters; 0 if not applicable
        - data_0_outcrop (str): outcrop status: "surface", "subsurface", or "both"
        - data_0_pbdb_collections (int): number of Paleobiology Database collections from this unit
        - data_0_pbdb_occurrences (int): number of Paleobiology Database fossil occurrences from this unit
        - data_0_lith_0_atts_0 (str): first lithological attribute (e.g., ferruginous)
        - data_0_lith_0_name (str): name of the first lithology type (e.g., sandstone)
        - data_0_lith_0_prop (float): proportional abundance of the first lithology component (0–1)
        - data_0_lith_0_lith_id (int): unique identifier for the first lithology type
        - data_0_lith_0_type (str): broad lithology type category for the first component
        - data_0_lith_0_class (str): lithological class for the first component: sedimentary, igneous, metamorphic
        - data_0_environ_0_class (str): environment class: marine or non-marine
        - data_0_environ_0_type (str): specific environment type (e.g., fluvial)
        - data_0_environ_0_name (str): descriptive name of the environment
        - data_0_environ_0_environ_id (int): unique identifier for the environment type
        - data_0_econ_0 (str): placeholder for economic data (currently always empty)
        - data_0_measure_0_measure_class (str): class of measurement (e.g., geochemical)
        - data_0_measure_0_measure_type (str): specific type of measurement (e.g., major elements)
        - data_0_notes (str): additional notes or references for interpretation sources
        - data_0_color (str): hex color code used to represent the unit on maps
        - data_0_text_color (str): hex color code for text labels on maps
        - data_0_t_int_id (int): time interval ID for the top age
        - data_0_t_int_name (str): chronostratigraphic stage name at the top of the unit
        - data_0_t_int_age (float): age in million years of the top time interval boundary
        - data_0_t_prop (float): proportional position within the top time interval (0–1)
        - data_0_units_above_0 (int): first unit_id directly overlying this unit; 0 indicates no known unit
        - data_0_b_int_id (int): time interval ID for the bottom age
        - data_0_b_int_name (str): chronostratigraphic stage name at the base of the unit
        - data_0_b_int_age (float): age in million years of the bottom time interval boundary
        - data_0_b_prop (float): proportional position within the bottom time interval (0–1)
        - data_0_units_below_0 (int): first unit_id directly underlying this unit; 0 indicates no known unit
        - data_0_strat_name_long (Optional[str]): full formal name of the stratigraphic unit; null if unnamed
        - data_0_refs_0 (int): first reference ID corresponding to literature sources
        - data_0_clat (float): central latitude of the unit's geographic extent
        - data_0_clng (float): central longitude of the unit's geographic extent
        - data_0_t_plat (float): paleolatitude at the top age of the unit
        - data_0_t_plng (float): paleolongitude at the top age of the unit
        - data_0_b_plat (float): paleolatitude at the bottom age of the unit
        - data_0_b_plng (float): paleolongitude at the bottom age of the unit
        - refs_1 (str): full citation string for reference identified by 1
        - license (str): license under which the data is provided (e.g., CC-BY 4.0)
        - version (int): version number of the API response format
    """
    return {
        "data_0_unit_id": 12345,
        "data_0_section_id": 6789,
        "data_0_col_id": 234,
        "data_0_project_id": 12,
        "data_0_col_area": 45.6,
        "data_0_unit_name": "Unit A",
        "data_0_strat_name_id": 789,
        "data_0_Mbr": "MBR1",
        "data_0_Fm": "FM1",
        "data_0_Gp": "GP1",
        "data_0_SGp": "SGP1",
        "data_0_t_age": 150.5,
        "data_0_b_age": 160.2,
        "data_0_max_thick": 300,
        "data_0_min_thick": 150,
        "data_0_outcrop": "surface",
        "data_0_pbdb_collections": 5,
        "data_0_pbdb_occurrences": 120,
        "data_0_lith_0_atts_0": "ferruginous",
        "data_0_lith_0_name": "sandstone",
        "data_0_lith_0_prop": 0.75,
        "data_0_lith_0_lith_id": 101,
        "data_0_lith_0_type": "siliciclastic",
        "data_0_lith_0_class": "sedimentary",
        "data_0_environ_0_class": "non-marine",
        "data_0_environ_0_type": "fluvial",
        "data_0_environ_0_name": "inferred fluvial",
        "data_0_environ_0_environ_id": 201,
        "data_0_econ_0": "",
        "data_0_measure_0_measure_class": "sedimentological",
        "data_0_measure_0_measure_type": "environmental",
        "data_0_notes": "Interpreted from field observations.",
        "data_0_color": "#FFA500",
        "data_0_text_color": "#000000",
        "data_0_t_int_id": 301,
        "data_0_t_int_name": "Kimmeridgian",
        "data_0_t_int_age": 157.3,
        "data_0_t_prop": 0.65,
        "data_0_units_above_0": 12346,
        "data_0_b_int_id": 305,
        "data_0_b_int_name": "Oxfordian",
        "data_0_b_int_age": 163.5,
        "data_0_b_prop": 0.45,
        "data_0_units_below_0": 12344,
        "data_0_strat_name_long": "Kimmeridge Clay Formation",
        "data_0_refs_0": 501,
        "data_0_clat": 39.7392,
        "data_0_clng": -104.9903,
        "data_0_t_plat": 35.1,
        "data_0_t_plng": -90.2,
        "data_0_b_plat": 34.8,
        "data_0_b_plng": -89.9,
        "refs_1": "Smith, J. et al. (2020). Geologic Map of North America. GSA Special Paper 541.",
        "license": "CC-BY 4.0",
        "version": 1
    }

def macrostrat_api_server_find_units(lat: float, lng: float, responseType: str) -> Dict[str, Any]:
    """
    Query Macrostrat geologic units based on geographic coordinates and response type.
    
    This function simulates querying the Macrostrat API to retrieve detailed information
    about geologic units at a given latitude and longitude. The response includes stratigraphic,
    lithologic, environmental, and bibliographic data.
    
    Args:
        lat (float): A valid latitude in decimal degrees (between -90 and 90)
        lng (float): A valid longitude in decimal degrees (between -180 and 180)
        responseType (str): The length of response - either "long" or "short". 
                           Long provides detailed information.
    
    Returns:
        Dict containing:
        - data (List[Dict]): list of geologic units with detailed attributes including:
            - unit_id, section_id, col_id, project_id
            - unit_name, strat_name_id, member/formation/group abbreviations
            - age (t_age, b_age), thickness (max_thick, min_thick)
            - lithology breakdown with proportions and classifications
            - depositional environment interpretations
            - measurement types available
            - references, coordinates, paleocoordinates
        - refs (Dict): mapping of reference IDs to full bibliographic citations
        - license (str): data license (e.g., CC-BY 4.0)
        - version (int): API response format version
    
    Raises:
        ValueError: If latitude or longitude are out of valid range, or if responseType is invalid
    """
    # Input validation
    if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
        raise ValueError("Latitude must be a number between -90 and 90 degrees")
    
    if not isinstance(lng, (int, float)) or not (-180 <= lng <= 180):
        raise ValueError("Longitude must be a number between -180 and 180 degrees")
    
    if responseType not in ["short", "long"]:
        raise ValueError("responseType must be either 'short' or 'long'")
    
    # Call external API (simulated)
    api_data = call_external_api("macrostrat-api-server-find-units")
    
    # Construct lithology list
    lithology = [{
        "atts": [api_data["data_0_lith_0_atts_0"]],
        "name": api_data["data_0_lith_0_name"],
        "prop": api_data["data_0_lith_0_prop"],
        "lith_id": api_data["data_0_lith_0_lith_id"],
        "type": api_data["data_0_lith_0_type"],
        "class": api_data["data_0_lith_0_class"]
    }]
    
    # Construct environment list
    environment = [{
        "class": api_data["data_0_environ_0_class"],
        "type": api_data["data_0_environ_0_type"],
        "name": api_data["data_0_environ_0_name"],
        "environ_id": api_data["data_0_environ_0_environ_id"]
    }]
    
    # Construct economic resources list (currently always empty in examples)
    economic = []
    
    # Construct measurements list
    measurements = [{
        "measure_class": api_data["data_0_measure_0_measure_class"],
        "measure_type": api_data["data_0_measure_0_measure_type"]
    }]
    
    # Construct units above/below lists
    units_above = [api_data["data_0_units_above_0"]] if api_data["data_0_units_above_0"] != 0 else []
    units_below = [api_data["data_0_units_below_0"]] if api_data["data_0_units_below_0"] != 0 else []
    
    # Construct references list
    refs_list = [api_data["data_0_refs_0"]] if "data_0_refs_0" in api_data else []
    
    # Build the main data structure
    data = [{
        "unit_id": api_data["data_0_unit_id"],
        "section_id": api_data["data_0_section_id"],
        "col_id": api_data["data_0_col_id"],
        "project_id": api_data["data_0_project_id"],
        "col_area": api_data["data_0_col_area"],
        "unit_name": api_data["data_0_unit_name"],
        "strat_name_id": api_data["data_0_strat_name_id"] if api_data["data_0_strat_name_id"] is not None else None,
        "Mbr": api_data["data_0_Mbr"],
        "Fm": api_data["data_0_Fm"],
        "Gp": api_data["data_0_Gp"],
        "SGp": api_data["data_0_SGp"],
        "t_age": api_data["data_0_t_age"],
        "b_age": api_data["data_0_b_age"],
        "max_thick": api_data["data_0_max_thick"] if api_data["data_0_max_thick"] != 0 else 0,
        "min_thick": api_data["data_0_min_thick"] if api_data["data_0_min_thick"] != 0 else 0,
        "outcrop": api_data["data_0_outcrop"],
        "pbdb_collections": api_data["data_0_pbdb_collections"],
        "pbdb_occurrences": api_data["data_0_pbdb_occurrences"],
        "lith": lithology,
        "environ": environment,
        "econ": economic,
        "measure": measurements,
        "notes": api_data["data_0_notes"],
        "color": api_data["data_0_color"],
        "text_color": api_data["data_0_text_color"],
        "t_int_id": api_data["data_0_t_int_id"],
        "t_int_name": api_data["data_0_t_int_name"],
        "t_int_age": api_data["data_0_t_int_age"],
        "t_prop": api_data["data_0_t_prop"],
        "units_above": units_above,
        "b_int_id": api_data["data_0_b_int_id"],
        "b_int_name": api_data["data_0_b_int_name"],
        "b_int_age": api_data["data_0_b_int_age"],
        "b_prop": api_data["data_0_b_prop"],
        "units_below": units_below,
        "strat_name_long": api_data["data_0_strat_name_long"] if api_data["data_0_strat_name_long"] is not None else None,
        "refs": refs_list,
        "clat": api_data["data_0_clat"],
        "clng": api_data["data_0_clng"],
        "t_plat": api_data["data_0_t_plat"],
        "t_plng": api_data["data_0_t_plng"],
        "b_plat": api_data["data_0_b_plat"],
        "b_plng": api_data["data_0_b_plng"]
    }]
    
    # Build references dictionary
    refs = {}
    if "refs_1" in api_data:
        refs["1"] = api_data["refs_1"]
    
    # Return final structured response
    return {
        "data": data,
        "refs": refs,
        "license": api_data["license"],
        "version": api_data["version"]
    }