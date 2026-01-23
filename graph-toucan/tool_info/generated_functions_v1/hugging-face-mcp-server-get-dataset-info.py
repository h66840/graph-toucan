from typing import Dict, List, Any
import datetime
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching dataset information from Hugging Face API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - id (str): Unique identifier of the dataset on Hugging Face
        - author (str): Username or organization that created or uploaded the dataset
        - tag_0 (str): First metadata tag describing the dataset
        - tag_1 (str): Second metadata tag describing the dataset
        - downloads (int): Total number of times the dataset has been downloaded
        - likes (int): Number of community likes or upvotes the dataset has received
        - lastModified (str): ISO 8601 timestamp indicating when the dataset was last updated
        - description (str): Textual description of the dataset, including source, content, and usage notes
    """
    # Generate realistic mock data based on dataset_id (tool_name)
    sample_ids = ["squad", "glue", "imdb", "wikihow", "cnn_dailymail"]
    tasks = ["question-answering", "text-classification", "summarization", "language-modeling"]
    domains = ["news", "academic", "social-media", "wikipedia", "books"]
    licenses = ["apache-2.0", "mit", "cc-by-4.0", "openrail", "unknown"]

    dataset_id = "squad" if "squad" in tool_name.lower() else random.choice(sample_ids)
    task = random.choice(tasks)
    domain = random.choice(domains)
    license_tag = random.choice(licenses)

    return {
        "id": dataset_id,
        "author": f"{dataset_id}_creator",
        "tag_0": task,
        "tag_1": domain,
        "downloads": random.randint(10000, 5000000),
        "likes": random.randint(100, 20000),
        "lastModified": (
            datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
        ).isoformat(),
        "description": (
            f"This is a synthetic dataset mock for {dataset_id}. "
            f"It is commonly used for {task} tasks in the {domain} domain. "
            f"For more information, visit https://huggingface.co/datasets/{dataset_id}"
        ),
    }


def hugging_face_mcp_server_get_dataset_info(dataset_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific dataset from Hugging Face.

    Args:
        dataset_id (str): The ID of the dataset (e.g., 'squad')

    Returns:
        Dict[str, Any]: Dictionary containing detailed dataset information with the following keys:
            - id (str): Unique identifier of the dataset on Hugging Face
            - author (str): Username or organization that created or uploaded the dataset
            - tags (List[str]): List of metadata tags describing properties such as task type, language, size, format, and licensing
            - downloads (int): Total number of times the dataset has been downloaded
            - likes (int): Number of community likes or upvotes the dataset has received
            - lastModified (str): ISO 8601 timestamp indicating when the dataset was last updated
            - description (str): Textual description of the dataset, including source, content, and usage notes

    Raises:
        ValueError: If dataset_id is empty or not a string
    """
    # Input validation
    if not dataset_id or not isinstance(dataset_id, str):
        raise ValueError("dataset_id must be a non-empty string")

    # Call external API to get flattened data
    api_data = call_external_api(f"hugging-face-mcp-server-get-dataset-info-{dataset_id}")

    # Construct the output structure with proper nesting
    result = {
        "id": api_data["id"],
        "author": api_data["author"],
        "tags": [api_data["tag_0"], api_data["tag_1"]],
        "downloads": api_data["downloads"],
        "likes": api_data["likes"],
        "lastModified": api_data["lastModified"],
        "description": api_data["description"],
    }

    return result