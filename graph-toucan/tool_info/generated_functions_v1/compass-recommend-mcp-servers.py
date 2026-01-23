from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MCP server recommendations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first recommended MCP server
        - result_0_description (str): Description of the first recommended MCP server
        - result_0_github_url (str): GitHub URL of the first recommended MCP server
        - result_0_similarity (float): Similarity score of the first recommendation
        - result_1_title (str): Title of the second recommended MCP server
        - result_1_description (str): Description of the second recommended MCP server
        - result_1_github_url (str): GitHub URL of the second recommended MCP server
        - result_1_similarity (float): Similarity score of the second recommendation
    """
    return {
        "result_0_title": "aws-lambda-mcp-server",
        "result_0_description": "MCP Server for deploying AWS Lambda functions with Python 3.9 runtime support",
        "result_0_github_url": "https://github.com/mcp-servers/aws-lambda-mcp",
        "result_0_similarity": 0.95,
        "result_1_title": "stripe-webhook-mcp-handler",
        "result_1_description": "MCP Server for handling Stripe webhook events including refund processing",
        "result_1_github_url": "https://github.com/mcp-servers/stripe-webhook-mcp",
        "result_1_similarity": 0.87
    }

def compass_recommend_mcp_servers(query: str) -> Dict[str, Any]:
    """
    Recommends external MCP servers based on a specific query describing the required server.
    
    The query should be specific and actionable, including:
    - Target platform/vendor (e.g. AWS, Stripe, MongoDB)
    - Exact operation/service (e.g. Lambda deployment, webhook handling)
    - Additional context if applicable (e.g. Python, refund events)
    
    Args:
        query (str): Description for the MCP Server needed. Must be specific and actionable.
    
    Returns:
        Dict containing a list of recommended MCP servers with their title, description, 
        GitHub URL, and similarity score.
        
    Example:
        >>> compass_recommend_mcp_servers("MCP Server for AWS Lambda Python3.9 deployment")
        {
            "results": [
                {
                    "title": "aws-lambda-mcp-server",
                    "description": "MCP Server for deploying AWS Lambda functions with Python 3.9 runtime support",
                    "github_url": "https://github.com/mcp-servers/aws-lambda-mcp",
                    "similarity": 0.95
                },
                {
                    "title": "stripe-webhook-mcp-handler",
                    "description": "MCP Server for handling Stripe webhook events including refund processing",
                    "github_url": "https://github.com/mcp-servers/stripe-webhook-mcp",
                    "similarity": 0.87
                }
            ]
        }
    
    Raises:
        ValueError: If the query is missing or empty.
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    
    # Normalize query for internal processing
    normalized_query = query.strip().lower()
    
    # Call external API to get flat response data
    api_data = call_external_api("compass-recommend-mcp-servers")
    
    # Construct results list from flat API data
    results = [
        {
            "title": api_data["result_0_title"],
            "description": api_data["result_0_description"],
            "github_url": api_data["result_0_github_url"],
            "similarity": api_data["result_0_similarity"]
        },
        {
            "title": api_data["result_1_title"],
            "description": api_data["result_1_description"],
            "github_url": api_data["result_1_github_url"],
            "similarity": api_data["result_1_similarity"]
        }
    ]
    
    # Return structured response matching output schema
    return {"results": results}