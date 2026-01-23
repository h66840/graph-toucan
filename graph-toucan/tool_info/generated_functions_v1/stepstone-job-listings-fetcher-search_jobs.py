from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching job listing data from external API for Stepstone.de.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - search_summary_search_terms (str): Comma-separated search terms used
        - search_summary_location_zip_code (str): ZIP code for location-based search
        - search_summary_radius_km (int): Search radius in kilometers
        - search_summary_total_jobs_found (int): Total number of jobs found
        - results_by_term_0_search_term (str): First search term
        - results_by_term_0_job_count (int): Number of jobs for first term
        - results_by_term_0_job_0_title (str): Title of first job for first term
        - results_by_term_0_job_0_company (str): Company of first job for first term
        - results_by_term_0_job_0_description (str): Description of first job for first term
        - results_by_term_0_job_0_link (str): Link to first job for first term
        - results_by_term_0_job_1_title (str): Title of second job for first term
        - results_by_term_0_job_1_company (str): Company of second job for first term
        - results_by_term_0_job_1_description (str): Description of second job for first term
        - results_by_term_0_job_1_link (str): Link to second job for first term
        - results_by_term_1_search_term (str): Second search term
        - results_by_term_1_job_count (int): Number of jobs for second term
        - results_by_term_1_job_0_title (str): Title of first job for second term
        - results_by_term_1_job_0_company (str): Company of first job for second term
        - results_by_term_1_job_0_description (str): Description of first job for second term
        - results_by_term_1_job_0_link (str): Link to first job for second term
        - results_by_term_1_job_1_title (str): Title of second job for second term
        - results_by_term_1_job_1_company (str): Company of second job for second term
        - results_by_term_1_job_1_description (str): Description of second job for second term
        - results_by_term_1_job_1_link (str): Link to second job for second term
    """
    return {
        "search_summary_search_terms": "Python Developer,Data Scientist",
        "search_summary_location_zip_code": "10115",
        "search_summary_radius_km": 10,
        "search_summary_total_jobs_found": 42,
        "results_by_term_0_search_term": "Python Developer",
        "results_by_term_0_job_count": 23,
        "results_by_term_0_job_0_title": "Senior Python Developer",
        "results_by_term_0_job_0_company": "TechCorp GmbH",
        "results_by_term_0_job_0_description": "Exciting opportunity for a Senior Python Developer to work on scalable backend systems.",
        "results_by_term_0_job_0_link": "https://stepstone.de/job/12345",
        "results_by_term_0_job_1_title": "Junior Python Developer",
        "results_by_term_0_job_1_company": "StartupXYZ",
        "results_by_term_0_job_1_description": "Join our agile team as a Junior Python Developer and grow your skills.",
        "results_by_term_0_job_1_link": "https://stepstone.de/job/67890",
        "results_by_term_1_search_term": "Data Scientist",
        "results_by_term_1_job_count": 19,
        "results_by_term_1_job_0_title": "Lead Data Scientist",
        "results_by_term_1_job_0_company": "AnalyticsPro AG",
        "results_by_term_1_job_0_description": "Lead data science initiatives in a fast-paced environment using cutting-edge ML tools.",
        "results_by_term_1_job_0_link": "https://stepstone.de/job/54321",
        "results_by_term_1_job_1_title": "Data Scientist",
        "results_by_term_1_job_1_company": "InsightLabs",
        "results_by_term_1_job_1_description": "Work with large datasets to extract actionable insights and build predictive models.",
        "results_by_term_1_job_1_link": "https://stepstone.de/job/98765",
    }

def stepstone_job_listings_fetcher_search_jobs(
    radius: Optional[int] = None,
    search_terms: Optional[List[str]] = None,
    zip_code: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for job listings on Stepstone.de using multiple search terms.
    
    Args:
        radius (Optional[int]): Search radius in kilometers. Defaults to 10 if not provided.
        search_terms (Optional[List[str]]): List of job search terms to look for. Defaults to ["Python Developer", "Data Scientist"].
        zip_code (Optional[str]): German postal code for location-based search. Defaults to "10115" if not provided.
    
    Returns:
        Dict containing:
        - search_summary (Dict): Contains 'search_terms', 'location_zip_code', 'radius_km', and 'total_jobs_found'
        - results_by_term (List[Dict]): List of result groups per search term, each with 'search_term', 'jobs', and 'job_count'
          where 'jobs' is a list of job_entry dicts with 'title', 'company', 'description', 'link'
    
    Example:
        {
            "search_summary": {
                "search_terms": ["Python Developer", "Data Scientist"],
                "location_zip_code": "10115",
                "radius_km": 10,
                "total_jobs_found": 42
            },
            "results_by_term": [
                {
                    "search_term": "Python Developer",
                    "job_count": 23,
                    "jobs": [
                        {
                            "title": "Senior Python Developer",
                            "company": "TechCorp GmbH",
                            "description": "Exciting opportunity...",
                            "link": "https://stepstone.de/job/12345"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    """
    # Input validation and defaults
    if radius is None:
        radius = 10
    if not isinstance(radius, int) or radius < 0:
        raise ValueError("Radius must be a non-negative integer")
        
    if zip_code is None:
        zip_code = "10115"
    if not isinstance(zip_code, str) or not zip_code.strip():
        raise ValueError("ZIP code must be a non-empty string")
    zip_code = zip_code.strip()
    
    if search_terms is None:
        search_terms = ["Python Developer", "Data Scientist"]
    if not isinstance(search_terms, list) or len(search_terms) == 0:
        raise ValueError("Search terms must be a non-empty list")
    # Filter out empty terms and convert to list of non-empty strings
    search_terms = [term.strip() for term in search_terms if isinstance(term, str) and term.strip()]
    if len(search_terms) == 0:
        raise ValueError("At least one valid search term is required")

    # Call external API (simulation)
    api_data = call_external_api("stepstone-job-listings-fetcher-search_jobs")
    
    # Construct search_summary
    search_summary = {
        "search_terms": search_terms,
        "location_zip_code": zip_code,
        "radius_km": radius,
        "total_jobs_found": api_data["search_summary_total_jobs_found"]
    }
    
    # Construct results_by_term
    results_by_term = []
    
    # Process first search term results
    term_0_jobs = [
        {
            "title": api_data["results_by_term_0_job_0_title"],
            "company": api_data["results_by_term_0_job_0_company"],
            "description": api_data["results_by_term_0_job_0_description"],
            "link": api_data["results_by_term_0_job_0_link"]
        },
        {
            "title": api_data["results_by_term_0_job_1_title"],
            "company": api_data["results_by_term_0_job_1_company"],
            "description": api_data["results_by_term_0_job_1_description"],
            "link": api_data["results_by_term_0_job_1_link"]
        }
    ]
    
    results_by_term.append({
        "search_term": api_data["results_by_term_0_search_term"],
        "jobs": term_0_jobs,
        "job_count": api_data["results_by_term_0_job_count"]
    })
    
    # Process second search term results
    term_1_jobs = [
        {
            "title": api_data["results_by_term_1_job_0_title"],
            "company": api_data["results_by_term_1_job_0_company"],
            "description": api_data["results_by_term_1_job_0_description"],
            "link": api_data["results_by_term_1_job_0_link"]
        },
        {
            "title": api_data["results_by_term_1_job_1_title"],
            "company": api_data["results_by_term_1_job_1_company"],
            "description": api_data["results_by_term_1_job_1_description"],
            "link": api_data["results_by_term_1_job_1_link"]
        }
    ]
    
    results_by_term.append({
        "search_term": api_data["results_by_term_1_search_term"],
        "jobs": term_1_jobs,
        "job_count": api_data["results_by_term_1_job_count"]
    })
    
    # Construct final result
    result = {
        "search_summary": search_summary,
        "results_by_term": results_by_term
    }
    
    return result