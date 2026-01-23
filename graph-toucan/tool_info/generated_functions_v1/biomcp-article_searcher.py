from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed article search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_pmid (int): PMID of first article
        - result_0_title (str): Title of first article
        - result_0_abstract (str): Abstract of first article
        - result_0_authors (str): Authors of first article as a comma-separated string
        - result_0_publication_date (str): Publication date in ISO format
        - result_0_journal (str): Journal name
        - result_0_doi (str): DOI of the article
        - result_1_pmid (int): PMID of second article
        - result_1_title (str): Title of second article
        - result_1_abstract (str): Abstract of second article
        - result_1_authors (str): Authors of second article as a comma-separated string
        - result_1_publication_date (str): Publication date in ISO format
        - result_1_journal (str): Journal name
        - result_1_doi (str): DOI of the article
        - total_count (int): Number of results returned (max 40)
        - query_summary (str): Natural language summary of search criteria
        - metadata_search_timestamp (str): ISO format timestamp of search execution
        - metadata_max_results_returned (int): Max number of results allowed (40)
        - metadata_source_database (str): Source database (e.g., PubMed)
        - has_more_results (bool): True if more than 40 results exist
    """
    return {
        "result_0_pmid": 12345678,
        "result_0_title": "Effects of Cisplatin on Non-small cell lung carcinoma: A comprehensive study",
        "result_0_abstract": "This study investigates the efficacy of Cisplatin in treating Non-small cell lung carcinoma. Results show significant tumor reduction in 60% of patients after 12 weeks of treatment.",
        "result_0_authors": "Smith J, Johnson A, Lee M",
        "result_0_publication_date": "2022-08-15",
        "result_0_journal": "Journal of Clinical Oncology",
        "result_0_doi": "10.1234/jco.2022.12345",
        "result_1_pmid": 87654321,
        "result_1_title": "EGFR gene expression and its role in Lung Adenocarcinoma progression",
        "result_1_abstract": "We analyzed EGFR gene expression patterns in 200 Lung Adenocarcinoma patients. Overexpression was linked to poorer prognosis and resistance to standard therapies.",
        "result_1_authors": "Wang X, Brown T, Davis R",
        "result_1_publication_date": "2023-03-22",
        "result_1_journal": "Cancer Research",
        "result_1_doi": "10.1234/cancerres.2023.67890",
        "total_count": 2,
        "query_summary": "Search for articles related to chemicals: Cisplatin; diseases: Non-small cell lung carcinoma, Lung Adenocarcinoma; genes: EGFR; variants: BRAF V600E; keywords: targeted therapy",
        "metadata_search_timestamp": datetime.datetime.now().isoformat(),
        "metadata_max_results_returned": 40,
        "metadata_source_database": "PubMed",
        "has_more_results": False
    }


def biomcp_article_searcher(
    call_benefit: str,
    chemicals: Optional[str] = None,
    diseases: Optional[str] = None,
    genes: Optional[str] = None,
    keywords: Optional[str] = None,
    variants: Optional[str] = None
) -> Dict[str, Any]:
    """
    Searches PubMed articles using structured criteria.

    Parameters:
        call_benefit (str): Define and summarize why this function is being called and the intended benefit
        chemicals (Optional[str]): Comma-separated string of chemicals for filtering results
        diseases (Optional[str]): Comma-separated string of diseases (e.g., Hypertension, Lung Adenocarcinoma)
        genes (Optional[str]): Comma-separated string of genes for filtering results
        keywords (Optional[str]): Comma-separated string of other keywords for filtering results
        variants (Optional[str]): Comma-separated string of variants for filtering results

    Returns:
        Dict containing:
        - results (List[Dict]): List of article records with keys 'pmid', 'title', 'abstract', 'authors',
          'publication_date', 'journal', and 'doi'
        - total_count (int): Total number of articles returned (≤40)
        - query_summary (str): Natural language summary of search criteria
        - metadata (Dict): Includes 'search_timestamp', 'max_results_returned', 'source_database'
        - has_more_results (bool): Whether more than 40 matching articles exist

    Notes:
        - Full terms are used over abbreviations
        - Keywords are used for terms that don't fit in other categories
        - Input parameters can be provided as comma-separated strings
    """
    # Validate required parameter
    if not call_benefit or not call_benefit.strip():
        raise ValueError("Parameter 'call_benefit' is required and cannot be empty.")

    # Normalize input parameters (convert to lists if they are strings)
    def parse_param(param: Optional[str]) -> List[str]:
        if param is None:
            return []
        if isinstance(param, str):
            return [item.strip() for item in param.split(",") if item.strip()]
        return []

    chemicals_list = parse_param(chemicals)
    diseases_list = parse_param(diseases)
    genes_list = parse_param(genes)
    keywords_list = parse_param(keywords)
    variants_list = parse_param(variants)

    # Call external API (simulated)
    api_data = call_external_api("biomcp-article_searcher")

    # Construct results list from indexed fields
    results = []
    for i in range(api_data["total_count"]):
        result = {
            "pmid": api_data[f"result_{i}_pmid"],
            "title": api_data[f"result_{i}_title"],
            "abstract": api_data[f"result_{i}_abstract"],
            "authors": api_data[f"result_{i}_authors"],
            "publication_date": api_data[f"result_{i}_publication_date"],
            "journal": api_data[f"result_{i}_journal"],
            "doi": api_data[f"result_{i}_doi"]
        }
        results.append(result)

    # Construct metadata
    metadata = {
        "search_timestamp": api_data["metadata_search_timestamp"],
        "max_results_returned": api_data["metadata_max_results_returned"],
        "source_database": api_data["metadata_source_database"]
    }

    # Return final structured response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "query_summary": api_data["query_summary"],
        "metadata": metadata,
        "has_more_results": api_data["has_more_results"]
    }