from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for research paper search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first research paper
        - result_0_authors (str): Authors of the first research paper (comma-separated)
        - result_0_publication_year (int): Publication year of the first paper
        - result_0_abstract (str): Abstract of the first research paper
        - result_0_doi (str): DOI of the first research paper
        - result_0_journal_conference (str): Journal or conference name for the first paper
        - result_0_relevance_score (float): Relevance score (0-1) for the first paper
        - result_1_title (str): Title of the second research paper
        - result_1_authors (str): Authors of the second research paper (comma-separated)
        - result_1_publication_year (int): Publication year of the second paper
        - result_1_abstract (str): Abstract of the second research paper
        - result_1_doi (str): DOI of the second research paper
        - result_1_journal_conference (str): Journal or conference name for the second paper
        - result_1_relevance_score (float): Relevance score (0-1) for the second paper
        - total_count (int): Total number of matching research papers found
        - query_summary (str): Natural language summary of the search query
        - metadata_retrieval_time (float): Time taken to retrieve results in seconds
        - metadata_source_databases (str): Comma-separated list of source databases used
        - metadata_filters_applied (str): Description of any filters applied during search
    """
    return {
        "result_0_title": "Attention Is All You Need",
        "result_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin",
        "result_0_publication_year": 2017,
        "result_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
        "result_0_doi": "10.48550/arXiv.1706.03762",
        "result_0_journal_conference": "Advances in Neural Information Processing Systems (NeurIPS)",
        "result_0_relevance_score": 0.98,
        "result_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "result_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "result_1_publication_year": 2018,
        "result_1_abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.",
        "result_1_doi": "10.48550/arXiv.1810.04805",
        "result_1_journal_conference": "arXiv preprint",
        "result_1_relevance_score": 0.96,
        "total_count": 150,
        "query_summary": "Search for foundational research papers on transformer models in natural language processing",
        "metadata_retrieval_time": 1.25,
        "metadata_source_databases": "arXiv, Google Scholar, Semantic Scholar",
        "metadata_filters_applied": "Publication year >= 2015, peer-reviewed only"
    }

def exa_search_research_paper_search_exa(query: str, numResults: Optional[int] = 5) -> Dict[str, Any]:
    """
    Search for academic papers and research using Exa AI - specializes in finding scholarly articles, 
    research papers, and academic content. Returns detailed information about research findings and academic sources.
    
    Args:
        query (str): Research paper search query (required)
        numResults (Optional[int]): Number of research papers to return (default: 5)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of research papers with fields such as title, authors, publication year, 
          abstract, DOI, journal/conference, and relevance score
        - total_count (int): Total number of matching research papers found for the query
        - query_summary (str): A brief natural language summary of what the search query aimed to find
        - metadata (Dict): Additional information about the search execution including retrieval time, 
          source databases used, and any filters applied
    
    Raises:
        ValueError: If query is empty or None
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    if numResults is None:
        numResults = 5
    elif numResults <= 0:
        raise ValueError("numResults must be a positive integer")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("exa-search-research_paper_search_exa")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result
    results.append({
        "title": api_data["result_0_title"],
        "authors": api_data["result_0_authors"].split(", "),
        "publication_year": api_data["result_0_publication_year"],
        "abstract": api_data["result_0_abstract"],
        "doi": api_data["result_0_doi"],
        "journal/conference": api_data["result_0_journal_conference"],
        "relevance_score": api_data["result_0_relevance_score"]
    })
    
    # Process second result
    results.append({
        "title": api_data["result_1_title"],
        "authors": api_data["result_1_authors"].split(", "),
        "publication_year": api_data["result_1_publication_year"],
        "abstract": api_data["result_1_abstract"],
        "doi": api_data["result_1_doi"],
        "journal/conference": api_data["result_1_journal_conference"],
        "relevance_score": api_data["result_1_relevance_score"]
    })
    
    # If more results are requested beyond what we have, repeat the pattern (for simulation)
    while len(results) < numResults:
        # In a real implementation, we would fetch more results
        # Here we just duplicate the last result with slight modification for realism
        last_result = results[-1].copy()
        last_result["relevance_score"] = max(0.0, last_result["relevance_score"] - 0.05)
        results.append(last_result)
    
    # Limit results to requested number
    results = results[:numResults]
    
    # Construct metadata dictionary
    metadata = {
        "retrieval_time": api_data["metadata_retrieval_time"],
        "source_databases": [db.strip() for db in api_data["metadata_source_databases"].split(",")],
        "filters_applied": api_data["metadata_filters_applied"]
    }
    
    # Return final structured response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "query_summary": api_data["query_summary"],
        "metadata": metadata
    }