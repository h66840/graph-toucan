from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - library_name (str): Name of the selected library
        - library_description (str): Description of the library
        - library_source (str): Source URL of the library documentation
        - documentation_entries_0_title (str): Title of first documentation entry
        - documentation_entries_0_description (str): Description of first entry
        - documentation_entries_0_language (str): Code language of first entry
        - documentation_entries_0_code (str): Code example of first entry
        - documentation_entries_1_title (str): Title of second documentation entry
        - documentation_entries_1_description (str): Description of second entry
        - documentation_entries_1_language (str): Code language of second entry
        - documentation_entries_1_code (str): Code example of second entry
    """
    return {
        "library_name": "Next.js",
        "library_description": "The React Framework for Production",
        "library_source": "https://nextjs.org/docs",
        "documentation_entries_0_title": "Dynamic Routing",
        "documentation_entries_0_description": "Learn how to create dynamic routes in Next.js using file naming conventions.",
        "documentation_entries_0_language": "javascript",
        "documentation_entries_0_code": "function Post({ params }) {\n  return <div>Post: {params.id}</div>;\n}\n\nexport async function generateStaticParams() {\n  return [{ id: '1' }, { id: '2' }, { id: '3' }];\n}\n\nexport default Post;",
        "documentation_entries_1_title": "API Routes",
        "documentation_entries_1_description": "Build API endpoints inside your Next.js app using the pages/api directory.",
        "documentation_entries_1_language": "javascript",
        "documentation_entries_1_code": "export default function handler(req, res) {\n  res.status(200).json({ name: 'John Doe' });\n}"
    }

def docfork_get_library_docs(libraryName: str, topic: str, tokens: Optional[int] = 10000) -> Dict[str, Any]:
    """
    Retrieves up-to-date documentation and code examples for a specified library with focus on a given topic.
    
    Args:
        libraryName (str): Author and library name pair to search for (e.g., 'vercel/next.js', 'reactjs/react.dev')
        topic (str): Topic to focus the documentation on (e.g., 'routing', 'authentication', 'hooks')
        tokens (Optional[int]): Maximum number of tokens to retrieve (default: 10000)
    
    Returns:
        Dict containing:
        - library (Dict): with 'name', 'description', and 'source' fields
        - documentation_entries (List[Dict]): list of entries with 'title', 'description', 'language', and 'code'
    
    Raises:
        ValueError: If libraryName or topic is empty
    """
    if not libraryName:
        raise ValueError("libraryName is required")
    if not topic:
        raise ValueError("topic is required")
    
    # Fetch simulated external data
    api_data = call_external_api("docfork-get-library-docs")
    
    # Construct nested output structure
    result = {
        "library": {
            "name": api_data["library_name"],
            "description": api_data["library_description"],
            "source": api_data["library_source"]
        },
        "documentation_entries": [
            {
                "title": api_data["documentation_entries_0_title"],
                "description": api_data["documentation_entries_0_description"],
                "language": api_data["documentation_entries_0_language"],
                "code": api_data["documentation_entries_0_code"]
            },
            {
                "title": api_data["documentation_entries_1_title"],
                "description": api_data["documentation_entries_1_description"],
                "language": api_data["documentation_entries_1_language"],
                "code": api_data["documentation_entries_1_code"]
            }
        ]
    }
    
    return result