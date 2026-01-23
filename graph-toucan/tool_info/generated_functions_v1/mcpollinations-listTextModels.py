from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing text models.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - model_0_name (str): Name of the first model
        - model_0_description (str): Description of the first model
        - model_0_provider (str): Provider of the first model
        - model_0_tier (str): Tier of the first model
        - model_0_community (bool): Whether the first model is community-driven
        - model_0_aliases_0 (str): First alias of the first model
        - model_0_aliases_1 (str): Second alias of the first model
        - model_0_input_modalities_0 (str): First input modality of the first model
        - model_0_input_modalities_1 (str): Second input modality of the first model
        - model_0_output_modalities_0 (str): First output modality of the first model
        - model_0_output_modalities_1 (str): Second output modality of the first model
        - model_0_tools_0 (str): First tool supported by the first model
        - model_0_tools_1 (str): Second tool supported by the first model
        - model_0_vision (bool): Whether the first model supports vision
        - model_0_audio (bool): Whether the first model supports audio
        - model_0_maxInputChars (int): Maximum input characters for the first model
        - model_0_voices_0 (str): First voice option for the first model
        - model_0_voices_1 (str): Second voice option for the first model
        - model_0_uncensored (bool): Whether the first model is uncensored
        - model_1_name (str): Name of the second model
        - model_1_description (str): Description of the second model
        - model_1_provider (str): Provider of the second model
        - model_1_tier (str): Tier of the second model
        - model_1_community (bool): Whether the second model is community-driven
        - model_1_aliases_0 (str): First alias of the second model
        - model_1_aliases_1 (str): Second alias of the second model
        - model_1_input_modalities_0 (str): First input modality of the second model
        - model_1_input_modalities_1 (str): Second input modality of the second model
        - model_1_output_modalities_0 (str): First output modality of the second model
        - model_1_output_modalities_1 (str): Second output modality of the second model
        - model_1_tools_0 (str): First tool supported by the second model
        - model_1_tools_1 (str): Second tool supported by the second model
        - model_1_vision (bool): Whether the second model supports vision
        - model_1_audio (bool): Whether the second model supports audio
        - model_1_maxInputChars (int): Maximum input characters for the second model
        - model_1_voices_0 (str): First voice option for the second model
        - model_1_voices_1 (str): Second voice option for the second model
        - model_1_uncensored (bool): Whether the second model is uncensored
    """
    return {
        "model_0_name": "Llama-3-8B-Text",
        "model_0_description": "A powerful text generation model based on Llama architecture.",
        "model_0_provider": "Meta",
        "model_0_tier": "premium",
        "model_0_community": False,
        "model_0_aliases_0": "llama3-text",
        "model_0_aliases_1": "meta-llama3",
        "model_0_input_modalities_0": "text",
        "model_0_input_modalities_1": "code",
        "model_0_output_modalities_0": "text",
        "model_0_output_modalities_1": "code",
        "model_0_tools_0": "code_interpreter",
        "model_0_tools_1": "web_search",
        "model_0_vision": False,
        "model_0_audio": False,
        "model_0_maxInputChars": 32768,
        "model_0_voices_0": "neutral",
        "model_0_voices_1": "formal",
        "model_0_uncensored": False,
        "model_1_name": "Mistral-7B-Instruct",
        "model_1_description": "High-performance instruction-tuned text model.",
        "model_1_provider": "Mistral AI",
        "model_1_tier": "standard",
        "model_1_community": True,
        "model_1_aliases_0": "mistral-instruct",
        "model_1_aliases_1": "mistral-7b",
        "model_1_input_modalities_0": "text",
        "model_1_input_modalities_1": "structured_data",
        "model_1_output_modalities_0": "text",
        "model_1_output_modalities_1": "json",
        "model_1_tools_0": "database_query",
        "model_1_tools_1": "code_interpreter",
        "model_1_vision": False,
        "model_1_audio": True,
        "model_1_maxInputChars": 16384,
        "model_1_voices_0": "casual",
        "model_1_voices_1": "professional",
        "model_1_uncensored": True,
    }

def mcpollinations_listTextModels() -> List[Dict[str, Any]]:
    """
    List available text models from the MCPollinations service.
    
    Returns:
        List[Dict]: A list of dictionaries, each representing a text model with the following keys:
            - name (str): Model name
            - description (str): Model description
            - provider (str): Model provider
            - tier (str): Model tier (e.g., 'standard', 'premium')
            - community (bool): Whether the model is community-driven
            - aliases (List[str]): List of alternative names for the model
            - input_modalities (List[str]): List of supported input modalities
            - output_modalities (List[str]): List of supported output modalities
            - tools (List[str]): List of tools the model can use
            - vision (bool): Whether the model supports vision input
            - audio (bool): Whether the model supports audio input
            - Optional fields:
                - maxInputChars (int): Maximum number of input characters
                - voices (List[str]): Available voice options
                - uncensored (bool): Whether the model is uncensored
    """
    try:
        # Fetch flattened data from external API simulation
        api_data = call_external_api("mcpollinations-listTextModels")
        
        # Construct the first model from flattened fields
        model_0 = {
            "name": api_data["model_0_name"],
            "description": api_data["model_0_description"],
            "provider": api_data["model_0_provider"],
            "tier": api_data["model_0_tier"],
            "community": api_data["model_0_community"],
            "aliases": [api_data["model_0_aliases_0"], api_data["model_0_aliases_1"]],
            "input_modalities": [api_data["model_0_input_modalities_0"], api_data["model_0_input_modalities_1"]],
            "output_modalities": [api_data["model_0_output_modalities_0"], api_data["model_0_output_modalities_1"]],
            "tools": [api_data["model_0_tools_0"], api_data["model_0_tools_1"]],
            "vision": api_data["model_0_vision"],
            "audio": api_data["model_0_audio"],
            "maxInputChars": api_data["model_0_maxInputChars"],
            "voices": [api_data["model_0_voices_0"], api_data["model_0_voices_1"]],
            "uncensored": api_data["model_0_uncensored"]
        }
        
        # Construct the second model from flattened fields
        model_1 = {
            "name": api_data["model_1_name"],
            "description": api_data["model_1_description"],
            "provider": api_data["model_1_provider"],
            "tier": api_data["model_1_tier"],
            "community": api_data["model_1_community"],
            "aliases": [api_data["model_1_aliases_0"], api_data["model_1_aliases_1"]],
            "input_modalities": [api_data["model_1_input_modalities_0"], api_data["model_1_input_modalities_1"]],
            "output_modalities": [api_data["model_1_output_modalities_0"], api_data["model_1_output_modalities_1"]],
            "tools": [api_data["model_1_tools_0"], api_data["model_1_tools_1"]],
            "vision": api_data["model_1_vision"],
            "audio": api_data["model_1_audio"],
            "maxInputChars": api_data["model_1_maxInputChars"],
            "voices": [api_data["model_1_voices_0"], api_data["model_1_voices_1"]],
            "uncensored": api_data["model_1_uncensored"]
        }
        
        return [model_0, model_1]
        
    except Exception as e:
        # In case of any error, return empty list
        return []