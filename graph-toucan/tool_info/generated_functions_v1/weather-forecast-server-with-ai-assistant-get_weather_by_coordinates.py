from typing import Dict, Any, Optional
import random
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - konum_enlem (float): Latitude coordinate
        - konum_boylam (float): Longitude coordinate
        - konum_sehir (str): City name
        - konum_ulke (str): Country name
        - hava_durumu_ana_durum (str): Main weather condition (e.g., Clear, Rain)
        - hava_durumu_aciklama (str): Detailed weather description
        - hava_durumu_ikon (str): Weather icon code
        - sicaklik_mevcut (float): Current temperature
        - sicaklik_hissedilen (float): Feels-like temperature
        - sicaklik_minimum (float): Minimum temperature
        - sicaklik_maksimum (float): Maximum temperature
        - sicaklik_birim (str): Temperature unit (°C or °F)
        - atmosfer_basinc (int): Atmospheric pressure in hPa
        - atmosfer_nem (int): Humidity percentage
        - atmosfer_gorus_mesafesi (int): Visibility in meters
        - ruzgar_hiz (float): Wind speed
        - ruzgar_yon (int): Wind direction in degrees
        - ruzgar_birim (str): Wind speed unit (e.g., m/s)
        - bulutluluk_yuzde (int): Cloud coverage percentage
        - gunes_dogus (int): Sunrise timestamp (Unix time)
        - gunes_batis (int): Sunset timestamp (Unix time)
        - zaman_veri_zamani (int): Data timestamp (Unix time)
        - zaman_saat_dilimi (int): Timezone offset in seconds
        - yagis_son_1_saat (float): Rain volume in last hour in mm
        - yagis_birim (str): Precipitation unit (e.g., mm)
    """
    # Generate realistic but simulated data based on coordinates
    now = datetime.now()
    sunrise = int((now.replace(hour=6, minute=0, second=0, microsecond=0) - datetime(1970, 1, 1)).total_seconds())
    sunset = int((now.replace(hour=18, minute=0, second=0, microsecond=0) - datetime(1970, 1, 1)).total_seconds())
    current_time = int(now.timestamp())

    return {
        "konum_enlem": 41.0082,
        "konum_boylam": 28.9784,
        "konum_sehir": "Istanbul",
        "konum_ulke": "TR",
        "hava_durumu_ana_durum": random.choice(["Clear", "Clouds", "Rain", "Snow", "Mist"]),
        "hava_durumu_aciklama": "clear sky",
        "hava_durumu_ikon": "01d",
        "sicaklik_mevcut": 22.5,
        "sicaklik_hissedilen": 24.0,
        "sicaklik_minimum": 20.0,
        "sicaklik_maksimum": 25.0,
        "sicaklik_birim": "°C",
        "atmosfer_basinc": 1013,
        "atmosfer_nem": 65,
        "atmosfer_gorus_mesafesi": 10000,
        "ruzgar_hiz": 3.5,
        "ruzgar_yon": 180,
        "ruzgar_birim": "m/s",
        "bulutluluk_yuzde": 20,
        "gunes_dogus": sunrise,
        "gunes_batis": sunset,
        "zaman_veri_zamani": current_time,
        "zaman_saat_dilimi": 10800,
        "yagis_son_1_saat": 0.0,
        "yagis_birim": "mm"
    }


def weather_forecast_server_with_ai_assistant_get_weather_by_coordinates(
    latitude: float,
    longitude: float,
    units: Optional[str] = "metric"
) -> Dict[str, Any]:
    """
    Enlem ve boylam koordinatlarına göre hava durumu bilgilerini getirir.

    Args:
        latitude (float): Enlem (-90 ile 90 arasında)
        longitude (float): Boylam (-180 ile 180 arasında)
        units (Optional[str]): Ölçü birimi (metric, imperial, standard). Varsayılan: metric

    Returns:
        JSON formatında hava durumu bilgileri, aşağıdaki yapıda:
        - konum: enlem, boylam, şehir, ülke
        - hava_durumu: ana_durum, açıklama, ikon
        - sıcaklık: mevcut, hissedilen, minimum, maksimum, birim
        - atmosfer: basınç, nem, görüş_mesafesi
        - rüzgar: hız, yön, birim
        - bulutluluk: yüzde
        - güneş: doğuş, batış
        - zaman: veri_zamanı, saat_dilimi
        - yağış: son_1_saat, birim (opsiyonel)

    Raises:
        ValueError: Geçersiz enlem/boylam veya birim değeri girilirse
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    if units not in ["metric", "imperial", "standard", None]:
        raise ValueError("Units must be one of: metric, imperial, standard")

    # Fetch simulated data from external API
    api_data = call_external_api("weather-forecast-server-with-ai-assistant-get_weather_by_coordinates")

    # Adjust temperature unit if needed
    temp_unit = "°C"
    speed_unit = "m/s"
    if units == "imperial":
        temp_unit = "°F"
        speed_unit = "mph"

    # Construct nested response structure
    result = {
        "konum": {
            "enlem": api_data["konum_enlem"],
            "boylam": api_data["konum_boylam"],
            "şehir": api_data["konum_sehir"],
            "ülke": api_data["konum_ulke"]
        },
        "hava_durumu": {
            "ana_durum": api_data["hava_durumu_ana_durum"],
            "açıklama": api_data["hava_durumu_aciklama"],
            "ikon": api_data["hava_durumu_ikon"]
        },
        "sıcaklık": {
            "mevcut": api_data["sicaklik_mevcut"],
            "hissedilen": api_data["sicaklik_hissedilen"],
            "minimum": api_data["sicaklik_minimum"],
            "maksimum": api_data["sicaklik_maksimum"],
            "birim": temp_unit
        },
        "atmosfer": {
            "basınç": api_data["atmosfer_basinc"],
            "nem": api_data["atmosfer_nem"],
            "görüş_mesafesi": api_data["atmosfer_gorus_mesafesi"]
        },
        "rüzgar": {
            "hız": api_data["ruzgar_hiz"],
            "yön": api_data["ruzgar_yon"],
            "birim": speed_unit
        },
        "bulutluluk": {
            "yüzde": api_data["bulutluluk_yuzde"]
        },
        "güneş": {
            "doğuş": api_data["gunes_dogus"],
            "batış": api_data["gunes_batis"]
        },
        "zaman": {
            "veri_zamanı": api_data["zaman_veri_zamani"],
            "saat_dilimi": api_data["zaman_saat_dilimi"]
        },
        "yağış": {
            "son_1_saat": api_data["yagis_son_1_saat"],
            "birim": api_data["yagis_birim"]
        }
    }

    return result