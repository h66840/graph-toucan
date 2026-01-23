from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching paper information from Hugging Face MCP server.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): The title of the paper
        - authors_0 (str): First author name
        - authors_1 (str): Second author name
        - abstract (str): The abstract or summary of the research paper
        - arxiv_id (str): The arXiv identifier for the paper
        - published_date (str): Publication date in ISO format (YYYY-MM-DD)
        - updated_date (str): Last updated date in ISO format (YYYY-MM-DD)
        - pdf_url (str): Direct URL to the PDF version of the paper on arXiv
        - huggingface_url (str): URL to the paper's page on Hugging Face
        - primary_category (str): Primary arXiv category classification
        - categories_0 (str): First arXiv category
        - categories_1 (str): Second arXiv category
        - doi (str): Digital Object Identifier (DOI), if available
        - license (str): License information for the paper
        - model_links_0_model_name (str): Name of first model mentioned
        - model_links_0_url (str): Hugging Face URL of first model
        - model_links_1_model_name (str): Name of second model mentioned
        - model_links_1_url (str): Hugging Face URL of second model
        - citation_count (int): Number of citations the paper has received
        - references_0_title (str): Title of first reference
        - references_0_arxiv_id (str): arXiv ID of first reference, if available
        - references_0_doi (str): DOI of first reference, if available
        - references_1_title (str): Title of second reference
        - references_1_arxiv_id (str): arXiv ID of second reference, if available
        - references_1_doi (str): DOI of second reference, if available
        - datasets_used_0 (str): Name of first dataset used
        - datasets_used_1 (str): Name of second dataset used
        - tasks_addressed_0 (str): First ML task addressed
        - tasks_addressed_1 (str): Second ML task addressed
        - metrics_reported_0_task (str): Task for first reported metric
        - metrics_reported_0_dataset (str): Dataset for first reported metric
        - metrics_reported_0_metric_name (str): Name of first metric
        - metrics_reported_0_value (float): Value of first metric
        - metrics_reported_1_task (str): Task for second reported metric
        - metrics_reported_1_dataset (str): Dataset for second reported metric
        - metrics_reported_1_metric_name (str): Name of second metric
        - metrics_reported_1_value (float): Value of second metric
    """
    return {
        "title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "authors_0": "Jacob Devlin",
        "authors_1": "Ming-Wei Chang",
        "abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.",
        "arxiv_id": "1810.04805",
        "published_date": "2018-10-11",
        "updated_date": "2019-01-15",
        "pdf_url": "https://arxiv.org/pdf/1810.04805.pdf",
        "huggingface_url": "https://huggingface.co/papers/1810.04805",
        "primary_category": "cs.CL",
        "categories_0": "cs.CL",
        "categories_1": "cs.AI",
        "doi": "10.48550/arXiv.1810.04805",
        "license": "arXiv.org perpetual, non-exclusive license",
        "model_links_0_model_name": "bert-base-uncased",
        "model_links_0_url": "https://huggingface.co/bert-base-uncased",
        "model_links_1_model_name": "bert-large-cased",
        "model_links_1_url": "https://huggingface.co/bert-large-cased",
        "citation_count": 45000,
        "references_0_title": "Attention is All You Need",
        "references_0_arxiv_id": "1706.03762",
        "references_0_doi": "10.48550/arXiv.1706.03762",
        "references_1_title": "Deep Residual Learning for Image Recognition",
        "references_1_arxiv_id": "1512.03385",
        "references_1_doi": "10.1109/CVPR.2016.90",
        "datasets_used_0": "SQuAD",
        "datasets_used_1": "GLUE",
        "tasks_addressed_0": "question answering",
        "tasks_addressed_1": "text classification",
        "metrics_reported_0_task": "question answering",
        "metrics_reported_0_dataset": "SQuAD v1.1",
        "metrics_reported_0_metric_name": "F1",
        "metrics_reported_0_value": 93.2,
        "metrics_reported_1_task": "text classification",
        "metrics_reported_1_dataset": "MNLI",
        "metrics_reported_1_metric_name": "accuracy",
        "metrics_reported_1_value": 86.7,
    }

def hugging_face_mcp_server_get_paper_info(arxiv_id: str) -> Dict[str, Any]:
    """
    Get information about a specific paper on Hugging Face using its arXiv ID.
    
    Args:
        arxiv_id (str): The arXiv ID of the paper (e.g., '1810.04805')
    
    Returns:
        Dict containing paper information with the following structure:
        - title (str): The title of the paper
        - authors (List[str]): List of author names associated with the paper
        - abstract (str): The abstract or summary of the research paper
        - arxiv_id (str): The arXiv identifier for the paper
        - published_date (str): Publication date in ISO format (YYYY-MM-DD)
        - updated_date (str): Last updated date in ISO format (YYYY-MM-DD)
        - pdf_url (str): Direct URL to the PDF version of the paper on arXiv
        - huggingface_url (str): URL to the paper's page on Hugging Face
        - primary_category (str): Primary arXiv category classification
        - categories (List[str]): List of all arXiv categories this paper belongs to
        - doi (str): Digital Object Identifier (DOI), if available
        - license (str): License information for the paper
        - model_links (List[Dict]): List of dictionaries containing model names and their corresponding Hugging Face URLs
        - citation_count (int): Number of citations the paper has received
        - references (List[Dict]): List of references cited by the paper, each with 'title' and optionally 'arxiv_id' or 'doi'
        - datasets_used (List[str]): Names of datasets referenced or used in the paper
        - tasks_addressed (List[str]): Machine learning tasks addressed in the paper
        - metrics_reported (List[Dict]): Performance metrics reported in the paper with task, dataset, metric_name, and value
    
    Raises:
        ValueError: If arxiv_id is empty or None
    """
    if not arxiv_id:
        raise ValueError("arxiv_id is required")
    
    # Call external API to get paper data (with flattened structure)
    api_data = call_external_api("hugging-face-mcp-server-get-paper-info")
    
    # Construct nested structure matching output schema
    result = {
        "title": api_data["title"],
        "authors": [
            api_data["authors_0"],
            api_data["authors_1"]
        ],
        "abstract": api_data["abstract"],
        "arxiv_id": api_data["arxiv_id"],
        "published_date": api_data["published_date"],
        "updated_date": api_data["updated_date"],
        "pdf_url": api_data["pdf_url"],
        "huggingface_url": api_data["huggingface_url"],
        "primary_category": api_data["primary_category"],
        "categories": [
            api_data["categories_0"],
            api_data["categories_1"]
        ],
        "doi": api_data["doi"],
        "license": api_data["license"],
        "model_links": [
            {
                "model_name": api_data["model_links_0_model_name"],
                "url": api_data["model_links_0_url"]
            },
            {
                "model_name": api_data["model_links_1_model_name"],
                "url": api_data["model_links_1_url"]
            }
        ],
        "citation_count": api_data["citation_count"],
        "references": [
            {
                "title": api_data["references_0_title"],
                "arxiv_id": api_data["references_0_arxiv_id"],
                "doi": api_data["references_0_doi"]
            },
            {
                "title": api_data["references_1_title"],
                "arxiv_id": api_data["references_1_arxiv_id"],
                "doi": api_data["references_1_doi"]
            }
        ],
        "datasets_used": [
            api_data["datasets_used_0"],
            api_data["datasets_used_1"]
        ],
        "tasks_addressed": [
            api_data["tasks_addressed_0"],
            api_data["tasks_addressed_1"]
        ],
        "metrics_reported": [
            {
                "task": api_data["metrics_reported_0_task"],
                "dataset": api_data["metrics_reported_0_dataset"],
                "metric_name": api_data["metrics_reported_0_metric_name"],
                "value": api_data["metrics_reported_0_value"]
            },
            {
                "task": api_data["metrics_reported_1_task"],
                "dataset": api_data["metrics_reported_1_dataset"],
                "metric_name": api_data["metrics_reported_1_metric_name"],
                "value": api_data["metrics_reported_1_value"]
            }
        ]
    }
    
    return result