from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for nationality detection.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - isim (str): Input name that was analyzed
        - tahmin_0_ulke (str): First predicted country
        - tahmin_0_olasilik (float): Confidence percentage for first prediction
        - tahmin_1_ulke (str): Second predicted country
        - tahmin_1_olasilik (float): Confidence percentage for second prediction
    """
    return {
        "isim": "Ahmet",
        "tahmin_0_ulke": "Turkey",
        "tahmin_0_olasilik": 85.5,
        "tahmin_1_ulke": "Germany",
        "tahmin_1_olasilik": 12.3
    }

def nationality_detection_service_get_nationality(name: str) -> Dict[str, Any]:
    """
    Verilen isme göre kişinin en olası milliyetlerini tahmin eder.
    
    Args:
        name (str): Analiz edilecek isim
        
    Returns:
        Dict containing:
        - isim (str): the input name that was analyzed for nationality prediction
        - tahminler (List[Dict]): list of predicted nationalities, each containing 'ülke' (country name) and 'olasılık (%)' (prediction confidence percentage)
        
    Example:
        {
            "isim": "Ahmet",
            "tahminler": [
                {"ülke": "Turkey", "olasılık (%)": 85.5},
                {"ülke": "Germany", "olasılık (%)": 12.3}
            ]
        }
    """
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    
    # Fetch data from simulated external API
    api_data = call_external_api("nationality-detection-service-get_nationality")
    
    # Override the default name with the input name
    api_data["isim"] = name
    
    # Construct the nested output structure
    result = {
        "isim": api_data["isim"],
        "tahminler": [
            {
                "ülke": api_data["tahmin_0_ulke"],
                "olasılık (%)": api_data["tahmin_0_olasilik"]
            },
            {
                "ülke": api_data["tahmin_1_ulke"],
                "olasılık (%)": api_data["tahmin_1_olasilik"]
            }
        ]
    }
    
    return result