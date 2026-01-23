from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for arxiv-research-assistant-scrape_recent_category_papers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_id (str): ArXiv ID of the first paper
        - paper_0_authors (str): Comma-separated authors of the first paper
        - paper_0_published_date (str): Publication date of the first paper in ISO format
        - paper_0_category (str): Category of the first paper
        - paper_0_arxiv_url (str): URL to the paper on arXiv
        - paper_0_pdf_url (str): URL to the PDF of the paper
        - paper_0_abstract (str): Abstract text of the first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_id (str): ArXiv ID of the second paper
        - paper_1_authors (str): Comma-separated authors of the second paper
        - paper_1_published_date (str): Publication date of the second paper in ISO format
        - paper_1_category (str): Category of the second paper
        - paper_1_arxiv_url (str): URL to the paper on arXiv
        - paper_1_pdf_url (str): URL to the PDF of the paper
        - paper_1_abstract (str): Abstract text of the second paper
    """
    return {
        "paper_0_title": "Quantum Entanglement in Neural Networks",
        "paper_0_id": "2401.12345",
        "paper_0_authors": "Alice Johnson, Bob Smith",
        "paper_0_published_date": "2024-01-15T10:30:00Z",
        "paper_0_category": "quant-ph",
        "paper_0_arxiv_url": "https://arxiv.org/abs/2401.12345",
        "paper_0_pdf_url": "https://arxiv.org/pdf/2401.12345.pdf",
        "paper_0_abstract": "This paper explores quantum entanglement within artificial neural networks.",
        
        "paper_1_title": "Efficient Algorithms for Large-Scale Graph Processing",
        "paper_1_id": "2401.12346",
        "paper_1_authors": "Carol Davis, David Wilson",
        "paper_1_published_date": "2024-01-14T09:15:00Z",
        "paper_1_category": "cs.DS",
        "paper_1_arxiv_url": "https://arxiv.org/abs/2401.12346",
        "paper_1_pdf_url": "https://arxiv.org/pdf/2401.12346.pdf",
        "paper_1_abstract": "We present new algorithms for processing large-scale graphs efficiently."
    }

def arxiv_research_assistant_scrape_recent_category_papers(
    category: str, 
    max_results: Optional[int] = None
) -> Dict[str, Any]:
    """
    Scrapes the recent papers from a specified arXiv category and returns a list of paper entries.

    Args:
        category (str): The arXiv category to scrape (e.g., 'cs.AI', 'quant-ph').
        max_results (Optional[int]): Maximum number of results to return. Defaults to 2 if None.

    Returns:
        Dict[str, Any]: A dictionary containing a list of paper entries under the key 'papers'.
        Each paper entry is a dict with keys: 'title', 'id', 'authors', 'published_date',
        'category', 'arxiv_url', 'pdf_url', and 'abstract'.

    Raises:
        ValueError: If category is empty or not a string.
    """
    if not category or not isinstance(category, str):
        raise ValueError("Category must be a non-empty string.")

    if max_results is None:
        max_results = 2
    else:
        max_results = min(max(max_results, 1), 2)  # Limit to 1 or 2 for simulation

    api_data = call_external_api("arxiv-research-assistant-scrape_recent_category_papers")

    papers: List[Dict[str, Any]] = []

    for i in range(max_results):
        paper_key_prefix = f"paper_{i}"
        try:
            paper = {
                "title": api_data[f"{paper_key_prefix}_title"],
                "id": api_data[f"{paper_key_prefix}_id"],
                "authors": api_data[f"{paper_key_prefix}_authors"],
                "published_date": api_data[f"{paper_key_prefix}_published_date"],
                "category": api_data[f"{paper_key_prefix}_category"],
                "arxiv_url": api_data[f"{paper_key_prefix}_arxiv_url"],
                "pdf_url": api_data[f"{paper_key_prefix}_pdf_url"],
                "abstract": api_data[f"{paper_key_prefix}_abstract"]
            }
            papers.append(paper)
        except KeyError as e:
            raise KeyError(f"Missing expected field in API response: {e}")

    return {"papers": papers}