from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for multi-LLM cross-check.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - llm_0_name (str): Name of the first LLM (e.g., "GPT-4")
        - llm_0_response (str): Response from the first LLM or error message
        - llm_1_name (str): Name of the second LLM (e.g., "Claude-3")
        - llm_1_response (str): Response from the second LLM or error message
    """
    return {
        "llm_0_name": "GPT-4",
        "llm_0_response": '{"completion": "Based on the prompt, here is my analysis: ..."}',
        "llm_1_name": "Claude-3",
        "llm_1_response": '{"completion": "I interpret the prompt as follows: ..."}'
    }

def multi_llm_cross_check_server_cross_check(prompt: str) -> Dict[str, Any]:
    """
    Cross-check answers from multiple public LLM APIs given a prompt.
    The goal is to show a list of answers from different LLMs.

    Args:
        prompt (str): The input prompt to send to the LLMs.

    Returns:
        Dict[str, Any]: A dictionary containing the responses from each LLM.
                        Each key is the name of an LLM, and its value is either:
                        - The response from the LLM in JSON format (as string or dict)
                        - An error message if the request to the LLM failed
    """
    if not isinstance(prompt, str):
        return {"error": "Prompt must be a string"}
    
    if not prompt.strip():
        return {"error": "Prompt cannot be empty"}

    try:
        api_data = call_external_api("multi-llm-cross-check-server-cross_check")
        
        responses = {}
        
        # Construct responses dictionary from flattened API data
        llm_0_name = api_data.get("llm_0_name", "Unknown LLM")
        llm_0_response = api_data.get("llm_0_response", "Error: No response received")
        responses[llm_0_name] = llm_0_response
        
        llm_1_name = api_data.get("llm_1_name", "Unknown LLM")
        llm_1_response = api_data.get("llm_1_response", "Error: No response received")
        responses[llm_1_name] = llm_1_response

        return {"responses": responses}
    
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}