from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for multi-agent debate tool.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - agent_0_id (str): First registered agent ID
        - agent_1_id (str): Second registered agent ID
        - total_arguments (int): Total number of arguments made so far
        - last_action (str): Most recent action type ("register", "argue", "rebut", "judge")
        - verdict_text (str or None): Final verdict text; first line must be "pro", "con", or "inconclusive"
        - needs_more_rounds (bool): Whether additional rounds are needed
    """
    return {
        "agent_0_id": "pro",
        "agent_1_id": "con",
        "total_arguments": 5,
        "last_action": "judge",
        "verdict_text": "pro\nThe pro side presented stronger evidence and logical consistency.",
        "needs_more_rounds": False
    }

def multi_agent_debate_multiagentdebate(
    action: str,
    agentId: str,
    round: int,
    needsMoreRounds: bool,
    content: Optional[str] = None,
    targetAgentId: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates a structured multi-persona debate system with registration, argumentation, rebuttals, and judging.
    
    Args:
        action (str): One of "register", "argue", "rebut", "judge"
        agentId (str): ID of the agent performing the action (e.g., "pro", "con", "judge", or custom)
        round (int): Current debate round number (>= 1)
        needsMoreRounds (bool): Whether more rounds are desired after this action
        content (str, optional): Argument text or verdict content
        targetAgentId (str, optional): Agent being rebutted (required only for "rebut" action)
    
    Returns:
        Dict containing:
            - agents (List[str]): List of registered agent IDs
            - totalArguments (int): Total number of arguments (including rebuttals) made so far
            - lastAction (str): Type of most recent action
            - verdict (str or None): Final judgment text (first line: "pro", "con", or "inconclusive")
            - needsMoreRounds (bool): Whether additional rounds are required
    
    Raises:
        ValueError: If invalid action is provided or required fields are missing
    """
    # Validate inputs
    valid_actions = {"register", "argue", "rebut", "judge"}
    if action not in valid_actions:
        raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}")
    
    if round < 1:
        raise ValueError("Round must be >= 1")
    
    if action == "rebut" and not targetAgentId:
        raise ValueError("targetAgentId is required for 'rebut' action")
    
    # Simulate interaction with external system
    api_data = call_external_api("multi-agent-debate-multiagentdebate")
    
    # Construct agents list from flat API response
    agents: List[str] = []
    for i in range(2):  # We expect 2 agents based on API mock
        agent_key = f"agent_{i}_id"
        if agent_key in api_data and api_data[agent_key]:
            agents.append(api_data[agent_key])
    
    # Extract other fields
    totalArguments = api_data["total_arguments"]
    lastAction = api_data["last_action"]
    
    # Process verdict
    verdict: Optional[str] = api_data["verdict_text"]
    if verdict == "null" or verdict is None:
        verdict = None
    
    # Use input needsMoreRounds unless verdict is final and judge has spoken
    final_needs_more_rounds = needsMoreRounds
    if lastAction == "judge" and not needsMoreRounds:
        # Once judge gives verdict and needsMoreRounds is False, debate ends
        final_needs_more_rounds = False
    
    return {
        "agents": agents,
        "totalArguments": totalArguments,
        "lastAction": lastAction,
        "verdict": verdict,
        "needsMoreRounds": final_needs_more_rounds
    }