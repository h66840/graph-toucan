from typing import Dict, List, Any, Optional

def decision_framework_server_decisionFramework(
    analysisType: str,
    constraints: List[str],
    decisionId: str,
    decisionStatement: str,
    riskTolerance: str,
    stage: str,
    iteration: int,
    nextStageNeeded: bool,
    options: List[str],
    criteria: Optional[List[str]] = None,
    criteriaEvaluations: Optional[List[Dict[str, Any]]] = None,
    expectedValues: Optional[Dict[str, float]] = None,
    informationGaps: Optional[List[Dict[str, str]]] = None,
    multiCriteriaScores: Optional[Dict[str, float]] = None,
    possibleOutcomes: Optional[List[Dict[str, Any]]] = None,
    recommendation: Optional[str] = None,
    sensitivityInsights: Optional[List[str]] = None,
    suggestedNextStage: Optional[str] = None,
    timeHorizon: str = "short-term"
) -> Dict[str, Any]:
    """
    Performs structured decision analysis using a computational framework.
    
    This function evaluates decision options based on provided criteria, constraints,
    risk tolerance, and other parameters to produce a comprehensive decision report
    including expected values, multi-criteria scores, and recommendations.
    
    Args:
        analysisType: Type of decision analysis (e.g., "multi-criteria", "expected-utility")
        constraints: List of constraints affecting the decision
        decisionId: Unique identifier for the decision
        decisionStatement: Clear statement of the decision to be made
        riskTolerance: Risk tolerance level ("low", "medium", "high")
        stage: Current stage of the decision process (e.g., "evaluation", "recommendation")
        iteration: Current iteration number of the analysis
        nextStageNeeded: Whether another stage is required
        options: Available options or alternatives
        criteria: Evaluation criteria (optional)
        criteriaEvaluations: Evaluations of options against criteria (optional)
        expectedValues: Expected utility values for each option (optional)
        informationGaps: Gaps in information affecting the decision (optional)
        multiCriteriaScores: Multi-criteria evaluation scores for each option (optional)
        possibleOutcomes: Possible outcomes and their probabilities (optional)
        recommendation: Final recommendation (optional)
        sensitivityInsights: Insights from sensitivity analysis (optional)
        suggestedNextStage: Suggested next stage if further analysis is needed (optional)
        timeHorizon: Time frame for the decision ("short-term", "medium-term", "long-term")
    
    Returns:
        A dictionary containing the decision analysis results with the following structure:
        - decisionId: unique identifier for the decision
        - decisionStatement: clear statement of the decision to be made
        - analysisType: type of decision analysis performed
        - stage: current stage of the decision process
        - iteration: current iteration number
        - optionCount: number of options evaluated
        - criteriaCount: number of criteria used
        - outcomesCount: number of possible outcomes considered
        - nextStageNeeded: whether another stage is required
        - suggestedNextStage: suggested next stage if further analysis is needed
        - recommendation: final recommendation based on the analysis
        - expectedValues: mapping of option IDs to expected utility values
        - multiCriteriaScores: mapping of option IDs to multi-criteria scores
        - informationGaps: list of information gaps with description, impact, and researchMethod
        - sensitivityInsights: list of insights from sensitivity analysis
    """
    # Input validation
    if not decisionId:
        raise ValueError("decisionId is required")
    if not decisionStatement:
        raise ValueError("decisionStatement is required")
    if not analysisType:
        raise ValueError("analysisType is required")
    if not stage:
        raise ValueError("stage is required")
    if not options:
        raise ValueError("options are required")
    if riskTolerance not in ["low", "medium", "high"]:
        raise ValueError("riskTolerance must be 'low', 'medium', or 'high'")
    if timeHorizon not in ["short-term", "medium-term", "long-term"]:
        raise ValueError("timeHorizon must be 'short-term', 'medium-term', or 'long-term'")
    
    # Count criteria if provided
    criteria_count = len(criteria) if criteria else 0
    
    # Count possible outcomes if provided
    outcomes_count = len(possibleOutcomes) if possibleOutcomes else 0
    
    # Use provided values or default to empty structures
    info_gaps = informationGaps if informationGaps else []
    sens_insights = sensitivityInsights if sensitivityInsights else []
    
    # Construct result dictionary
    result: Dict[str, Any] = {
        "decisionId": decisionId,
        "decisionStatement": decisionStatement,
        "analysisType": analysisType,
        "stage": stage,
        "iteration": iteration,
        "optionCount": len(options),
        "criteriaCount": criteria_count,
        "outcomesCount": outcomes_count,
        "nextStageNeeded": nextStageNeeded,
        "suggestedNextStage": suggestedNextStage,
        "recommendation": recommendation,
        "expectedValues": expectedValues or {},
        "multiCriteriaScores": multiCriteriaScores or {},
        "informationGaps": info_gaps,
        "sensitivityInsights": sens_insights
    }
    
    return result