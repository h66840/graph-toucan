from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for code search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_file_url (str): URL of the first matched file
        - result_0_repository (str): Repository identifier of the first result
        - result_0_language (str): Language of the first result
        - result_0_num_matches (int): Number of matches in the first file
        - result_0_snippet_0 (str): First snippet from the first file (if snippets included)
        - result_0_snippet_1 (str): Second snippet from the first file
        - result_1_file_url (str): URL of the second matched file
        - result_1_repository (str): Repository identifier of the second result
        - result_1_language (str): Language of the second result
        - result_1_num_matches (int): Number of matches in the second file
        - result_1_snippet_0 (str): First snippet from the second file
        - result_1_snippet_1 (str): Second snippet from the second file
        - truncated (bool): Whether results were truncated due to token limit
        - error (str): Error message if any occurred, otherwise empty string
    """
    return {
        "result_0_file_url": "https://github.com/example/repo1/blob/main/src/utils.py",
        "result_0_repository": "github.com/example/repo1",
        "result_0_language": "Python",
        "result_0_num_matches": 3,
        "result_0_snippet_0": 'def validate_input(data):\\n    if not data:\\n        raise ValueError("Invalid input")',
        "result_0_snippet_1": 'result = process(data)\\nreturn result',
        "result_1_file_url": "https://github.com/example/repo2/blob/main/lib/helper.ts",
        "result_1_repository": "github.com/example/repo2",
        "result_1_language": "TypeScript",
        "result_1_num_matches": 2,
        "result_1_snippet_0": 'console.log("Starting service...");\\nawait init();',
        "result_1_snippet_1": 'export const CONFIG = {\\n  timeout: 5000,\\n  retries: 3\\n};',
        "truncated": False,
        "error": ""
    }

def sourcebot_code_search_server_search_code(
    query: str,
    caseSensitive: Optional[bool] = False,
    filterByLanguages: Optional[List[str]] = None,
    filterByRepoIds: Optional[List[str]] = None,
    includeCodeSnippets: Optional[bool] = False,
    maxTokens: Optional[int] = 10000
) -> Dict[str, Any]:
    """
    Fetches code that matches the provided regex pattern in `query`. This is NOT a semantic search.
    Results are returned as an array of matching files, with the file's URL, repository, and language.
    
    If the `includeCodeSnippets` property is true, code snippets containing the matches will be included.
    When referencing a file in your response, **ALWAYS** include the file's external URL as a link.
    **ONLY USE** the `filterByRepoIds` property if the request requires searching a specific repo(s).

    Args:
        query (str): The regex pattern to search for. Spaces and special characters must be escaped with a single backslash.
        caseSensitive (bool, optional): Whether the search should be case sensitive. Defaults to False.
        filterByLanguages (List[str], optional): List of GitHub linguist languages to scope the search.
        filterByRepoIds (List[str], optional): List of Sourcebot-compatible repository IDs to search within.
        includeCodeSnippets (bool, optional): Whether to include code snippets in the response. Defaults to False.
        maxTokens (int, optional): Maximum number of tokens to return. Must be at least 10000. Defaults to 10000.

    Returns:
        Dict containing:
        - results (List[Dict]): List of matched code files with file_url, repository, language, num_matches, and snippets
        - truncated (bool): Whether the response was truncated due to token limit
        - error (str): Error message if the request failed

    Each result dict contains:
        - file_url (str): Full URL to the file in the repository
        - repository (str): Repository identifier in format 'host.com/org/repo'
        - language (str): Programming language of the file
        - num_matches (int): Number of regex matches found in the file
        - snippets (List[str]): Code blocks around matches (only if includeCodeSnippets is True)
    """
    # Input validation
    if not query or not query.strip():
        return {
            "results": [],
            "truncated": False,
            "error": "Query parameter is required and cannot be empty"
        }

    if maxTokens is not None and maxTokens < 10000:
        maxTokens = 10000

    # Call external API (simulated)
    api_data = call_external_api("sourcebot_code_search_server_search_code")

    # Extract error if present
    if api_data.get("error"):
        return {
            "results": [],
            "truncated": api_data.get("truncated", False),
            "error": api_data["error"]
        }

    # Construct results list from flattened API response
    results = []

    for i in range(2):  # Process up to 2 results (0-indexed)
        prefix = f"result_{i}"
        file_url_key = f"{prefix}_file_url"
        if file_url_key not in api_data or not api_data[file_url_key]:
            continue

        result = {
            "file_url": api_data[f"{prefix}_file_url"],
            "repository": api_data[f"{prefix}_repository"],
            "language": api_data[f"{prefix}_language"],
            "num_matches": api_data[f"{prefix}_num_matches"]
        }

        # Add snippets only if requested
        if includeCodeSnippets:
            snippets = []
            snippet_0 = api_data.get(f"{prefix}_snippet_0")
            snippet_1 = api_data.get(f"{prefix}_snippet_1")
            if snippet_0:
                snippets.append(snippet_0)
            if snippet_1:
                snippets.append(snippet_1)
            result["snippets"] = snippets

        results.append(result)

    return {
        "results": results,
        "truncated": api_data.get("truncated", False),
        "error": ""
    }