from typing import Dict, List, Any, Optional
import re
import json

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


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for workflow expression validation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - valid (bool): Whether all expressions are valid
        - errors_0_nodeId (str): Node ID of first error
        - errors_0_property (str): Property path of first error
        - errors_0_expression (str): Expression string of first error
        - errors_0_errorType (str): Type of first error
        - errors_0_message (str): Error message of first error
        - errors_0_location (str): Location info of first error
        - errors_1_nodeId (str): Node ID of second error
        - errors_1_property (str): Property path of second error
        - errors_1_expression (str): Expression string of second error
        - errors_1_errorType (str): Type of second error
        - errors_1_message (str): Error message of second error
        - errors_1_location (str): Location info of second error
        - warnings_0_nodeId (str): Node ID of first warning
        - warnings_0_property (str): Property path of first warning
        - warnings_0_message (str): Warning message of first warning
        - warnings_0_suggestion (str): Suggestion for first warning
        - warnings_1_nodeId (str): Node ID of second warning
        - warnings_1_property (str): Property path of second warning
        - warnings_1_message (str): Warning message of second warning
        - warnings_1_suggestion (str): Suggestion for second warning
        - summary_totalNodesChecked (int): Total nodes checked
        - summary_expressionsParsed (int): Total expressions parsed
        - summary_errorsCount (int): Total number of errors
        - summary_warningsCount (int): Total number of warnings
        - summary_failedNodeIds_0 (str): First failed node ID
        - summary_failedNodeIds_1 (str): Second failed node ID
    """
    return {
        "valid": False,
        "errors_0_nodeId": "node_123",
        "errors_0_property": "parameters.body",
        "errors_0_expression": "{{ $json.invalidPath }}",
        "errors_0_errorType": "VARIABLE_REFERENCE",
        "errors_0_message": "Referenced variable '$json.invalidPath' does not exist in context",
        "errors_0_location": "line 1, column 5",
        "errors_1_nodeId": "node_456",
        "errors_1_property": "parameters.options",
        "errors_1_expression": "{{ $node('NonExistent').json }}",
        "errors_1_errorType": "NODE_REFERENCE",
        "errors_1_message": "Referenced node 'NonExistent' does not exist in workflow",
        "errors_1_location": "line 3, column 12",
        "warnings_0_nodeId": "node_789",
        "warnings_0_property": "parameters.legacy",
        "warnings_0_message": "Deprecated syntax used: $execution",
        "warnings_0_suggestion": "Use $run instead of $execution",
        "warnings_1_nodeId": "node_123",
        "warnings_1_property": "parameters.body",
        "warnings_1_message": "Unreachable context variable detected",
        "warnings_1_suggestion": "Ensure previous nodes output required data",
        "summary_totalNodesChecked": 5,
        "summary_expressionsParsed": 8,
        "summary_errorsCount": 2,
        "summary_warningsCount": 2,
        "summary_failedNodeIds_0": "node_123",
        "summary_failedNodeIds_1": "node_456"
    }

def ennkaheksa_validate_workflow_expressions(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all n8n expressions in a workflow. Checks expression syntax ({{ }}), variable references 
    ($json, $node, $input), node references exist, and context availability. Returns specific errors 
    with locations. Use this to catch expression errors before runtime.
    
    Args:
        workflow (Dict[str, Any]): The workflow JSON to check for expression errors. Must contain 
                                 'nodes' array with node definitions and their parameters.
    
    Returns:
        Dict containing:
        - valid (bool): Whether all expressions in the workflow are valid
        - errors (List[Dict]): List of detailed error objects with nodeId, property, expression, 
                              errorType, message, and location
        - warnings (List[Dict]): List of non-critical issues with nodeId, property, message, and suggestion
        - summary (Dict): Aggregated validation statistics including totalNodesChecked, 
                        expressionsParsed, errorsCount, warningsCount, and failedNodeIds
    """
    if not workflow or "nodes" not in workflow:
        return {
            "valid": False,
            "errors": [{
                "nodeId": None,
                "property": "workflow",
                "expression": None,
                "errorType": "WORKFLOW_STRUCTURE",
                "message": "Invalid workflow structure: missing 'nodes' array",
                "location": None
            }],
            "warnings": [],
            "summary": {
                "totalNodesChecked": 0,
                "expressionsParsed": 0,
                "errorsCount": 1,
                "warningsCount": 0,
                "failedNodeIds": []
            }
        }

    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    expressions_parsed = 0
    failed_node_ids = set()

    # Extract node names for reference checking
    available_node_names = {node.get("name"): node.get("id") for node in workflow["nodes"] if "name" in node}

    # Regex to find n8n expressions {{ ... }}
    expression_pattern = re.compile(r'\{\{\s*(.*?)\s*\}\}')

    # Traverse all nodes and their parameters
    for node in workflow["nodes"]:
        node_id = node.get("id")
        node_name = node.get("name", "Unknown")
        
        # Recursively search for expressions in parameters
        def traverse_parameters(obj: Any, path: str = ""):
            nonlocal expressions_parsed
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key == "parameters":
                        # Skip parameters object itself but continue into its children
                        traverse_parameters(value, current_path)
                    elif isinstance(value, (dict, list)):
                        traverse_parameters(value, current_path)
                    else:
                        # Check if value is a string containing expression
                        if isinstance(value, str):
                            matches = expression_pattern.findall(value)
                            for match in matches:
                                expressions_parsed += 1
                                expr = "{{ " + match + " }}"
                                
                                # Check for deprecated syntax
                                if "$execution" in match:
                                    warnings.append({
                                        "nodeId": node_id,
                                        "property": current_path,
                                        "message": "Deprecated syntax used: $execution",
                                        "suggestion": "Use $run instead of $execution"
                                    })
                                
                                # Check variable references
                                if "$json" in match and not re.search(r'\$json\.[\w]+', match):
                                    errors.append({
                                        "nodeId": node_id,
                                        "property": current_path,
                                        "expression": expr,
                                        "errorType": "VARIABLE_REFERENCE",
                                        "message": "Invalid $json reference - must specify property path",
                                        "location": None
                                    })
                                    failed_node_ids.add(node_id)
                                
                                # Check node references
                                node_ref_match = re.search(r'\$node\(([^)]+)\)', match)
                                if node_ref_match:
                                    referenced_node = node_ref_match.group(1).strip("'\"")
                                    if referenced_node not in available_node_names:
                                        errors.append({
                                            "nodeId": node_id,
                                            "property": current_path,
                                            "expression": expr,
                                            "errorType": "NODE_REFERENCE",
                                            "message": f"Referenced node '{referenced_node}' does not exist in workflow",
                                            "location": None
                                        })
                                        failed_node_ids.add(node_id)
                                
                                # Check context availability (basic heuristics)
                                if "$input" in match and "input" not in str(obj):
                                    warnings.append({
                                        "nodeId": node_id,
                                        "property": current_path,
                                        "message": "Unreachable context variable detected: $input",
                                        "suggestion": "Ensure previous nodes output required data"
                                    })
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    traverse_parameters(item, current_path)

        # Start traversal from node parameters
        if "parameters" in node:
            traverse_parameters(node["parameters"])

    # Build summary
    summary = {
        "totalNodesChecked": len(workflow["nodes"]),
        "expressionsParsed": expressions_parsed,
        "errorsCount": len(errors),
        "warningsCount": len(warnings),
        "failedNodeIds": list(failed_node_ids)
    }

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "summary": summary
    }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
