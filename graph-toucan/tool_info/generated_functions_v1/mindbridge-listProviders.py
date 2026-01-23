from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing LLM providers and models.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - provider_0_name (str): Name of the first provider
        - provider_0_model_0 (str): First model name for provider 0
        - provider_0_model_1 (str): Second model name for provider 0
        - provider_0_supportsReasoning (bool): Whether provider 0 supports reasoning
        - provider_1_name (str): Name of the second provider
        - provider_1_model_0 (str): First model name for provider 1
        - provider_1_model_1 (str): Second model name for provider 1
        - provider_1_supportsReasoning (bool): Whether provider 1 supports reasoning
    """
    return {
        "provider_0_name": "OpenAI",
        "provider_0_model_0": "gpt-4",
        "provider_0_model_1": "gpt-3.5-turbo",
        "provider_0_supportsReasoning": True,
        "provider_1_name": "Anthropic",
        "provider_1_model_0": "claude-3-opus",
        "provider_1_model_1": "claude-3-sonnet",
        "provider_1_supportsReasoning": True
    }

def mindbridge_listProviders() -> Dict[str, Any]:
    """
    List all configured LLM providers and their available models.
    
    Returns:
        Dict containing:
        - providers (Dict): mapping of provider names (str) to their configuration,
          each containing 'models' (List[str]) and 'supportsReasoning' (bool)
          
    Example:
        {
            "providers": {
                "OpenAI": {
                    "models": ["gpt-4", "gpt-3.5-turbo"],
                    "supportsReasoning": True
                },
                "Anthropic": {
                    "models": ["claude-3-opus", "claude-3-sonnet"],
                    "supportsReasoning": True
                }
            }
        }
    """
    try:
        api_data = call_external_api("mindbridge-listProviders")
        
        providers = {}
        
        # Process first provider
        provider_0_name = api_data.get("provider_0_name")
        if provider_0_name:
            providers[provider_0_name] = {
                "models": [
                    api_data.get("provider_0_model_0", ""),
                    api_data.get("provider_0_model_1", "")
                ],
                "supportsReasoning": api_data.get("provider_0_supportsReasoning", False)
            }
        
        # Process second provider
        provider_1_name = api_data.get("provider_1_name")
        if provider_1_name:
            providers[provider_1_name] = {
                "models": [
                    api_data.get("provider_1_model_0", ""),
                    api_data.get("provider_1_model_1", "")
                ],
                "supportsReasoning": api_data.get("provider_1_supportsReasoning", False)
            }
        
        return {"providers": providers}
        
    except Exception as e:
        # In case of any error, return empty providers dict
        return {"providers": {}}