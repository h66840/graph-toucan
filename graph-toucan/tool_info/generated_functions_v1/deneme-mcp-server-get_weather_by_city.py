from typing import Dict, Any, Optional
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - konum_enlem (float): Latitude of the location
        - konum_boylam (float): Longitude of the location
        - konum_sehir (str): City name
        - konum_ulke (str): Country code
        - hava_durumu_ana_durum (str): Main weather condition (e.g., Clear, Clouds)
        - hava_durumu_aciklama (str): Detailed weather description
        - hava_durumu_ikon (str): Weather icon code
        - sicaklik_mevcut (float): Current temperature
        - sicaklik_hissedilen (float): Feels-like temperature
        - sicaklik_minimum (float): Minimum temperature
        - sicaklik_maksimum (float): Maximum temperature
        - sicaklik_birim (str): Temperature unit (e.g., Celsius, Fahrenheit)
        - atmosfer_basinc (int): Atmospheric pressure in hPa
        - atmosfer_nem (int): Humidity percentage
        - atmosfer_gorus_mesafesi (int): Visibility in meters
        - ruzgar_hiz (float): Wind speed
        - ruzgar_yon (int): Wind direction in degrees
        - ruzgar_birim (str): Wind speed unit (e.g., m/s, mph)
        - bulutluluk_yuzde (int): Cloud coverage percentage
        - gunes_dogus (int): Sunrise time as Unix timestamp
        - gunes_batis (int): Sunset time as Unix timestamp
        - zaman_veri_zamani (int): Data timestamp as Unix timestamp
        - zaman_saat_dilimi (int): Timezone offset in seconds
        - yagis_son_1_saat (float): Rainfall amount in last hour
        - yagis_birim (str): Rain unit (e.g., mm)
    """
    # Simulate realistic weather data based on city and units
    now = datetime.now(timezone.utc)
    base_timestamp = int(now.timestamp())
    timezone_offset = random.choice([-18000, -14400, 0, 3600, 7200, 10800])  # Example offsets

    return {
        "konum_enlem": round(random.uniform(-90, 90), 6),
        "konum_boylam": round(random.uniform(-180, 180), 6),
        "konum_sehir": "Istanbul",
        "konum_ulke": "TR",
        "hava_durumu_ana_durum": random.choice(["Clear", "Clouds", "Rain", "Snow", "Thunderstorm"]),
        "hava_durumu_aciklama": "clear sky",
        "hava_durumu_ikon": "01d",
        "sicaklik_mevcut": round(random.uniform(15, 35), 2),
        "sicaklik_hissedilen": round(random.uniform(15, 35), 2),
        "sicaklik_minimum": round(random.uniform(10, 20), 2),
        "sicaklik_maksimum": round(random.uniform(30, 40), 2),
        "sicaklik_birim": "Celsius",
        "atmosfer_basinc": random.randint(980, 1040),
        "atmosfer_nem": random.randint(30, 90),
        "atmosfer_gorus_mesafesi": 10000,
        "ruzgar_hiz": round(random.uniform(0, 15), 2),
        "ruzgar_yon": random.randint(0, 360),
        "ruzgar_birim": "m/s",
        "bulutluluk_yuzde": random.randint(0, 100),
        "gunes_dogus": base_timestamp - 36000,  # 10 hours before now
        "gunes_batis": base_timestamp + 36000,  # 10 hours after now
        "zaman_veri_zamani": base_timestamp,
        "zaman_saat_dilimi": timezone_offset,
        "yagis_son_1_saat": round(random.uniform(0, 5), 2),
        "yagis_birim": "mm",
    }


def deneme_mcp_server_get_weather_by_city(
    city_name: str, country_code: Optional[str] = None, units: Optional[str] = None
) -> Dict[str, Any]:
    """
    Şehir adına göre hava durumu bilgilerini getirir.

    Args:
        city_name (str): Şehir adı
        country_code (str, optional): Ülke kodu (örn: TR, US)
        units (str, optional): Ölçü birimi (metric, imperial, standard)

    Returns:
        JSON formatında hava durumu bilgileri içeren sözlük. İçerdiği anahtarlar:
        - konum: enlem, boylam, şehir, ülke
        - hava_durumu: ana_durum, açıklama, ikon
        - sıcaklık: mevcut, hissedilen, minimum, maksimum, birim
        - atmosfer: basınç, nem, görüş_mesafesi
        - rüzgar: hız, yön, birim
        - bulutluluk: yüzde
        - güneş: doğuş, batış
        - zaman: veri_zamanı, saat_dilimi
        - yağış: son_1_saat, birim (opsiyonel)
    """
    # Input validation
    if not city_name or not city_name.strip():
        raise ValueError("city_name is required and cannot be empty")

    if units and units not in ["metric", "imperial", "standard"]:
        raise ValueError("units must be one of: metric, imperial, standard")

    # Fetch simulated external data
    api_data = call_external_api("deneme-mcp-server-get_weather_by_city")

    # Adjust temperature unit based on requested units
    temp_unit = "Celsius"
    if units == "imperial":
        temp_unit = "Fahrenheit"
    elif units == "standard":
        temp_unit = "Kelvin"

    # Construct the nested output structure
    result: Dict[str, Any] = {
        "konum": {
            "enlem": api_data["konum_enlem"],
            "boylam": api_data["konum_boylam"],
            "şehir": api_data["konum_sehir"],
            "ülke": api_data["konum_ulke"],
        },
        "hava_durumu": {
            "ana_durum": api_data["hava_durumu_ana_durum"],
            "açıklama": api_data["hava_durumu_aciklama"],
            "ikon": api_data["hava_durumu_ikon"],
        },
        "sıcaklık": {
            "mevcut": api_data["sicaklik_mevcut"],
            "hissedilen": api_data["sicaklik_hissedilen"],
            "minimum": api_data["sicaklik_minimum"],
            "maksimum": api_data["sicaklik_maksimum"],
            "birim": temp_unit,
        },
        "atmosfer": {
            "basınç": api_data["atmosfer_basinc"],
            "nem": api_data["atmosfer_nem"],
            "görüş_mesafesi": api_data["atmosfer_gorus_mesafesi"],
        },
        "rüzgar": {
            "hız": api_data["ruzgar_hiz"],
            "yön": api_data["ruzgar_yon"],
            "birim": api_data["ruzgar_birim"],
        },
        "bulutluluk": {
            "yüzde": api_data["bulutluluk_yuzde"],
        },
        "güneş": {
            "doğuş": api_data["gunes_dogus"],
            "batış": api_data["gunes_batis"],
        },
        "zaman": {
            "veri_zamanı": api_data["zaman_veri_zamani"],
            "saat_dilimi": api_data["zaman_saat_dilimi"],
        },
    }

    # Add rainfall data if available
    if "yagis_son_1_saat" in api_data and api_data["yagis_son_1_saat"] > 0:
        result["yağış"] = {
            "son_1_saat": api_data["yagis_son_1_saat"],
            "birim": api_data["yagis_birim"],
        }

    return result