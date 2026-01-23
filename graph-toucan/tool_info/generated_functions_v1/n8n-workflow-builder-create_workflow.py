from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for n8n workflow creation.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_0_type (str): Type of the first node
        - node_0_name (str): Name of the first node
        - node_0_position_x (int): X coordinate of the first node
        - node_0_position_y (int): Y coordinate of the first node
        - node_1_type (str): Type of the second node
        - node_1_name (str): Name of the second node
        - node_1_position_x (int): X coordinate of the second node
        - node_1_position_y (int): Y coordinate of the second node
        - connection_0_node (str): Target node name in the first connection
        - connection_0_type (str): Type of the first connection (e.g., main)
        - connection_0_index (int): Index of the first connection
        - connection_0_sourceNode (str): Source node name in the first connection
        - connection_0_sourceIndex (int): Source index of the first connection
        - connection_1_node (str): Target node name in the second connection
        - connection_1_type (str): Type of the second connection
        - connection_1_index (int): Index of the second connection
        - connection_1_sourceNode (str): Source node name in the second connection
        - connection_1_sourceIndex (int): Source index of the second connection
    """
    return {
        "node_0_type": "n8n-nodes-base.start",
        "node_0_name": "Start",
        "node_0_position_x": 0,
        "node_0_position_y": 0,
        "node_1_type": "n8n-nodes-base.httpRequest",
        "node_1_name": "HTTP Request",
        "node_1_position_x": 300,
        "node_1_position_y": 0,
        "connection_0_node": "HTTP Request",
        "connection_0_type": "main",
        "connection_0_index": 0,
        "connection_0_sourceNode": "Start",
        "connection_0_sourceIndex": 0,
        "connection_1_node": "Debug",
        "connection_1_type": "main",
        "connection_1_index": 0,
        "connection_1_sourceNode": "HTTP Request",
        "connection_1_sourceIndex": 0,
    }

def n8n_workflow_builder_create_workflow(nodes: List[Dict[str, Any]], connections: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Create and configure n8n workflows programmatically.
    
    This function simulates creating an n8n workflow by generating a structured
    representation of nodes and connections based on input parameters.
    
    Args:
        nodes (List[Dict[str, Any]]): Required list of node configurations. Each node should have
            'type', 'name', 'parameters', and 'position' fields.
        connections (Optional[List[Dict[str, Any]]]): Optional list of connection configurations.
            Each connection should specify source and target nodes, type, and indices.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - nodes (List[Dict]): List of node objects with 'type', 'name', 'parameters', and 'position'
            - connections (Dict): Dictionary of connections by type (e.g., 'main'), each containing
              a list of connection details including 'node', 'type', 'index', 'sourceNode', 'sourceIndex'
    
    Raises:
        ValueError: If nodes list is empty or None
    """
    if not nodes:
        raise ValueError("Nodes list is required and cannot be empty")
    
    # Get simulated external API data
    api_data = call_external_api("n8n-workflow-builder-create_workflow")
    
    # Process nodes - use input nodes if provided, otherwise use API-simulated nodes
    processed_nodes = []
    for i, node in enumerate(nodes):
        # Use input node data, fallback to simulated data if needed
        node_type = node.get('type', api_data.get(f'node_{i}_type', f'unknown_node_{i}'))
        node_name = node.get('name', api_data.get(f'node_{i}_name', f'Node_{i}'))
        node_parameters = node.get('parameters', {})
        node_position_x = node.get('position', {}).get('x', api_data.get(f'node_{i}_position_x', i * 200))
        node_position_y = node.get('position', {}).get('y', api_data.get(f'node_{i}_position_y', 0))
        
        processed_nodes.append({
            'type': node_type,
            'name': node_name,
            'parameters': node_parameters,
            'position': {
                'x': node_position_x,
                'y': node_position_y
            }
        })
    
    # Process connections - use input connections if provided, otherwise use simulated ones
    processed_connections = {'main': []}
    
    if connections:
        # Group connections by type from input
        for conn in connections:
            conn_type = conn.get('type', 'main')
            if conn_type not in processed_connections:
                processed_connections[conn_type] = []
            processed_connections[conn_type].append({
                'node': conn.get('node'),
                'type': conn_type,
                'index': conn.get('index', 0),
                'sourceNode': conn.get('sourceNode'),
                'sourceIndex': conn.get('sourceIndex', 0)
            })
    else:
        # Use simulated connections
        for i in range(2):  # Two simulated connections
            conn_key = f'connection_{i}'
            if f'{conn_key}_node' in api_data:
                conn_type = api_data[f'{conn_key}_type']
                if conn_type not in processed_connections:
                    processed_connections[conn_type] = []
                processed_connections[conn_type].append({
                    'node': api_data[f'{conn_key}_node'],
                    'type': conn_type,
                    'index': api_data[f'{conn_key}_index'],
                    'sourceNode': api_data[f'{conn_key}_sourceNode'],
                    'sourceIndex': api_data[f'{conn_key}_sourceIndex']
                })
    
    return {
        'nodes': processed_nodes,
        'connections': processed_connections
    }