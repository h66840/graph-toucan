from typing import Dict, List, Any
from datetime import datetime

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


def ennkaheksa_validate_workflow_connections(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate only the connections in a workflow.
    
    Checks:
    - All connections point to existing nodes
    - No cycles (infinite loops)
    - No orphaned nodes
    - Proper trigger node setup
    - AI tool connections are valid (correct types between AI Agents and tool nodes)
    
    This function performs structural validation of workflow connections and is faster than full validation.
    
    Args:
        workflow (Dict[str, Any]): The workflow JSON with 'nodes' array and 'connections' object.
    
    Returns:
        Dict[str, Any]: Validation result containing:
            - is_valid (bool): Whether the workflow connections pass all validation checks
            - errors (List[Dict]): List of validation error objects with 'type', 'message', 'details'
            - warnings (List[Dict]): List of non-blocking warnings with 'type', 'message', 'details'
            - validated_at (str): ISO 8601 timestamp of validation
            - summary (Dict): Aggregated stats on connections, orphaned nodes, cycles, etc.
    """
    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    summary = {
        "total_connections": 0,
        "orphaned_nodes_count": 0,
        "cycle_count": 0,
        "invalid_references_count": 0,
        "ai_tool_connection_issues_count": 0
    }

    validated_at = datetime.utcnow().isoformat() + "Z"

    # Input validation
    if not isinstance(workflow, dict):
        return {
            "is_valid": False,
            "errors": [
                {
                    "type": "INVALID_INPUT",
                    "message": "Workflow must be a JSON object",
                    "details": {"received_type": type(workflow).__name__}
                }
            ],
            "warnings": [],
            "validated_at": validated_at,
            "summary": summary
        }

    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})

    if not isinstance(nodes, list):
        return {
            "is_valid": False,
            "errors": [
                {
                    "type": "INVALID_STRUCTURE",
                    "message": "Nodes must be an array",
                    "details": {"nodes_type": type(nodes).__name__}
                }
            ],
            "warnings": [],
            "validated_at": validated_at,
            "summary": summary
        }

    if not isinstance(connections, dict):
        return {
            "is_valid": False,
            "errors": [
                {
                    "type": "INVALID_STRUCTURE",
                    "message": "Connections must be an object",
                    "details": {"connections_type": type(connections).__name__}
                }
            ],
            "warnings": [],
            "validated_at": validated_at,
            "summary": summary
        }

    node_ids = {node.get("id") for node in nodes if isinstance(node, dict) and "id" in node}
    node_types = {node.get("id"): node.get("type") for node in nodes if isinstance(node, dict) and "id" in node}

    # Check for missing IDs
    for node in nodes:
        if not isinstance(node, dict):
            errors.append({
                "type": "INVALID_NODE",
                "message": "Node must be an object",
                "details": {"node": str(node)}
            })
            continue
        if "id" not in node:
            errors.append({
                "type": "MISSING_NODE_ID",
                "message": "Node is missing required 'id' field",
                "details": {"node": node}
            })

    # Validate connections point to existing nodes
    connection_count = 0
    for source_id, targets in connections.items():
        if not isinstance(targets, list):
            errors.append({
                "type": "INVALID_CONNECTION_FORMAT",
                "message": "Connection targets must be an array",
                "details": {"source_id": source_id, "targets_type": type(targets).__name__}
            })
            continue

        if source_id not in node_ids:
            errors.append({
                "type": "INVALID_REFERENCE",
                "message": "Connection source does not exist",
                "details": {"source_id": source_id}
            })
            summary["invalid_references_count"] += 1
            continue

        for target in targets:
            if not isinstance(target, dict):
                errors.append({
                    "type": "INVALID_CONNECTION_TARGET",
                    "message": "Connection target must be an object",
                    "details": {"source_id": source_id, "target": target}
                })
                continue

            target_id = target.get("nodeId")
            if target_id not in node_ids:
                errors.append({
                    "type": "INVALID_REFERENCE",
                    "message": "Connection target does not exist",
                    "details": {"source_id": source_id, "target_id": target_id}
                })
                summary["invalid_references_count"] += 1
            connection_count += 1

    summary["total_connections"] = connection_count

    # Check for orphaned nodes (nodes not connected to any other node)
    connected_node_ids = set()
    for source_id, targets in connections.items():
        if source_id in node_ids:
            connected_node_ids.add(source_id)
        for target in targets:
            if isinstance(target, dict) and target.get("nodeId") in node_ids:
                connected_node_ids.add(target.get("nodeId"))

    orphaned_nodes = node_ids - connected_node_ids
    summary["orphaned_nodes_count"] = len(orphaned_nodes)
    
    if orphaned_nodes:
        warnings.append({
            "type": "ORPHANED_NODES",
            "message": f"Found {len(orphaned_nodes)} nodes with no connections",
            "details": {"orphaned_node_ids": list(orphaned_nodes)}
        })

    # Check for cycles using DFS
    visited = set()
    rec_stack = set()
    cycle_found = False

    def has_cycle(node_id: str) -> bool:
        if node_id not in visited:
            visited.add(node_id)
            rec_stack.add(node_id)

            if node_id in connections:
                for target in connections[node_id]:
                    if isinstance(target, dict):
                        target_id = target.get("nodeId")
                        if target_id in rec_stack:
                            return True
                        if target_id in node_ids and has_cycle(target_id):
                            return True

            rec_stack.remove(node_id)
        return False

    for node_id in node_ids:
        if has_cycle(node_id):
            cycle_found = True
            break

    if cycle_found:
        errors.append({
            "type": "CYCLE_DETECTED",
            "message": "Workflow contains a cycle (infinite loop)",
            "details": {"description": "At least one cycle found in the workflow connections"}
        })
        summary["cycle_count"] = 1  # We don't count all cycles, just detect presence

    # Check trigger node setup
    trigger_nodes = [node for node in nodes if isinstance(node, dict) and node.get("type") == "trigger"]
    if len(trigger_nodes) == 0:
        errors.append({
            "type": "MISSING_TRIGGER",
            "message": "Workflow must have at least one trigger node",
            "details": {"trigger_count": 0}
        })
    else:
        # Trigger nodes should not have incoming connections
        for trigger in trigger_nodes:
            trigger_id = trigger.get("id")
            has_incoming = any(
                target.get("nodeId") == trigger_id
                for src_id, targets in connections.items()
                for target in targets
                if isinstance(target, dict)
            )
            if has_incoming:
                errors.append({
                    "type": "INVALID_TRIGGER_CONNECTION",
                    "message": "Trigger node should not have incoming connections",
                    "details": {"trigger_id": trigger_id}
                })

    # Validate AI tool connections
    ai_agent_nodes = [node for node in nodes if isinstance(node, dict) and node.get("type") == "ai_agent"]
    tool_nodes = [node for node in nodes if isinstance(node, dict) and node.get("type") == "tool"]

    ai_agent_ids = {node.get("id") for node in ai_agent_nodes}
    tool_node_ids = {node.get("id") for node in tool_nodes}

    # AI agents can connect to tool nodes, but not vice versa
    for source_id, targets in connections.items():
        if source_id in tool_node_ids:
            for target in targets:
                if isinstance(target, dict):
                    target_id = target.get("nodeId")
                    if target_id in ai_agent_ids:
                        errors.append({
                            "type": "INVALID_AI_TOOL_CONNECTION",
                            "message": "Tool node cannot connect to AI agent node",
                            "details": {"source_id": source_id, "target_id": target_id}
                        })
                        summary["ai_tool_connection_issues_count"] += 1

    # AI agents should only connect to tool nodes or other valid nodes
    for source_id, targets in connections.items():
        if source_id in ai_agent_ids:
            for target in targets:
                if isinstance(target, dict):
                    target_id = target.get("nodeId")
                    if target_id in node_ids and node_types.get(target_id) not in ["tool", "condition", "output"]:
                        warnings.append({
                            "type": "SUBOPTIMAL_AI_CONNECTION",
                            "message": "AI agent connected to non-tool node",
                            "details": {
                                "source_id": source_id,
                                "target_id": target_id,
                                "target_type": node_types.get(target_id)
                            }
                        })

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "validated_at": validated_at,
        "summary": summary
    }