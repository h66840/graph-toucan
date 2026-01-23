from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for clinical trial locations.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - nct_id (str): The NCT ID for which location data was retrieved
        - study_title (str): Brief title of the clinical trial
        - status (str): Status of the API call ('success' or 'error')
        - error_message (str): Description of error if retrieval failed
        - fetched_at (str): ISO 8601 timestamp when data was retrieved
        - location_0_facility_name (str): Name of first facility
        - location_0_city (str): City of first facility
        - location_0_state (str): State of first facility
        - location_0_country (str): Country of first facility
        - location_0_zip_code (str): ZIP code of first facility (optional)
        - location_0_contact_0_role (str): Role of first contact at first facility
        - location_0_contact_0_name (str): Name of first contact at first facility
        - location_0_contact_0_email (str): Email of first contact at first facility
        - location_0_contact_0_phone (str): Phone of first contact at first facility
        - location_0_contact_1_role (str): Role of second contact at first facility
        - location_0_contact_1_name (str): Name of second contact at first facility
        - location_0_contact_1_email (str): Email of second contact at first facility
        - location_0_contact_1_phone (str): Phone of second contact at first facility
        - location_1_facility_name (str): Name of second facility
        - location_1_city (str): City of second facility
        - location_1_state (str): State of second facility
        - location_1_country (str): Country of second facility
        - location_1_zip_code (str): ZIP code of second facility (optional)
        - location_1_contact_0_role (str): Role of first contact at second facility
        - location_1_contact_0_name (str): Name of first contact at second facility
        - location_1_contact_0_email (str): Email of first contact at second facility
        - location_1_contact_0_phone (str): Phone of first contact at second facility
        - location_1_contact_1_role (str): Role of second contact at second facility
        - location_1_contact_1_name (str): Name of second contact at second facility
        - location_1_contact_1_email (str): Email of second contact at second facility
        - location_1_contact_1_phone (str): Phone of second contact at second facility
    """
    return {
        "nct_id": "NCT04280705",
        "study_title": "A Study of Drug X in Patients With Condition Y",
        "status": "success",
        "error_message": "",
        "fetched_at": datetime.now().isoformat(),
        "location_0_facility_name": "Massachusetts General Hospital",
        "location_0_city": "Boston",
        "location_0_state": "MA",
        "location_0_country": "United States",
        "location_0_zip_code": "02114",
        "location_0_contact_0_role": "Principal Investigator",
        "location_0_contact_0_name": "Dr. John Smith",
        "location_0_contact_0_email": "jsmith@mgh.harvard.edu",
        "location_0_contact_0_phone": "+1-617-726-2200",
        "location_0_contact_1_role": "Study Coordinator",
        "location_0_contact_1_name": "Jane Doe",
        "location_0_contact_1_email": "jane.doe@mgh.harvard.edu",
        "location_0_contact_1_phone": "+1-617-726-5555",
        "location_1_facility_name": "Brigham and Women's Hospital",
        "location_1_city": "Boston",
        "location_1_state": "MA",
        "location_1_country": "United States",
        "location_1_zip_code": "02115",
        "location_1_contact_0_role": "Principal Investigator",
        "location_1_contact_0_name": "Dr. Robert Johnson",
        "location_1_contact_0_email": "rjohnson@bwh.harvard.edu",
        "location_1_contact_0_phone": "+1-617-732-5500",
        "location_1_contact_1_role": "Study Coordinator",
        "location_1_contact_1_name": "Alice Brown",
        "location_1_contact_1_email": "alice.brown@bwh.harvard.edu",
        "location_1_contact_1_phone": "+1-617-732-6666",
    }

def biomcp_trial_locations(call_benefit: str, nct_id: str) -> Dict[str, Any]:
    """
    Retrieves contact and location details for a single clinical trial identified by its NCT ID.
    
    This function simulates fetching the ContactsLocationsModule from the ClinicalTrials.gov v2 API
    for a given NCT ID and returns structured location and contact information in Markdown format.
    
    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        nct_id (str): A single NCT ID (e.g., "NCT04280705")
    
    Returns:
        Dict containing:
        - locations (List[Dict]): List of facility locations with contact and address details
        - nct_id (str): The NCT ID for which location data was retrieved
        - study_title (str): Brief title of the clinical trial
        - status (str): Status of the API call ('success' or 'error')
        - error_message (str): Description of error if retrieval failed
        - fetched_at (str): ISO 8601 timestamp indicating when the data was retrieved
    """
    # Input validation
    if not nct_id or not isinstance(nct_id, str) or not nct_id.upper().startswith("NCT"):
        return {
            "locations": [],
            "nct_id": nct_id,
            "study_title": "",
            "status": "error",
            "error_message": "Invalid NCT ID provided. Must be a valid NCT identifier (e.g., NCT04280705).",
            "fetched_at": datetime.now().isoformat()
        }
    
    try:
        # Call external API simulation
        api_data = call_external_api("biomcp_trial_locations")
        
        # Construct locations list from flattened API data
        locations = []
        
        # Process first location
        if api_data.get("location_0_facility_name"):
            location_0_contacts = []
            if api_data.get("location_0_contact_0_name"):
                location_0_contacts.append({
                    "role": api_data["location_0_contact_0_role"],
                    "name": api_data["location_0_contact_0_name"],
                    "email": api_data["location_0_contact_0_email"],
                    "phone": api_data["location_0_contact_0_phone"]
                })
            if api_data.get("location_0_contact_1_name"):
                location_0_contacts.append({
                    "role": api_data["location_0_contact_1_role"],
                    "name": api_data["location_0_contact_1_name"],
                    "email": api_data["location_0_contact_1_email"],
                    "phone": api_data["location_0_contact_1_phone"]
                })
            
            locations.append({
                "facility_name": api_data["location_0_facility_name"],
                "city": api_data["location_0_city"],
                "state": api_data["location_0_state"],
                "country": api_data["location_0_country"],
                "zip_code": api_data.get("location_0_zip_code"),
                "contacts": location_0_contacts
            })
        
        # Process second location
        if api_data.get("location_1_facility_name"):
            location_1_contacts = []
            if api_data.get("location_1_contact_0_name"):
                location_1_contacts.append({
                    "role": api_data["location_1_contact_0_role"],
                    "name": api_data["location_1_contact_0_name"],
                    "email": api_data["location_1_contact_0_email"],
                    "phone": api_data["location_1_contact_0_phone"]
                })
            if api_data.get("location_1_contact_1_name"):
                location_1_contacts.append({
                    "role": api_data["location_1_contact_1_role"],
                    "name": api_data["location_1_contact_1_name"],
                    "email": api_data["location_1_contact_1_email"],
                    "phone": api_data["location_1_contact_1_phone"]
                })
            
            locations.append({
                "facility_name": api_data["location_1_facility_name"],
                "city": api_data["location_1_city"],
                "state": api_data["location_1_state"],
                "country": api_data["location_1_country"],
                "zip_code": api_data.get("location_1_zip_code"),
                "contacts": location_1_contacts
            })
        
        return {
            "locations": locations,
            "nct_id": api_data["nct_id"],
            "study_title": api_data["study_title"],
            "status": api_data["status"],
            "error_message": api_data["error_message"],
            "fetched_at": api_data["fetched_at"]
        }
        
    except Exception as e:
        return {
            "locations": [],
            "nct_id": nct_id,
            "study_title": "",
            "status": "error",
            "error_message": f"Failed to retrieve trial locations: {str(e)}",
            "fetched_at": datetime.now().isoformat()
        }