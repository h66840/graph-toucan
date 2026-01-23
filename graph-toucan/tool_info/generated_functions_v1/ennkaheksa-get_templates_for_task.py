from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for getting templates for a task.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - task (str): the type of task for which templates are retrieved
        - description (str): description of what the task involves and what kind of workflows it supports
        - count (int): total number of templates returned in this response
        - template_0_id (int): unique identifier for the first template
        - template_0_name (str): title of the first template workflow
        - template_0_description (str): detailed explanation of the first template’s purpose
        - template_0_author_name (str): full name of the first template's author
        - template_0_author_username (str): n8n.io username of the first template's author
        - template_0_author_verified (bool): whether the first template's author is verified
        - template_0_nodes_0 (str): first node used in the first template
        - template_0_nodes_1 (str): second node used in the first template
        - template_0_views (int): number of times the first template has been viewed
        - template_0_created (str): ISO 8601 timestamp when the first template was published
        - template_0_url (str): public URL to the first template on n8n.io
        - template_1_id (int): unique identifier for the second template
        - template_1_name (str): title of the second template workflow
        - template_1_description (str): detailed explanation of the second template’s purpose
        - template_1_author_name (str): full name of the second template's author
        - template_1_author_username (str): n8n.io username of the second template's author
        - template_1_author_verified (bool): whether the second template's author is verified
        - template_1_nodes_0 (str): first node used in the second template
        - template_1_nodes_1 (str): second node used in the second template
        - template_1_views (int): number of times the second template has been viewed
        - template_1_created (str): ISO 8601 timestamp when the second template was published
        - template_1_url (str): public URL to the second template on n8n.io
    """
    return {
        "task": "email_automation",
        "description": "Automate sending, receiving, and processing emails using n8n workflows. Supports Gmail, Outlook, SMTP, and more.",
        "count": 2,
        "template_0_id": 101,
        "template_0_name": "Send Daily Digest Email",
        "template_0_description": "This template sends a daily digest email with summarized data from various sources. Ideal for reporting and team updates.",
        "template_0_author_name": "John Doe",
        "template_0_author_username": "johndoe_n8n",
        "template_0_author_verified": True,
        "template_0_nodes_0": "Schedule Trigger",
        "template_0_nodes_1": "Email",
        "template_0_views": 1500,
        "template_0_created": "2023-04-10T08:30:00Z",
        "template_0_url": "https://n8n.io/templates/send-daily-digest",
        "template_1_id": 102,
        "template_1_name": "Process Incoming Emails",
        "template_1_description": "Automatically process incoming emails, extract attachments, and save data to cloud storage or databases.",
        "template_1_author_name": "Jane Smith",
        "template_1_author_username": "janesmith_n8n",
        "template_1_author_verified": False,
        "template_1_nodes_0": "IMAP",
        "template_1_nodes_1": "Google Drive",
        "template_1_views": 980,
        "template_1_created": "2023-05-15T12:45:00Z",
        "template_1_url": "https://n8n.io/templates/process-incoming-emails"
    }

def ennkaheksa_get_templates_for_task(task: str) -> Dict[str, Any]:
    """
    Get recommended templates for common automation tasks.
    
    Args:
        task (str): The type of task to get templates for. 
                   Valid options: ai_automation, data_sync, webhook_processing, email_automation,
                   slack_integration, data_transformation, file_processing, scheduling,
                   api_integration, database_operations.
    
    Returns:
        Dict containing:
        - task (str): the type of task for which templates are retrieved
        - description (str): description of what the task involves and what kind of workflows it supports
        - count (int): total number of templates returned in this response
        - templates (List[Dict]): list of template objects with fields:
          - id (int)
          - name (str)
          - description (str)
          - author (Dict with name, username, verified)
          - nodes (List[str])
          - views (int)
          - created (str): ISO 8601 timestamp
          - url (str)
    
    Raises:
        ValueError: If task is not one of the allowed values
    """
    allowed_tasks = [
        "ai_automation", "data_sync", "webhook_processing", "email_automation",
        "slack_integration", "data_transformation", "file_processing",
        "scheduling", "api_integration", "database_operations"
    ]
    
    if not task:
        raise ValueError("Parameter 'task' is required")
    
    if task not in allowed_tasks:
        raise ValueError(f"Invalid task: {task}. Must be one of {allowed_tasks}")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("ennkaheksa-get_templates_for_task")
    
    # Construct templates list from flattened API response
    templates = [
        {
            "id": api_data["template_0_id"],
            "name": api_data["template_0_name"],
            "description": api_data["template_0_description"],
            "author": {
                "name": api_data["template_0_author_name"],
                "username": api_data["template_0_author_username"],
                "verified": api_data["template_0_author_verified"]
            },
            "nodes": [
                api_data["template_0_nodes_0"],
                api_data["template_0_nodes_1"]
            ],
            "views": api_data["template_0_views"],
            "created": api_data["template_0_created"],
            "url": api_data["template_0_url"]
        },
        {
            "id": api_data["template_1_id"],
            "name": api_data["template_1_name"],
            "description": api_data["template_1_description"],
            "author": {
                "name": api_data["template_1_author_name"],
                "username": api_data["template_1_author_username"],
                "verified": api_data["template_1_author_verified"]
            },
            "nodes": [
                api_data["template_1_nodes_0"],
                api_data["template_1_nodes_1"]
            ],
            "views": api_data["template_1_views"],
            "created": api_data["template_1_created"],
            "url": api_data["template_1_url"]
        }
    ]
    
    # Return final structured response
    return {
        "task": api_data["task"],
        "description": api_data["description"],
        "count": api_data["count"],
        "templates": templates
    }