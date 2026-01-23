from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face model information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - id (str): unique identifier of the model
        - name (str): full name of the model including namespace
        - author (str): username or organization that created the model
        - pipeline_tag (str): primary task type of the model
        - downloads (int): total number of downloads for the model
        - likes (int): number of community likes or upvotes for the model
        - lastModified (str): ISO 8601 timestamp string indicating when the model was last updated
        - description (str): textual description of the model
        - tag_0 (str): first tag associated with the model
        - tag_1 (str): second tag associated with the model
    """
    return {
        "id": "12345",
        "name": "google/bert-base-uncased",
        "author": "google",
        "pipeline_tag": "text-classification",
        "downloads": 1500000,
        "likes": 5000,
        "lastModified": "2023-04-15T10:30:00Z",
        "description": "A base-uncased BERT model from Google.",
        "tag_0": "bert",
        "tag_1": "pytorch"
    }

def hugging_face_mcp_server_get_model_info(model_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific model from Hugging Face.
    
    Args:
        model_id (str): The ID of the model (e.g., 'google/bert-base-uncased')
    
    Returns:
        Dict containing detailed model information with the following keys:
        - id (str): unique identifier of the model
        - name (str): full name of the model including namespace
        - author (str): username or organization that created the model
        - tags (List[str]): list of tags associated with the model
        - pipeline_tag (str): primary task type of the model
        - downloads (int): total number of downloads
        - likes (int): number of community likes
        - lastModified (str): ISO 8601 timestamp of last update
        - description (str): model description
    
    Raises:
        ValueError: If model_id is empty or not a string
    """
    if not model_id or not isinstance(model_id, str):
        raise ValueError("model_id must be a non-empty string")
    
    # Call external API to get model data (simulated)
    api_data = call_external_api("hugging-face-mcp-server-get-model-info")
    
    # Construct the output structure with proper nesting
    result = {
        "id": api_data["id"],
        "name": api_data["name"],
        "author": api_data["author"],
        "tags": [
            api_data["tag_0"],
            api_data["tag_1"]
        ],
        "pipeline_tag": api_data["pipeline_tag"],
        "downloads": api_data["downloads"],
        "likes": api_data["likes"],
        "lastModified": api_data["lastModified"],
        "description": api_data["description"]
    }
    
    return result