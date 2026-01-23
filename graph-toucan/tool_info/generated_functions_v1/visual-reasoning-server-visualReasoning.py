from typing import Dict, List, Any, Optional
import time
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for visual reasoning operations.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - diagramId (str): Identifier for the diagram
        - operationStatus (str): Status of the operation ('success', 'failure', 'partial')
        - updatedElements_0_id (str): ID of first updated element
        - updatedElements_0_type (str): Type of first updated element
        - updatedElements_0_label (str): Label of first updated element
        - updatedElements_0_x (float): X position of first updated element
        - updatedElements_0_y (float): Y position of first updated element
        - updatedElements_1_id (str): ID of second updated element
        - updatedElements_1_type (str): Type of second updated element
        - updatedElements_1_label (str): Label of second updated element
        - updatedElements_1_x (float): X position of second updated element
        - updatedElements_1_y (float): Y position of second updated element
        - diagramSnapshot_elements_count (int): Number of elements in diagram
        - diagramSnapshot_connections_count (int): Number of connections
        - diagramSnapshot_bounds_min_x (float): Minimum X coordinate
        - diagramSnapshot_bounds_min_y (float): Minimum Y coordinate
        - diagramSnapshot_bounds_max_x (float): Maximum X coordinate
        - diagramSnapshot_bounds_max_y (float): Maximum Y coordinate
        - insightsGenerated_0 (str): First generated insight
        - insightsGenerated_1 (str): Second generated insight
        - observationsRecorded_0 (str): First recorded observation
        - observationsRecorded_1 (str): Second recorded observation
        - hypothesesProposed_0 (str): First proposed hypothesis
        - hypothesesProposed_1 (str): Second proposed hypothesis
        - nextOperationSuggestion_operation (str): Suggested next operation type
        - nextOperationSuggestion_targetElements_0 (str): First target element ID for next operation
        - nextOperationSuggestion_targetElements_1 (str): Second target element ID for next operation
        - nextOperationSuggestion_reason (str): Reason for suggested operation
        - iterationComplete (int): Iteration number completed
        - hasMoreOperations (bool): Whether more operations are expected
        - visualMetrics_nodeCount (int): Total number of nodes
        - visualMetrics_edgeDensity (float): Edge density metric
        - visualMetrics_hierarchyDepth (int): Depth of hierarchy in diagram
        - visualMetrics_symmetryScore (float): Symmetry measurement (0-1)
        - executionDurationMs (float): Execution time in milliseconds
    """
    # Simulate realistic variation based on operation type
    statuses = ["success", "partial", "success", "success"]  # biased toward success
    operation_status = random.choice(statuses)

    # Generate element IDs if not provided
    elem_id_1 = f"elem_{int(time.time() * 1000) % 100000}"
    elem_id_2 = f"elem_{(int(time.time() * 1000) % 100000) + 1}"

    return {
        "diagramId": "diagram_12345",
        "operationStatus": operation_status,
        "updatedElements_0_id": elem_id_1,
        "updatedElements_0_type": "node",
        "updatedElements_0_label": "Process A",
        "updatedElements_0_x": round(random.uniform(50, 300), 2),
        "updatedElements_0_y": round(random.uniform(50, 300), 2),
        "updatedElements_1_id": elem_id_2,
        "updatedElements_1_type": "decision",
        "updatedElements_1_label": "Decision B",
        "updatedElements_1_x": round(random.uniform(350, 600), 2),
        "updatedElements_1_y": round(random.uniform(50, 300), 2),
        "diagramSnapshot_elements_count": random.randint(2, 10),
        "diagramSnapshot_connections_count": random.randint(1, 8),
        "diagramSnapshot_bounds_min_x": 0.0,
        "diagramSnapshot_bounds_min_y": 0.0,
        "diagramSnapshot_bounds_max_x": round(random.uniform(700, 1000), 2),
        "diagramSnapshot_bounds_max_y": round(random.uniform(500, 800), 2),
        "insightsGenerated_0": "Emergent pattern suggests feedback loop between core components.",
        "insightsGenerated_1": "High node centrality indicates potential bottleneck at Process A.",
        "observationsRecorded_0": "Two main clusters forming with sparse inter-cluster connections.",
        "observationsRecorded_1": "Asymmetric layout may reflect unbalanced data flow.",
        "hypothesesProposed_0": "Optimizing connection weights could improve overall throughput.",
        "hypothesesProposed_1": "Introducing parallel processing at Decision B may reduce latency.",
        "nextOperationSuggestion_operation": random.choice(["transform", "observe", "update"]),
        "nextOperationSuggestion_targetElements_0": elem_id_1,
        "nextOperationSuggestion_targetElements_1": elem_id_2,
        "nextOperationSuggestion_reason": "Further transformation could reveal optimization opportunities in critical path.",
        "iterationComplete": 1,
        "hasMoreOperations": True,
        "visualMetrics_nodeCount": random.randint(5, 20),
        "visualMetrics_edgeDensity": round(random.uniform(0.1, 0.7), 2),
        "visualMetrics_hierarchyDepth": random.randint(2, 5),
        "visualMetrics_symmetryScore": round(random.uniform(0.2, 0.9), 2),
        "executionDurationMs": round(random.uniform(10, 200), 2),
    }


def visual_reasoning_server_visualReasoning(
    diagramId: str,
    diagramType: str,
    operation: str,
    iteration: int,
    nextOperationNeeded: bool,
    elements: Optional[List[Dict[str, Any]]] = None,
    observation: Optional[str] = None,
    insight: Optional[str] = None,
    hypothesis: Optional[str] = None,
    transformationType: Optional[str] = None,
) -> Dict[str, Any]:
    """
    A detailed tool for diagrammatic thinking and spatial representation.
    This function simulates creating and manipulating visual representations of problems
    such as system diagrams, flowcharts, concept maps, and other visual models.

    Args:
        diagramId (str): Identifier for the diagram being manipulated or created
        diagramType (str): The type of diagram (graph, flowchart, state diagram, etc.)
        operation (str): The type of operation to perform (create, update, delete, transform, observe)
        iteration (int): Current iteration of the visual reasoning process
        nextOperationNeeded (bool): Whether another operation is needed in the reasoning process
        elements (Optional[List[Dict[str, Any]]]): The visual elements to operate on
        observation (Optional[str]): Observations about the current visual state
        insight (Optional[str]): Insights derived from the visual representation
        hypothesis (Optional[str]): Hypotheses based on the visual pattern
        transformationType (Optional[str]): For transform operations: the type of transformation

    Returns:
        Dict containing:
        - diagramId (str): Identifier for the diagram
        - operationStatus (str): Status of the operation: 'success', 'failure', or 'partial'
        - updatedElements (List[Dict]): List of updated/created elements with id, type, label, position
        - diagramSnapshot (Dict): Current state of the diagram including elements, relationships, bounds
        - insightsGenerated (List[str]): Derived insights from the visual reasoning step
        - observationsRecorded (List[str]): Observations made during this iteration
        - hypothesesProposed (List[str]): Hypotheses generated based on visual patterns
        - nextOperationSuggestion (Dict): Suggested next operation with operation, targetElements, reason
        - iterationComplete (int): The iteration number this output corresponds to
        - hasMoreOperations (bool): Indicates whether further operations are expected
        - visualMetrics (Dict): Quantitative metrics about the diagram structure
        - executionDurationMs (float): Time taken to execute the operation in milliseconds
    """
    # Input validation
    if not diagramId:
        raise ValueError("diagramId is required")
    if not diagramType:
        raise ValueError("diagramType is required")
    if not operation:
        raise ValueError("operation is required")
    if iteration < 0:
        raise ValueError("iteration must be non-negative")

    # Valid operations
    valid_operations = {"create", "update", "delete", "transform", "observe"}
    if operation not in valid_operations:
        return {
            "diagramId": diagramId,
            "operationStatus": "failure",
            "updatedElements": [],
            "diagramSnapshot": {
                "elements": [],
                "connections": [],
                "bounds": {"minX": 0, "minY": 0, "maxX": 0, "maxY": 0},
                "layout": {},
            },
            "insightsGenerated": [],
            "observationsRecorded": [],
            "hypothesesProposed": [],
            "nextOperationSuggestion": {
                "operation": "",
                "targetElements": [],
                "reason": "Invalid operation type specified"
            },
            "iterationComplete": iteration,
            "hasMoreOperations": False,
            "visualMetrics": {
                "nodeCount": 0,
                "edgeDensity": 0.0,
                "hierarchyDepth": 0,
                "symmetryScore": 0.0
            },
            "executionDurationMs": 0.0,
        }

    # Start timing
    start_time = time.time()

    # Simulate processing delay
    time.sleep(random.uniform(0.01, 0.05))

    # Call external API to simulate visual reasoning step
    api_response = call_external_api("visual_reasoning")

    # Extract data from API response
    operation_status = api_response["operationStatus"]
    elem_id_1 = api_response["updatedElements_0_id"]
    elem_id_2 = api_response["updatedElements_1_id"]

    # Build updated elements list
    updated_elements = [
        {
            "id": elem_id_1,
            "type": api_response["updatedElements_0_type"],
            "label": api_response["updatedElements_0_label"],
            "x": api_response["updatedElements_0_x"],
            "y": api_response["updatedElements_0_y"],
        },
        {
            "id": elem_id_2,
            "type": api_response["updatedElements_1_type"],
            "label": api_response["updatedElements_1_label"],
            "x": api_response["updatedElements_1_x"],
            "y": api_response["updatedElements_1_y"],
        },
    ]

    # Build diagram snapshot
    diagram_snapshot = {
        "elements": updated_elements,
        "connections": [
            {"source": elem_id_1, "target": elem_id_2, "type": "data_flow"}
        ],
        "bounds": {
            "minX": api_response["diagramSnapshot_bounds_min_x"],
            "minY": api_response["diagramSnapshot_bounds_min_y"],
            "maxX": api_response["diagramSnapshot_bounds_max_x"],
            "maxY": api_response["diagramSnapshot_bounds_max_y"],
        },
        "layout": {"type": "hierarchical", "orientation": "left-right"},
    }

    # Build insights, observations, hypotheses
    insights_generated = [
        api_response["insightsGenerated_0"],
        api_response["insightsGenerated_1"],
    ]
    observations_recorded = [
        api_response["observationsRecorded_0"],
        api_response["observationsRecorded_1"],
    ]
    hypotheses_proposed = [
        api_response["hypothesesProposed_0"],
        api_response["hypothesesProposed_1"],
    ]

    # Build next operation suggestion
    next_operation_suggestion = {
        "operation": api_response["nextOperationSuggestion_operation"],
        "targetElements": [
            api_response["nextOperationSuggestion_targetElements_0"],
            api_response["nextOperationSuggestion_targetElements_1"],
        ],
        "reason": api_response["nextOperationSuggestion_reason"],
    }

    # Build visual metrics
    visual_metrics = {
        "nodeCount": api_response["visualMetrics_nodeCount"],
        "edgeDensity": api_response["visualMetrics_edgeDensity"],
        "hierarchyDepth": api_response["visualMetrics_hierarchyDepth"],
        "symmetryScore": api_response["visualMetrics_symmetryScore"],
    }

    # Calculate execution duration
    execution_duration_ms = round((time.time() - start_time) * 1000, 2)

    # Return structured response
    return {
        "diagramId": diagramId,
        "operationStatus": operation_status,
        "updatedElements": updated_elements,
        "diagramSnapshot": diagram_snapshot,
        "insightsGenerated": insights_generated,
        "observationsRecorded": observations_recorded,
        "hypothesesProposed": hypotheses_proposed,
        "nextOperationSuggestion": next_operation_suggestion,
        "iterationComplete": api_response["iterationComplete"],
        "hasMoreOperations": api_response["hasMoreOperations"],
        "visualMetrics": visual_metrics,
        "executionDurationMs": execution_duration_ms,
    }