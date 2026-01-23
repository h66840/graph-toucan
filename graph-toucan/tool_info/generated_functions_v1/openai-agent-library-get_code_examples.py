from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAI Agents SDK code examples.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - examples_0_path (str): Path of the first code example
        - examples_0_url (str): URL of the first code example
        - examples_0_content (str): Content of the first code example
        - examples_0_matched_by (str): Match reason for the first example
        - examples_1_path (str): Path of the second code example
        - examples_1_url (str): URL of the second code example
        - examples_1_content (str): Content of the second code example
        - examples_1_matched_by (str): Match reason for the second example
        - error (str): Error message if no examples found
        - debug_info_search_topic (str): The topic that was searched
        - debug_info_search_terms_0 (str): First search term used
        - debug_info_search_terms_1 (str): Second search term used
        - debug_info_errors (str): Any internal errors during search
    """
    return {
        "examples_0_path": "agents/assistant_streaming.py",
        "examples_0_url": "https://github.com/openai/agents-sdk/blob/main/examples/assistant_streaming.py",
        "examples_0_content": 'from openai import Agent\n\ndef create_streaming_agent():\n    agent = Agent(model="gpt-4")\n    for event in agent.run_stream(prompt="Hello"):\n        print(event)\n',
        "examples_0_matched_by": "keyword",
        "examples_1_path": "tools/custom_tool_usage.py",
        "examples_1_url": "https://github.com/openai/agents-sdk/blob/main/examples/custom_tool_usage.py",
        "examples_1_content": 'from openai import Agent, Tool\n\nclass Calculator(Tool):\n    name = "calculator"\n    description = "performs math operations"\n\n    def call(self, expression: str) -> str:\n        return str(eval(expression))\n',
        "examples_1_matched_by": "semantic",
        "error": "",
        "debug_info_search_topic": "agent streaming and custom tools",
        "debug_info_search_terms_0": "streaming",
        "debug_info_search_terms_1": "custom tools",
        "debug_info_errors": None
    }

def openai_agent_library_get_code_examples(topic: str) -> Dict[str, Any]:
    """
    Get code examples related to a specific OpenAI Agents SDK topic.
    
    Args:
        topic (str): The topic to search code examples for (required)
    
    Returns:
        Dict containing:
        - examples (List[Dict]): List of code example objects with 'path', 'url', 'content', and 'matched_by' fields
        - error (Optional[str]): Error message if no examples found
        - debug_info (Dict): Debugging metadata including search topic, terms, and internal errors
    """
    if not topic or not topic.strip():
        return {
            "examples": [],
            "error": "Topic is required but was not provided or empty.",
            "debug_info": {
                "search_topic": "",
                "search_terms": [],
                "errors": "Input validation failed: topic is required"
            }
        }

    topic_lower = topic.lower().strip()
    api_data = call_external_api("openai-agent-library-get_code_examples")

    # Construct examples list from indexed fields
    examples: List[Dict[str, str]] = []
    for i in range(2):
        path_key = f"examples_{i}_path"
        url_key = f"examples_{i}_url"
        content_key = f"examples_{i}_content"
        matched_by_key = f"examples_{i}_matched_by"
        
        if all(key in api_data and api_data[key] for key in [path_key, url_key, content_key, matched_by_key]):
            examples.append({
                "path": api_data[path_key],
                "url": api_data[url_key],
                "content": api_data[content_key],
                "matched_by": api_data[matched_by_key]
            })

    # Construct debug_info
    debug_info = {
        "search_topic": api_data.get("debug_info_search_topic", topic),
        "search_terms": [],
        "errors": api_data.get("debug_info_errors")
    }
    
    # Collect search terms
    for i in range(2):
        term_key = f"debug_info_search_terms_{i}"
        if term_key in api_data and api_data[term_key]:
            debug_info["search_terms"].append(api_data[term_key])

    # Return final structured response
    return {
        "examples": examples,
        "error": api_data.get("error", "") or None if api_data.get("error") else None,
        "debug_info": debug_info
    }