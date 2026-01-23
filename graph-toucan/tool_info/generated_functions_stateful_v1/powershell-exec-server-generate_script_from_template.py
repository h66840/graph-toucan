from typing import Dict, Any, Optional
from datetime import datetime
import string

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


def powershell_exec_server_generate_script_from_template(
    template_name: str,
    parameters: Dict[str, Any],
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Generate a PowerShell script from a template by replacing placeholders with provided parameters.
    
    Args:
        template_name: Name of the template to use (without .ps1 extension)
        parameters: Dictionary of parameters to replace in the template
        output_path: Where to save the generated script (optional)
        timeout: Command timeout in seconds (1-300, default 60)
        
    Returns:
        Dictionary containing:
        - script_content: The full generated PowerShell script content as a string
        - output_path: Filesystem path where the generated script was saved
        - success: Whether the script generation completed successfully
        - error_message: Description of any error that occurred during template processing
        - parameters_applied: Dictionary of parameter keys that were replaced in the template and their values
        - template_used: Name of the template that was used to generate the script
        - generated_at: Timestamp (ISO 8601 format) when the script was generated
    """
    result = {
        "script_content": "",
        "output_path": output_path,
        "success": False,
        "error_message": None,
        "parameters_applied": {},
        "template_used": template_name,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    
    try:
        # Validate inputs
        if not template_name or not isinstance(template_name, str):
            raise ValueError("template_name must be a non-empty string")
            
        if parameters is None:
            parameters = {}
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a dictionary")
            
        if timeout is None:
            timeout = 60
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("timeout must be an integer between 1 and 300")
        
        # Simulate template content based on template name
        # In a real implementation, this would load from actual template files
        template_content = f"""
# PowerShell Script Generated from Template: {template_name}
# Generated at: {result['generated_at']}

# Configuration Parameters
{chr(10).join([f'$${key} = "{value}"' for key, value in parameters.items()])}

# Main execution logic
try {{
    Write-Host "Executing {template_name} template..."
    # Template-specific logic would go here
    Write-Host "Processing with the following parameters:"
    {chr(10).join([f'Write-Host "  {key}: {value}"' for key, value in parameters.items()])}
    
    # Simulated work
    Start-Sleep -Seconds 1
    
    Write-Host "Template execution completed successfully."
}} catch {{
    Write-Error "An error occurred during script execution: $($_.Exception.Message)"
    exit 1
}}
"""
        
        # Process template by replacing placeholders
        # Using $${param} syntax in template to match our pattern above
        script_content = template_content
        
        # Track which parameters were actually applied
        applied_params = {}
        for key, value in parameters.items():
            # In our simulated template, we already formatted the content with the values
            applied_params[key] = value
        
        result["script_content"] = script_content
        result["parameters_applied"] = applied_params
        result["success"] = True
        
        # If output_path is specified, we'd write to file (simulated here)
        if output_path:
            # In a real implementation: with open(output_path, 'w') as f: f.write(script_content)
            result["output_path"] = output_path
        
    except Exception as e:
        result["error_message"] = str(e)
        result["success"] = False
    
    return result