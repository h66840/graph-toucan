from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cat facts.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - fact (str): A random cat fact
    """
    # Simulated cat facts
    cat_facts = [
        "Cats spend about 70% of their lives sleeping.",
        "A group of cats is called a clowder."
    ]
    
    return {
        "fact": cat_facts[0]  # Return one random fact (simulated)
    }

def cat_facts_service_cat_fact() -> Dict[str, Any]:
    """
    Cat Facts API'den rastgele kedi bilgisi alır.
    
    Bu fonksiyon, dış bir API çağrısını simüle ederek rastgele bir kedi bilgisi döner.
    
    Returns:
        Dict[str, Any]: Rastgele kedi bilgisi içeren sözlük.
            - fact (str): Cat Facts API tarafından dönen rastgele bir kedi bilgisi
    """
    try:
        # Dış API'den veri al
        api_data = call_external_api("cat-facts-service-cat_fact")
        
        # Sonucu oluştur
        result = {
            "fact": api_data["fact"]
        }
        
        return result
        
    except Exception as e:
        # Hata durumunda varsayılan bir kedi bilgisi döner
        return {
            "fact": "Cats have five toes on their front paws, but only four on their back ones."
        }