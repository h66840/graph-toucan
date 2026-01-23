from typing import Dict, List, Any, Optional
import datetime
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face Space info.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - name (str): Display name of the Space
        - id (str): Unique identifier of the Space
        - author (str): Username or organization that owns the Space
        - created_at (str): Creation timestamp in ISO 8601 format
        - last_updated (str): Last update timestamp in ISO 8601 format
        - sdk (str): SDK used to build the Space
        - sdk_version (str): Version of the SDK used
        - app_url (str): Public URL where the Space is hosted
        - visibility (str): Visibility status ('public' or 'private')
        - status (str): Current operational status
        - hardware_accelerator (str): Type of accelerator (e.g., 't4', 'a10g')
        - hardware_cpu (str): CPU specification
        - hardware_memory (str): Memory specification
        - storage_used_bytes (int): Used storage in bytes
        - storage_limit_bytes (int): Total storage limit in bytes
        - git_repository (str): URL of the underlying Git repository
        - description (str): Markdown-formatted description
        - tags_0 (str): First tag associated with the Space
        - tags_1 (str): Second tag associated with the Space
        - likes (int): Number of likes or stars
        - concurrents (int): Number of users currently interacting
        - webhook_url (str): Webhook endpoint URL if configured
        - variables_ENV_0_KEY (str): First environment variable key
        - variables_ENV_0_VALUE (str): First environment variable value
        - variables_ENV_1_KEY (str): Second environment variable key
        - variables_ENV_1_VALUE (str): Second environment variable value
        - secrets_0 (str): First secret name
        - secrets_1 (str): Second secret name
    """
    base_time = datetime.datetime.now(datetime.timezone.utc)
    created_at = (base_time - datetime.timedelta(days=30)).isoformat()
    last_updated = (base_time - datetime.timedelta(hours=2)).isoformat()

    return {
        "name": "Diffusers Demo",
        "id": "huggingface/diffusers-demo",
        "author": "huggingface",
        "created_at": created_at,
        "last_updated": last_updated,
        "sdk": "gradio",
        "sdk_version": "3.37.0",
        "app_url": "https://huggingface.co/spaces/huggingface/diffusers-demo",
        "visibility": "public",
        "status": "running",
        "hardware_accelerator": "t4",
        "hardware_cpu": "2vCPU",
        "hardware_memory": "16GB",
        "storage_used_bytes": 1073741824,
        "storage_limit_bytes": 4294967296,
        "git_repository": "https://huggingface.co/spaces/huggingface/diffusers-demo",
        "description": "# Diffusers Demo\nThis space demonstrates text-to-image generation using diffusion models.",
        "tags_0": "diffusion",
        "tags_1": "image-generation",
        "likes": 1542,
        "concurrents": 23,
        "webhook_url": "https://huggingface.co/api/spaces/huggingface/diffusers-demo/webhook",
        "variables_ENV_0_KEY": "MODEL_NAME",
        "variables_ENV_0_VALUE": "runwayml/stable-diffusion-v1-5",
        "variables_ENV_1_KEY": "USE_AUTH",
        "variables_ENV_1_VALUE": "false",
        "secrets_0": "HF_TOKEN",
        "secrets_1": "API_KEY"
    }


def hugging_face_mcp_server_get_space_info(space_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific Hugging Face Space.
    
    Args:
        space_id (str): The ID of the Space (e.g., 'huggingface/diffusers-demo')
    
    Returns:
        Dict containing detailed information about the Space with the following structure:
        - name (str): The display name of the Space
        - id (str): The unique identifier of the Space
        - author (str): Username or organization that owns the Space
        - created_at (str): Timestamp when the Space was created, in ISO 8601 format
        - last_updated (str): Timestamp of the most recent update to the Space, in ISO 8601 format
        - sdk (str): The SDK used to build the Space
        - sdk_version (str): Version of the SDK used
        - app_url (str): Public URL where the Space application is hosted
        - visibility (str): Indicates whether the Space is 'public' or 'private'
        - status (str): Current operational status of the Space
        - hardware (Dict): Details about allocated hardware
            - accelerator (str): Type of accelerator
            - cpu (str): CPU specification
            - memory (str): Memory specification
        - storage (Dict): Information about storage usage and limits
            - used_bytes (int): Used storage in bytes
            - limit_bytes (int): Total storage limit in bytes
        - git_repository (str): URL of the underlying Git repository
        - description (str): Markdown-formatted description of the Space
        - tags (List[str]): List of tags associated with the Space
        - likes (int): Number of likes or stars the Space has received
        - concurrents (int): Number of users currently interacting with the Space
        - webhook_url (str): Endpoint URL for receiving webhook events
        - variables (Dict): Environment variables defined for the Space
        - secrets (List[str]): List of secret names available in the Space environment
    
    Raises:
        ValueError: If space_id is empty or invalid
    """
    if not space_id or not isinstance(space_id, str) or not space_id.strip():
        raise ValueError("space_id must be a non-empty string")
    
    # Call external API to get flat data
    api_data = call_external_api("hugging-face-mcp-server-get-space-info")
    
    # Construct nested hardware dict
    hardware = {
        "accelerator": api_data["hardware_accelerator"],
        "cpu": api_data["hardware_cpu"],
        "memory": api_data["hardware_memory"]
    }
    
    # Construct nested storage dict
    storage = {
        "used_bytes": api_data["storage_used_bytes"],
        "limit_bytes": api_data["storage_limit_bytes"]
    }
    
    # Construct list of tags
    tags = [
        api_data["tags_0"],
        api_data["tags_1"]
    ]
    
    # Construct environment variables dict
    variables = {
        api_data["variables_ENV_0_KEY"]: api_data["variables_ENV_0_VALUE"],
        api_data["variables_ENV_1_KEY"]: api_data["variables_ENV_1_VALUE"]
    }
    
    # Construct list of secrets
    secrets = [
        api_data["secrets_0"],
        api_data["secrets_1"]
    ]
    
    # Build final result matching output schema
    result = {
        "name": api_data["name"],
        "id": api_data["id"],
        "author": api_data["author"],
        "created_at": api_data["created_at"],
        "last_updated": api_data["last_updated"],
        "sdk": api_data["sdk"],
        "sdk_version": api_data["sdk_version"],
        "app_url": api_data["app_url"],
        "visibility": api_data["visibility"],
        "status": api_data["status"],
        "hardware": hardware,
        "storage": storage,
        "git_repository": api_data["git_repository"],
        "description": api_data["description"],
        "tags": tags,
        "likes": api_data["likes"],
        "concurrents": api_data["concurrents"],
        "webhook_url": api_data["webhook_url"],
        "variables": variables,
        "secrets": secrets
    }
    
    return result