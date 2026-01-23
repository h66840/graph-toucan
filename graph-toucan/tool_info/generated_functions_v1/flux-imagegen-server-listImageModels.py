def flux_imagegen_server_listImageModels():
    """
    List available image models from the flux image generation server.
    
    Returns:
        Dict with the following keys:
        - models (List[str]): list of available image model names, such as 'flux', 'kontext', 'turbo'
        - error (str, optional): error message if the request to list models failed, otherwise None
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - model_0 (str): Name of the first available image model
            - model_1 (str): Name of the second available image model
            - error (str, optional): Error message if request failed; None if successful
        """
        return {
            "model_0": "flux",
            "model_1": "turbo",
            "error": None
        }

    try:
        api_data = call_external_api("flux-imagegen-server-listImageModels")
        
        # Construct result according to output schema
        result = {}
        
        # Add models list from indexed fields
        models = []
        if "model_0" in api_data and api_data["model_0"] is not None:
            models.append(api_data["model_0"])
        if "model_1" in api_data and api_data["model_1"] is not None:
            models.append(api_data["model_1"])
        result["models"] = models
        
        # Add error field if present
        if "error" in api_data and api_data["error"] is not None:
            result["error"] = api_data["error"]
        
        return result

    except Exception as e:
        return {"models": [], "error": str(e)}