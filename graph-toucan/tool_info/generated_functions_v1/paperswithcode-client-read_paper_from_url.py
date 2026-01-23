from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from PapersWithCode API for a paper by URL.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): The title of the academic paper
        - abstract (str): Summary of the paper's content and contributions
        - author_0 (str): First author name
        - author_1 (str): Second author name
        - published_date (str): Publication date in ISO format (e.g., '2023-01-01')
        - pdf_url (str): Direct URL to the PDF version of the paper
        - official_code_url_0 (str): First official code URL
        - official_code_framework_0 (str): Framework for first official code
        - official_code_url_1 (str): Second official code URL
        - official_code_framework_1 (str): Framework for second official code
        - dataset_0 (str): First dataset name
        - dataset_1 (str): Second dataset name
        - task_0 (str): First associated task
        - task_1 (str): Second associated task
        - method_0 (str): First method used
        - method_1 (str): Second method used
        - metric_name_0 (str): First metric name
        - metric_value_0 (float): Value of first metric
        - metric_name_1 (str): Second metric name
        - metric_value_1 (float): Value of second metric
        - results_summary (str): High-level summary of results or findings
        - doi (str): Digital Object Identifier (DOI) for the paper
        - citation_count (int): Number of citations the paper has received
        - is_open_access (bool): Whether the paper is openly accessible
        - related_paper_0_title (str): Title of first related paper
        - related_paper_0_url (str): URL of first related paper
        - related_paper_0_similarity_score (float): Similarity score of first related paper
        - related_paper_1_title (str): Title of second related paper
        - related_paper_1_url (str): URL of second related paper
        - related_paper_1_similarity_score (float): Similarity score of second related paper
        - raw_metadata_str (str): JSON string representation of raw metadata
    """
    return {
        "title": "Attention Is All You Need",
        "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
        "author_0": "Ashish Vaswani",
        "author_1": "Noam Shazeer",
        "published_date": "2017-06-12",
        "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "official_code_url_0": "https://github.com/tensorflow/tensor2tensor",
        "official_code_framework_0": "TensorFlow",
        "official_code_url_1": "https://github.com/pytorch/fairseq",
        "official_code_framework_1": "PyTorch",
        "dataset_0": "WMT 2014 English-German",
        "dataset_1": "WMT 2014 English-French",
        "task_0": "Machine Translation",
        "task_1": "Sequence Transduction",
        "method_0": "Transformer",
        "method_1": "Self-Attention",
        "metric_name_0": "BLEU",
        "metric_value_0": 28.4,
        "metric_name_1": "Training Time",
        "metric_value_1": 3600.0,
        "results_summary": "The Transformer achieves state-of-the-art results on English-to-German and English-to-French translation tasks with significantly faster training times.",
        "doi": "10.48550/arXiv.1706.03762",
        "citation_count": 45000,
        "is_open_access": True,
        "related_paper_0_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "related_paper_0_url": "https://paperswithcode.com/paper/bert-pre-training-of-deep-bidirectional",
        "related_paper_0_similarity_score": 0.85,
        "related_paper_1_title": "Image Transformer",
        "related_paper_1_url": "https://paperswithcode.com/paper/image-transformer",
        "related_paper_1_similarity_score": 0.72,
        "raw_metadata_str": '{"paper_url": "https://paperswithcode.com/paper/attention-is-all-you-need", "task": "Machine Translation", "data": []}'
    }

def paperswithcode_client_read_paper_from_url(paper_url: str) -> Dict[str, Any]:
    """
    Explain a paper by URL in PapersWithCode.
    
    Args:
        paper_url (str): The URL of the academic paper on PapersWithCode.
    
    Returns:
        Dict containing detailed information about the paper with the following structure:
        - title (str): The title of the academic paper
        - abstract (str): Summary of the paper's content and contributions
        - authors (List[str]): List of author names associated with the paper
        - published_date (str): Publication date in ISO format (e.g., '2023-01-01')
        - pdf_url (str): Direct URL to the PDF version of the paper
        - official_code_urls (List[Dict]): List of dictionaries containing official code links, each with 'url' and 'framework' if available
        - datasets (List[str]): Names of datasets referenced or used in the paper
        - tasks (List[str]): Machine learning or research tasks associated with the paper
        - methods (List[str]): Key techniques or methodologies proposed or used in the paper
        - metrics (Dict): Performance metrics reported in the paper, mapping metric name to value(s)
        - results_summary (str): High-level summary of results or findings extracted from the paper
        - doi (str): Digital Object Identifier (DOI) for the paper, if available
        - citation_count (int): Number of citations the paper has received
        - is_open_access (bool): Whether the paper is openly accessible
        - related_papers (List[Dict]): List of similar or related papers, each with 'title', 'paper_url', and 'similarity_score'
        - raw_metadata (Dict): Original unprocessed metadata from PapersWithCode API
    
    Raises:
        ValueError: If paper_url is empty or invalid
    """
    if not paper_url or not paper_url.strip():
        raise ValueError("paper_url is required and cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("paperswithcode-client-read_paper_from_url")
    
    # Construct authors list
    authors = []
    if "author_0" in api_data and api_data["author_0"]:
        authors.append(api_data["author_0"])
    if "author_1" in api_data and api_data["author_1"]:
        authors.append(api_data["author_1"])
    
    # Construct official_code_urls list
    official_code_urls = []
    if "official_code_url_0" in api_data and api_data["official_code_url_0"]:
        official_code_urls.append({
            "url": api_data["official_code_url_0"],
            "framework": api_data.get("official_code_framework_0", "")
        })
    if "official_code_url_1" in api_data and api_data["official_code_url_1"]:
        official_code_urls.append({
            "url": api_data["official_code_url_1"],
            "framework": api_data.get("official_code_framework_1", "")
        })
    
    # Construct datasets list
    datasets = []
    if "dataset_0" in api_data and api_data["dataset_0"]:
        datasets.append(api_data["dataset_0"])
    if "dataset_1" in api_data and api_data["dataset_1"]:
        datasets.append(api_data["dataset_1"])
    
    # Construct tasks list
    tasks = []
    if "task_0" in api_data and api_data["task_0"]:
        tasks.append(api_data["task_0"])
    if "task_1" in api_data and api_data["task_1"]:
        tasks.append(api_data["task_1"])
    
    # Construct methods list
    methods = []
    if "method_0" in api_data and api_data["method_0"]:
        methods.append(api_data["method_0"])
    if "method_1" in api_data and api_data["method_1"]:
        methods.append(api_data["method_1"])
    
    # Construct metrics dictionary
    metrics = {}
    if "metric_name_0" in api_data and api_data["metric_name_0"]:
        metrics[api_data["metric_name_0"]] = api_data["metric_value_0"]
    if "metric_name_1" in api_data and api_data["metric_name_1"]:
        metrics[api_data["metric_name_1"]] = api_data["metric_value_1"]
    
    # Construct related_papers list
    related_papers = []
    if "related_paper_0_title" in api_data and api_data["related_paper_0_title"]:
        related_papers.append({
            "title": api_data["related_paper_0_title"],
            "paper_url": api_data["related_paper_0_url"],
            "similarity_score": api_data["related_paper_0_similarity_score"]
        })
    if "related_paper_1_title" in api_data and api_data["related_paper_1_title"]:
        related_papers.append({
            "title": api_data["related_paper_1_title"],
            "paper_url": api_data["related_paper_1_url"],
            "similarity_score": api_data["related_paper_1_similarity_score"]
        })
    
    # Parse raw metadata from JSON string
    import json
    try:
        raw_metadata = json.loads(api_data.get("raw_metadata_str", "{}"))
    except json.JSONDecodeError:
        raw_metadata = {}
    
    # Return structured response
    return {
        "title": api_data.get("title", ""),
        "abstract": api_data.get("abstract", ""),
        "authors": authors,
        "published_date": api_data.get("published_date", ""),
        "pdf_url": api_data.get("pdf_url", ""),
        "official_code_urls": official_code_urls,
        "datasets": datasets,
        "tasks": tasks,
        "methods": methods,
        "metrics": metrics,
        "results_summary": api_data.get("results_summary", ""),
        "doi": api_data.get("doi", ""),
        "citation_count": api_data.get("citation_count", 0),
        "is_open_access": api_data.get("is_open_access", False),
        "related_papers": related_papers,
        "raw_metadata": raw_metadata
    }