from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Met Museum departments.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - department_0_id (int): ID of the first department
        - department_0_display_name (str): Display name of the first department
        - department_1_id (int): ID of the second department
        - department_1_display_name (str): Display name of the second department
    """
    return {
        "department_0_id": 1,
        "department_0_display_name": "American Decorative Arts",
        "department_1_id": 2,
        "department_1_display_name": "Ancient Near Eastern Art"
    }

def met_museum_server_list_departments() -> Dict[str, Any]:
    """
    List all departments in the Metropolitan Museum of Art (Met Museum).
    
    This function retrieves department data by calling an external API simulation
    and constructs the proper nested structure as defined in the output schema.
    
    Returns:
        Dict containing a single key 'departments' with a list of department objects.
        Each department object is a dictionary with 'id' (int) and 'display_name' (str).
    """
    try:
        api_data = call_external_api("met-museum-server-list-departments")
        
        departments: List[Dict[str, Any]] = [
            {
                "id": api_data["department_0_id"],
                "display_name": api_data["department_0_display_name"]
            },
            {
                "id": api_data["department_1_id"],
                "display_name": api_data["department_1_display_name"]
            }
        ]
        
        return {
            "departments": departments
        }
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing department data: {e}")