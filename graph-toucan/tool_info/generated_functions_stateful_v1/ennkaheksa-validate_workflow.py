from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def ennkaheksa_validate_workflow(options: Optional[Dict[str, Any]] = None, workflow: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Validate an entire n8n workflow before deployment.
    
    Performs comprehensive validation of workflow structure, node connections (including ai_tool connections),
    expressions, best practices, and AI Agent configurations. Checks for valid $fromAI() expressions and
    AI tool integrations. Returns a detailed report with errors, warnings, and improvement suggestions.
    
    Args:
        options (Optional[Dict[str, Any]]): Optional validation settings to customize behavior
        workflow (Optional[Dict[str, Any]]): The complete workflow JSON to validate. Must include 'nodes' array and 'connections' object.
    
    Returns:
        Dict[str, Any]: Validation report with the following structure:
            - valid (bool): Whether the workflow passed all critical validations
            - summary (Dict): High-level metrics about the workflow
            - errors (List[Dict]): List of validation errors with node and message details
            - warnings (List[Dict]): List of validation warnings with detailed messages
            - suggestions (List[str]): General best practice recommendations
    """
    # Initialize result
    result: Dict[str, Any] = {
        "valid": True,
        "summary": {
            "totalNodes": 0,
            "enabledNodes": 0,
            "triggerNodes": 0,
            "validConnections": 0,
            "invalidConnections": 0,
            "expressionsValidated": 0,
            "errorCount": 0,
            "warningCount": 0
        },
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    # Input validation
    if workflow is None:
        result["valid"] = False
        result["errors"].append({
            "node": "workflow",
            "message": {
                "type": "missing_field",
                "property": "workflow",
                "message": "Workflow is required",
                "fix": "Provide a valid workflow object with nodes and connections"
            }
        })
        result["summary"]["errorCount"] = 1
        return result
    
    if "nodes" not in workflow:
        result["valid"] = False
        result["errors"].append({
            "node": "workflow",
            "message": {
                "type": "missing_field",
                "property": "nodes",
                "message": "Workflow must contain a nodes array",
                "fix": "Add a 'nodes' array to the workflow"
            }
        })
        result["summary"]["errorCount"] = 1
        return result
    
    if "connections" not in workflow:
        result["valid"] = False
        result["errors"].append({
            "node": "workflow",
            "message": {
                "type": "missing_field",
                "property": "connections",
                "message": "Workflow must contain a connections object",
                "fix": "Add a 'connections' object to the workflow"
            }
        })
        result["summary"]["errorCount"] = 1
        return result
    
    nodes = workflow["nodes"]
    connections = workflow["connections"]
    
    # Initialize summary counters
    total_nodes = len(nodes)
    enabled_nodes = 0
    trigger_nodes = 0
    valid_connections = 0
    invalid_connections = 0
    expressions_validated = 0
    
    # Validate each node
    for node in nodes:
        node_name = node.get("name", "unknown")
        
        # Check if node has name
        if not node_name or node_name == "unknown":
            result["valid"] = False
            result["errors"].append({
                "node": node_name,
                "message": {
                    "type": "invalid_configuration",
                    "property": "name",
                    "message": "Node must have a valid name",
                    "fix": "Assign a descriptive name to the node"
                }
            })
        
        # Count enabled nodes
        if node.get("disabled") is not True:
            enabled_nodes += 1
        
        # Identify trigger nodes
        node_type = node.get("type", "")
        if "trigger" in node_type.lower():
            trigger_nodes += 1
        
        # Validate node parameters and expressions
        parameters = node.get("parameters", {})
        for param_key, param_value in parameters.items():
            # Check for expression patterns like $fromAI()
            if isinstance(param_value, str):
                if "$fromAI()" in param_value:
                    expressions_validated += 1
                    # Validate AI expression syntax
                    if not param_value.strip().startswith("$fromAI()"):
                        result["warnings"].append({
                            "node": node_name,
                            "message": {
                                "type": "expression_warning",
                                "property": f"parameters.{param_key}",
                                "message": f"Unconventional use of $fromAI() expression",
                                "suggestion": "Use $fromAI() at the beginning of expressions for clarity"
                            }
                        })
                elif "{{$" in param_value or "{{" in param_value:
                    expressions_validated += 1
    
    # Validate connections
    for source_node, connection_map in connections.items():
        if not isinstance(connection_map, dict):
            continue
            
        for output_index, destinations in connection_map.items():
            if not isinstance(destinations, list):
                continue
                
            for dest_pair in destinations:
                if not isinstance(dest_pair, list) or len(dest_pair) != 2:
                    invalid_connections += 1
                    result["valid"] = False
                    result["errors"].append({
                        "node": source_node,
                        "message": {
                            "type": "connection_error",
                            "property": "connections",
                            "message": f"Invalid connection format from {source_node}",
                            "fix": "Ensure connections are in [destination_node, input_index] format"
                        }
                    })
                else:
                    valid_connections += 1
    
    # Update summary
    result["summary"]["totalNodes"] = total_nodes
    result["summary"]["enabledNodes"] = enabled_nodes
    result["summary"]["triggerNodes"] = trigger_nodes
    result["summary"]["validConnections"] = valid_connections
    result["summary"]["invalidConnections"] = invalid_connections
    result["summary"]["expressionsValidated"] = expressions_validated
    result["summary"]["errorCount"] = len(result["errors"])
    result["summary"]["warningCount"] = len(result["warnings"])
    
    # Determine overall validity
    if len(result["errors"]) > 0:
        result["valid"] = False
    
    # Add suggestions based on findings
    if trigger_nodes == 0:
        result["suggestions"].append("Add a trigger node to start the workflow automatically")
    
    if trigger_nodes > 1:
        result["suggestions"].append("Consider using only one trigger node for clearer workflow execution flow")
    
    if total_nodes > 10 and valid_connections < total_nodes:
        result["suggestions"].append("Break down large workflows into smaller, reusable sub-workflows")
    
    if expressions_validated == 0:
        result["suggestions"].append("Use expressions like $fromAI() to make your workflow dynamic and data-driven")
    
    if enabled_nodes < total_nodes * 0.5:
        result["suggestions"].append("Review disabled nodes - consider removing unused nodes to simplify the workflow")
    
    return result