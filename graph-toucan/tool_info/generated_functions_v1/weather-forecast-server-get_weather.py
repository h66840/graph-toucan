def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching weather data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location (str): Name and country of the location in format "City, Country"
        - condition (str): General weather condition (e.g., Açık, Kapalı, Parçalı Az Bulutlu)
        - temperature_current (float): Current temperature in °C
        - temperature_feels_like (float): Perceived temperature in °C
        - temperature_min (float): Minimum temperature of the day in °C
        - temperature_max (float): Maximum temperature of the day in °C
        - humidity (int): Relative humidity as a percentage
        - pressure (int): Atmospheric pressure in hPa
        - wind_speed (float): Wind speed in m/s
        - advice_summary (str): User-friendly summary or recommendations based on weather
        - advice_tag_0 (str): First recommendation label
        - advice_tag_1 (str): Second recommendation label
    """
    return {
        "location": "Istanbul, TR",
        "condition": "Parçalı Az Bulutlu",
        "temperature_current": 21.5,
        "temperature_feels_like": 23.0,
        "temperature_min": 18.0,
        "temperature_max": 24.5,
        "humidity": 65,
        "pressure": 1013,
        "wind_speed": 3.2,
        "advice_summary": "Hava oldukça güzel, dışarı çıkıp doğanın tadını çıkarabilirsiniz.",
        "advice_tag_0": "Güzel hava!",
        "advice_tag_1": "Bol su için"
    }


def weather_forecast_server_get_weather(latitude: float, longitude: float) -> dict:
    """
    Kullanıcı dostu hava durumu asistanı - koordinatlara göre hava durumu getirir.

    Bu araç, kullanıcıyla dostane iletişim kurar ve hava durumu bilgilerini
    anlaşılır şekilde sunar.

    Args:
        latitude (float): Enlem (-90 ile 90 arasında)
        longitude (float): Boylam (-180 ile 180 arasında)

    Returns:
        dict: Kullanıcı dostu formatta hava durumu bilgileri şunları içerir:
            - location (str): Şehir ve ülke adı ("Şehir, Ülke" formatında)
            - condition (str): Genel hava durumu (örneğin, Açık, Kapalı, Parçalı Az Bulutlu)
            - temperature_current (float): Mevcut sıcaklık (°C)
            - temperature_feels_like (float): Hissedilen sıcaklık (°C)
            - temperature_min (float): Günün minimum sıcaklığı (°C)
            - temperature_max (float): Günün maksimum sıcaklığı (°C)
            - humidity (int): Bağıl nem yüzdesi
            - pressure (int): Atmosferik basınç (hPa)
            - wind_speed (float): Rüzgar hızı (m/s)
            - advice_summary (str): Hava durumuna göre kullanıcıya yönelik öneriler
            - advice_tags (List[str]): Kısa öneri etiketleri listesi

    Raises:
        ValueError: Geçersiz enlem veya boylam değerleri girildiğinde
    """
    # Input validation
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        raise ValueError("Enlem ve boylam sayısal değerler olmalıdır.")
    if not (-90 <= latitude <= 90):
        raise ValueError("Enlem -90 ile 90 arasında olmalıdır.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Boylam -180 ile 180 arasında olmalıdır.")

    # Fetch simulated external data
    api_data = call_external_api("weather-forecast-server-get_weather")

    # Construct output structure matching schema exactly
    result = {
        "location": api_data["location"],
        "condition": api_data["condition"],
        "temperature_current": api_data["temperature_current"],
        "temperature_feels_like": api_data["temperature_feels_like"],
        "temperature_min": api_data["temperature_min"],
        "temperature_max": api_data["temperature_max"],
        "humidity": api_data["humidity"],
        "pressure": api_data["pressure"],
        "wind_speed": api_data["wind_speed"],
        "advice_summary": api_data["advice_summary"],
        "advice_tags": [
            api_data["advice_tag_0"],
            api_data["advice_tag_1"]
        ]
    }

    return result