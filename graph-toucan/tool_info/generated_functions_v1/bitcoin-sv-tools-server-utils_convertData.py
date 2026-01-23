from typing import Dict, Any
import base64
import binascii

def bitcoin_sv_tools_server_utils_convertData(args: Dict[str, str]) -> Dict[str, str]:
    """
    Converts data between different encodings (utf8, hex, base64, binary).
    
    Parameters:
        args (dict): A dictionary containing the following keys:
            - data (str): The string to convert
            - from (str): Source encoding format (utf8, hex, base64, or binary)
            - to (str): Target encoding format (utf8, hex, base64, or binary)
    
    Returns:
        Dict[str, str]: A dictionary with the key 'converted_data' containing the resulting converted data as a string.
    
    Raises:
        ValueError: If required parameters are missing or if an invalid encoding format is specified.
    """
    # Extract parameters
    if 'data' not in args:
        raise ValueError("Missing required parameter: data")
    if 'from' not in args:
        raise ValueError("Missing required parameter: from")
    if 'to' not in args:
        raise ValueError("Missing required parameter: to")
    
    data = args['data']
    source_format = args['from'].lower()
    target_format = args['to'].lower()
    
    # Validate formats
    valid_formats = ['utf8', 'hex', 'base64', 'binary']
    if source_format not in valid_formats:
        raise ValueError(f"Invalid source format: {source_format}. Must be one of {valid_formats}")
    if target_format not in valid_formats:
        raise ValueError(f"Invalid target format: {target_format}. Must be one of {valid_formats}")
    
    # Convert from source format to bytes
    try:
        if source_format == 'utf8':
            byte_data = data.encode('utf-8')
        elif source_format == 'hex':
            byte_data = bytes.fromhex(data)
        elif source_format == 'base64':
            byte_data = base64.b64decode(data)
        elif source_format == 'binary':
            # Binary input is expected to be a string of comma-separated integers (byte values)
            byte_values = [int(b.strip()) for b in data.split(',')]
            byte_data = bytes(byte_values)
    except Exception as e:
        raise ValueError(f"Failed to decode data from {source_format}: {str(e)}")
    
    # Convert bytes to target format
    try:
        if target_format == 'utf8':
            result = byte_data.decode('utf-8')
        elif target_format == 'hex':
            result = byte_data.hex()
        elif target_format == 'base64':
            result = base64.b64encode(byte_data).decode('ascii')
        elif target_format == 'binary':
            # Represent as comma-separated byte values
            result = ','.join(str(b) for b in byte_data)
    except Exception as e:
        raise ValueError(f"Failed to encode data to {target_format}: {str(e)}")
    
    return {"converted_data": result}