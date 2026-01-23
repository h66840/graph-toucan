from typing import Dict, List, Any

def deneme_mcp_server_weather_greeting() -> Dict[str, Any]:
    """
    Hava durumu asistanının karşılama mesajı.
    
    Returns:
        Dict containing:
        - greeting_message (str): Friendly welcome message from the weather assistant
        - assistant_role (str): Stated role or purpose of the assistant
        - supported_features (List[Dict]): List of supported input methods with details
        - call_to_action (str): Prompt asking user for location input
        - emojis_used (List[str]): Emojis used in the message for tone/emphasis
        - location_input_hints (List[str]): Example phrases for requesting weather by location
    """
    greeting_message = "Merhaba! 🌤️ Hava durumu asistanına hoş geldiniz!"
    assistant_role = "I am your weather assistant"
    supported_features = [
        {
            "method_type": "coordinates",
            "description": "Enlem ve boylam kullanarak hava durumu sorgulama",
            "examples": ["40.7128, -74.0060", "39.9334, 32.8597"]
        },
        {
            "method_type": "city name",
            "description": "Şehir adı ile hava durumu bilgisi alma",
            "examples": ["İstanbul", "New York", "Tokyo"]
        },
        {
            "method_type": "natural language",
            "description": "Doğal dil kullanarak hava durumu sorgulama",
            "examples": ["Yarın İstanbul'da hava nasıl olacak?", "Bugün Paris'te yağmur mu var?"]
        }
    ]
    call_to_action = "Lütfen hava durumunu öğrenmek istediğiniz konumu girin."
    emojis_used = ["🌤️", "🌦️", "🌧️", "🌨️", "☀️"]
    location_input_hints = [
        "İstanbul için hava durumu",
        "New York'ta bugün hava nasıl?",
        "39.9334, 32.8597 koordinatları için hava durumu",
        "Yarın Tokyo'da güneş mi var?"
    ]

    return {
        "greeting_message": greeting_message,
        "assistant_role": assistant_role,
        "supported_features": supported_features,
        "call_to_action": call_to_action,
        "emojis_used": emojis_used,
        "location_input_hints": location_input_hints
    }