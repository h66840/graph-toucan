from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for collaborative reasoning.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - session_id (str): Unique identifier for the collaboration session
        - topic (str): The topic or problem being addressed
        - stage (str): Current stage of the collaborative process
        - iteration (int): Current iteration number
        - persona_count (int): Total number of personas
        - contribution_count (int): Total number of contributions made
        - disagreement_count (int): Number of active disagreements
        - active_persona_id (str): ID of the currently active persona
        - next_persona_id (str): ID of the next persona to contribute
        - next_contribution_needed (bool): Whether another contribution is needed
        - error (str): Error message if any, otherwise empty string
        - status (str): Status of the response ("success" or "failed")
    """
    return {
        "session_id": "sess_abc123xyz",
        "topic": "Climate change mitigation strategies",
        "stage": "integration",
        "iteration": 3,
        "persona_count": 4,
        "contribution_count": 7,
        "disagreement_count": 2,
        "active_persona_id": "scientist",
        "next_persona_id": "economist",
        "next_contribution_needed": True,
        "error": "",
        "status": "success"
    }

def collaborative_reasoning_server_collaborativeReasoning(
    activePersonaId: str,
    personas: List[Dict[str, Any]],
    sessionId: str,
    topic: str,
    stage: str,
    iteration: int,
    nextContributionNeeded: bool,
    contributions: List[Dict[str, Any]],
    consensusPoints: Optional[List[str]] = None,
    disagreements: Optional[List[str]] = None,
    finalRecommendation: Optional[str] = None,
    keyInsights: Optional[List[str]] = None,
    nextPersonaId: Optional[str] = None,
    openQuestions: Optional[List[str]] = None,
    suggestedContributionTypes: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Simulates structured collaborative reasoning among multiple expert personas.

    This function models a multi-perspective problem-solving process where diverse
    personas contribute insights, debate disagreements, and work toward consensus
    on complex topics.

    Args:
        activePersonaId (str): ID of the currently active persona
        personas (List[Dict[str, Any]]): List of expert personas with their attributes
        sessionId (str): Unique identifier for this collaboration session
        topic (str): The topic or problem being addressed
        stage (str): Current stage of the collaborative process (e.g., ideation, integration, decision)
        iteration (int): Current iteration of the collaboration
        nextContributionNeeded (bool): Whether another contribution is needed
        contributions (List[Dict[str, Any]]): Contributions from the personas
        consensusPoints (Optional[List[str]]): Points of consensus among participants
        disagreements (Optional[List[str]]): Points of disagreement between personas
        finalRecommendation (Optional[str]): Final recommendation based on the collaboration
        keyInsights (Optional[List[str]]): Key insights from the collaboration
        nextPersonaId (Optional[str]): ID of the persona that should contribute next
        openQuestions (Optional[List[str]]): Open questions requiring further exploration
        suggestedContributionTypes (Optional[List[str]]): Suggested types for the next contribution

    Returns:
        Dict[str, Any]: A dictionary containing the state of the collaborative reasoning process
        with the following keys:
            - sessionId (str): unique identifier for the collaboration session
            - topic (str): the topic or problem being addressed
            - stage (str): current stage of the collaborative process
            - iteration (int): current iteration number
            - personaCount (int): total number of personas
            - contributionCount (int): total number of contributions made so far
            - disagreementCount (int): number of active disagreements
            - activePersonaId (str): ID of the currently active persona
            - nextPersonaId (str): ID of the persona scheduled to contribute next
            - nextContributionNeeded (bool): indicates whether further contributions are required
            - error (str): error message if the tool execution failed
            - status (str): status of the tool response ("failed" if an error occurred)

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not sessionId:
        return {
            "sessionId": "",
            "topic": "",
            "stage": "",
            "iteration": 0,
            "personaCount": 0,
            "contributionCount": 0,
            "disagreementCount": 0,
            "activePersonaId": "",
            "nextPersonaId": "",
            "nextContributionNeeded": False,
            "error": "sessionId is required",
            "status": "failed"
        }
    
    if not topic:
        return {
            "sessionId": sessionId,
            "topic": "",
            "stage": "",
            "iteration": 0,
            "personaCount": 0,
            "contributionCount": 0,
            "disagreementCount": 0,
            "activePersonaId": "",
            "nextPersonaId": "",
            "nextContributionNeeded": False,
            "error": "topic is required",
            "status": "failed"
        }
    
    if not personas:
        return {
            "sessionId": sessionId,
            "topic": topic,
            "stage": stage,
            "iteration": iteration,
            "personaCount": 0,
            "contributionCount": len(contributions) if contributions else 0,
            "disagreementCount": len(disagreements) if disagreements else 0,
            "activePersonaId": activePersonaId,
            "nextPersonaId": nextPersonaId or "",
            "nextContributionNeeded": nextContributionNeeded,
            "error": "at least one persona is required",
            "status": "failed"
        }
    
    if not contributions:
        return {
            "sessionId": sessionId,
            "topic": topic,
            "stage": stage,
            "iteration": iteration,
            "personaCount": len(personas),
            "contributionCount": 0,
            "disagreementCount": len(disagreements) if disagreements else 0,
            "activePersonaId": activePersonaId,
            "nextPersonaId": nextPersonaId or "",
            "nextContributionNeeded": True,
            "error": "at least one contribution is required",
            "status": "failed"
        }

    try:
        # Get data from simulated external API
        api_data = call_external_api("collaborative-reasoning-server-collaborativeReasoning")
        
        # Construct result using both computed values and API data
        result = {
            "sessionId": sessionId,
            "topic": topic,
            "stage": stage,
            "iteration": iteration,
            "personaCount": len(personas),
            "contributionCount": len(contributions),
            "disagreementCount": len(disagreements) if disagreements else 0,
            "activePersonaId": activePersonaId,
            "nextPersonaId": nextPersonaId or api_data["next_persona_id"],
            "nextContributionNeeded": nextContributionNeeded,
            "error": "",
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        return {
            "sessionId": sessionId,
            "topic": topic,
            "stage": stage,
            "iteration": iteration,
            "personaCount": len(personas),
            "contributionCount": len(contributions) if contributions else 0,
            "disagreementCount": len(disagreements) if disagreements else 0,
            "activePersonaId": activePersonaId,
            "nextPersonaId": nextPersonaId or "",
            "nextContributionNeeded": nextContributionNeeded,
            "error": f"Internal error during collaborative reasoning: {str(e)}",
            "status": "failed"
        }