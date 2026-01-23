from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location (str): Full location name including city and country
        - weather_condition (str): General weather description
        - temperature_current (float): Current temperature in Celsius
        - temperature_feels_like (float): Perceived temperature in Celsius
        - temperature_min (float): Minimum temperature of the day
        - temperature_max (float): Maximum temperature of the day
        - humidity (int): Relative humidity as percentage
        - pressure (int): Atmospheric pressure in hPa
        - wind_speed (float): Wind speed in meters per second
        - advisory_0 (str): First user-friendly recommendation
        - advisory_1 (str): Second user-friendly recommendation
    """
    return {
        "location": "İstanbul kenti, TR",
        "weather_condition": "Parçalı Bulutlu",
        "temperature_current": 18.5,
        "temperature_feels_like": 19.0,
        "temperature_min": 16.0,
        "temperature_max": 21.0,
        "humidity": 65,
        "pressure": 1015,
        "wind_speed": 3.2,
        "advisory_0": "Hafif rüzgar var. Hafif bir ceketle dışarı çıkabilirsiniz.",
        "advisory_1": "Güneşli aralar olacak. Gözlük takmayı unutmayın."
    }

def deneme_mcp_server_get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Kullanıcı dostu hava durumu asistanı - koordinatlara göre hava durumu getirir.
    
    Bu fonksiyon, verilen enlem ve boylam değerlerine göre hava durumu bilgilerini
    simüle eder ve kullanıcı dostu bir formatta döner.
    
    Args:
        latitude (float): Enlem değeri (-90 ile 90 arasında)
        longitude (float): Boylam değeri (-180 ile 180 arasında)
    
    Returns:
        Dict[str, Any]: Kullanıcı dostu formatta hava durumu bilgileri:
            - location (str): Şehir ve ülke bilgisi
            - weather_condition (str): Genel hava durumu açıklaması
            - temperature_current (float): Mevcut sıcaklık (Celsius)
            - temperature_feels_like (float): Hissedilen sıcaklık (Celsius)
            - temperature_min (float): Günkü minimum sıcaklık
            - temperature_max (float): Günkü maksimum sıcaklık
            - humidity (int): Bağıl nem yüzdesi
            - pressure (int): Atmosferik basınç (hPa)
            - wind_speed (float): Rüzgar hızı (m/s)
            - advisories (List[str]): Hava durumuna göre kullanıcı önerileri
    
    Raises:
        ValueError: Geçersiz koordinat değerleri girildiğinde
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    
    # Fetch simulated data from external API
    api_data = call_external_api("deneme-mcp-server-get_weather")
    
    # Construct the result matching the output schema
    result = {
        "location": api_data["location"],
        "weather_condition": api_data["weather_condition"],
        "temperature_current": api_data["temperature_current"],
        "temperature_feels_like": api_data["temperature_feels_like"],
        "temperature_min": api_data["temperature_min"],
        "temperature_max": api_data["temperature_max"],
        "humidity": api_data["humidity"],
        "pressure": api_data["pressure"],
        "wind_speed": api_data["wind_speed"],
        "advisories": [
            api_data["advisory_0"],
            api_data["advisory_1"]
        ]
    }
    
    return result