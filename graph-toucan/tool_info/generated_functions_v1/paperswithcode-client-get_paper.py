from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode paper retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): The title of the academic paper
        - abstract (str): The abstract or summary of the paper
        - author_0_name (str): Name of the first author
        - author_0_affiliation (str): Affiliation of the first author
        - author_1_name (str): Name of the second author
        - author_1_affiliation (str): Affiliation of the second author
        - published_date (str): Publication date in ISO format
        - paper_url (str): URL to the paper on PapersWithCode or external site
        - pdf_url (str): Direct URL to the PDF version of the paper
        - code_link_0_url (str): URL of the first code implementation
        - code_link_0_framework (str): Framework used in the first code implementation
        - code_link_1_url (str): URL of the second code implementation
        - code_link_1_framework (str): Framework used in the second code implementation
        - citations_count (int): Number of citations the paper has received
        - dataset_0 (str): Name of the first dataset used
        - dataset_1 (str): Name of the second dataset used
        - task_0 (str): First research task addressed
        - task_1 (str): Second research task addressed
        - method_0 (str): First method or model used
        - method_1 (str): Second method or model used
        - doi (str): Digital Object Identifier (DOI) of the paper
        - conference (str): Name of the conference where the paper was presented
        - metadata_retrieval_timestamp (str): Timestamp when data was retrieved
        - metadata_source (str): Source of the data (e.g., 'PapersWithCode API')
        - metadata_version (str): Version of the API or data format
    """
    return {
        "title": "Attention Is All You Need",
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
        "author_0_name": "Ashish Vaswani",
        "author_0_affiliation": "Google Brain",
        "author_1_name": "Noam Shazeer",
        "author_1_affiliation": "Google Research",
        "published_date": "2017-06-12",
        "paper_url": "https://paperswithcode.com/paper/attention-is-all-you-need",
        "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "code_link_0_url": "https://github.com/tensorflow/tensor2tensor",
        "code_link_0_framework": "TensorFlow",
        "code_link_1_url": "https://github.com/pytorch/fairseq",
        "code_link_1_framework": "PyTorch",
        "citations_count": 45000,
        "dataset_0": "WMT 2014 English-German",
        "dataset_1": "WMT 2014 English-French",
        "task_0": "Machine Translation",
        "task_1": "Sequence Transduction",
        "method_0": "Transformer",
        "method_1": "Self-Attention",
        "doi": "10.48550/arXiv.1706.03762",
        "conference": "NeurIPS",
        "metadata_retrieval_timestamp": "2023-11-15T10:30:00Z",
        "metadata_source": "PapersWithCode API",
        "metadata_version": "v1"
    }

def paperswithcode_client_get_paper(paper_id: str) -> Dict[str, Any]:
    """
    Get a paper by ID from PapersWithCode.
    
    Args:
        paper_id (str): The unique identifier of the paper in PapersWithCode.
    
    Returns:
        Dict containing the paper details with the following structure:
        - title (str): The title of the academic paper
        - abstract (str): The abstract or summary of the paper
        - authors (List[Dict]): List of authors with their details (name, affiliation)
        - published_date (str): Publication date in ISO format
        - paper_url (str): URL to the paper on PapersWithCode or external site
        - pdf_url (str): Direct URL to the PDF version of the paper
        - code_links (List[Dict]): List of code implementations with URLs and framework information
        - citations_count (int): Number of citations the paper has received
        - datasets_used (List[str]): Names of datasets used in the research
        - tasks (List[str]): Research tasks or areas the paper addresses
        - methods (List[str]): Methods or models proposed or used in the paper
        - doi (str): Digital Object Identifier (DOI) of the paper if available
        - conference (str): Name of the conference where the paper was presented
        - metadata (Dict): Additional metadata such as retrieval timestamp, source, or version info
    
    Raises:
        ValueError: If paper_id is empty or None.
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("paperswithcode-client-get_paper")
    
    # Construct authors list
    authors = [
        {
            "name": api_data["author_0_name"],
            "affiliation": api_data["author_0_affiliation"]
        },
        {
            "name": api_data["author_1_name"],
            "affiliation": api_data["author_1_affiliation"]
        }
    ]
    
    # Construct code links list
    code_links = [
        {
            "url": api_data["code_link_0_url"],
            "framework": api_data["code_link_0_framework"]
        },
        {
            "url": api_data["code_link_1_url"],
            "framework": api_data["code_link_1_framework"]
        }
    ]
    
    # Construct datasets used list
    datasets_used = [
        api_data["dataset_0"],
        api_data["dataset_1"]
    ]
    
    # Construct tasks list
    tasks = [
        api_data["task_0"],
        api_data["task_1"]
    ]
    
    # Construct methods list
    methods = [
        api_data["method_0"],
        api_data["method_1"]
    ]
    
    # Construct metadata dict
    metadata = {
        "retrieval_timestamp": api_data["metadata_retrieval_timestamp"],
        "source": api_data["metadata_source"],
        "version": api_data["metadata_version"]
    }
    
    # Assemble final result matching output schema
    result = {
        "title": api_data["title"],
        "abstract": api_data["abstract"],
        "authors": authors,
        "published_date": api_data["published_date"],
        "paper_url": api_data["paper_url"],
        "pdf_url": api_data["pdf_url"],
        "code_links": code_links,
        "citations_count": api_data["citations_count"],
        "datasets_used": datasets_used,
        "tasks": tasks,
        "methods": methods,
        "doi": api_data["doi"],
        "conference": api_data["conference"],
        "metadata": metadata
    }
    
    return result