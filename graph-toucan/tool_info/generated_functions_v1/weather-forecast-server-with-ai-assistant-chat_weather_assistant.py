from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather forecast assistant.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - greeting (str): Friendly welcome message from the assistant
        - instructions (str): Explanation of how to provide location for weather information
        - coordinate_option_0_label (str): Label of first coordinate format example
        - coordinate_option_0_value (str): Value of first coordinate format example
        - coordinate_option_1_label (str): Label of second coordinate format example
        - coordinate_option_1_value (str): Value of second coordinate format example
        - city_option_0_label (str): Label of first city query example
        - city_option_0_value (str): Value of first city query example
        - city_option_1_label (str): Label of second city query example
        - city_option_1_value (str): Value of second city query example
        - prompt_question (str): Question asking user to specify location for weather forecast
    """
    return {
        "greeting": "Merhaba! Hava durumu asistanına hoş geldiniz.",
        "instructions": "Hava durumu bilgisi almak için lütfen bir konum belirtin. Koordinatlar veya şehir adı kullanabilirsiniz.",
        "coordinate_option_0_label": "Enlem ve Boylam (ondalıklı)",
        "coordinate_option_0_value": "41.0082, 28.9784",
        "coordinate_option_1_label": "Derece, Dakika, Saniye",
        "coordinate_option_1_value": "41°00'29\"N, 28°58'42\"E",
        "city_option_0_label": "Şehir Adı",
        "city_option_0_value": "İstanbul",
        "city_option_1_label": "Ülke ile Birlikte Şehir",
        "city_option_1_value": "Ankara, Türkiye",
        "prompt_question": "Hava durumu bilgisi almak istediğiniz yeri belirtir misiniz?"
    }

def weather_forecast_server_with_ai_assistant_chat_weather_assistant(message: str) -> Dict[str, Any]:
    """
    Hava durumu asistanı ile sohbet et.

    Bu araç kullanıcının mesajlarını analiz eder ve uygun yanıtlar verir.
    Koordinat bilgilerini toplar ve hava durumu sorgular.

    Args:
        message (str): Kullanıcının mesajı

    Returns:
        Dict containing:
        - greeting (str): Friendly welcome message from the assistant
        - instructions (str): Explanation of how to provide location for weather information
        - coordinate_options (List[Dict]): Examples of coordinate formats user can provide
        - city_options (List[Dict]): Example city queries user can use
        - prompt_question (str): Question asking user to specify location for weather forecast
    """
    # Validate input
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    if not message.strip():
        raise ValueError("Message cannot be empty or whitespace")
    
    # Fetch data from external API simulation
    api_data = call_external_api("weather-forecast-server-with-ai-assistant-chat_weather_assistant")
    
    # Construct coordinate_options list from flattened API response
    coordinate_options = [
        {
            "label": api_data["coordinate_option_0_label"],
            "value": api_data["coordinate_option_0_value"]
        },
        {
            "label": api_data["coordinate_option_1_label"],
            "value": api_data["coordinate_option_1_value"]
        }
    ]
    
    # Construct city_options list from flattened API response
    city_options = [
        {
            "label": api_data["city_option_0_label"],
            "value": api_data["city_option_0_value"]
        },
        {
            "label": api_data["city_option_1_label"],
            "value": api_data["city_option_1_value"]
        }
    ]
    
    # Build final response structure matching output schema
    result = {
        "greeting": api_data["greeting"],
        "instructions": api_data["instructions"],
        "coordinate_options": coordinate_options,
        "city_options": city_options,
        "prompt_question": api_data["prompt_question"]
    }
    
    return result