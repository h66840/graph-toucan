from typing import Dict, Any

def elevator_pitch_generate_pitch_tool(
    problem: str,
    sector: str,
    solution: str,
    target_audience: str,
    tone: str
) -> Dict[str, Any]:
    """
    Generates a concise and compelling elevator pitch based on the provided inputs.
    
    Parameters:
        problem (str): The core problem being addressed for the target audience.
        sector (str): The industry or market sector the solution operates in.
        solution (str): The proposed product or service that solves the stated problem.
        target_audience (str): The specific group of users or customers the solution is designed for.
        tone (str): The desired tone of the pitch (e.g., confident, professional, enthusiastic).

    Returns:
        Dict[str, Any]: A dictionary containing the generated pitch and metadata with the following keys:
            - pitch (str): The full generated elevator pitch text.
            - tone_used (str): The tone applied in generating the pitch.
            - sector (str): The industry or market sector.
            - target_audience (str): The intended customer group.
            - problem (str): The core problem addressed.
            - solution (str): The proposed solution.
    """
    # Input validation
    if not all([problem.strip(), sector.strip(), solution.strip(), target_audience.strip(), tone.strip()]):
        raise ValueError("All input fields must be non-empty strings.")

    # Define tone-based prefixes or styles
    tone_modifiers = {
        "confident": "We confidently solve ",
        "professional": "Our professional solution addresses ",
        "enthusiastic": "Excitingly, we tackle ",
        "innovative": "Innovatively, we transform ",
        "visionary": "Visionarily, we're redefining ",
        "urgent": "Urgently, we fix ",
        "inspirational": "Inspiring change, we overcome "
    }

    # Use default tone style if tone not in modifiers
    prefix = tone_modifiers.get(tone.lower(), f"{tone.capitalize()}: ")
    
    # Construct the pitch
    pitch_text = (
        f"{prefix}{problem.lower().rstrip('.')} for {target_audience.lower()} "
        f"in the {sector.lower()} sector, using {solution.lower().rstrip('.')} "
        f"to deliver impactful results."
    )

    # Capitalize first letter and ensure proper ending
    pitch_text = pitch_text[0].upper() + pitch_text[1:]
    if not pitch_text.endswith('.'):
        pitch_text += '.'

    return {
        "pitch": pitch_text,
        "tone_used": tone,
        "sector": sector,
        "target_audience": target_audience,
        "problem": problem,
        "solution": solution
    }