from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching clinical trial data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - trial_0_nct_id (str): NCT ID of first trial
        - trial_0_title (str): Title of first trial
        - trial_0_status (str): Recruitment status of first trial
        - trial_0_url (str): URL for first trial details
        - trial_0_brief_summary (str): Brief summary of first trial
        - trial_0_conditions (str): Comma-separated conditions for first trial
        - trial_0_interventions (str): Comma-separated interventions for first trial
        - trial_0_phases (str): Trial phase(s) for first trial
        - trial_0_enrollment (int): Enrollment number for first trial
        - trial_0_study_type (str): Study type of first trial
        - trial_0_study_design (str): Study design of first trial
        - trial_0_start_date (str): Start date of first trial (YYYY-MM-DD)
        - trial_0_completion_date (str): Completion date of first trial (YYYY-MM-DD)
        - trial_0_has_results (bool): Whether first trial has results published
        - trial_1_nct_id (str): NCT ID of second trial
        - trial_1_title (str): Title of second trial
        - trial_1_status (str): Recruitment status of second trial
        - trial_1_url (str): URL for second trial details
        - trial_1_brief_summary (str): Brief summary of second trial
        - trial_1_conditions (str): Comma-separated conditions for second trial
        - trial_1_interventions (str): Comma-separated interventions for second trial
        - trial_1_phases (str): Trial phase(s) for second trial
        - trial_1_enrollment (int): Enrollment number for second trial
        - trial_1_study_type (str): Study type of second trial
        - trial_1_study_design (str): Study design of second trial
        - trial_1_start_date (str): Start date of second trial (YYYY-MM-DD)
        - trial_1_completion_date (str): Completion date of second trial (YYYY-MM-DD)
        - trial_1_has_results (bool): Whether second trial has results published
    """
    return {
        "trial_0_nct_id": "NCT04567890",
        "trial_0_title": "Phase II Study of Drug X in Metastatic Breast Cancer",
        "trial_0_status": "Recruiting",
        "trial_0_url": "https://clinicaltrials.gov/study/NCT04567890",
        "trial_0_brief_summary": "This is a phase II trial evaluating the efficacy and safety of Drug X in patients with metastatic breast cancer.",
        "trial_0_conditions": "breast cancer, metastatic",
        "trial_0_interventions": "Drug X, chemotherapy",
        "trial_0_phases": "Phase 2",
        "trial_0_enrollment": 150,
        "trial_0_study_type": "Interventional",
        "trial_0_study_design": "Randomized, Open-label",
        "trial_0_start_date": "2022-03-15",
        "trial_0_completion_date": "2025-06-30",
        "trial_0_has_results": False,
        "trial_1_nct_id": "NCT01234567",
        "trial_1_title": "Phase III Trial of Pembrolizumab in Non-Small Cell Lung Cancer",
        "trial_1_status": "Active, not recruiting",
        "trial_1_url": "https://clinicaltrials.gov/study/NCT01234567",
        "trial_1_brief_summary": "A multicenter, randomized, double-blind phase III trial of pembrolizumab versus placebo in NSCLC patients.",
        "trial_1_conditions": "non-small cell lung cancer",
        "trial_1_interventions": "pembrolizumab, placebo",
        "trial_1_phases": "Phase 3",
        "trial_1_enrollment": 500,
        "trial_1_study_type": "Interventional",
        "trial_1_study_design": "Randomized, Double-blind",
        "trial_1_start_date": "2020-01-10",
        "trial_1_completion_date": "2024-12-01",
        "trial_1_has_results": True,
    }

def biomcp_trial_searcher(
    call_benefit: str,
    conditions: Optional[Any] = None,
    terms: Optional[Any] = None,
    interventions: Optional[Any] = None,
    recruiting_status: Optional[Any] = None,
    study_type: Optional[Any] = None,
    nct_ids: Optional[Any] = None,
    lat: Optional[Any] = None,
    long: Optional[Any] = None,
    distance: Optional[Any] = None,
    min_date: Optional[Any] = None,
    max_date: Optional[Any] = None,
    date_field: Optional[Any] = None,
    phase: Optional[Any] = None,
    age_group: Optional[Any] = None,
    primary_purpose: Optional[Any] = None,
    intervention_type: Optional[Any] = None,
    sponsor_type: Optional[Any] = None,
    study_design: Optional[Any] = None,
    sort: Optional[Any] = None,
    next_page_hash: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Searches for clinical trials based on specified criteria.
    
    Parameters:
        call_benefit (str): Define and summarize why this function is being called and the intended benefit
        conditions (Any, optional): Condition terms (e.g., "breast cancer") - list or comma-separated string
        terms (Any, optional): General search terms - list or comma-separated string
        interventions (Any, optional): Intervention names (e.g., "pembrolizumab") - list or comma-separated string
        recruiting_status (Any, optional): Study recruitment status (OPEN, CLOSED, ANY)
        study_type (Any, optional): Type of study
        nct_ids (Any, optional): Clinical trial NCT IDs - list or comma-separated string
        lat (Any, optional): Latitude for location search
        long (Any, optional): Longitude for location search
        distance (Any, optional): Distance from lat/long in miles
        min_date (Any, optional): Minimum date for filtering (YYYY-MM-DD)
        max_date (Any, optional): Maximum date for filtering (YYYY-MM-DD)
        date_field (Any, optional): Date field to filter on
        phase (Any, optional): Trial phase filter
        age_group (Any, optional): Age group filter
        primary_purpose (Any, optional): Primary purpose of the trial
        intervention_type (Any, optional): Type of intervention
        sponsor_type (Any, optional): Type of sponsor
        study_design (Any, optional): Study design
        sort (Any, optional): Sort order for results
        next_page_hash (Any, optional): Token to retrieve the next page of results
    
    Returns:
        Dict containing:
        - trials (List[Dict]): list of clinical trial records with fields:
            'nct_id', 'title', 'status', 'url', 'brief_summary', 'conditions',
            'interventions', 'phases', 'enrollment', 'study_type', 'study_design',
            'start_date', 'completion_date', 'has_results'
        - error (str, optional): error message if execution failed
    """
    try:
        # Validate required parameter
        if not call_benefit or not isinstance(call_benefit, str):
            return {"error": "call_benefit is required and must be a non-empty string"}
        
        # Fetch simulated external data
        api_data = call_external_api("biomcp_trial_searcher")
        
        # Construct trials list from flattened API response
        trials = [
            {
                "nct_id": api_data["trial_0_nct_id"],
                "title": api_data["trial_0_title"],
                "status": api_data["trial_0_status"],
                "url": api_data["trial_0_url"],
                "brief_summary": api_data["trial_0_brief_summary"],
                "conditions": [cond.strip() for cond in api_data["trial_0_conditions"].split(",")],
                "interventions": [interv.strip() for interv in api_data["trial_0_interventions"].split(",")],
                "phases": api_data["trial_0_phases"],
                "enrollment": api_data["trial_0_enrollment"],
                "study_type": api_data["trial_0_study_type"],
                "study_design": api_data["trial_0_study_design"],
                "start_date": api_data["trial_0_start_date"],
                "completion_date": api_data["trial_0_completion_date"],
                "has_results": api_data["trial_0_has_results"]
            },
            {
                "nct_id": api_data["trial_1_nct_id"],
                "title": api_data["trial_1_title"],
                "status": api_data["trial_1_status"],
                "url": api_data["trial_1_url"],
                "brief_summary": api_data["trial_1_brief_summary"],
                "conditions": [cond.strip() for cond in api_data["trial_1_conditions"].split(",")],
                "interventions": [interv.strip() for interv in api_data["trial_1_interventions"].split(",")],
                "phases": api_data["trial_1_phases"],
                "enrollment": api_data["trial_1_enrollment"],
                "study_type": api_data["trial_1_study_type"],
                "study_design": api_data["trial_1_study_design"],
                "start_date": api_data["trial_1_start_date"],
                "completion_date": api_data["trial_1_completion_date"],
                "has_results": api_data["trial_1_has_results"]
            }
        ]
        
        return {"trials": trials}
        
    except Exception as e:
        return {"error": str(e)}