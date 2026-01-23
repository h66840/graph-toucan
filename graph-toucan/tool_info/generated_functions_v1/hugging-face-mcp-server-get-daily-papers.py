from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face daily papers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_authors_0 (str): First author of the first paper
        - paper_0_authors_1 (str): Second author of the first paper
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_published_date (str): Published date of the first paper in ISO format
        - paper_0_url (str): URL to the first paper
        - paper_0_huggingface_url (str): Hugging Face discussion URL for the first paper
        - paper_0_tags_0 (str): First tag for the first paper
        - paper_0_tags_1 (str): Second tag for the first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_authors_0 (str): First author of the second paper
        - paper_1_authors_1 (str): Second author of the second paper
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_published_date (str): Published date of the second paper in ISO format
        - paper_1_url (str): URL to the second paper
        - paper_1_huggingface_url (str): Hugging Face discussion URL for the second paper
        - paper_1_tags_0 (str): First tag for the second paper
        - paper_1_tags_1 (str): Second tag for the second paper
        - total_count (int): Total number of papers returned
        - date (str): Date for which papers were curated (YYYY-MM-DD)
        - curated_by (str): Name of the curator or source team
        - metadata_retrieval_timestamp (str): Timestamp when data was retrieved (ISO format)
        - metadata_version (str): Version of the API or data format
        - metadata_filters_applied_include_survey (bool): Whether survey filter was applied
        - metadata_filters_applied_include_tutorial (bool): Whether tutorial filter was applied
    """
    return {
        "paper_0_title": "A Survey of Transformer-Based Large Language Models",
        "paper_0_authors_0": "Alice Johnson",
        "paper_0_authors_1": "Bob Smith",
        "paper_0_abstract": "This paper presents a comprehensive survey of recent advancements in transformer-based language models, focusing on scalability, efficiency, and downstream task performance.",
        "paper_0_published_date": "2023-10-01T10:00:00Z",
        "paper_0_url": "https://arxiv.org/abs/2310.0001",
        "paper_0_huggingface_url": "https://huggingface.co/papers/2310.0001",
        "paper_0_tags_0": "NLP",
        "paper_0_tags_1": "Transformers",
        "paper_1_title": "Efficient Vision Transformers for Edge Devices",
        "paper_1_authors_0": "Carol Davis",
        "paper_1_authors_1": "David Wilson",
        "paper_1_abstract": "We propose a novel architecture for vision transformers that reduces computational overhead by 50% while maintaining competitive accuracy on image classification tasks.",
        "paper_1_published_date": "2023-10-01T11:30:00Z",
        "paper_1_url": "https://arxiv.org/abs/2310.0002",
        "paper_1_huggingface_url": "https://huggingface.co/papers/2310.0002",
        "paper_1_tags_0": "Computer Vision",
        "paper_1_tags_1": "Efficient AI",
        "total_count": 2,
        "date": "2023-10-01",
        "curated_by": "Hugging Face Team",
        "metadata_retrieval_timestamp": "2023-10-01T12:00:00Z",
        "metadata_version": "1.0.0",
        "metadata_filters_applied_include_survey": True,
        "metadata_filters_applied_include_tutorial": False,
    }

def hugging_face_mcp_server_get_daily_papers() -> Dict[str, Any]:
    """
    Get the list of daily papers curated by Hugging Face.

    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper entries with keys:
            - title (str)
            - authors (List[str])
            - abstract (str)
            - published_date (str in ISO format)
            - url (str)
            - huggingface_url (str)
            - tags (List[str])
        - total_count (int): Total number of papers returned
        - date (str): The date for which papers were curated (YYYY-MM-DD)
        - curated_by (str): Name or identifier of the curator
        - metadata (Dict): Additional contextual information including:
            - retrieval_timestamp (str in ISO format)
            - version (str)
            - filters_applied (Dict with filter criteria)
    
    Raises:
        KeyError: If expected fields are missing from API response
        ValueError: If data validation fails
    """
    try:
        api_data = call_external_api("hugging-face-mcp-server-get-daily-papers")

        # Construct papers list
        papers = [
            {
                "title": api_data["paper_0_title"],
                "authors": [
                    api_data["paper_0_authors_0"],
                    api_data["paper_0_authors_1"]
                ],
                "abstract": api_data["paper_0_abstract"],
                "published_date": api_data["paper_0_published_date"],
                "url": api_data["paper_0_url"],
                "huggingface_url": api_data["paper_0_huggingface_url"],
                "tags": [
                    api_data["paper_0_tags_0"],
                    api_data["paper_0_tags_1"]
                ]
            },
            {
                "title": api_data["paper_1_title"],
                "authors": [
                    api_data["paper_1_authors_0"],
                    api_data["paper_1_authors_1"]
                ],
                "abstract": api_data["paper_1_abstract"],
                "published_date": api_data["paper_1_published_date"],
                "url": api_data["paper_1_url"],
                "huggingface_url": api_data["paper_1_huggingface_url"],
                "tags": [
                    api_data["paper_1_tags_0"],
                    api_data["paper_1_tags_1"]
                ]
            }
        ]

        # Construct metadata
        metadata = {
            "retrieval_timestamp": api_data["metadata_retrieval_timestamp"],
            "version": api_data["metadata_version"],
            "filters_applied": {
                "include_survey": api_data["metadata_filters_applied_include_survey"],
                "include_tutorial": api_data["metadata_filters_applied_include_tutorial"]
            }
        }

        # Construct final result
        result = {
            "papers": papers,
            "total_count": api_data["total_count"],
            "date": api_data["date"],
            "curated_by": api_data["curated_by"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to process daily papers data: {str(e)}")