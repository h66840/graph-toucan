from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for arXiv paper information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the paper
        - author_0 (str): First author name
        - author_1 (str): Second author name
        - publication_date (str): Publication date in YYYY-MM-DD format
        - category_0 (str): First arXiv category (e.g., cs.CV)
        - category_1 (str): Second arXiv category (e.g., cs.CL)
        - doi (str): DOI identifier if available, otherwise None
        - arxiv_url (str): URL to the paper's abstract page on arXiv
        - pdf_url (str): URL to the PDF version of the paper
        - abstract (str): Full abstract text describing the paper's content and contributions
    """
    return {
        "title": "Attention Is All You Need",
        "author_0": "Ashish Vaswani",
        "author_1": "Noam Shazeer",
        "publication_date": "2017-06-12",
        "category_0": "cs.CL",
        "category_1": "cs.LG",
        "doi": "10.48550/arXiv.1706.03762",
        "arxiv_url": "https://arxiv.org/abs/1706.03762",
        "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks "
                   "in an encoder-decoder configuration. The best performing models also connect the encoder and decoder "
                   "through an attention mechanism. We propose a new simple network architecture, the Transformer, "
                   "based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."
    }

def arxiv_research_assistant_get_paper_info(paper_id: str) -> Dict[str, Any]:
    """
    Fetches detailed information about a research paper from arXiv using its paper ID.
    
    Args:
        paper_id (str): The arXiv paper ID (e.g., '1706.03762') used to retrieve paper details.
    
    Returns:
        Dict containing the following keys:
        - title (str): Title of the paper
        - authors (List[str]): List of author names
        - publication_date (str): Publication date in YYYY-MM-DD format
        - categories (List[str]): List of arXiv categories (e.g., cs.CV, cs.CL)
        - doi (Optional[str]): DOI identifier if available, otherwise None
        - arxiv_url (str): URL to the paper's abstract page on arXiv
        - pdf_url (str): URL to the PDF version of the paper
        - abstract (str): Full abstract text describing the paper's content and contributions
    
    Raises:
        ValueError: If paper_id is empty or invalid.
    """
    if not paper_id or not paper_id.strip():
        raise ValueError("paper_id is required and cannot be empty")

    # Call simulated external API to get flat data
    api_data = call_external_api("arxiv-research-assistant-get_paper_info")
    
    # Construct nested output structure as per schema
    result = {
        "title": api_data["title"],
        "authors": [
            api_data["author_0"],
            api_data["author_1"]
        ],
        "publication_date": api_data["publication_date"],
        "categories": [
            api_data["category_0"],
            api_data["category_1"]
        ],
        "doi": api_data["doi"] if api_data["doi"] != "None" else None,
        "arxiv_url": api_data["arxiv_url"],
        "pdf_url": api_data["pdf_url"],
        "abstract": api_data["abstract"]
    }
    
    return result