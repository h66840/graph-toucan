from typing import Dict, Any, Optional
import datetime
import textwrap
import os
import re

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


def powershell_exec_server_generate_bigfix_action_script(
    description: str,
    action_logic: str,
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Generate a BigFix action script to perform remediation or configuration changes.
    
    Creates a PowerShell action script that follows IBM BigFix best practices:
    - Proper exit codes (0=success, 1=retryable failure, 2=non-retryable failure)
    - BigFix client log integration for monitoring
    - System restore point creation before changes
    - Comprehensive error handling and logging
    - Event log integration for troubleshooting
    
    Args:
        description: Clear description of what the script should accomplish
        action_logic: PowerShell code that performs the action using Complete-Action
        output_path: Optional file path where the script will be saved
        timeout: Command timeout in seconds (1-300, default 60)
        
    Returns:
        Dictionary containing:
        - script_content: The full generated PowerShell script content
        - script_path: File path where the script was saved if output_path was provided; otherwise null
        - success: Indicates whether the script generation completed successfully
        - error_message: Error details if script generation failed; otherwise null
        - metadata: Additional information about the generated script
    """
    try:
        # Input validation
        if not description or not isinstance(description, str):
            return {
                "script_content": "",
                "script_path": None,
                "success": False,
                "error_message": "Description is required and must be a non-empty string",
                "metadata": {}
            }
        
        if not action_logic or not isinstance(action_logic, str):
            return {
                "script_content": "",
                "script_path": None,
                "success": False,
                "error_message": "Action logic is required and must be a non-empty string",
                "metadata": {}
            }
        
        # Validate timeout
        if timeout is None:
            timeout = 60
        elif not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            return {
                "script_content": "",
                "script_path": None,
                "success": False,
                "error_message": "Timeout must be an integer between 1 and 300 seconds",
                "metadata": {}
            }
        
        # Generate the PowerShell script content
        script_content = f"""# IBM BigFix Action Script
# Description: {description}
# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Timeout: {timeout} seconds

#Requires -RunAsAdministrator

# Create system restore point before making changes
try {{
    Write-BigFixLog "Creating system restore point..."
    $restorePointDescription = "BigFix Action: {description[:50]}..."
    Checkpoint-Computer -Description $restorePointDescription -RestorePointType MODIFY_SETTINGS -ErrorAction SilentlyContinue
    Write-BigFixLog "System restore point created successfully"
}} catch {{
    Write-BigFixLog "Warning: Could not create system restore point: $($_.Exception.Message)"
}}

# Ensure Write-BigFixLog function is available
if (-not (Get-Command Write-BigFixLog -ErrorAction SilentlyContinue)) {{
    function Write-BigFixLog {{
        param([string]$Message)
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Verbose "[$timestamp] $Message"
        # Also write to Windows Event Log for troubleshooting
        try {{
            Write-EventLog -LogName Application -Source "BigFix Client" -EntryType Information -EventId 1000 -Message $Message -ErrorAction SilentlyContinue
        }} catch {{
            # Fail silently if event log write fails
        }}
    }}
}}

# Ensure Complete-Action function is available
if (-not (Get-Command Complete-Action -ErrorAction SilentlyContinue)) {{
    function Complete-Action {{
        param(
            [Parameter(Mandatory=$true)][string]$Result,
            [string]$Message = ""
        )
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        switch ($Result) {{
            "Success" {{ 
                Write-BigFixLog "Action completed successfully: $Message"
                exit 0
            }}
            "RetryableFailure" {{ 
                Write-BigFixLog "Action failed (retryable): $Message"
                exit 1
            }}
            "NonRetryableFailure" {{ 
                Write-BigFixLog "Action failed (non-retryable): $Message"
                exit 2
            }}
            default {{ 
                Write-BigFixLog "Action completed with unknown result: $Result - $Message"
                exit 2
            }}
        }}
    }}
}}

# Main action logic
Write-BigFixLog "Starting action: {description}"
try {{
{textwrap.indent(action_logic.strip(), '    ')}
}} catch {{
    $errorMessage = "Unhandled exception in action logic: $($_.Exception.Message)"
    Write-BigFixLog $errorMessage
    Complete-Action -Result "RetryableFailure" -Message $errorMessage
}}

# Fallback in case Complete-Action was not called
Write-BigFixLog "Action logic completed without calling Complete-Action, assuming success"
Complete-Action -Result "Success" -Message "Action completed"
"""

        # Save to file if output_path is provided
        script_path = None
        if output_path:
            try:
                # Safe path validation
                # Convert to absolute path and normalize
                safe_path = os.path.abspath(output_path)
                
                # Validate that the path doesn't contain suspicious patterns
                if re.search(r'[<>|;&$`!]', output_path):
                    return {
                        "script_content": "",
                        "script_path": None,
                        "success": False,
                        "error_message": "Invalid characters in file path",
                        "metadata": {}
                    }
                
                # Ensure the file has a .ps1 extension
                if not safe_path.lower().endswith('.ps1'):
                    safe_path += '.ps1'
                
                # Write the file with safe path
                with open(safe_path, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                script_path = safe_path
            except Exception as e:
                return {
                    "script_content": "",
                    "script_path": None,
                    "success": False,
                    "error_message": f"Failed to write script to file: {str(e)}",
                    "metadata": {}
                }

        # Create metadata
        metadata = {
            "description": description,
            "timeout_seconds": timeout,
            "generated_at": datetime.datetime.now().isoformat(),
            "create_restore_point": True,
            "requires_admin": True,
            "bigfix_compatible": True
        }

        return {
            "script_content": script_content,
            "script_path": script_path,
            "success": True,
            "error_message": None,
            "metadata": metadata
        }

    except Exception as e:
        return {
            "script_content": "",
            "script_path": None,
            "success": False,
            "error_message": f"Unexpected error during script generation: {str(e)}",
            "metadata": {}
        }