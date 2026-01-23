from typing import Dict, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API by tool name.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - konum_enlem (float): Latitude coordinate
        - konum_boylam (float): Longitude coordinate
        - konum_sehir (str): City name
        - konum_ulke (str): Country code
        - hava_durumu_ana_durum (str): Main weather condition (e.g., Clear, Clouds)
        - hava_durumu_aciklama (str): Detailed weather description
        - hava_durumu_ikon (str): Weather icon code
        - sicaklik_mevcut (float): Current temperature
        - sicaklik_hissedilen (float): Feels-like temperature
        - sicaklik_minimum (float): Minimum temperature
        - sicaklik_maksimum (float): Maximum temperature
        - sicaklik_birim (str): Temperature unit ('°C' or '°F')
        - atmosfer_basinc (int): Atmospheric pressure in hPa
        - atmosfer_nem (int): Humidity percentage
        - atmosfer_gorus_mesafesi (int): Visibility distance in meters
        - ruzgar_hiz (float): Wind speed
        - ruzgar_yon (int): Wind direction in degrees
        - ruzgar_birim (str): Wind speed unit ('m/s' or 'mph')
        - bulutluluk_yuzde (int): Cloudiness percentage
        - gunes_dogus (int): Sunrise time as Unix timestamp
        - gunes_batis (int): Sunset time as Unix timestamp
        - zaman_veri_zamani (int): Data retrieval time as Unix timestamp
        - zaman_saat_dilimi (int): Timezone offset in seconds
    """
    # Simulate realistic weather data based on coordinates
    latitude = 40.7128 if abs(40.7128) <= 90 else 0.0
    longitude = -74.0060 if abs(-74.0060) <= 180 else 0.0

    # Random but plausible weather values
    main_conditions = ["Clear", "Clouds", "Rain", "Snow", "Mist"]
    descriptions = {
        "Clear": "açık hava",
        "Clouds": "parçalı bulutlu",
        "Rain": "hafif yağmur",
        "Snow": "kar yağıyor",
        "Mist": "sisli"
    }
    icons = {
        "Clear": "01d",
        "Clouds": "02d",
        "Rain": "10d",
        "Snow": "13d",
        "Mist": "50d"
    }

    condition = random.choice(main_conditions)
    temp_c = round(random.uniform(15, 35), 1)
    feels_like = round(temp_c + random.uniform(-3, 3), 1)
    temp_min = round(temp_c - random.uniform(2, 5), 1)
    temp_max = round(temp_c + random.uniform(2, 5), 1)

    pressure = random.randint(980, 1040)
    humidity = random.randint(30, 90)
    visibility = random.randint(1000, 10000)
    wind_speed = round(random.uniform(1, 10), 1)
    wind_deg = random.randint(0, 360)
    cloudiness = random.randint(0, 100)

    now = int(time.time())
    timezone_offset = random.choice([-18000, -14400, 0, 3600, 7200, 10800])  # Example offsets
    sunrise = now - 12 * 3600 + timezone_offset  # Rough estimate
    sunset = now - 4 * 3600 + timezone_offset

    unit_temp = "°C"
    unit_wind = "m/s"

    return {
        "konum_enlem": latitude,
        "konum_boylam": longitude,
        "konum_sehir": "New York",
        "konum_ulke": "US",
        "hava_durumu_ana_durum": condition,
        "hava_durumu_aciklama": descriptions[condition],
        "hava_durumu_ikon": icons[condition],
        "sicaklik_mevcut": temp_c,
        "sicaklik_hissedilen": feels_like,
        "sicaklik_minimum": temp_min,
        "sicaklik_maksimum": temp_max,
        "sicaklik_birim": unit_temp,
        "atmosfer_basinc": pressure,
        "atmosfer_nem": humidity,
        "atmosfer_gorus_mesafesi": visibility,
        "ruzgar_hiz": wind_speed,
        "ruzgar_yon": wind_deg,
        "ruzgar_birim": unit_wind,
        "bulutluluk_yuzde": cloudiness,
        "gunes_dogus": sunrise,
        "gunes_batis": sunset,
        "zaman_veri_zamani": now,
        "zaman_saat_dilimi": timezone_offset,
    }


def deneme_mcp_server_get_weather_by_coordinates(latitude: float, longitude: float, units: Optional[str] = "metric") -> Dict[str, Any]:
    """
    Enlem ve boylam koordinatlarına göre hava durumu bilgilerini getirir.

    Args:
        latitude (float): Enlem (-90 ile 90 arasında)
        longitude (float): Boylam (-180 ile 180 arasında)
        units (Optional[str]): Ölçü birimi (metric, imperial, standard). Varsayılan: metric

    Returns:
        Dict[str, Any]: JSON formatında hava durumu bilgileri, aşağıdaki yapıda:
        - konum: Dict with 'enlem', 'boylam', 'şehir', 'ülke'
        - hava_durumu: Dict with 'ana_durum', 'açıklama', 'ikon'
        - sıcaklık: Dict with 'mevcut', 'hissedilen', 'minimum', 'maksimum', 'birim'
        - atmosfer: Dict with 'basınç', 'nem', 'görüş_mesafesi'
        - rüzgar: Dict with 'hız', 'yön', 'birim'
        - bulutluluk: Dict with 'yüzde'
        - güneş: Dict with 'doğuş', 'batış'
        - zaman: Dict with 'veri_zamanı', 'saat_dilimi'

    Raises:
        ValueError: Eğer latitude veya longitude geçersizse
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    if units not in ["metric", "imperial", "standard", None]:
        raise ValueError("Units must be one of: metric, imperial, standard")

    # Fetch simulated external data
    raw_data = call_external_api("deneme-mcp-server-get_weather_by_coordinates")

    # Convert temperature to Fahrenheit if units is imperial
    temp_mevcut = raw_data["sicaklik_mevcut"]
    temp_hissedilen = raw_data["sicaklik_hissedilen"]
    temp_min = raw_data["sicaklik_minimum"]
    temp_max = raw_data["sicaklik_maksimum"]
    birim = raw_data["sicaklik_birim"]

    if units == "imperial":
        temp_mevcut = temp_mevcut * 9 / 5 + 32
        temp_hissedilen = temp_hissedilen * 9 / 5 + 32
        temp_min = temp_min * 9 / 5 + 32
        temp_max = temp_max * 9 / 5 + 32
        birim = "°F"

    # Convert wind speed to mph if units is imperial
    ruzgar_hiz = raw_data["ruzgar_hiz"]
    ruzgar_birim = raw_data["ruzgar_birim"]
    if units == "imperial":
        ruzgar_hiz = round(ruzgar_hiz * 2.23694, 1)
        ruzgar_birim = "mph"

    # Construct the nested output structure as per schema
    result = {
        "konum": {
            "enlem": raw_data["konum_enlem"],
            "boylam": raw_data["konum_boylam"],
            "şehir": raw_data["konum_sehir"],
            "ülke": raw_data["konum_ulke"]
        },
        "hava_durumu": {
            "ana_durum": raw_data["hava_durumu_ana_durum"],
            "açıklama": raw_data["hava_durumu_aciklama"],
            "ikon": raw_data["hava_durumu_ikon"]
        },
        "sıcaklık": {
            "mevcut": temp_mevcut,
            "hissedilen": temp_hissedilen,
            "minimum": temp_min,
            "maksimum": temp_max,
            "birim": birim
        },
        "atmosfer": {
            "basınç": raw_data["atmosfer_basinc"],
            "nem": raw_data["atmosfer_nem"],
            "görüş_mesafesi": raw_data["atmosfer_gorus_mesafesi"]
        },
        "rüzgar": {
            "hız": ruzgar_hiz,
            "yön": raw_data["ruzgar_yon"],
            "birim": ruzgar_birim
        },
        "bulutluluk": {
            "yüzde": raw_data["bulutluluk_yuzde"]
        },
        "güneş": {
            "doğuş": raw_data["gunes_dogus"],
            "batış": raw_data["gunes_batis"]
        },
        "zaman": {
            "veri_zamanı": raw_data["zaman_veri_zamani"],
            "saat_dilimi": raw_data["zaman_saat_dilimi"]
        }
    }

    return result