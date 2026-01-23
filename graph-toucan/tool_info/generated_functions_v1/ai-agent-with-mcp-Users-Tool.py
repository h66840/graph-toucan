from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - user_0_id (int): First user's unique identifier
        - user_0_name (str): First user's full name
        - user_0_email (str): First user's email address
        - user_0_role (str): First user's role in the system
        - user_1_id (int): Second user's unique identifier
        - user_1_name (str): Second user's full name
        - user_1_email (str): Second user's email address
        - user_1_role (str): Second user's role in the system
        - total_count (int): Total number of users available from the API
        - page (int): Current page number in pagination
        - per_page (int): Number of users returned per page
        - has_more (bool): Whether more pages are available
        - metadata_timestamp (str): Timestamp of the request
        - metadata_api_version (str): Version of the API used
        - metadata_filter_role (str): Role filter applied on server side, if any
    """
    return {
        "user_0_id": 1,
        "user_0_name": "Alice Johnson",
        "user_0_email": "alice.johnson@example.com",
        "user_0_role": "admin",
        "user_1_id": 2,
        "user_1_name": "Bob Smith",
        "user_1_email": "bob.smith@example.com",
        "user_1_role": "user",
        "total_count": 50,
        "page": 1,
        "per_page": 2,
        "has_more": True,
        "metadata_timestamp": "2023-10-05T12:34:56Z",
        "metadata_api_version": "v2",
        "metadata_filter_role": "all"
    }

def ai_agent_with_mcp_Users_Tool() -> Dict[str, Any]:
    """
    Fetches a list of users from an external API.

    Returns:
        Dict containing:
        - users (List[Dict]): List of user objects with id, name, email, and role
        - total_count (int): Total number of users available
        - page (int): Current page number
        - per_page (int): Number of users per page
        - has_more (bool): Whether more pages are available
        - metadata (Dict): Additional request information including timestamp, API version, and filters
    """
    try:
        api_data = call_external_api("ai-agent-with-mcp-Users Tool")

        users = [
            {
                "id": api_data["user_0_id"],
                "name": api_data["user_0_name"],
                "email": api_data["user_0_email"],
                "role": api_data["user_0_role"]
            },
            {
                "id": api_data["user_1_id"],
                "name": api_data["user_1_name"],
                "email": api_data["user_1_email"],
                "role": api_data["user_1_role"]
            }
        ]

        metadata = {
            "timestamp": api_data["metadata_timestamp"],
            "api_version": api_data["metadata_api_version"],
            "filter_role": api_data["metadata_filter_role"]
        }

        result = {
            "users": users,
            "total_count": api_data["total_count"],
            "page": api_data["page"],
            "per_page": api_data["per_page"],
            "has_more": api_data["has_more"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching user data: {str(e)}")