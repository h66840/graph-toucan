from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for batch paper lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_author_0 (str): First author of the first paper
        - paper_0_author_1 (str): Second author of the first paper
        - paper_0_id (str): ID of the first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_author_0 (str): First author of the second paper
        - paper_1_author_1 (str): Second author of the second paper
        - paper_1_id (str): ID of the second paper
        - error (str): Error message if any occurred, otherwise empty string
    """
    return {
        "paper_0_title": "Attention Is All You Need",
        "paper_0_author_0": "Ashish Vaswani",
        "paper_0_author_1": "Noam Shazeer",
        "paper_0_id": "1234567890",
        "paper_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "paper_1_author_0": "Jacob Devlin",
        "paper_1_author_1": "Ming-Wei Chang",
        "paper_1_id": "0987654321",
        "error": ""
    }

def ai_research_assistant_semantic_scholar_papers_batch(paperIds: List[str]) -> Dict[str, Any]:
    """
    Look up multiple papers by their IDs (Semantic Scholar IDs, arXiv IDs, DOIs, etc.).
    
    Args:
        paperIds (List[str]): Array of paper IDs to look up.
        
    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper entries, each with 'title', 'authors' (List[str]), and optional 'id'.
          If a paper is not found, it may include a 'status' field indicating the issue.
        - error (Optional[str]): Error message if the request failed, otherwise None.
    """
    if not paperIds:
        return {
            "papers": [],
            "error": "No paper IDs provided"
        }

    try:
        # Call the simulated external API
        api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-batch")
        
        # Extract error if present
        error = api_data.get("error", "") or None
        
        # Construct papers list from flattened API response
        papers: List[Dict[str, Any]] = []
        
        for i in range(2):  # We expect two papers based on the API mock
            title_key = f"paper_{i}_title"
            id_key = f"paper_{i}_id"
            author_0_key = f"paper_{i}_author_0"
            author_1_key = f"paper_{i}_author_1"
            
            if title_key in api_data and api_data[title_key]:
                authors = []
                if author_0_key in api_data and api_data[author_0_key]:
                    authors.append(api_data[author_0_key])
                if author_1_key in api_data and api_data[author_1_key]:
                    authors.append(api_data[author_1_key])
                
                paper = {
                    "title": api_data[title_key],
                    "authors": authors,
                    "id": api_data.get(id_key)
                }
                papers.append(paper)
        
        return {
            "papers": papers,
            "error": error
        }
        
    except Exception as e:
        return {
            "papers": [],
            "error": f"An unexpected error occurred: {str(e)}"
        }