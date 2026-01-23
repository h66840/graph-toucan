from typing import Dict, Any, Optional
import math
import base64
import string

def qr_code_server_generate_qrcode(
    content: str,
    errorCorrectionLevel: Optional[str] = "M",
    format: Optional[str] = "image",
    size: Optional[int] = 5
) -> Dict[str, str]:
    """
    Generate QR codes in various formats with customizable error correction levels and sizes.
    
    Args:
        content (str): The text content to encode in the QR code (required)
        errorCorrectionLevel (str, optional): Error correction level: 
            'L' (7%), 'M' (15%), 'Q' (25%), 'H' (30%). Default is 'M'
        format (str, optional): Output format: 'image' for PNG QR code, 'text' for terminal-friendly output. Default is 'image'
        size (int, optional): Size of the QR code (1-10). Default is 5
    
    Returns:
        Dict[str, str]: Dictionary containing:
            - message (str): Confirmation message indicating QR code was generated
            - content (str): The original content that was encoded
    
    Raises:
        ValueError: If required content is empty or parameters are out of valid range
    """
    # Input validation
    if not content:
        raise ValueError("Content is required and cannot be empty")
    
    valid_error_levels = ['L', 'M', 'Q', 'H']
    if errorCorrectionLevel not in valid_error_levels:
        raise ValueError(f"errorCorrectionLevel must be one of {valid_error_levels}")
    
    valid_formats = ['image', 'text']
    if format not in valid_formats:
        raise ValueError(f"format must be one of {valid_formats}")
    
    if not isinstance(size, int) or size < 1 or size > 10:
        raise ValueError("size must be an integer between 1 and 10")
    
    # Simulate QR code generation logic
    # In a real implementation, this would involve actual QR encoding algorithm
    # Here we simulate based on inputs
    
    # Generate a deterministic "pattern" based on content for demonstration
    content_hash = sum(ord(c) for c in content) % 1000
    
    if format == "text":
        # Create a simple ASCII representation of QR code
        # Size determines the dimension (n x n matrix)
        dimension = 21 + (size - 1) * 2  # QR base size 21x21, grows with size
        
        # Simplified: create a checkerboard-like pattern seeded by content
        pattern = []
        for i in range(min(dimension, 7)):  # Limit text output height for readability
            row = ""
            for j in range(min(dimension, 20)):  # Limit width
                # Create pattern based on position and content hash
                if ((i + j + content_hash) % 3 == 0):
                    row += "██"
                else:
                    row += "  "
            pattern.append(row)
        
        qr_representation = "\n".join(pattern)
        
    else:  # format == "image"
        # Simulate PNG generation by creating a base64-encoded placeholder
        # In reality this would use a QR library like qrcode
        pixel_size = 21 * size  # Standard QR code starts at 21x21 modules
        # Create a simple base64-encoded PNG placeholder
        # This is just a minimal valid PNG base64 for demonstration
        png_data = f"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=={content_hash}"
        qr_representation = base64.b64encode(png_data.encode()).decode()
    
    # Generate confirmation message
    error_level_desc = {
        'L': '7% error correction',
        'M': '15% error correction', 
        'Q': '25% error correction',
        'H': '30% error correction'
    }[errorCorrectionLevel]
    
    message = f"QR code generated successfully with {error_level_desc}, size {size}, format {format}"
    
    return {
        "message": message,
        "content": content
    }