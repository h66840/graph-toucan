from typing import List, Dict, Any
import re

from typing import List, Dict, Any
import re

def lyrical_mcp_count_syllables(word: str) -> int:
    """
    Count the number of syllables in a word using heuristic rules.
    
    Args:
        word (str): The word to count syllables for.
    
    Returns:
        int: The number of syllables in the word. Returns at least 1 for valid words.
    """
    word = word.lower().strip()
    if not word.isalpha():
        return 0
    
    # Handle empty word
    if not word:
        return 0
    
    # Handle single character words
    if len(word) == 1:
        return 1 if word in "aeiouy" else 0
    
    # Count vowel groups (consecutive vowels count as one syllable)
    vowels = "aeiouy"
    syllable_count = 0
    prev_was_vowel = False
    
    for i, char in enumerate(word):
        is_vowel = char in vowels
        
        if is_vowel:
            # Only count if previous char was not a vowel (new vowel group)
            if not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = True
        else:
            prev_was_vowel = False
    
    # Adjust for silent 'e' at the end
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    # Adjust for 'le' at the end (e.g., "table", "little")
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    
    # Adjust for words ending with 'ed' (past tense, often doesn't add a syllable)
    if word.endswith('ed') and len(word) > 2:
        # If the word before 'ed' ends with 't' or 'd', it usually adds a syllable
        if word[-3] in 'td':
            pass  # Keep the syllable
        # If the word before 'ed' ends with a vowel sound, subtract one
        elif word[-3] in vowels:
            syllable_count -= 1
    
    # Ensure at least 1 syllable for valid words
    return max(1, syllable_count)

def lyrical_mcp_count_syllables(input_string: str) -> Dict[str, List[int]]:
    """
    Counts the number of syllables for each line in the input English text string.
    
    This function splits the input string into lines, and for each line, counts the total
    number of syllables by summing syllable counts of individual words. Blank lines return 0.
    It uses heuristic rules for syllable counting.
    
    Args:
        input_string (str): The input text string where each line will be analyzed.
    
    Returns:
        Dict[str, List[int]]: A dictionary with key 'syllable_counts' mapping to a list of integers.
                              Each integer represents the syllable count for the respective line.
                              Blank or unparseable lines return 0.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string.")
    
    lines = input_string.splitlines()
    syllable_counts = []
    
    for line in lines:
        line = line.strip()
        if not line:
            syllable_counts.append(0)
            continue
        
        words = re.findall(r"[a-zA-Z]+", line)
        total_syllables = sum(count_syllables(word) for word in words)
        syllable_counts.append(total_syllables)
    
    return {"syllable_counts": syllable_counts}