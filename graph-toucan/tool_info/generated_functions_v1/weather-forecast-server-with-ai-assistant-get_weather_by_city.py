from typing import Dict, Any, Optional
import random
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - error (str): Error message if any, otherwise empty string
        - mesaj (str): Human-readable message about result
        - sehir (str): Name of the requested city
        - ulke_kodu (str): Country code in ISO format
        - konum_enlem (float): Latitude of the location
        - konum_boylam (float): Longitude of the location
        - konum_sehir (str): City name in location data
        - konum_ulke (str): Country code in location data
        - hava_durumu_ana_durum (str): Main weather condition (e.g., Clear, Rain)
        - hava_durumu_aciklama (str): Weather description in Turkish
        - hava_durumu_ikon (str): Weather icon code
        - sicaklik_mevcut (float): Current temperature
        - sicaklik_hissedilen (float): Feels-like temperature
        - sicaklik_minimum (float): Minimum temperature
        - sicaklik_maksimum (float): Maximum temperature
        - sicaklik_birim (str): Temperature unit (e.g., °C, °F)
        - atmosfer_basinc (int): Atmospheric pressure in hPa
        - atmosfer_nem (int): Humidity percentage
        - atmosfer_gorus_mesafesi (int): Visibility in meters
        - ruzgar_hiz (float): Wind speed
        - ruzgar_yon (int): Wind direction in degrees
        - ruzgar_birim (str): Wind speed unit
        - bulutluluk_yuzde (int): Cloudiness percentage
        - gunes_dogus (int): Sunrise time as Unix timestamp
        - gunes_batis (int): Sunset time as Unix timestamp
        - zaman_veri_zamani (int): Data timestamp as Unix timestamp
        - zaman_saat_dilimi (int): Timezone offset in seconds
    """
    # Simulate possible error cases
    if random.random() < 0.1:  # 10% error rate simulation
        return {
            "error": "API request failed",
            "mesaj": "Şehir bulunamadı",
            "sehir": "",
            "ulke_kodu": "TR",
            "konum_enlem": 0.0,
            "konum_boylam": 0.0,
            "konum_sehir": "",
            "konum_ulke": "",
            "hava_durumu_ana_durum": "",
            "hava_durumu_aciklama": "",
            "hava_durumu_ikon": "",
            "sicaklik_mevcut": 0.0,
            "sicaklik_hissedilen": 0.0,
            "sicaklik_minimum": 0.0,
            "sicaklik_maksimum": 0.0,
            "sicaklik_birim": "",
            "atmosfer_basinc": 0,
            "atmosfer_nem": 0,
            "atmosfer_gorus_mesafesi": 0,
            "ruzgar_hiz": 0.0,
            "ruzgar_yon": 0,
            "ruzgar_birim": "",
            "bulutluluk_yuzde": 0,
            "gunes_dogus": 0,
            "gunes_batis": 0,
            "zaman_veri_zamani": 0,
            "zaman_saat_dilimi": 0,
        }

    # Generate realistic mock data
    city_names = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya"]
    weather_conditions = [
        ("Clear", "Açık", "01d"),
        ("Clouds", "Parçalı Bulutlu", "02d"),
        ("Rain", "Yağmurlu", "10d"),
        ("Snow", "Karlı", "13d"),
        ("Fog", "Sisli", "50d"),
    ]
    current_condition = random.choice(weather_conditions)

    now = datetime.now()
    sunrise = int((now.replace(hour=6, minute=0, second=0, microsecond=0) - datetime(1970, 1, 1)).total_seconds())
    sunset = int((now.replace(hour=18, minute=0, second=0, microsecond=0) - datetime(1970, 1, 1)).total_seconds())
    data_time = int(now.timestamp())
    timezone_offset = 10800  # UTC+3 for Turkey

    temp_base = random.uniform(0, 35)
    temp_unit = "°C"

    return {
        "error": "",
        "mesaj": "Hava durumu bilgisi başarıyla alındı",
        "sehir": random.choice(city_names),
        "ulke_kodu": "TR",
        "konum_enlem": round(random.uniform(36.0, 42.0), 6),
        "konum_boylam": round(random.uniform(26.0, 45.0), 6),
        "konum_sehir": random.choice(city_names),
        "konum_ulke": "TR",
        "hava_durumu_ana_durum": current_condition[0],
        "hava_durumu_aciklama": current_condition[1],
        "hava_durumu_ikon": current_condition[2],
        "sicaklik_mevcut": round(temp_base, 1),
        "sicaklik_hissedilen": round(temp_base + random.uniform(-3, 3), 1),
        "sicaklik_minimum": round(temp_base - random.uniform(2, 10), 1),
        "sicaklik_maksimum": round(temp_base + random.uniform(2, 10), 1),
        "sicaklik_birim": temp_unit,
        "atmosfer_basinc": random.randint(980, 1040),
        "atmosfer_nem": random.randint(30, 95),
        "atmosfer_gorus_mesafesi": random.randint(1000, 10000),
        "ruzgar_hiz": round(random.uniform(0, 15), 1),
        "ruzgar_yon": random.randint(0, 360),
        "ruzgar_birim": "m/s",
        "bulutluluk_yuzde": random.randint(0, 100),
        "gunes_dogus": sunrise,
        "gunes_batis": sunset,
        "zaman_veri_zamani": data_time,
        "zaman_saat_dilimi": timezone_offset,
    }


def weather_forecast_server_with_ai_assistant_get_weather_by_city(
    city_name: str, country_code: Optional[str] = None, units: Optional[str] = None
) -> Dict[str, Any]:
    """
    Şehir adına göre hava durumu bilgilerini getirir.

    Bu fonksiyon, dış bir API'ye benzetilmiş veri kaynağından şehir bazlı hava durumu bilgilerini alır
    ve istenen yapıdaki JSON formatında döner.

    Args:
        city_name (str): Şehir adı
        country_code (str, optional): Ülke kodu (örn: TR, US)
        units (str, optional): Ölçü birimi (metric, imperial, standard)

    Returns:
        Dict[str, Any]: JSON formatında hava durumu bilgileri. Hata durumunda 'error' ve 'mesaj' alanları döner.
        Başarılı durumda aşağıdaki yapıyı içerir:
        - mesaj (str): Sonuç hakkında insan-okunabilir mesaj
        - şehir (str): İstenen şehir adı
        - ülke_kodu (str): Ülke kodu (ISO formatında)
        - konum (Dict): Coğrafi konum bilgileri (enlem, boylam, şehir, ülke)
        - hava_durumu (Dict): Hava durumu durumu (ana_durum, açıklama, ikon)
        - sıcaklık (Dict): Sıcaklık değerleri (mevcut, hissedilen, minimum, maksimum, birim)
        - atmosfer (Dict): Atmosferik koşullar (basınç, nem, görüş_mesafesi)
        - rüzgar (Dict): Rüzgar bilgileri (hız, yön, birim)
        - bulutluluk (Dict): Bulutluluk yüzdesi
        - güneş (Dict): Güneşin doğuş ve batış zamanları (timestamp)
        - zaman (Dict): Veri zamanı ve saat dilimi bilgisi
    """
    # Input validation
    if not city_name or not city_name.strip():
        return {
            "error": "City name is required",
            "mesaj": "Şehir adı gereklidir"
        }

    # Call external API simulation
    api_response = call_external_api("get_weather")

    # If there was an error in API call
    if api_response["error"]:
        return {
            "error": api_response["error"],
            "mesaj": api_response["mesaj"]
        }

    # Transform the flat API response into nested structure
    result = {
        "mesaj": api_response["mesaj"],
        "şehir": api_response["sehir"],
        "ülke_kodu": api_response["ulke_kodu"],
        "konum": {
            "enlem": api_response["konum_enlem"],
            "boylam": api_response["konum_boylam"],
            "şehir": api_response["konum_sehir"],
            "ülke": api_response["konum_ulke"]
        },
        "hava_durumu": {
            "ana_durum": api_response["hava_durumu_ana_durum"],
            "açıklama": api_response["hava_durumu_aciklama"],
            "ikon": api_response["hava_durumu_ikon"]
        },
        "sıcaklık": {
            "mevcut": api_response["sicaklik_mevcut"],
            "hissedilen": api_response["sicaklik_hissedilen"],
            "minimum": api_response["sicaklik_minimum"],
            "maksimum": api_response["sicaklik_maksimum"],
            "birim": api_response["sicaklik_birim"]
        },
        "atmosfer": {
            "basınç": api_response["atmosfer_basinc"],
            "nem": api_response["atmosfer_nem"],
            "görüş_mesafesi": api_response["atmosfer_gorus_mesafesi"]
        },
        "rüzgar": {
            "hız": api_response["ruzgar_hiz"],
            "yön": api_response["ruzgar_yon"],
            "birim": api_response["ruzgar_birim"]
        },
        "bulutluluk": {
            "yüzde": api_response["bulutluluk_yuzde"]
        },
        "güneş": {
            "doğuş": api_response["gunes_dogus"],
            "batış": api_response["gunes_batis"]
        },
        "zaman": {
            "veri_zamanı": api_response["zaman_veri_zamani"],
            "saat_dilimi": api_response["zaman_saat_dilimi"]
        }
    }

    return result