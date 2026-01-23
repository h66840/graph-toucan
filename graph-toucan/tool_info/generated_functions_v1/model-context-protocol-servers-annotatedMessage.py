from typing import Dict, Any, Optional

def model_context_protocol_servers_annotatedMessage(includeImage: Optional[bool] = False, messageType: str = "") -> Dict[str, Any]:
    """
    Demonstrates how annotations can be used to provide metadata about content.
    
    This function generates an annotated message with structured metadata based on the specified message type.
    It simulates different annotation patterns such as success, error, or debug messages with associated diagnostics.
    
    Args:
        includeImage (Optional[bool]): Whether to include an example image reference in the details.
        messageType (str): Type of message to demonstrate different annotation patterns. 
                          Supported types: 'success', 'error', 'warning', 'debug'.
                          
    Returns:
        Dict[str, Any]: A dictionary containing:
            - message (str): The main content of the annotated message.
            - status (str): The type of message indicating the operational outcome.
            - details (Dict): Optional structured metadata associated with the message.
    """
    # Input validation
    if not messageType:
        raise ValueError("messageType is required and cannot be empty")
        
    supported_types = ['success', 'error', 'warning', 'debug']
    if messageType not in supported_types:
        raise ValueError(f"messageType must be one of {supported_types}")

    # Base message content based on type
    message_templates = {
        'success': "Operation completed successfully",
        'error': "An error occurred during processing",
        'warning': "Operation completed with warnings",
        'debug': "Debug information available"
    }
    
    # Status is same as message type
    status = messageType
    message = message_templates[messageType]
    
    # Generate details based on message type
    details: Dict[str, Any] = {}
    
    if messageType == 'success':
        details = {
            'latency': 125.7,
            'cache_hit_ratio': 0.92,
            'records_processed': 1500
        }
    elif messageType == 'error':
        details = {
            'error_code': 'E500',
            'retry_count': 3,
            'expected_duration': 200.0
        }
    elif messageType == 'warning':
        details = {
            'latency': 850.3,
            'memory_usage_mb': 768,
            'threshold_exceeded': 'response_time'
        }
    elif messageType == 'debug':
        details = {
            'timestamp': '2023-11-15T10:30:00Z',
            'thread_id': 12345,
            'cache_hit_ratio': 0.67,
            'query_count': 8
        }
    
    # Optionally include image reference
    if includeImage:
        details['image_url'] = 'https://example.com/visualizations/debug_flow.png'
        details['image_caption'] = f'System flow diagram for {messageType} message'

    return {
        'message': message,
        'status': status,
        'details': details
    }