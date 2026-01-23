from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for clinical trial outcomes.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - outcomes_primary_outcomes_0_title (str): Title of first primary outcome
        - outcomes_primary_outcomes_0_description (str): Description of first primary outcome
        - outcomes_primary_outcomes_0_time_frame (str): Time frame for first primary outcome
        - outcomes_primary_outcomes_0_measure (str): Measure used in first primary outcome
        - outcomes_primary_outcomes_0_value (str): Result value for first primary outcome
        - outcomes_primary_outcomes_1_title (str): Title of second primary outcome
        - outcomes_primary_outcomes_1_description (str): Description of second primary outcome
        - outcomes_primary_outcomes_1_time_frame (str): Time frame for second primary outcome
        - outcomes_primary_outcomes_1_measure (str): Measure used in second primary outcome
        - outcomes_primary_outcomes_1_value (str): Result value for second primary outcome
        - outcomes_secondary_outcomes_0_title (str): Title of first secondary outcome
        - outcomes_secondary_outcomes_0_description (str): Description of first secondary outcome
        - outcomes_secondary_outcomes_0_time_frame (str): Time frame for first secondary outcome
        - outcomes_secondary_outcomes_0_measure (str): Measure used in first secondary outcome
        - outcomes_secondary_outcomes_0_value (str): Result value for first secondary outcome
        - outcomes_secondary_outcomes_1_title (str): Title of second secondary outcome
        - outcomes_secondary_outcomes_1_description (str): Description of second secondary outcome
        - outcomes_secondary_outcomes_1_time_frame (str): Time frame for second secondary outcome
        - outcomes_secondary_outcomes_1_measure (str): Measure used in second secondary outcome
        - outcomes_secondary_outcomes_1_value (str): Result value for second secondary outcome
        - results_available (bool): Whether numerical results are posted
        - participant_flow_0_group_name (str): Name of first group/arm
        - participant_flow_0_enrolled_count (int): Number enrolled in first group
        - participant_flow_0_completed_count (int): Number completed in first group
        - participant_flow_0_withdrawn_count (int): Number withdrawn in first group
        - participant_flow_1_group_name (str): Name of second group/arm
        - participant_flow_1_enrolled_count (int): Number enrolled in second group
        - participant_flow_1_completed_count (int): Number completed in second group
        - participant_flow_1_withdrawn_count (int): Number withdrawn in second group
        - adverse_events_total_with_events (int): Total participants with adverse events
        - adverse_events_serious_adverse_events (int): Number of serious adverse events
        - adverse_events_event_listings_0_event_term (str): Term for first adverse event
        - adverse_events_event_listings_0_system_org_class (str): Organ class for first event
        - adverse_events_event_listings_0_frequency (int): Frequency of first event
        - adverse_events_event_listings_0_severity (str): Severity level of first event
        - adverse_events_event_listings_1_event_term (str): Term for second adverse event
        - adverse_events_event_listings_1_system_org_class (str): Organ class for second event
        - adverse_events_event_listings_1_frequency (int): Frequency of second event
        - adverse_events_event_listings_1_severity (str): Severity level of second event
        - has_serious_adverse_events (bool): Whether any serious adverse events occurred
        - results_url (str): URL to full results on ClinicalTrials.gov
        - status (str): Status of retrieval ('success', 'no_results_found', 'invalid_nct_id')
        - error_message (str): Error description if applicable
    """
    return {
        "outcomes_primary_outcomes_0_title": "Change in Pain Intensity",
        "outcomes_primary_outcomes_0_description": "Assessed using a visual analog scale (VAS) from 0 to 10.",
        "outcomes_primary_outcomes_0_time_frame": "Week 12",
        "outcomes_primary_outcomes_0_measure": "Mean change from baseline in VAS score",
        "outcomes_primary_outcomes_0_value": "Mean difference: -2.3 (95% CI: -3.1 to -1.5)",
        "outcomes_primary_outcomes_1_title": "Physical Function Improvement",
        "outcomes_primary_outcomes_1_description": "Measured by the 6-minute walk test.",
        "outcomes_primary_outcomes_1_time_frame": "Week 24",
        "outcomes_primary_outcomes_1_measure": "Change in distance walked",
        "outcomes_primary_outcomes_1_value": "Mean increase: 45 meters",
        "outcomes_secondary_outcomes_0_title": "Quality of Life Score",
        "outcomes_secondary_outcomes_0_description": "Evaluated using SF-36 survey.",
        "outcomes_secondary_outcomes_0_time_frame": "Week 12",
        "outcomes_secondary_outcomes_0_measure": "Change in SF-36 physical component score",
        "outcomes_secondary_outcomes_0_value": "Mean change: +8.2 points",
        "outcomes_secondary_outcomes_1_title": "Patient Global Impression of Change",
        "outcomes_secondary_outcomes_1_description": "Subjective assessment of improvement.",
        "outcomes_secondary_outcomes_1_time_frame": "Week 24",
        "outcomes_secondary_outcomes_1_measure": "Proportion reporting 'much improved' or 'very much improved'",
        "outcomes_secondary_outcomes_1_value": "67% of participants",
        "results_available": True,
        "participant_flow_0_group_name": "Treatment Group A",
        "participant_flow_0_enrolled_count": 150,
        "participant_flow_0_completed_count": 138,
        "participant_flow_0_withdrawn_count": 12,
        "participant_flow_1_group_name": "Placebo Group B",
        "participant_flow_1_enrolled_count": 152,
        "participant_flow_1_completed_count": 140,
        "participant_flow_1_withdrawn_count": 12,
        "adverse_events_total_with_events": 45,
        "adverse_events_serious_adverse_events": 6,
        "adverse_events_event_listings_0_event_term": "Nausea",
        "adverse_events_event_listings_0_system_org_class": "Gastrointestinal Disorders",
        "adverse_events_event_listings_0_frequency": 23,
        "adverse_events_event_listings_0_severity": "Mild",
        "adverse_events_event_listings_1_event_term": "Headache",
        "adverse_events_event_listings_1_system_org_class": "Nervous System Disorders",
        "adverse_events_event_listings_1_frequency": 18,
        "adverse_events_event_listings_1_severity": "Moderate",
        "has_serious_adverse_events": True,
        "results_url": "https://clinicaltrials.gov/study/NCT04280705/results",
        "status": "success",
        "error_message": ""
    }

def biomcp_trial_outcomes(call_benefit: str, nct_id: str) -> Dict[str, Any]:
    """
    Retrieves outcome measures, results (if available), and adverse event data for a single clinical trial.

    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        nct_id (str): A single NCT ID (e.g., "NCT04280705").

    Returns:
        Dict containing:
        - outcomes (Dict): Contains 'primary_outcomes' and 'secondary_outcomes' lists with outcome details.
        - results_available (bool): Whether actual numerical results are posted.
        - participant_flow (List[Dict]): Participant progression through the trial by group.
        - adverse_events (Dict): Summary of adverse events including total counts and event listings.
        - has_serious_adverse_events (bool): Flag indicating presence of serious adverse events.
        - results_url (str): Direct URL to the full results section.
        - status (str): Status of the data retrieval ('success', 'no_results_found', 'invalid_nct_id').
        - error_message (Optional[str]): Error message if an error occurred.

    Raises:
        ValueError: If required inputs are missing or invalid.
    """
    if not call_benefit.strip():
        return {
            "status": "error",
            "error_message": "Parameter 'call_benefit' is required and cannot be empty."
        }
    
    if not nct_id or not nct_id.startswith("NCT") or len(nct_id) < 11:
        return {
            "status": "invalid_nct_id",
            "error_message": f"Invalid NCT ID format: '{nct_id}'. Must start with 'NCT' and have a valid identifier."
        }

    try:
        api_data = call_external_api("biomcp-trial_outcomes")

        # Construct primary outcomes list
        primary_outcomes = [
            {
                "title": api_data["outcomes_primary_outcomes_0_title"],
                "description": api_data["outcomes_primary_outcomes_0_description"],
                "time_frame": api_data["outcomes_primary_outcomes_0_time_frame"],
                "measure": api_data["outcomes_primary_outcomes_0_measure"],
                "value": api_data["outcomes_primary_outcomes_0_value"]
            },
            {
                "title": api_data["outcomes_primary_outcomes_1_title"],
                "description": api_data["outcomes_primary_outcomes_1_description"],
                "time_frame": api_data["outcomes_primary_outcomes_1_time_frame"],
                "measure": api_data["outcomes_primary_outcomes_1_measure"],
                "value": api_data["outcomes_primary_outcomes_1_value"]
            }
        ]

        # Construct secondary outcomes list
        secondary_outcomes = [
            {
                "title": api_data["outcomes_secondary_outcomes_0_title"],
                "description": api_data["outcomes_secondary_outcomes_0_description"],
                "time_frame": api_data["outcomes_secondary_outcomes_0_time_frame"],
                "measure": api_data["outcomes_secondary_outcomes_0_measure"],
                "value": api_data["outcomes_secondary_outcomes_0_value"]
            },
            {
                "title": api_data["outcomes_secondary_outcomes_1_title"],
                "description": api_data["outcomes_secondary_outcomes_1_description"],
                "time_frame": api_data["outcomes_secondary_outcomes_1_time_frame"],
                "measure": api_data["outcomes_secondary_outcomes_1_measure"],
                "value": api_data["outcomes_secondary_outcomes_1_value"]
            }
        ]

        # Construct participant flow list
        participant_flow = [
            {
                "group_name": api_data["participant_flow_0_group_name"],
                "enrolled_count": api_data["participant_flow_0_enrolled_count"],
                "completed_count": api_data["participant_flow_0_completed_count"],
                "withdrawn_count": api_data["participant_flow_0_withdrawn_count"]
            },
            {
                "group_name": api_data["participant_flow_1_group_name"],
                "enrolled_count": api_data["participant_flow_1_enrolled_count"],
                "completed_count": api_data["participant_flow_1_completed_count"],
                "withdrawn_count": api_data["participant_flow_1_withdrawn_count"]
            }
        ]

        # Construct adverse events listing
        adverse_events_listings = [
            {
                "event_term": api_data["adverse_events_event_listings_0_event_term"],
                "system_org_class": api_data["adverse_events_event_listings_0_system_org_class"],
                "frequency": api_data["adverse_events_event_listings_0_frequency"],
                "severity": api_data["adverse_events_event_listings_0_severity"]
            },
            {
                "event_term": api_data["adverse_events_event_listings_1_event_term"],
                "system_org_class": api_data["adverse_events_event_listings_1_system_org_class"],
                "frequency": api_data["adverse_events_event_listings_1_frequency"],
                "severity": api_data["adverse_events_event_listings_1_severity"]
            }
        ]

        # Construct final result
        result = {
            "outcomes": {
                "primary_outcomes": primary_outcomes,
                "secondary_outcomes": secondary_outcomes
            },
            "results_available": api_data["results_available"],
            "participant_flow": participant_flow,
            "adverse_events": {
                "total_with_events": api_data["adverse_events_total_with_events"],
                "serious_adverse_events": api_data["adverse_events_serious_adverse_events"],
                "event_listings": adverse_events_listings
            },
            "has_serious_adverse_events": api_data["has_serious_adverse_events"],
            "results_url": api_data["results_url"],
            "status": api_data["status"]
        }

        if api_data.get("error_message"):
            result["error_message"] = api_data["error_message"]

        return result

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}"
        }