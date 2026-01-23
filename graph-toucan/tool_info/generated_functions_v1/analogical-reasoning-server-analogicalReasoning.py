from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for analogical reasoning.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - analogyId (str): Unique identifier for the analogy
        - purpose (str): Purpose of the analogy; one of "explanation", "prediction", "problem-solving", "creative-generation"
        - iteration (int): Current iteration number
        - sourceDomain (str): Name of the source domain
        - targetDomain (str): Name of the target domain
        - mappingCount (int): Number of established mappings
        - inferenceCount (int): Number of inferences drawn
        - nextOperationNeeded (bool): Whether another operation is needed
        - suggestedOperations_0 (str): First suggested next operation
        - suggestedOperations_1 (str): Second suggested next operation
    """
    return {
        "analogyId": "analogy-12345",
        "purpose": "problem-solving",
        "iteration": 1,
        "sourceDomain": "Mechanical Systems",
        "targetDomain": "Economic Markets",
        "mappingCount": 3,
        "inferenceCount": 2,
        "nextOperationNeeded": True,
        "suggestedOperations_0": "add-mapping",
        "suggestedOperations_1": "draw-inference"
    }

def analogical_reasoning_server_analogicalReasoning(
    analogyId: str,
    confidence: float,
    iteration: int,
    purpose: str,
    sourceDomain: Dict[str, Any],
    targetDomain: Dict[str, Any],
    mappings: Optional[List[Dict[str, Any]]] = None,
    inferences: Optional[List[Dict[str, Any]]] = None,
    limitations: Optional[List[str]] = None,
    strengths: Optional[List[str]] = None,
    suggestedOperations: Optional[List[str]] = None,
    nextOperationNeeded: bool = False
) -> Dict[str, Any]:
    """
    Performs analogical reasoning between a source and target domain to support explanation, prediction,
    problem-solving, or creative generation.

    This function computes a structured representation of the analogy, including mappings, inferences,
    and evaluation metrics, based purely on input parameters.

    Args:
        analogyId (str): Unique identifier for this analogy
        confidence (float): Confidence in the overall analogy (0.0-1.0)
        iteration (int): Current iteration of the analogy development
        purpose (str): Purpose of the analogy; must be one of "explanation", "prediction",
                      "problem-solving", or "creative-generation"
        sourceDomain (Dict[str, Any]): The familiar domain used as the basis for the analogy,
                                       must include at least a 'name' field
        targetDomain (Dict[str, Any]): The domain being understood through the analogy,
                                       must include at least a 'name' field
        mappings (Optional[List[Dict[str, Any]]]): List of mappings between source and target elements
        inferences (Optional[List[Dict[str, Any]]]): List of inferences drawn from the analogy
        limitations (Optional[List[str]]): List of limitations of the analogy
        strengths (Optional[List[str]]): List of strengths of the analogy
        suggestedOperations (Optional[List[str]]): List of suggested next operations
        nextOperationNeeded (bool): Whether further refinement is needed

    Returns:
        Dict[str, Any]: A dictionary containing the structured analogy output with the following keys:
            - analogyId (str): unique identifier for the analogy
            - purpose (str): purpose of the analogy
            - iteration (int): current iteration number
            - sourceDomain (str): name of the source domain
            - targetDomain (str): name of the target domain
            - mappingCount (int): number of established mappings
            - inferenceCount (int): number of inferences drawn
            - nextOperationNeeded (bool): whether further operations are required
            - suggestedOperations (List[str]): list of suggested next steps

    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Input validation
    if not analogyId:
        raise ValueError("analogyId is required")
    if not (0.0 <= confidence <= 1.0):
        raise ValueError("confidence must be between 0.0 and 1.0")
    if purpose not in ["explanation", "prediction", "problem-solving", "creative-generation"]:
        raise ValueError("purpose must be one of: explanation, prediction, problem-solving, creative-generation")
    if "name" not in sourceDomain:
        raise ValueError("sourceDomain must contain a 'name' field")
    if "name" not in targetDomain:
        raise ValueError("targetDomain must contain a 'name' field")

    # Compute counts
    mapping_count = len(mappings) if mappings is not None else 0
    inference_count = len(inferences) if inferences is not None else 0

    # Use external API simulation to get standardized output (for consistency in real use)
    api_data = call_external_api("analogical-reasoning-server-analogicalReasoning")

    # Construct result using input-derived computation, not just API data
    result = {
        "analogyId": analogyId,
        "purpose": purpose,
        "iteration": iteration,
        "sourceDomain": sourceDomain["name"],
        "targetDomain": targetDomain["name"],
        "mappingCount": mapping_count,
        "inferenceCount": inference_count,
        "nextOperationNeeded": nextOperationNeeded,
        "suggestedOperations": suggestedOperations or [api_data["suggestedOperations_0"], api_data["suggestedOperations_1"]]
    }

    return result