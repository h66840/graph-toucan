from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for clinical trial protocol information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - nct_id (str): NCT identifier for the clinical trial
        - url (str): URL to the full study on ClinicalTrials.gov
        - brief_title (str): short title of the trial
        - official_title (str): full official title of the trial
        - org_study_id (str): identifier assigned by the organization conducting the study
        - organization_name (str): name of the organization responsible for the study
        - organization_class (str): classification of the organization (e.g., NIH)
        - overall_status (str): current status of the trial (e.g., COMPLETED)
        - status_verified_date (str): date when the status was last verified
        - study_first_submit_date (str): date when the study was first submitted
        - study_first_submit_qc_date (str): date when the first submission passed quality control
        - results_first_submit_date (str): date when results were first submitted
        - results_first_submit_qc_date (str): date when results submission passed quality control
        - last_update_submit_date (str): date of the most recent update submission
        - start_date (str): actual start date of the study
        - primary_completion_date (str): actual primary completion date
        - completion_date (str): actual overall completion date
        - study_first_post_date (str): date when the study was first posted
        - results_first_post_date (str): date when results were first posted
        - last_update_post_date (str): date when the last update was posted
        - has_expanded_access (bool): whether the trial offers expanded access to investigational drugs
        - responsible_party_type (str): role type of the responsible party (e.g., SPONSOR)
        - lead_sponsor_name (str): name of the lead sponsor
        - lead_sponsor_class (str): classification of the lead sponsor (e.g., NIH)
        - is_fda_regulated_drug (bool): whether the study involves an FDA-regulated drug
        - is_fda_regulated_device (bool): whether the study involves an FDA-regulated device
        - is_us_export (bool): whether the trial is subject to US export regulations
        - brief_summary (str): concise summary of the trial's purpose and methods
        - detailed_description (str): comprehensive description of the trial including design, procedures, and rationale
        - condition (str): medical condition under study (e.g., COVID-19)
        - keyword_0 (str): first keyword associated with the trial
        - study_type (str): type of study (e.g., INTERVENTIONAL)
        - allocation (str): method of participant assignment (e.g., RANDOMIZED)
        - intervention_model (str): structure of the intervention groups (e.g., PARALLEL)
        - primary_purpose (str): main objective of the intervention (e.g., TREATMENT)
        - masking (str): level of blinding (e.g., DOUBLE)
        - who_masked_0 (str): first party blinded in the trial (e.g., PARTICIPANT)
        - enrollment_count (int): actual number of participants enrolled
        - enrollment_type (str): descriptor for enrollment count (e.g., ACTUAL)
        - phase_0 (str): first phase of the clinical trial (e.g., PHASE3)
        - arm_group_0_label (str): label of the first trial arm
        - arm_group_0_type (str): type of the first trial arm
        - arm_group_0_description (str): description of the first trial arm
        - arm_group_0_intervention_names_0 (str): first intervention name in the first arm
        - intervention_0_type (str): type of the first intervention
        - intervention_0_name (str): name of the first intervention
        - intervention_0_description (str): description of the first intervention
        - intervention_0_arm_group_labels_0 (str): first arm group label for the first intervention
        - eligibility_criteria_raw (str): full text of inclusion and exclusion criteria as provided
        - healthy_volunteers (bool): whether healthy volunteers are allowed
        - sex (str): eligible sex(es) for participation (e.g., ALL)
        - minimum_age (str): minimum age requirement (e.g., "18 Years")
        - maximum_age (str): maximum age requirement (e.g., "99 Years")
        - std_age_0 (str): first standardized age category eligible for the trial (e.g., ADULT)
    """
    return {
        "nct_id": "NCT04280705",
        "url": "https://clinicaltrials.gov/study/NCT04280705",
        "brief_title": "A Study of Drug X in Patients With Disease Y",
        "official_title": "A Phase 3 Randomized, Double-Blind, Placebo-Controlled Study to Evaluate the Efficacy and Safety of Drug X in Patients With Disease Y",
        "org_study_id": "DX-2020-01",
        "organization_name": "BioPharma Inc.",
        "organization_class": "INDUSTRY",
        "overall_status": "COMPLETED",
        "status_verified_date": "2023-05-10",
        "study_first_submit_date": "2020-02-15",
        "study_first_submit_qc_date": "2020-02-18",
        "results_first_submit_date": "2023-04-01",
        "results_first_submit_qc_date": "2023-04-05",
        "last_update_submit_date": "2023-05-10",
        "start_date": "2020-03-01",
        "primary_completion_date": "2022-12-15",
        "completion_date": "2023-03-30",
        "study_first_post_date": "2020-02-20",
        "results_first_post_date": "2023-04-10",
        "last_update_post_date": "2023-05-15",
        "has_expanded_access": True,
        "responsible_party_type": "SPONSOR",
        "lead_sponsor_name": "BioPharma Inc.",
        "lead_sponsor_class": "INDUSTRY",
        "is_fda_regulated_drug": True,
        "is_fda_regulated_device": False,
        "is_us_export": False,
        "brief_summary": "This study evaluates the efficacy and safety of Drug X compared to placebo in patients with Disease Y.",
        "detailed_description": "The study is a multicenter, randomized, double-blind, placebo-controlled trial. Participants will be randomized 1:1 to receive either Drug X or placebo for 52 weeks. The primary endpoint is change from baseline in symptom score at week 52.",
        "condition": "Disease Y",
        "keyword_0": "Drug X",
        "study_type": "INTERVENTIONAL",
        "allocation": "RANDOMIZED",
        "intervention_model": "PARALLEL",
        "primary_purpose": "TREATMENT",
        "masking": "DOUBLE",
        "who_masked_0": "PARTICIPANT",
        "enrollment_count": 500,
        "enrollment_type": "ACTUAL",
        "phase_0": "PHASE3",
        "arm_group_0_label": "Drug X Group",
        "arm_group_0_type": "EXPERIMENTAL",
        "arm_group_0_description": "Participants receive Drug X 10mg orally once daily for 52 weeks.",
        "arm_group_0_intervention_names_0": "Drug X",
        "intervention_0_type": "DRUG",
        "intervention_0_name": "Drug X",
        "intervention_0_description": "Oral tablet, 10mg, once daily.",
        "intervention_0_arm_group_labels_0": "Drug X Group",
        "eligibility_criteria_raw": "Inclusion Criteria:\n- Age 18-75\n- Confirmed diagnosis of Disease Y\n- Able to provide informed consent\n\nExclusion Criteria:\n- Severe liver disease\n- Pregnancy or breastfeeding\n- Known hypersensitivity to Drug X",
        "healthy_volunteers": False,
        "sex": "ALL",
        "minimum_age": "18 Years",
        "maximum_age": "75 Years",
        "std_age_0": "ADULT"
    }

def biomcp_trial_protocol(call_benefit: str, nct_id: str) -> str:
    """
    Retrieves core protocol information for a single clinical trial identified by its NCT ID.
    
    This function simulates fetching standard "Protocol" view modules (like ID, Status, Sponsor,
    Design, Eligibility) from the ClinicalTrials.gov v2 API and returns a Markdown-formatted
    summary of the trial details.
    
    Parameters:
        call_benefit (str): Explanation of why this function is being called and the intended benefit.
        nct_id (str): A single NCT ID (e.g., "NCT04280705") identifying the clinical trial.
    
    Returns:
        str: A Markdown formatted string detailing title, status, sponsor, purpose, study design,
             phase, interventions, eligibility criteria, and other key trial information.
             Returns an error message in Markdown if input validation fails.
    
    Raises:
        ValueError: If nct_id is not a valid string starting with 'NCT'.
    """
    # Input validation
    if not nct_id or not isinstance(nct_id, str) or not nct_id.upper().startswith('NCT'):
        return f"## Error\nInvalid NCT ID provided: `{nct_id}`. Please provide a valid NCT ID (e.g., NCT04280705)."
    
    if not call_benefit or not isinstance(call_benefit, str):
        return "## Error\n`call_benefit` is required to explain the purpose of this query."

    try:
        # Fetch simulated external data
        api_data = call_external_api("biomcp-trial_protocol")
        
        # Construct nested output structure from flat API data
        result = {
            "nct_id": api_data["nct_id"],
            "url": api_data["url"],
            "brief_title": api_data["brief_title"],
            "official_title": api_data["official_title"],
            "org_study_id": api_data["org_study_id"],
            "organization_name": api_data["organization_name"],
            "organization_class": api_data["organization_class"],
            "overall_status": api_data["overall_status"],
            "status_verified_date": api_data["status_verified_date"],
            "study_first_submit_date": api_data["study_first_submit_date"],
            "study_first_submit_qc_date": api_data["study_first_submit_qc_date"],
            "results_first_submit_date": api_data["results_first_submit_date"],
            "results_first_submit_qc_date": api_data["results_first_submit_qc_date"],
            "last_update_submit_date": api_data["last_update_submit_date"],
            "start_date": api_data["start_date"],
            "primary_completion_date": api_data["primary_completion_date"],
            "completion_date": api_data["completion_date"],
            "study_first_post_date": api_data["study_first_post_date"],
            "results_first_post_date": api_data["results_first_post_date"],
            "last_update_post_date": api_data["last_update_post_date"],
            "has_expanded_access": api_data["has_expanded_access"],
            "responsible_party_type": api_data["responsible_party_type"],
            "lead_sponsor_name": api_data["lead_sponsor_name"],
            "lead_sponsor_class": api_data["lead_sponsor_class"],
            "is_fda_regulated_drug": api_data["is_fda_regulated_drug"],
            "is_fda_regulated_device": api_data["is_fda_regulated_device"],
            "is_us_export": api_data["is_us_export"],
            "brief_summary": api_data["brief_summary"],
            "detailed_description": api_data["detailed_description"],
            "condition": api_data["condition"],
            "keywords": [api_data["keyword_0"]] if api_data.get("keyword_0") else [],
            "study_type": api_data["study_type"],
            "allocation": api_data["allocation"],
            "intervention_model": api_data["intervention_model"],
            "primary_purpose": api_data["primary_purpose"],
            "masking": api_data["masking"],
            "who_masked": [api_data["who_masked_0"]] if api_data.get("who_masked_0") else [],
            "enrollment_count": api_data["enrollment_count"],
            "enrollment_type": api_data["enrollment_type"],
            "phases": [api_data["phase_0"]] if api_data.get("phase_0") else [],
            "arm_groups": [
                {
                    "label": api_data["arm_group_0_label"],
                    "type": api_data["arm_group_0_type"],
                    "description": api_data["arm_group_0_description"],
                    "intervention_names": [api_data["arm_group_0_intervention_names_0"]] 
                    if api_data.get("arm_group_0_intervention_names_0") else []
                }
            ],
            "interventions": [
                {
                    "type": api_data["intervention_0_type"],
                    "name": api_data["intervention_0_name"],
                    "description": api_data["intervention_0_description"],
                    "arm_group_labels": [api_data["intervention_0_arm_group_labels_0"]] 
                    if api_data.get("intervention_0_arm_group_labels_0") else []
                }
            ],
            "eligibility_criteria_raw": api_data["eligibility_criteria_raw"],
            "healthy_volunteers": api_data["healthy_volunteers"],
            "sex": api_data["sex"],
            "minimum_age": api_data["minimum_age"],
            "maximum_age": api_data["maximum_age"],
            "std_ages": [api_data["std_age_0"]] if api_data.get("std_age_0") else []
        }
        
        # Generate Markdown output
        markdown_output = f"""## Clinical Trial Protocol Summary

### Trial Identification
- **NCT ID**: [{result['nct_id']}]({result['url']})
- **Brief Title**: {result['brief_title']}
- **Official Title**: {result['official_title']}
- **Organization Study ID**: {result['org_study_id']}

### Sponsor & Organization
- **Organization**: {result['organization_name']} ({result['organization_class']})
- **Lead Sponsor**: {result['lead_sponsor_name']} ({result['lead_sponsor_class']})
- **Responsible Party**: {result['responsible_party_type']}

### Status & Timeline
- **Status**: {result['overall_status']}
- **Status Verified**: {result['status_verified_date']}
- **Start Date**: {result['start_date']}
- **Primary Completion**: {result['primary_completion_date']}
- **Completion Date**: {result['completion_date']}
- **First Submitted**: {result['study_first_submit_date']}
- **First Posted**: {result['study_first_post_date']}
- **Last Update Submitted**: {result['last_update_submit_date']}
- **Last Update Posted**: {result['last_update_post_date']}

### Regulatory Information
- **FDA Regulated Drug**: {'Yes' if result['is_fda_regulated_drug'] else 'No'}
- **FDA Regulated Device**: {'Yes' if result['is_fda_regulated_device'] else 'No'}
- **US Export**: {'Yes' if result['is_us_export'] else 'No'}
- **Expanded Access**: {'Yes' if result['has_expanded_access'] else 'No'}

### Study Details
- **Condition**: {result['condition']}
- **Keywords**: {', '.join(result['keywords']) if result['keywords'] else 'None'}
- **Study Type**: {result['study_type']}
- **Allocation**: {result['allocation']}
- **Intervention Model**: {result['intervention_model']}
- **Primary Purpose**: {result['primary_purpose']}
- **Masking**: {result['masking']}
- **Masked Parties**: {', '.join(result['who_masked']) if result['who_masked'] else 'None'}
- **Enrollment**: {result['enrollment_count']} ({result['enrollment_type']})
- **Phase(s)**: {', '.join(result['phases']) if result['phases'] else 'Not Applicable'}

### Interventions
{chr(10).join([f"- **{arm['label']}** ({arm['type']}): {arm['description']} (Interventions: {', '.join(arm['intervention_names'])})" for arm in result['arm_groups']])}

### Eligibility Criteria
- **Healthy Volunteers**: {'Accepted' if result['healthy_volunteers'] else 'Not Accepted'}
- **Sex**: {result['sex']}
- **Minimum Age**: {result['minimum_age']}
- **Maximum Age**: {result['maximum_age']}
- **Standard Ages**: {', '.join(result['std_ages']) if result['std_ages'] else 'None'}

#### Raw Criteria
{result['eligibility_criteria_raw']}

### Descriptions
**Brief Summary**  
{result['brief_summary']}

**Detailed Description**  
{result['detailed_description']}
"""
        return markdown_output.strip()
        
    except Exception as e:
        return f"## Error\nAn unexpected error occurred while processing the request: `{str(e)}`"