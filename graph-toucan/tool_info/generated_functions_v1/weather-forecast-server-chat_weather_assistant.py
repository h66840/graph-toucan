from typing import Dict, Any, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external weather API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - response_type (str): Type of response (e.g., "weather_summary", "input_request", "error")
        - message (str): Assistant's reply message in natural language
        - required_inputs_0 (str): First required input type ("coordinates" or "city_name")
        - required_inputs_1 (str): Second required input type if needed
        - coordinates_format_examples_0 (str): Example format for coordinates
        - coordinates_format_examples_1 (str): Another example format for coordinates
        - city_format_examples_0 (str): Example format for city name query
        - city_format_examples_1 (str): Another example format for city name query
        - error_occurred (bool): Whether an error occurred
        - error_details (str): Description of the error if any
        - has_weather_info (bool): Whether weather info was retrieved
        - friendly_tone (bool): Whether the tone is friendly and conversational
        - requested_actions_0 (str): First action requested from user
        - requested_actions_1 (str): Second action requested from user
    """
    return {
        "response_type": "input_request",
        "message": "Merhaba! 🌤️ Hava durumu bilgisi için konumunu paylaşman gerekiyor. Koordinatlarını veya şehir adını yazabilir misin? 😊",
        "required_inputs_0": "coordinates",
        "required_inputs_1": "city_name",
        "coordinates_format_examples_0": "41.0082, 28.9784",
        "coordinates_format_examples_1": "Enlem: 41.0082, Boylam: 28.9784",
        "city_format_examples_0": "İstanbul için hava durumu",
        "city_format_examples_1": "Ankara'da bugün hava nasıl?",
        "error_occurred": False,
        "error_details": "",
        "has_weather_info": False,
        "friendly_tone": True,
        "requested_actions_0": "share location",
        "requested_actions_1": "specify city"
    }

def weather_forecast_server_chat_weather_assistant(message: str) -> Dict[str, Any]:
    """
    Hava durumu asistanı ile sohbet et.
    
    Bu fonksiyon kullanıcının mesajını analiz eder ve uygun yanıtlar verir.
    Koordinat bilgilerini toplar ve hava durumu sorgular.
    
    Args:
        message (str): Kullanıcının mesajı
        
    Returns:
        Dict containing:
            - response_type (str): type of response indicating whether it's a request for input, error, or weather information
            - message (str): the main textual content of the assistant's reply
            - required_inputs (List[str]): list of inputs user must provide to proceed
            - coordinates_format_examples (List[str]): example formats for providing coordinates
            - city_format_examples (List[str]): example formats for city-based queries
            - error_occurred (bool): indicates whether an error was encountered
            - error_details (str): description of the error if one occurred
            - has_weather_info (bool): indicates whether weather-related information was successfully retrieved
            - friendly_tone (bool): indicates if the message is delivered in a conversational tone
            - requested_actions (List[str]): list of actions or questions the assistant is prompting the user to take
    """
    try:
        if not isinstance(message, str):
            raise ValueError("Message must be a string")

        message_lower = message.strip().lower()
        
        # Call simulated external API
        api_data = call_external_api("weather-forecast-server-chat_weather_assistant")
        
        # Construct output structure based on schema
        result = {
            "response_type": api_data["response_type"],
            "message": api_data["message"],
            "required_inputs": [],
            "coordinates_format_examples": [],
            "city_format_examples": [],
            "error_occurred": api_data["error_occurred"],
            "error_details": api_data["error_details"],
            "has_weather_info": api_data["has_weather_info"],
            "friendly_tone": api_data["friendly_tone"],
            "requested_actions": []
        }
        
        # Populate lists from indexed fields
        if api_data.get("required_inputs_0"):
            result["required_inputs"].append(api_data["required_inputs_0"])
        if api_data.get("required_inputs_1"):
            result["required_inputs"].append(api_data["required_inputs_1"])
            
        if api_data.get("coordinates_format_examples_0"):
            result["coordinates_format_examples"].append(api_data["coordinates_format_examples_0"])
        if api_data.get("coordinates_format_examples_1"):
            result["coordinates_format_examples"].append(api_data["coordinates_format_examples_1"])
            
        if api_data.get("city_format_examples_0"):
            result["city_format_examples"].append(api_data["city_format_examples_0"])
        if api_data.get("city_format_examples_1"):
            result["city_format_examples"].append(api_data["city_format_examples_1"])
            
        if api_data.get("requested_actions_0"):
            result["requested_actions"].append(api_data["requested_actions_0"])
        if api_data.get("requested_actions_1"):
            result["requested_actions"].append(api_data["requested_actions_1"])

        # Simple logic to change response based on message content
        if not message_lower:
            result["message"] = "Merhaba! 🌤️ Hava durumu bilgisi almak ister misin? Lütfen bir şehir adı ya da koordinat gir. 📍"
        elif any(word in message_lower for word in ["hava", "durum", "clima", "weather"]):
            if any(word in message_lower for word in ["ist", "ankar", "izmir", "bursa", "adana"]):
                result["message"] = f"{message.split()[0].capitalize()} için hava durumu: Güneşli ve güzel! ☀️ Sıcaklık: 24°C"
                result["has_weather_info"] = True
                result["response_type"] = "weather_summary"
                result["required_inputs"] = []
                result["requested_actions"] = []
            elif any(coord_part in message_lower for coord_part in ["n", "s", "e", "w", "enlem", "boylam", ","]):
                result["message"] = "Koordinat alındı! 🛰️ Hava durumu bilgisi geliyor... Bulutlu, yer yer açık. 🌥️"
                result["has_weather_info"] = True
                result["response_type"] = "weather_summary"
                result["required_inputs"] = []
                result["requested_actions"] = []
        
        return result
        
    except Exception as e:
        return {
            "response_type": "error",
            "message": "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin. 🙁",
            "required_inputs": [],
            "coordinates_format_examples": [
                "41.0082, 28.9784",
                "Enlem: 41.0082, Boylam: 28.9784"
            ],
            "city_format_examples": [
                "İstanbul için hava durumu",
                "Ankara'da bugün hava nasıl?"
            ],
            "error_occurred": True,
            "error_details": f"Processing error: {str(e)}",
            "has_weather_info": False,
            "friendly_tone": True,
            "requested_actions": ["try again"]
        }