from typing import Dict, Any

def elevator_pitch_analyze_idea_tool(idea: str) -> Dict[str, str]:
    """
    Extracts key business components from a given business idea, including sector, target audience, problem, and solution.
    
    Args:
        idea (str): The business idea to analyze. Must be a non-empty string.
    
    Returns:
        Dict[str, str]: A dictionary containing the following keys:
            - sector (str): The industry or market sector identified from the business idea.
            - target_audience (str): The specific group of users or customers the idea targets.
            - problem (str): The core problem or pain point the idea addresses.
            - solution (str): How the idea solves the identified problem, including key features or value proposition.
    
    Raises:
        ValueError: If the input idea is empty or not a string.
    """
    if not isinstance(idea, str):
        raise ValueError("The idea must be a string.")
    if not idea.strip():
        raise ValueError("The idea cannot be empty or whitespace only.")
    
    # Normalize input
    idea_lower = idea.strip().lower()
    
    # Simple keyword-based analysis logic
    sectors = {
        "teknoloji": ["uygulama", "app", "platform", "software", "tech", "digital", "sistem", "ai", "yapay zeka"],
        "sağlık": ["sağlık", "health", "hospital", "clinic", "doktor", "tedavi", "ilaç", "wellness"],
        "eğitim": ["eğitim", "education", "online course", "e-learning", "öğret", "öğretmen", "öğrenci", "kurs"],
        "finans": ["finans", "finance", "bank", "kredi", "payment", "ödeme", "wallet", "cripto", "blockchain"],
        "perakende": ["mağaza", "store", "market", "alışveriş", "shopping", "retail", "ürün", "satış"],
        "ulaştırma": ["taşımacılık", "transport", "logistics", "kurye", "cargo", "shipping", "delivery"],
        "gıda": ["yemek", "food", "restoran", "cafe", "restaurant", "meal", "beslenme", "nutrition"]
    }
    
    # Default values
    sector = "Genel"
    for key, keywords in sectors.items():
        if any(kw in idea_lower for kw in keywords):
            sector = key.title()
            break
    
    # Placeholder logic for target audience based on common phrases
    if "öğrenci" in idea_lower:
        target_audience = "Öğrenciler"
    elif "işletme" in idea_lower or "kurum" in idea_lower or "company" in idea_lower:
        target_audience = "Küçük ve orta ölçekli işletmeler"
    elif "anne" in idea_lower or "baba" in idea_lower or "aile" in idea_lower:
        target_audience = "Aileler"
    elif "yaşlı" in idea_lower or "elderly" in idea_lower:
        target_audience = "Yaşlı bireyler"
    elif "genç" in idea_lower or "youth" in idea_lower:
        target_audience = "Gençler"
    else:
        target_audience = "Genel kitle"
    
    # Extract or infer problem (very basic pattern matching)
    problem_keywords = {
        "zorluk": "kullanıcıların karşılaştığı zorluklar",
        "yavaş": "yavaş süreçler",
        "pahalı": "yüksek maliyetler",
        "zaman": "zaman kaybı",
        "erişim": "sınırlı erişim",
        "kalite": "düşük kalite",
        "güvenlik": "güvenlik endişeleri"
    }
    found_problems = [label for word, label in problem_keywords.items() if word in idea_lower]
    problem = found_problems[0] if found_problems else "Kullanıcıların verimli bir şekilde hedeflerine ulaşamaması"
    
    # Construct solution based on idea content
    if "platform" in idea_lower or "uygulama" in idea_lower or "app" in idea_lower:
        solution = f"Bir {sector.lower()} platformu veya uygulaması geliştirilerek kullanıcılar için merkezileştirilmiş bir çözüm sunulur."
    elif "hizmet" in idea_lower or "service" in idea_lower:
        solution = f"{sector} sektöründe özelleştirilmiş hizmetler ile {target_audience.lower()} için {problem.lower()} çözülür."
    elif "ürün" in idea_lower or "product" in idea_lower:
        solution = f"Yeni bir {sector.lower()} ürünü ile {target_audience.lower()}, {problem.lower()} sorunundan kurtulur."
    else:
        solution = f"{sector} alanında {target_audience} için {problem} sorununu çözmek üzere yenilikçi bir yaklaşım sunulur."
    
    return {
        "sector": sector,
        "target_audience": target_audience,
        "problem": problem,
        "solution": solution
    }