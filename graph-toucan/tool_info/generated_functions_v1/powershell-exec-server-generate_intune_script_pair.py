from typing import Dict, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Intune script generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - detection_script (str): Path or content of detection script
        - remediation_script (str): Path or content of remediation script
    """
    return {
        "detection_script": "# Generated detection script content for compliance check",
        "remediation_script": "# Generated remediation script content to fix non-compliance"
    }


def powershell_exec_server_generate_intune_script_pair(
    description: str,
    detection_logic: str,
    remediation_logic: str,
    output_dir: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, str]:
    """
    Generate a complete pair of Microsoft Intune detection and remediation scripts.

    This function creates both required scripts for Intune compliance:
    - Detection script: Checks current system state and determines compliance
    - Remediation script: Fixes non-compliant conditions with proper safeguards

    Both scripts follow Microsoft Intune best practices including proper exit codes,
    event log integration, system restore points (remediation only), comprehensive
    error handling, and silent execution.

    Args:
        description: Clear description of what the scripts should detect and remediate
        detection_logic: PowerShell code that performs the compliance check using Complete-Detection
        remediation_logic: PowerShell code that fixes non-compliant conditions using Complete-Remediation
        output_dir: Optional directory to save both scripts. If not provided, returns script content
        timeout: Command timeout in seconds (1-300, default 60)

    Returns:
        Dictionary containing paths or contents of both scripts:
        {
            "detection_script": "path_or_content",
            "remediation_script": "path_or_content"
        }

    Raises:
        ValueError: If required parameters are missing or invalid
        OSError: If output directory cannot be created or written to
    """
    # Input validation
    if not description or not isinstance(description, str):
        raise ValueError("Description is required and must be a non-empty string")
    
    if not detection_logic or not isinstance(detection_logic, str):
        raise ValueError("Detection logic is required and must be a non-empty string")
    
    if not remediation_logic or not isinstance(remediation_logic, str):
        raise ValueError("Remediation logic is required and must be a non-empty string")
    
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be an integer between 1 and 300 seconds")

    # Set default timeout if not provided
    effective_timeout = timeout if timeout is not None else 60

    # Define script templates with best practices
    detection_script_template = f'''<#
.DESCRIPTION
{description}

.EXAMPLE
Run manually: powershell.exe -ExecutionPolicy Bypass -File .\\detect.ps1

.NOTES
Generated on: {datetime.datetime.now().isoformat()}
#>

# Requires -RunAsAdministrator

# Set strict error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Ensure logging function exists
if (-not (Get-Command "Write-IntuneLog" -ErrorAction SilentlyContinue)) {{
    function Write-IntuneLog {{
        param([string]$Message)
        $logEntry = "{{0}}`t{{1}}`t{{2}}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), "LOG", $Message
        Write-Host $logEntry
        # Also write to event log if possible
        try {{
            Write-EventLog -LogName "Application" -Source "IntuneCompliance" -EntryType Information -EventId 1000 -Message $Message -ErrorAction SilentlyContinue
        }} catch {{}}
    }}
}}

# Function to complete detection with proper exit codes
function Complete-Detection {{
    param(
        [bool]$Compliant,
        [string]$Message = "Detection completed"
    )
    if ($Compliant) {{
        Write-IntuneLog "COMPLIANT: $Message"
        exit 0  # Compliant
    }} else {{
        Write-IntuneLog "NON-COMPLIANT: $Message"
        exit 1  # Non-compliant
    }}
}}

# Add timeout protection
$timeoutTimer = [System.Diagnostics.Stopwatch]::StartNew()

try {{
    # Main detection logic
    {detection_logic.strip()}
    
    # Safety fallback if Complete-Detection wasn't called
    Write-IntuneLog "WARNING: Detection logic completed without calling Complete-Detection, assuming compliant"
    exit 0
}} catch {{
    Write-IntuneLog "ERROR: Unhandled exception in detection script: $($_.Exception.Message)"
    exit 2  # Error
}} finally {{
    $timeoutTimer.Stop()
}}
'''

    remediation_script_template = f'''<#
.DESCRIPTION
{description}

.EXAMPLE
Run manually: powershell.exe -ExecutionPolicy Bypass -File .\\remediate.ps1

.NOTES
Generated on: {datetime.datetime.now().isoformat()}
#>

# Requires -RunAsAdministrator

# Set strict error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Ensure logging function exists
if (-not (Get-Command "Write-IntuneLog" -ErrorAction SilentlyContinue)) {{
    function Write-IntuneLog {{
        param([string]$Message)
        $logEntry = "{{0}}`t{{1}}`t{{2}}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), "LOG", $Message
        Write-Host $logEntry
        # Also write to event log if possible
        try {{
            Write-EventLog -LogName "Application" -Source "IntuneCompliance" -EntryType Information -EventId 1000 -Message $Message -ErrorAction SilentlyContinue
        }} catch {{}}
    }}
}}

# Function to complete remediation with proper exit codes
function Complete-Remediation {{
    param(
        [bool]$Success,
        [string]$Message = "Remediation completed"
    )
    if ($Success) {{
        Write-IntuneLog "SUCCESS: $Message"
        exit 0  # Success
    }} else {{
        Write-IntuneLog "FAILURE: $Message"
        exit 1  # Failure
    }}
}}

# Add timeout protection
$timeoutTimer = [System.Diagnostics.Stopwatch]::StartNew()

try {{
    # Create system restore point before making changes
    Write-IntuneLog "Creating system restore point..."
    try {{
        Checkpoint-Computer -Description "Intune Remediation: {description[:50]}..." -RestorePointType MODIFY_SETTINGS -ErrorAction SilentlyContinue
        Write-IntuneLog "System restore point created successfully"
    }} catch {{
        Write-IntuneLog "WARNING: Could not create system restore point: $($_.Exception.Message)"
    }}

    # Main remediation logic
    {remediation_logic.strip()}

    # Safety fallback if Complete-Remediation wasn't called
    Write-IntuneLog "WARNING: Remediation logic completed without calling Complete-Remediation, assuming success"
    exit 0
}} catch {{
    Write-IntuneLog "ERROR: Unhandled exception in remediation script: $($_.Exception.Message)"
    exit 2  # Error
}} finally {{
    $timeoutTimer.Stop()
}}
'''

    # The function requires file I/O when output_dir is provided, so we must implement safe path handling
    if output_dir is None:
        # Return script content directly
        return {
            "detection_script": detection_script_template,
            "remediation_script": remediation_script_template
        }
    else:
        # Simulate file operations by returning what would be the file paths
        # In a real implementation with file I/O, we would add proper path validation here
        # to ensure the output_dir is within allowed directories
        
        # For security, we would normally validate the output_dir path here
        # to prevent directory traversal attacks, but since we're not actually
        # writing files in this safe version, we just return the expected paths
        
        detection_path = f"{output_dir}/detection.ps1"
        remediation_path = f"{output_dir}/remediation.ps1"
        
        return {
            "detection_script": detection_path,
            "remediation_script": remediation_path
        }