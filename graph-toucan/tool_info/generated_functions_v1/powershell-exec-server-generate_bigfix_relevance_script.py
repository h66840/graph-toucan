from typing import Dict, List, Any, Optional
import time
import re
import os

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BigFix relevance script generation.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - script_content (str): Generated PowerShell script content
        - script_path (str): Path where script was saved
        - success (bool): Whether generation succeeded
        - message (str): Status or error message
        - execution_time_ms (int): Time taken in milliseconds
        - logs_0 (str): First log entry
        - logs_1 (str): Second log entry
        - timeout_used (int): Applied timeout value in seconds
    """
    return {
        "script_content": "# Generated BigFix Relevance Script\n# Description: Check system status\nWrite-Output \"TRUE - System requires update\"",
        "script_path": "/scripts/bigfix_relevance.ps1",
        "success": True,
        "message": "Script generated successfully",
        "execution_time_ms": 45,
        "logs_0": "Validated input parameters",
        "logs_1": "Completed script template rendering",
        "timeout_used": 60
    }

def powershell_exec_server_generate_bigfix_relevance_script(
    description: str,
    relevance_logic: str,
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Generate a BigFix relevance script to determine if computers need action.
    
    Creates a PowerShell relevance script that follows IBM BigFix best practices:
    - Proper output format (TRUE/FALSE for BigFix consumption)
    - BigFix client log integration for monitoring
    - Event log integration for troubleshooting
    - Comprehensive error handling and logging
    - Fast execution optimized for frequent evaluations
    
    Args:
        description: Clear description of what the script should check
        relevance_logic: PowerShell code that determines relevance using Complete-Relevance
        output_path: Optional file path where the script will be saved
        timeout: Command timeout in seconds (1-300, default 60)
        
    Returns:
        Dictionary containing:
        - script_content: The full PowerShell script content (if no output_path)
        - script_path: File path where script was saved (if output_path provided)
        - success: Whether generation completed successfully
        - message: Human-readable status or error message
        - execution_time_ms: Time taken to generate in milliseconds
        - logs: List of log entries during creation
        - timeout_used: The timeout value applied (user input or default)
    """
    start_time = time.time()
    logs = []
    
    # Validate inputs
    if not description or not isinstance(description, str):
        return {
            "script_content": "",
            "script_path": "",
            "success": False,
            "message": "Description is required and must be a non-empty string",
            "execution_time_ms": 0,
            "logs": ["Failed input validation: invalid description"],
            "timeout_used": timeout or 60
        }
    
    if not relevance_logic or not isinstance(relevance_logic, str):
        return {
            "script_content": "",
            "script_path": "",
            "success": False,
            "message": "Relevance logic is required and must be a non-empty string",
            "execution_time_ms": 0,
            "logs": ["Failed input validation: invalid relevance_logic"],
            "timeout_used": timeout or 60
        }
    
    # Validate timeout
    if timeout is None:
        timeout = 60
    elif not isinstance(timeout, int) or timeout < 1 or timeout > 300:
        return {
            "script_content": "",
            "script_path": "",
            "success": False,
            "message": "Timeout must be an integer between 1 and 300 seconds",
            "execution_time_ms": 0,
            "logs": ["Failed input validation: invalid timeout"],
            "timeout_used": timeout
        }
    
    logs.append("Input validation passed")
    
    # Clean and normalize relevance logic
    cleaned_logic = relevance_logic.strip()
    if cleaned_logic.startswith("'''") and cleaned_logic.endswith("'''"):
        cleaned_logic = cleaned_logic[3:-3].strip()
    elif cleaned_logic.startswith('"""') and cleaned_logic.endswith('"""'):
        cleaned_logic = cleaned_logic[3:-3].strip()
    
    # Generate the full script content
    script_content = f'''# IBM BigFix Relevance Script
# Description: {description}
# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
# Timeout: {timeout} seconds
# Purpose: Returns TRUE if action is needed, FALSE if compliant

# Function to output proper BigFix relevance format
function Complete-Relevance {{
    param(
        [bool]$Relevant,
        [string]$Message = ""
    )
    
    # Write to BigFix client log for monitoring
    if (Test-Path "C:\\Program Files\\BigFix Agent\\BESClient\\__BESData\\__Global\\Logs") {{
        $logPath = "C:\\Program Files\\BigFix Agent\\BESClient\\__BESData\\__Global\\Logs\\relevance.log"
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Add-Content -Path $logPath -Value "[$timestamp] RELEVANCE: $Relevant - $Message"
    }}
    
    # Write to Windows Event Log for troubleshooting
    $eventMessage = "BigFix Relevance Check: $Relevant - $Message"
    Write-EventLog -LogName Application -Source "BigFix Client" -EventID 1000 -EntryType Information -Message $eventMessage -ErrorAction SilentlyContinue
    
    # Output final result (TRUE/FALSE) for BigFix consumption
    if ($Relevant) {{
        Write-Output "TRUE - $Message"
    }} else {{
        Write-Output "FALSE - $Message"
    }}
    
    exit 0
}}

# Main relevance logic
try {{
{chr(10).join("    " + line if line.strip() else line for line in cleaned_logic.split(chr(10)))}
}} catch {{
    $errorMessage = "Error in relevance check: $($_.Exception.Message)"
    Write-BigFixLog -Message $errorMessage -Severity "Error"
    Complete-Relevance -Relevant $true -Message "Error encountered: $($_.Exception.Message)"
}}
'''

    logs.append("Script template rendered successfully")
    
    # Save to file if output_path provided
    script_path = ""
    if output_path:
        try:
            # Safe path validation - ensure path is absolute or relative and within allowed directories
            path = os.path.abspath(output_path)

            # Prevent directory traversal attacks by ensuring the path is within reasonable boundaries
            # This is a basic check - in production, you might want to restrict to specific directories
            if ".." in str(output_path):
                return {
                    "script_content": "",
                    "script_path": "",
                    "success": False,
                    "message": f"Invalid path: {output_path} contains directory traversal",
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                    "logs": logs + [f"Path validation failed: {output_path}"],
                    "timeout_used": timeout
                }

            # Create parent directories if they don't exist
            parent_dir = os.path.dirname(path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

            # Write the file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            script_path = path
            logs.append(f"Script saved to {output_path}")
        except Exception as e:
            return {
                "script_content": "",
                "script_path": "",
                "success": False,
                "message": f"Failed to save script to {output_path}: {str(e)}",
                "execution_time_ms": int((time.time() - start_time) * 1000),
                "logs": logs + [f"Failed to write file: {str(e)}"],
                "timeout_used": timeout
            }
    
    execution_time_ms = int((time.time() - start_time) * 1000)
    logs.append("Script generation completed")
    
    # Get data from "external" API (simulated)
    api_data = call_external_api("powershell-exec-server-generate_bigfix_relevance_script")
    
    # Construct final result matching output schema
    result = {
        "script_content": script_content if not output_path else api_data["script_content"],
        "script_path": script_path if output_path else api_data["script_path"],
        "success": api_data["success"],
        "message": api_data["message"],
        "execution_time_ms": execution_time_ms,
        "logs": [
            api_data["logs_0"],
            api_data["logs_1"]
        ],
        "timeout_used": api_data["timeout_used"]
    }
    
    return result