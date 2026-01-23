from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather greeting.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - greeting_message (str): Friendly greeting message from weather assistant
        - assistant_name (str): Name of the weather assistant
        - timestamp (str): ISO 8601 formatted timestamp
        - suggested_actions_0 (str): First suggested action or question
        - suggested_actions_1 (str): Second suggested action or question
    """
    return {
        "greeting_message": "Merhaba! Sana nasıl yardımcı olabilirim?",
        "assistant_name": "HavaKoç",
        "timestamp": datetime.now().isoformat(),
        "suggested_actions_0": "Bugünün hava durumunu nasıl görebilirim?",
        "suggested_actions_1": "Yarın yağmur yağacak mı?"
    }

def weather_forecast_server_with_ai_assistant_weather_greeting() -> Dict[str, Any]:
    """
    Hava durumu asistanının karşılama mesajını üretir.

    Returns:
        Dict containing:
            - greeting_message (str): Dostane bir karşılama mesajı, hava durumu asistanı tarafından kullanıcıya hitap eder şekilde hazırlanır
            - assistant_name (str): Karşılama yapan hava durumu asistanının adı
            - timestamp (str): Mesajın oluşturulduğu zaman (ISO 8601 formatında)
            - suggested_actions (List[str]): Kullanıcının asistana ne sormak isteyebileceğine dair önerilen eylemler veya sorular
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("weather-forecast-server-with-ai-assistant-weather_greeting")
        
        # Construct the result with proper nested structure
        result = {
            "greeting_message": str(api_data.get("greeting_message", "Merhaba!")),
            "assistant_name": str(api_data.get("assistant_name", "WeatherBot")),
            "timestamp": str(api_data.get("timestamp", datetime.now().isoformat())),
            "suggested_actions": [
                str(api_data.get("suggested_actions_0", "Bugünün hava durumu nedir?")),
                str(api_data.get("suggested_actions_1", "Hafta sonu hava nasıl olacak?"))
            ]
        }
        
        return result
        
    except Exception as e:
        # Fallback safe response in case of any error
        return {
            "greeting_message": "Merhaba! Hava durumu asistanına hoş geldiniz.",
            "assistant_name": "WeatherBot",
            "timestamp": datetime.now().isoformat(),
            "suggested_actions": [
                "Bugünün hava durumunu nasıl görebilirim?",
                "Yarın yağmur yağacak mı?"
            ]
        }