from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - advice (str): A single piece of random advice or tip returned by the service
    """
    return {
        "advice": "Her sabah bir bardak su içmek, metabolizmayı hızlandırabilir."
    }

def soz_mcp_server_get_advice() -> Dict[str, Any]:
    """
    Rastgele tavsiye döner.
    
    Bu fonksiyon, dış bir servisten rastgele bir yaşam tavsiyesi alır ve bu tavsiyeyi döner.
    Dış servis çağrısı benzetimi için call_external_api fonksiyonu kullanılır.
    
    Returns:
        Dict[str, Any]: Tavsiye içeren bir sözlük. 
        - 'advice' (str): Rastgele bir tavsiye metni
    """
    try:
        # Dış API'den veri al
        api_data = call_external_api("soz-mcp-server-get_advice")
        
        # Sonucu oluştur
        result = {
            "advice": api_data["advice"]
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Expected data field missing in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while fetching advice: {str(e)}")