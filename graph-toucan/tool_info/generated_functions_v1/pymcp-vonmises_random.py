from typing import Dict, Any
import random
import math
from datetime import datetime

def pymcp_vonmises_random(mu: float) -> Dict[str, Any]:
    """
    Generate a random number from the von Mises distribution.
    
    This function generates a random angle from the von Mises distribution with a given mean angle mu (μ)
    and an elicited concentration parameter kappa (κ). The result includes metadata and timestamp.
    
    Args:
        mu (float): The mean angle mu (μ), expressed in radians between 0 and 2π
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - sample (float): A randomly generated angle from the von Mises distribution, in radians [0, 2π]
            - mu (float): The mean angle parameter (μ), echoed back
            - kappa (float): The concentration parameter (κ) used in the distribution
            - timestamp (str): ISO 8601 timestamp indicating when the sample was generated
            - metadata (Dict): Additional information about the sampling process
                - version (str): Method version
                - seed_state (str): String representation of the random seed state before sampling
                
    Raises:
        ValueError: If mu is not within the range [0, 2π]
    """
    # Input validation
    if not (0 <= mu <= 2 * math.pi):
        raise ValueError(f"mu must be in the range [0, 2π] radians. Received: {mu}")
    
    # Elicit or determine kappa - in this implementation, we use a reasonable default
    # that could be adjusted based on application needs
    kappa = 2.0  # concentration parameter, could be made configurable
    
    # Capture timestamp
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    # Capture seed state before sampling
    seed_state = str(random.getstate())
    
    # Generate random sample from von Mises distribution
    sample = random.vonmisesvariate(mu, kappa)
    
    # Normalize sample to [0, 2π] range
    sample = sample % (2 * math.pi)
    
    # Construct metadata
    metadata = {
        "version": "1.0",
        "seed_state": seed_state,
        "distribution": "von Mises",
        "mu_range": [0, 2 * math.pi]
    }
    
    # Return result dictionary matching output schema
    return {
        "sample": float(sample),
        "mu": float(mu),
        "kappa": float(kappa),
        "timestamp": timestamp,
        "metadata": metadata
    }