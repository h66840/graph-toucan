from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face collection info.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - collection_name (str): The display name of the collection
        - description (str): A detailed description of the collection's purpose and contents
        - created_at (str): Timestamp when the collection was created, in ISO 8601 format
        - last_updated (str): Timestamp when the collection was last modified, in ISO 8601 format
        - creator_namespace (str): Namespace of the creator (user or organization)
        - creator_type (str): Type of creator (user or org)
        - creator_avatar_url (str): URL to the avatar image of the creator
        - item_count (int): Total number of items in the collection
        - item_0_id (str): ID of the first item in the collection
        - item_0_type (str): Type of the first item (model/dataset/space)
        - item_0_name (str): Name of the first item
        - item_0_url (str): URL of the first item
        - item_0_created_at (str): Creation timestamp of the first item in ISO 8601
        - item_0_summary (str): Summary of the first item
        - item_1_id (str): ID of the second item in the collection
        - item_1_type (str): Type of the second item (model/dataset/space)
        - item_1_name (str): Name of the second item
        - item_1_url (str): URL of the second item
        - item_1_created_at (str): Creation timestamp of the second item in ISO 8601
        - item_1_summary (str): Summary of the second item
        - visibility (str): Whether the collection is public or private
        - tag_0 (str): First tag associated with the collection
        - tag_1 (str): Second tag associated with the collection
        - metadata_config (str): Configuration metadata of the collection
        - metadata_stats_views (int): Number of views as part of usage stats
        - is_pinned (bool): Indicates whether this collection is pinned by the namespace
    """
    return {
        "collection_name": "NLP Models Collection",
        "description": "A curated list of state-of-the-art NLP models for text classification and generation.",
        "created_at": "2023-01-15T08:30:00Z",
        "last_updated": "2023-10-20T14:22:45Z",
        "creator_namespace": "john_doe",
        "creator_type": "user",
        "creator_avatar_url": "https://huggingface.co/avatar/john_doe.jpg",
        "item_count": 2,
        "item_0_id": "bert-base-uncased",
        "item_0_type": "model",
        "item_0_name": "BERT Base Uncased",
        "item_0_url": "https://huggingface.co/bert-base-uncased",
        "item_0_created_at": "2022-12-01T10:00:00Z",
        "item_0_summary": "A pre-trained BERT model on English Wikipedia and BooksCorpus.",
        "item_1_id": "gpt2-finetuned-sst2",
        "item_1_type": "model",
        "item_1_name": "GPT-2 Fine-tuned on SST-2",
        "item_1_url": "https://huggingface.co/gpt2-finetuned-sst2",
        "item_1_created_at": "2023-01-10T16:45:30Z",
        "item_1_summary": "GPT-2 model fine-tuned for sentiment analysis on the SST-2 dataset.",
        "visibility": "public",
        "tag_0": "nlp",
        "tag_1": "models",
        "metadata_config": "default",
        "metadata_stats_views": 1500,
        "is_pinned": True
    }

def hugging_face_mcp_server_get_collection_info(collection_id: str, namespace: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific collection on Hugging Face.
    
    Args:
        collection_id (str): The ID part of the collection
        namespace (str): The namespace of the collection (user or organization)
    
    Returns:
        Dict containing detailed information about the collection with the following keys:
        - collection_name (str): The display name of the collection
        - description (str): A detailed description of the collection's purpose and contents
        - created_at (str): Timestamp when the collection was created, in ISO 8601 format
        - last_updated (str): Timestamp when the collection was last modified, in ISO 8601 format
        - creator (Dict): Information about the creator with keys: namespace, type, avatar_url
        - item_count (int): Total number of items in the collection
        - items (List[Dict]): List of items in the collection, each with id, type, name, url, created_at, summary
        - visibility (str): Whether the collection is public or private
        - tags (List[str]): Tags associated with the collection
        - metadata (Dict): Additional structured metadata like config or stats
        - is_pinned (bool): Whether the collection is pinned by the namespace
    
    Raises:
        ValueError: If collection_id or namespace is empty
    """
    if not collection_id:
        raise ValueError("collection_id is required")
    if not namespace:
        raise ValueError("namespace is required")

    # Fetch simulated external data
    api_data = call_external_api("hugging-face-mcp-server-get-collection-info")

    # Construct nested structure for creator
    creator = {
        "namespace": api_data["creator_namespace"],
        "type": api_data["creator_type"],
        "avatar_url": api_data["creator_avatar_url"]
    }

    # Construct list of items
    items = [
        {
            "id": api_data["item_0_id"],
            "type": api_data["item_0_type"],
            "name": api_data["item_0_name"],
            "url": api_data["item_0_url"],
            "created_at": api_data["item_0_created_at"],
            "summary": api_data["item_0_summary"]
        },
        {
            "id": api_data["item_1_id"],
            "type": api_data["item_1_type"],
            "name": api_data["item_1_name"],
            "url": api_data["item_1_url"],
            "created_at": api_data["item_1_created_at"],
            "summary": api_data["item_1_summary"]
        }
    ]

    # Construct tags list
    tags = [api_data["tag_0"], api_data["tag_1"]]

    # Construct metadata dict
    metadata = {
        "config": api_data["metadata_config"],
        "stats": {
            "views": api_data["metadata_stats_views"]
        }
    }

    # Build final result matching output schema
    result = {
        "collection_name": api_data["collection_name"],
        "description": api_data["description"],
        "created_at": api_data["created_at"],
        "last_updated": api_data["last_updated"],
        "creator": creator,
        "item_count": api_data["item_count"],
        "items": items,
        "visibility": api_data["visibility"],
        "tags": tags,
        "metadata": metadata,
        "is_pinned": api_data["is_pinned"]
    }

    return result