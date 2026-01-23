from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing available text models.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - model_0_name (str): Name of the first model
        - model_0_description (str): Description of the first model
        - model_0_provider (str): Provider of the first model
        - model_0_tier (str): Tier of the first model
        - model_0_community (bool): Whether the first model is community-driven
        - model_0_aliases (str): Aliases for the first model
        - model_0_input_modalities_0 (str): First input modality of the first model
        - model_0_input_modalities_1 (str): Second input modality of the first model
        - model_0_output_modalities_0 (str): First output modality of the first model
        - model_0_output_modalities_1 (str): Second output modality of the first model
        - model_0_tools (bool): Whether the first model supports tools
        - model_0_vision (bool): Whether the first model supports vision
        - model_0_audio (bool): Whether the first model supports audio
        - model_0_maxInputChars (int): Maximum input characters for the first model
        - model_0_reasoning (bool): Whether the first model supports reasoning
        - model_0_uncensored (bool): Whether the first model is uncensored
        - model_0_voices_0 (str): First voice option for the first model
        - model_0_voices_1 (str): Second voice option for the first model
        - model_1_name (str): Name of the second model
        - model_1_description (str): Description of the second model
        - model_1_provider (str): Provider of the second model
        - model_1_tier (str): Tier of the second model
        - model_1_community (bool): Whether the second model is community-driven
        - model_1_aliases (str): Aliases for the second model
        - model_1_input_modalities_0 (str): First input modality of the second model
        - model_1_input_modalities_1 (str): Second input modality of the second model
        - model_1_output_modalities_0 (str): First output modality of the second model
        - model_1_output_modalities_1 (str): Second output modality of the second model
        - model_1_tools (bool): Whether the second model supports tools
        - model_1_vision (bool): Whether the second model supports vision
        - model_1_audio (bool): Whether the second model supports audio
        - model_1_maxInputChars (int): Maximum input characters for the second model
        - model_1_reasoning (bool): Whether the second model supports reasoning
        - model_1_uncensored (bool): Whether the second model is uncensored
        - model_1_voices_0 (str): First voice option for the second model
        - model_1_voices_1 (str): Second voice option for the second model
    """
    return {
        "model_0_name": "llama-3-8b",
        "model_0_description": "Llama 3 8B parameter model optimized for general text generation",
        "model_0_provider": "Meta",
        "model_0_tier": "free",
        "model_0_community": False,
        "model_0_aliases": "llama3-8b,meta-llama-3-8b",
        "model_0_input_modalities_0": "text",
        "model_0_input_modalities_1": "code",
        "model_0_output_modalities_0": "text",
        "model_0_output_modalities_1": "code",
        "model_0_tools": True,
        "model_0_vision": False,
        "model_0_audio": False,
        "model_0_maxInputChars": 32768,
        "model_0_reasoning": True,
        "model_0_uncensored": False,
        "model_0_voices_0": "default",
        "model_0_voices_1": "narrative",

        "model_1_name": "mistral-large-vision",
        "model_1_description": "Mistral Large model with vision capabilities",
        "model_1_provider": "Mistral AI",
        "model_1_tier": "pro",
        "model_1_community": False,
        "model_1_aliases": "mistral-large",
        "model_1_input_modalities_0": "text",
        "model_1_input_modalities_1": "image",
        "model_1_output_modalities_0": "text",
        "model_1_output_modalities_1": "image_caption",
        "model_1_tools": True,
        "model_1_vision": True,
        "model_1_audio": False,
        "model_1_maxInputChars": 65536,
        "model_1_reasoning": True,
        "model_1_uncensored": False,
        "model_1_voices_0": "professional",
        "model_1_voices_1": "casual"
    }

def mcpollinations_multimodal_server_listTextModels() -> List[Dict[str, Any]]:
    """
    List available text models from the multimodal server.
    
    Returns:
        List[Dict]: A list of dictionaries containing information about available text models.
        Each dictionary contains the following keys:
        - name (str): Model name
        - description (str): Model description
        - provider (str): Model provider
        - tier (str): Model tier (e.g., free, pro)
        - community (bool): Whether the model is community-driven
        - aliases (str): Comma-separated aliases for the model
        - input_modalities (List[str]): List of supported input modalities
        - output_modalities (List[str]): List of supported output modalities
        - tools (bool): Whether the model supports tool use
        - vision (bool): Whether the model supports vision input
        - audio (bool): Whether the model supports audio input
        - maxInputChars (Optional[int]): Maximum number of input characters
        - reasoning (Optional[bool]): Whether the model supports reasoning
        - uncensored (Optional[bool]): Whether the model is uncensored
        - voices (Optional[List[str]]): List of available voice options
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("mcpollinations-multimodal-server-listTextModels")
        
        # Construct the first model
        model_0 = {
            "name": api_data["model_0_name"],
            "description": api_data["model_0_description"],
            "provider": api_data["model_0_provider"],
            "tier": api_data["model_0_tier"],
            "community": api_data["model_0_community"],
            "aliases": api_data["model_0_aliases"],
            "input_modalities": [
                api_data["model_0_input_modalities_0"],
                api_data["model_0_input_modalities_1"]
            ],
            "output_modalities": [
                api_data["model_0_output_modalities_0"],
                api_data["model_0_output_modalities_1"]
            ],
            "tools": api_data["model_0_tools"],
            "vision": api_data["model_0_vision"],
            "audio": api_data["model_0_audio"],
            "maxInputChars": api_data["model_0_maxInputChars"],
            "reasoning": api_data["model_0_reasoning"],
            "uncensored": api_data["model_0_uncensored"],
            "voices": [
                api_data["model_0_voices_0"],
                api_data["model_0_voices_1"]
            ]
        }
        
        # Construct the second model
        model_1 = {
            "name": api_data["model_1_name"],
            "description": api_data["model_1_description"],
            "provider": api_data["model_1_provider"],
            "tier": api_data["model_1_tier"],
            "community": api_data["model_1_community"],
            "aliases": api_data["model_1_aliases"],
            "input_modalities": [
                api_data["model_1_input_modalities_0"],
                api_data["model_1_input_modalities_1"]
            ],
            "output_modalities": [
                api_data["model_1_output_modalities_0"],
                api_data["model_1_output_modalities_1"]
            ],
            "tools": api_data["model_1_tools"],
            "vision": api_data["model_1_vision"],
            "audio": api_data["model_1_audio"],
            "maxInputChars": api_data["model_1_maxInputChars"],
            "reasoning": api_data["model_1_reasoning"],
            "uncensored": api_data["model_1_uncensored"],
            "voices": [
                api_data["model_1_voices_0"],
                api_data["model_1_voices_1"]
            ]
        }
        
        # Return list of models
        return [model_0, model_1]
    except Exception as e:
        # In case of any error, return empty list
        return []