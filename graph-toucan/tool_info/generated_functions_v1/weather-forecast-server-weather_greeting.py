from typing import Dict, List, Any

def weather_forecast_server_weather_greeting() -> Dict[str, Any]:
    """
    Hava durumu asistanının karşılama mesajı.
    
    Returns:
        Dict containing the following fields:
        - greeting_emoji (str): main emoji used in the greeting message
        - greeting_title (str): the bolded title line of the greeting
        - assistant_role (str): description of the assistant's purpose
        - usage_options (List[Dict]): list of usage methods with method, example, and description
        - call_to_action (str): final prompt asking user for location input
        - supporting_emojis (List[str]): emojis used throughout the message
    """
    return {
        "greeting_emoji": "🌤️",
        "greeting_title": "Merhaba! Hava Durumu Asistanınızım!",
        "assistant_role": "Size güncel ve doğru hava durumu bilgileri sunmak için buradayım.",
        "usage_options": [
            {
                "method": "Konum adı ile sorgu",
                "example": "İstanbul hava durumu",
                "description": "Şehir adı yazarak o bölgenin hava durumunu öğrenebilirsiniz."
            },
            {
                "method": "Konum etiketi ile sorgu",
                "example": "Evim için hava durumu",
                "description": "Kayıtlı konum etiketlerinizi kullanarak hava durumu bilgisi alabilirsiniz."
            }
        ],
        "call_to_action": "Lütfen hava durumunu öğrenmek istediğiniz konumu yazın:",
        "supporting_emojis": ["🌦️", "🌡️", "🌧️", "⛅", "💨"]
    }