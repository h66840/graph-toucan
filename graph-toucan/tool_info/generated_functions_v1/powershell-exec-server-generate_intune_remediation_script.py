from typing import Dict, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Intune remediation script generation.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - script_path (str): Path where the generated script was saved
    """
    return {
        "script_path": "C:\\IntuneScripts\\remediate_action.ps1"
    }


def powershell_exec_server_generate_intune_remediation_script(
    description: str,
    remediation_logic: str,
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, str]:
    """
    Generate a Microsoft Intune remediation script with enterprise-grade features.

    Creates a PowerShell remediation script that follows Microsoft Intune best practices:
    - Proper exit codes (0=success, 1=failure, 2=error)
    - Event log integration for monitoring and troubleshooting
    - System restore point creation before making changes
    - Comprehensive error handling and logging
    - No user interaction (required for Intune deployment)

    Args:
        description: Clear description of what the script should remediate
        remediation_logic: PowerShell code that performs the remediation
        output_path: Optional file path where the script will be saved
        timeout: Command timeout in seconds (1-300, default 60)

    Returns:
        Dictionary containing the path where the script was saved

    Raises:
        ValueError: If required parameters are missing or invalid
        RuntimeError: If script generation fails
    """
    # Input validation
    if not description or not isinstance(description, str):
        raise ValueError("Description is required and must be a non-empty string.")
    
    if not remediation_logic or not isinstance(remediation_logic, str):
        raise ValueError("Remediation logic is required and must be a non-empty string.")
    
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be an integer between 1 and 300 seconds.")
    
    # Set default output path if not provided
    if not output_path:
        safe_desc = "".join(x for x in description if x.isalnum() or x in "._- ")
        filename = f"intune_remediate_{safe_desc.strip().replace(' ', '_')}.ps1"
        output_path = f"./{filename}"
    
    # Generate PowerShell script content
    script_content = f'''# Microsoft Intune Remediation Script
# Generated: {datetime.datetime.now().isoformat()}
# Description: {description}
# Timeout: {timeout} seconds

#Requires -RunAsAdministrator

# Define constants
$EventLogSource = "IntuneRemediation"
$EventLogID_Success = 1000
$EventLogID_Failure = 1001
$EventLogID_Error = 1002

# Ensure event source exists
if (-not [System.Diagnostics.EventLog]::SourceExists($EventLogSource)) {{
    New-EventLog -LogName Application -Source $EventLogSource
}}

# Function to write to event log
function Write-IntuneLog {{
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$true)]
        [ValidateSet("Success", "Failure", "Error")]
        [string]$Level
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    switch ($Level) {{
        "Success" {{ Write-EventLog -LogName Application -Source $EventLogSource -EventID $EventLogID_Success -EntryType Information -Message $logMessage }}
        "Failure" {{ Write-EventLog -LogName Application -Source $EventLogSource -EventID $EventLogID_Failure -EntryType Warning -Message $logMessage }}
        "Error"   {{ Write-EventLog -LogName Application -Source $EventLogSource -EventID $EventLogID_Error -EntryType Error -Message $logMessage }}
    }}
    
    # Also write to host for Intune collection
    Write-Host $logMessage
}}

# Function to complete remediation with proper exit code
function Complete-Remediation {{
    param(
        [Parameter(Mandatory=$true)]
        [bool]$Success,
        
        [Parameter(Mandatory=$true)]
        [string]$Message
    )
    
    if ($Success) {{
        Write-IntuneLog -Message $Message -Level "Success"
        exit 0
    }} else {{
        Write-IntuneLog -Message $Message -Level "Failure"
        exit 1
    }}
}}

# Handle script-wide errors
$ErrorActionPreference = "Stop"

try {{
    Write-IntuneLog -Message "Starting remediation: {description}" -Level "Success"
    
    # Create system restore point before making changes
    try {{
        Checkpoint-Computer -Description "Intune Remediation: {description}" -RestorePointType MODIFY_SETTINGS -CompletionNotification
        Write-IntuneLog -Message "System restore point created successfully" -Level "Success"
    }} catch {{
        Write-IntuneLog -Message "Failed to create system restore point: $($_.Exception.Message)" -Level "Error"
        # Continue execution even if restore point fails
    }}
    
    # Set timeout for script execution
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $maxRuntimeMs = {timeout} * 1000
    
    # Execute the remediation logic
    try {{
{remediation_logic.strip().replace('\n', '\n' + ' ' * 8)}
    }} catch {{
        Write-IntuneLog -Message "Remediation failed: $($_.Exception.Message)" -Level "Error"
        exit 1
    }}
    
    # Check if timeout was exceeded
    $timer.Stop()
    if ($timer.ElapsedMilliseconds -gt $maxRuntimeMs) {{
        Write-IntuneLog -Message "Script exceeded timeout limit of {timeout} seconds" -Level "Error"
        exit 2
    }}
    
}} catch {{
    Write-IntuneLog -Message "Script execution error: $($_.Exception.Message)" -Level "Error"
    exit 2
}}

# Fallback exit if no Complete-Remediation was called
Write-IntuneLog -Message "Script completed without explicit completion call" -Level "Success"
exit 0
'''

    # Call external API to simulate service response (with only simple fields)
    api_response = call_external_api("powershell-exec-server-generate_intune_remediation_script")
    
    # Construct result matching output schema
    result = {
        "script_path": output_path
    }
    
    return result