from typing import Dict, Any

def pymcp_pirate_summary(text: str) -> Dict[str, Any]:
    """
    Summarise the given text in a pirate style.
    
    Args:
        text (str): The input text to be summarized in pirate style.
        
    Returns:
        Dict[str, Any]: A dictionary containing the pirate-style summary.
            - summary (str): The generated pirate-style summary of the input text.
            
    Raises:
        ValueError: If the input text is empty or not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input 'text' must be a string.")
    if not text.strip():
        raise ValueError("Input 'text' cannot be empty or whitespace only.")
    
    # Simple transformation to pirate-style summary
    # Replace common words and add pirate flavor
    pirate_words = {
        'the': 'thar',
        'is': 'be',
        'are': 'be',
        'you': 'ye',
        'your': 'yer',
        'have': 'hast',
        'with': 'wit',
        'to': "t'",
        'for': "fer",
        'and': 'an',
        'of': "o'",
        'my': "me",
        'me': "meself",
        'hello': 'ahoy',
        'hi': 'ahoy',
        'friend': 'matey',
        'goodbye': 'avast',
        'stop': 'halt',
        'run': 'sprint',
        'fast': 'swift',
        'ship': 'vessel',
        'captain': 'cap’n',
        'treasure': 'booty',
        'gold': 'doubloons',
        'island': 'isle',
        'sea': 'briny deep',
        'ocean': 'endless blue'
    }
    
    # Convert to lowercase for replacement, then fix capitalization
    lower_text = text.lower()
    words = lower_text.split()
    
    # Replace words with pirate equivalents
    pirate_words_replaced = []
    for word in words:
        # Handle punctuation
        punctuation = ''
        while word and not word[-1].isalnum():
            punctuation = word[-1] + punctuation
            word = word[:-1]
        if not word:
            pirate_words_replaced.append(punctuation)
            continue
        pirate_word = pirate_words.get(word, word)
        pirate_words_replaced.append(pirate_word + punctuation)
    
    # Join back and add pirate flair
    pirate_summary = ' '.join(pirate_words_replaced)
    
    # Capitalize first letter and add pirate exclamation if needed
    if pirate_summary:
        pirate_summary = pirate_summary[0].upper() + pirate_summary[1:]
        if not any(pirate_summary.endswith(p) for p in '.!?'):
            pirate_summary += ', ye scurvy dog!'
    
    return {"summary": pirate_summary}