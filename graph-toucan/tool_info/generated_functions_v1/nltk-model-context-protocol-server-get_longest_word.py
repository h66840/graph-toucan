from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for word processing.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - longest_word (str): The longest valid word that can be formed
    """
    return {
        "longest_word": "apple"
    }

def nltk_model_context_protocol_server_get_longest_word(letters_array: List[str], used_words: List[str]) -> Dict[str, Any]:
    """
    Reads words from 'corpora.txt', filters them using the letters in `letters_array`, 
    excludes those in `used_words`, and returns the longest valid word.

    Args:
        letters_array (List[str]): List of allowed letters (e.g. ['a', 'p', 'l', 'e'])
        used_words (List[str]): List of words already used (these won't be returned)

    Returns:
        Dict[str, Any]: A dictionary containing the longest valid word that can be formed
                       using only the letters in `letters_array` and not present in `used_words`.
                       - longest_word (str): the longest valid word found, or empty string if none
    """
    # Input validation
    if not isinstance(letters_array, list) or not all(isinstance(l, str) and len(l) == 1 for l in letters_array):
        raise ValueError("letters_array must be a list of single-character strings")
    
    if not isinstance(used_words, list) or not all(isinstance(w, str) for w in used_words):
        raise ValueError("used_words must be a list of strings")

    # Simulate reading from corpora.txt (in real scenario, this would read from file)
    # For demo, we'll use a small set of example words
    corpora_words = [
        "apple", "app", "lap", "peel", "leap", "pale", "peel", "elk", "lake", 
        "peak", "leek", "peep", "ape", "pap", "eel", "ale", "pal", "pea", "lap"
    ]

    # Convert letters_array to a multiset (count of each letter)
    from collections import Counter
    available_letters = Counter(letters_array)

    valid_words = []
    
    for word in corpora_words:
        # Skip if already used
        if word in used_words:
            continue
            
        # Check if word can be formed with available letters
        word_letters = Counter(word)
        if all(available_letters[letter] >= count for letter, count in word_letters.items()):
            valid_words.append(word)
    
    # Find the longest word
    longest_word = max(valid_words, key=len) if valid_words else ""
    
    # Return result in expected format
    return {
        "longest_word": longest_word
    }