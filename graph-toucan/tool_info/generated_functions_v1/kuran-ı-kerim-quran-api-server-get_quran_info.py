from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Quran information from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_juz_count (int): Total number of juz (parts) in the Quran
        - total_surah_count (int): Total number of surahs (chapters) in the Quran
        - total_ayah_count (int): Total number of ayahs (verses) in the Quran
        - total_ruku_count (int): Total number of rukus (paragraphs) in the Quran
        - total_makki_surahs (int): Number of Makki (revealed in Mecca) surahs
        - total_madani_surahs (int): Number of Madani (revealed in Medina) surahs
        - total_sajdah_ayat (int): Number of verses in the Quran that require prostration (sajdah)
        - sajdah_details_0_surah_number (int): Surah number of first sajdah ayah
        - sajdah_details_0_ayah_number (int): Ayah number of first sajdah ayah
        - sajdah_details_0_type (str): Type of sajdah (obligatory or recommended)
        - surah_list_0_name (str): Name of first surah
        - surah_list_0_revelation_order (int): Revelation order of first surah
        - surah_list_0_ayah_count (int): Number of ayahs in first surah
        - surah_list_0_classification (str): Classification of first surah (Makki/Madani)
        - juz_details_0_juz_number (int): Juz number
        - juz_details_0_start_surah (int): Starting surah number of juz
        - juz_details_0_start_ayah (int): Starting ayah number of juz
        - juz_details_0_end_surah (int): Ending surah number of juz
        - juz_details_0_end_ayah (int): Ending ayah number of juz
        - metadata_compilation_history (str): Compilation history of the Quran
        - metadata_script_type (str): Script type of the Quranic text
        - metadata_version (str): Version of the Quranic text
    """
    return {
        "total_juz_count": 30,
        "total_surah_count": 114,
        "total_ayah_count": 6236,
        "total_ruku_count": 558,
        "total_makki_surahs": 86,
        "total_madani_surahs": 28,
        "total_sajdah_ayat": 15,
        "sajdah_details_0_surah_number": 32,
        "sajdah_details_0_ayah_number": 15,
        "sajdah_details_0_type": "obligatory",
        "surah_list_0_name": "Al-Fatiha",
        "surah_list_0_revelation_order": 5,
        "surah_list_0_ayah_count": 7,
        "surah_list_0_classification": "Makki",
        "juz_details_0_juz_number": 1,
        "juz_details_0_start_surah": 1,
        "juz_details_0_start_ayah": 1,
        "juz_details_0_end_surah": 2,
        "juz_details_0_end_ayah": 141,
        "metadata_compilation_history": "Compiled during the time of Caliph Abu Bakr and standardized under Caliph Uthman.",
        "metadata_script_type": "Uthmani script",
        "metadata_version": "Uthmani Mushaf v1.0"
    }

def kuran_ı_kerim_quran_api_server_get_quran_info() -> Dict[str, Any]:
    """
    Fetches comprehensive information about the Quran including structural details,
    counts of various components, and metadata.
    
    Returns:
        Dict containing detailed Quranic information with the following keys:
        - total_juz_count (int): Total number of juz (parts) in the Quran
        - total_surah_count (int): Total number of surahs (chapters) in the Quran
        - total_ayah_count (int): Total number of ayahs (verses) in the Quran
        - total_ruku_count (int): Total number of rukus (paragraphs) in the Quran
        - total_makki_surahs (int): Number of Makki (revealed in Mecca) surahs
        - total_madani_surahs (int): Number of Madani (revealed in Medina) surahs
        - total_sajdah_ayat (int): Number of verses in the Quran that require prostration (sajdah)
        - sajdah_details (List[Dict]): List of sajdah ayahs with details like surah number, ayah number, and type
        - surah_list (List[Dict]): List of all surahs with their names, order of revelation, number of ayahs, and classification
        - juz_details (List[Dict]): Detailed breakdown of each juz including starting and ending surah-ayah range
        - metadata (Dict): Additional metadata such as compilation history, script type, and version of the Quranic text
    
    Raises:
        Exception: If there is an error in retrieving or processing the data.
    """
    try:
        api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_info")
        
        # Construct sajdah_details list
        sajdah_details = [
            {
                "surah_number": api_data["sajdah_details_0_surah_number"],
                "ayah_number": api_data["sajdah_details_0_ayah_number"],
                "type": api_data["sajdah_details_0_type"]
            }
        ]
        
        # Construct surah_list
        surah_list = [
            {
                "name": api_data["surah_list_0_name"],
                "revelation_order": api_data["surah_list_0_revelation_order"],
                "ayah_count": api_data["surah_list_0_ayah_count"],
                "classification": api_data["surah_list_0_classification"]
            }
        ]
        
        # Construct juz_details
        juz_details = [
            {
                "juz_number": api_data["juz_details_0_juz_number"],
                "start_surah": api_data["juz_details_0_start_surah"],
                "start_ayah": api_data["juz_details_0_start_ayah"],
                "end_surah": api_data["juz_details_0_end_surah"],
                "end_ayah": api_data["juz_details_0_end_ayah"]
            }
        ]
        
        # Construct metadata
        metadata = {
            "compilation_history": api_data["metadata_compilation_history"],
            "script_type": api_data["metadata_script_type"],
            "version": api_data["metadata_version"]
        }
        
        # Construct final result
        result = {
            "total_juz_count": api_data["total_juz_count"],
            "total_surah_count": api_data["total_surah_count"],
            "total_ayah_count": api_data["total_ayah_count"],
            "total_ruku_count": api_data["total_ruku_count"],
            "total_makki_surahs": api_data["total_makki_surahs"],
            "total_madani_surahs": api_data["total_madani_surahs"],
            "total_sajdah_ayat": api_data["total_sajdah_ayat"],
            "sajdah_details": sajdah_details,
            "surah_list": surah_list,
            "juz_details": juz_details,
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        raise Exception(f"Missing expected data field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve Quran information: {str(e)}")