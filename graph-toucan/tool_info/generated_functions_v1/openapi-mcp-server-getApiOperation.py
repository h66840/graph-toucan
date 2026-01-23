from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAPI operation details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - openapi (str): Version of the OpenAPI specification
        - info_title (str): Title of the API
        - info_description (str): Description of the API
        - info_version (str): Version of the API
        - info_contact_name (str): Contact name
        - info_contact_email (str): Contact email
        - info_license_name (str): License name
        - info_license_url (str): License URL
        - info_termsOfService (str): Terms of service URL
        - server_0_url (str): First server URL
        - server_0_description (str): Description of first server
        - server_1_url (str): Second server URL
        - server_1_description (str): Description of second server
        - path_operation_method (str): HTTP method for the operation
        - path_operation_summary (str): Summary of the operation
        - path_operation_description (str): Detailed description of the operation
        - path_operation_response_200_description (str): Description of 200 response
        - path_operation_response_200_content_application_json_schema_type (str): Response schema type
        - externalDocs_url (str): URL for external documentation
        - externalDocs_description (str): Description of external docs
        - component_schema_user_type (str): Type of user schema
        - component_schema_user_property_name_type (str): Type of name property in user schema
        - component_schema_user_property_email_type (str): Type of email property in user schema
    """
    return {
        "openapi": "3.0.1",
        "info_title": "Sample API",
        "info_description": "This is a sample API for demonstration purposes.",
        "info_version": "1.0.0",
        "info_contact_name": "API Support",
        "info_contact_email": "support@example.com",
        "info_license_name": "MIT",
        "info_license_url": "https://opensource.org/licenses/MIT",
        "info_termsOfService": "https://example.com/terms",
        "server_0_url": "https://api.example.com/v1",
        "server_0_description": "Production server",
        "server_1_url": "https://staging-api.example.com/v1",
        "server_1_description": "Staging server",
        "path_operation_method": "get",
        "path_operation_summary": "Get user by ID",
        "path_operation_description": "Retrieves a user by their unique identifier.",
        "path_operation_response_200_description": "Successful response with user object",
        "path_operation_response_200_content_application_json_schema_type": "object",
        "externalDocs_url": "https://docs.example.com",
        "externalDocs_description": "Find more info here",
        "component_schema_user_type": "object",
        "component_schema_user_property_name_type": "string",
        "component_schema_user_property_email_type": "string"
    }

def openapi_mcp_server_getApiOperation(id: str, operationIdOrRoute: str) -> Dict[str, Any]:
    """
    Get details about a specific operation from an OpenAPI specification.
    
    Args:
        id (str): API identifier, can be a known ID from openapisearch.com or a URL leading to a raw OpenAPI file
        operationIdOrRoute (str): Operation ID or route path to retrieve
    
    Returns:
        Dict containing OpenAPI specification details with the following structure:
        - openapi (str): version of the OpenAPI specification
        - info (Dict): metadata about the API including title, description, version, contact, license, and termsOfService
        - servers (List[Dict]): list of server objects with URL and description
        - paths (Dict): available paths and operations in the API
        - externalDocs (Dict): external documentation object with URL and description
        - components (Dict): reusable components such as schemas, security schemes, etc.
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    if not id:
        raise ValueError("Parameter 'id' is required")
    if not operationIdOrRoute:
        raise ValueError("Parameter 'operationIdOrRoute' is required")

    # Fetch simulated external data
    api_data = call_external_api("openapi-mcp-server-getApiOperation")
    
    # Construct nested info object
    info = {
        "title": api_data["info_title"],
        "description": api_data["info_description"],
        "version": api_data["info_version"],
        "contact": {
            "name": api_data["info_contact_name"],
            "email": api_data["info_contact_email"]
        },
        "license": {
            "name": api_data["info_license_name"],
            "url": api_data["info_license_url"]
        },
        "termsOfService": api_data["info_termsOfService"]
    }
    
    # Construct servers list
    servers = [
        {
            "url": api_data["server_0_url"],
            "description": api_data["server_0_description"]
        },
        {
            "url": api_data["server_1_url"],
            "description": api_data["server_1_description"]
        }
    ]
    
    # Construct paths object with dynamic route
    paths = {
        operationIdOrRoute: {
            "get": {
                "summary": api_data["path_operation_summary"],
                "description": api_data["path_operation_description"],
                "responses": {
                    "200": {
                        "description": api_data["path_operation_response_200_description"],
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": api_data["path_operation_response_200_content_application_json_schema_type"]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Construct externalDocs object
    externalDocs = {
        "url": api_data["externalDocs_url"],
        "description": api_data["externalDocs_description"]
    }
    
    # Construct components object
    components = {
        "schemas": {
            "User": {
                "type": api_data["component_schema_user_type"],
                "properties": {
                    "name": {
                        "type": api_data["component_schema_user_property_name_type"]
                    },
                    "email": {
                        "type": api_data["component_schema_user_property_email_type"]
                    }
                },
                "required": ["name", "email"]
            }
        }
    }
    
    # Assemble final result
    result = {
        "openapi": api_data["openapi"],
        "info": info,
        "servers": servers,
        "paths": paths,
        "externalDocs": externalDocs,
        "components": components
    }
    
    return result