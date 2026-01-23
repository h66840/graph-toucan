from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching word details from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - word (str): The word being defined
        - pronunciation (str): Phonetic pronunciation in slashes, e.g., /ˈnəʊnɪdʒ/
        - part_of_speech (str): Grammatical category of the word, e.g., Noun, Adjective
        - definition_0_definition (str): First definition text
        - definition_0_example (str): Example sentence for first definition
        - definition_0_synonyms_0 (str): First synonym in first definition
        - definition_0_synonyms_1 (str): Second synonym in first definition
        - definition_0_antonyms_0 (str): First antonym in first definition
        - definition_0_antonyms_1 (str): Second antonym in first definition
        - definition_1_definition (str): Second definition text
        - definition_1_example (str): Example sentence for second definition
        - definition_1_synonyms_0 (str): First synonym in second definition
        - definition_1_synonyms_1 (str): Second synonym in second definition
        - definition_1_antonyms_0 (str): First antonym in second definition
        - definition_1_antonyms_1 (str): Second antonym in second definition
        - synonyms_0 (str): First general synonym for the word
        - synonyms_1 (str): Second general synonym for the word
        - antonyms_0 (str): First general antonym for the word
        - antonyms_1 (str): Second general antonym for the word
    """
    return {
        "word": "example",
        "pronunciation": "/ɪɡˈzæmpəl/",
        "part_of_speech": "Noun",
        "definition_0_definition": "a thing serving as a pattern to be imitated or not to be imitated",
        "definition_0_example": "a good example of medieval architecture",
        "definition_0_synonyms_0": "model",
        "definition_0_synonyms_1": "pattern",
        "definition_0_antonyms_0": "anomaly",
        "definition_0_antonyms_1": "exception",
        "definition_1_definition": "a warning or punishment that serves as a deterrent",
        "definition_1_example": "they made an example of him to scare others",
        "definition_1_synonyms_0": "warning",
        "definition_1_synonyms_1": "deterrent",
        "definition_1_antonyms_0": "encouragement",
        "definition_1_antonyms_1": "incentive",
        "synonyms_0": "sample",
        "synonyms_1": "instance",
        "antonyms_0": "whole",
        "antonyms_1": "totality"
    }

def books_server_get_word_details(word: str) -> Dict[str, Any]:
    """
    Get detailed word information including pronunciation, synonyms, and examples.
    
    Args:
        word: The word to get detailed information for
    
    Returns:
        Detailed word information or error message with structure:
        - word (str): the word being defined
        - pronunciation (str): phonetic pronunciation in slashes, e.g., /ˈnəʊnɪdʒ/
        - part_of_speech (str): the grammatical category of the word, e.g., Noun, Adjective
        - definitions (List[Dict]): list of definition entries, each with 'definition' (str), 
          optional 'example' (str), and optional 'synonyms' (List[str]) and 'antonyms' (List[str])
        - synonyms (List[str]): general synonyms for the word, if provided at top level
        - antonyms (List[str]): general antonyms for the word, if provided at top level
    
    Raises:
        ValueError: If word is empty or None
    """
    # Input validation
    if not word or not word.strip():
        return {"error": "Word parameter is required and cannot be empty"}
    
    try:
        # Call external API to get data (returns flat structure)
        api_data = call_external_api("books-server-get_word_details")
        
        # Construct definitions list from indexed fields
        definitions = []
        
        # Process first definition
        def_0 = {
            "definition": api_data["definition_0_definition"]
        }
        if api_data.get("definition_0_example"):
            def_0["example"] = api_data["definition_0_example"]
        
        def_0_synonyms = []
        if api_data.get("definition_0_synonyms_0"):
            def_0_synonyms.append(api_data["definition_0_synonyms_0"])
        if api_data.get("definition_0_synonyms_1"):
            def_0_synonyms.append(api_data["definition_0_synonyms_1"])
        if def_0_synonyms:
            def_0["synonyms"] = def_0_synonyms
            
        def_0_antonyms = []
        if api_data.get("definition_0_antonyms_0"):
            def_0_antonyms.append(api_data["definition_0_antonyms_0"])
        if api_data.get("definition_0_antonyms_1"):
            def_0_antonyms.append(api_data["definition_0_antonyms_1"])
        if def_0_antonyms:
            def_0["antonyms"] = def_0_antonyms
            
        definitions.append(def_0)
        
        # Process second definition
        def_1 = {
            "definition": api_data["definition_1_definition"]
        }
        if api_data.get("definition_1_example"):
            def_1["example"] = api_data["definition_1_example"]
            
        def_1_synonyms = []
        if api_data.get("definition_1_synonyms_0"):
            def_1_synonyms.append(api_data["definition_1_synonyms_0"])
        if api_data.get("definition_1_synonyms_1"):
            def_1_synonyms.append(api_data["definition_1_synonyms_1"])
        if def_1_synonyms:
            def_1["synonyms"] = def_1_synonyms
            
        def_1_antonyms = []
        if api_data.get("definition_1_antonyms_0"):
            def_1_antonyms.append(api_data["definition_1_antonyms_0"])
        if api_data.get("definition_1_antonyms_1"):
            def_1_antonyms.append(api_data["definition_1_antonyms_1"])
        if def_1_antonyms:
            def_1["antonyms"] = def_1_antonyms
            
        definitions.append(def_1)
        
        # Construct synonyms and antonyms lists
        synonyms = []
        if api_data.get("synonyms_0"):
            synonyms.append(api_data["synonyms_0"])
        if api_data.get("synonyms_1"):
            synonyms.append(api_data["synonyms_1"])
            
        antonyms = []
        if api_data.get("antonyms_0"):
            antonyms.append(api_data["antonyms_0"])
        if api_data.get("antonyms_1"):
            antonyms.append(api_data["antonyms_1"])
        
        # Build final result structure matching output schema
        result = {
            "word": api_data["word"],
            "pronunciation": api_data["pronunciation"],
            "part_of_speech": api_data["part_of_speech"],
            "definitions": definitions,
            "synonyms": synonyms,
            "antonyms": antonyms
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Failed to retrieve word details: {str(e)}"}