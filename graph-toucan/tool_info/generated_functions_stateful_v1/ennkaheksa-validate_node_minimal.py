from typing import Dict, List, Any

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



def ennkaheksa_validate_node_minimal(config: Dict[str, Any], nodeType: str) -> Dict[str, Any]:
    """
    Quick validation that ONLY checks for missing required fields.
    
    Args:
        config (Dict[str, Any]): The node configuration to check
        nodeType (str): The node type to validate (e.g., "nodes-base.slack")
    
    Returns:
        Dict[str, Any]: Validation result containing:
            - nodeType (str): type identifier of the node being validated
            - displayName (str): human-readable name of the node type
            - valid (bool): True if no required fields are missing
            - missingRequiredFields (List[str]): list of required field names that are missing
    """
    # Define required fields per nodeType (minimal schema)
    required_fields_map = {
        "nodes-base.httpRequest": ["method", "url"],
        "nodes-base.slack": ["channel", "message"],
        "nodes-base.email": ["to", "subject", "body"],
        "nodes-base.timer": ["interval"],
        "nodes-base.function": ["functionCode"],
    }
    
    # Default to empty list if nodeType not found
    required_fields = required_fields_map.get(nodeType, [])
    
    # Find missing required fields
    missing_required_fields = [field for field in required_fields if field not in config]
    
    # Determine validity
    is_valid = len(missing_required_fields) == 0
    
    # Generate display name from nodeType (convert from kebab-case or dot notation)
    display_name = nodeType.split('.')[-1].replace('-', ' ').title() if nodeType else "Unknown"
    
    return {
        "nodeType": nodeType,
        "displayName": display_name,
        "valid": is_valid,
        "missingRequiredFields": missing_required_fields
    }