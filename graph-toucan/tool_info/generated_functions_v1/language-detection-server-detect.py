from typing import Dict, List, Any

def language_detection_server_detect(text: str) -> Dict[str, Any]:
    """
    Detect the language of the input text using computational heuristics.
    
    Args:
        text (str): The input text for which language needs to be detected.
    
    Returns:
        Dict[str, Any]: A dictionary containing a list of detected language results.
        Each result includes:
        - language (str): ISO 639-1 language code
        - isReliable (bool): Whether the detection is reliable
        - confidence (float): Confidence score between 0 and 1
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string.")
    
    if not text.strip():
        return {"detections": []}
    
    # Simple heuristic: check for common characters and words
    text_lower = text.lower().strip()
    detections = []
    
    # Basic language indicators based on character sets and common words
    if any(c in text_lower for c in 'àâäéèêëïîôöùûüÿç'):
        detections.append({
            "language": "fr",
            "isReliable": len(text_lower) > 10,
            "confidence": 0.9 if ' et ' in text_lower or ' le ' in text_lower or ' la ' in text_lower else 0.6
        })
    
    if any(c in text_lower for c in 'äöüß'):
        detections.append({
            "language": "de",
            "isReliable": len(text_lower) > 10,
            "confidence": 0.9 if ' der ' in text_lower or ' die ' in text_lower or ' und ' in text_lower else 0.6
        })
    
    if any(c in text_lower for c in 'ñáéíóúü'):
        detections.append({
            "language": "es",
            "isReliable": len(text_lower) > 10,
            "confidence": 0.9 if ' el ' in text_lower or ' la ' in text_lower or ' y ' in text_lower else 0.6
        })
    
    if 'the' in text_lower or 'is' in text_lower or 'are' in text_lower or 'was' in text_lower:
        detections.append({
            "language": "en",
            "isReliable": True,
            "confidence": 0.95
        })
    
    # Default fallback to English if nothing else matches
    if not detections:
        word_count = len(text_lower.split())
        confidence = min(0.3 + (word_count * 0.05), 0.8)  # Confidence increases with text length
        detections.append({
            "language": "en",
            "isReliable": word_count > 5,
            "confidence": confidence
        })
    
    # Sort by confidence descending
    detections.sort(key=lambda x: x["confidence"], reverse=True)
    
    return {"detections": detections}