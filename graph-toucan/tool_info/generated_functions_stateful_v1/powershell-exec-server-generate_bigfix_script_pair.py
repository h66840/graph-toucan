from typing import Dict, Any, Optional
import textwrap

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



def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BigFix script generation.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - relevance_script_content (str): Generated relevance script content
        - action_script_content (str): Generated action script content
        - relevance_script_path (str): Path where relevance script is saved
        - action_script_path (str): Path where action script is saved
        - script_pair_generated (bool): Whether script pair was successfully generated
    """
    return {
        "relevance_script_content": "# BigFix Relevance Script\n// Description: Manage application state\nif { existence of file \"C:\\\\Program Files\\\\MyApp\\\\app.exe\" } then false else true",
        "action_script_content": "# BigFix Action Script\n// Description: Install MyApp\ndelete __createfile\ncreatefile until end[comment]\nREM Download and install MyApp\n[comment]\nwaithidden powershell.exe -Command \"Start-Process msiexec -ArgumentList '/i', 'https://example.com/myapp.msi', '/quiet' -Wait\"",
        "relevance_script_path": "/output/relevance_script.bes",
        "action_script_path": "/output/action_script.bes",
        "script_pair_generated": True,
    }


def powershell_exec_server_generate_bigfix_script_pair(
    description: str,
    relevance_logic: str,
    action_logic: str,
    output_dir: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, str]:
    """
    Generate a complete pair of BigFix relevance and action scripts for deployment.

    This function creates both required scripts for IBM BigFix:
    - Relevance script: Determines which computers need the action (TRUE/FALSE output)
    - Action script: Performs the necessary changes with proper error handling

    Both scripts follow IBM BigFix best practices including proper output formats,
    exit codes, logging, system restore points, and silent execution.

    Args:
        description: Clear description of what the scripts should accomplish
        relevance_logic: PowerShell code that determines if action is needed
        action_logic: PowerShell code that performs the remediation
        output_dir: Optional directory to save both scripts. If not provided, returns content
        timeout: Command timeout in seconds (1-300, default 60)

    Returns:
        Dictionary containing both scripts: {"relevance_script": "content/path", "action_script": "content/path"}

    Raises:
        ValueError: If required parameters are missing or invalid
        OSError: If output directory cannot be created or written to
    """
    # Input validation
    if not description or not isinstance(description, str):
        raise ValueError("Description is required and must be a non-empty string")
    
    if not relevance_logic or not isinstance(relevance_logic, str):
        raise ValueError("Relevance logic is required and must be a non-empty string")
    
    if not action_logic or not isinstance(action_logic, str):
        raise ValueError("Action logic is required and must be a non-empty string")
    
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be an integer between 1 and 300 seconds")
    else:
        timeout = 60

    # Clean and normalize the logic strings
    relevance_logic = textwrap.dedent(relevance_logic).strip()
    action_logic = textwrap.dedent(action_logic).strip()

    # Generate relevance script
    relevance_script_lines = [
        f"// BigFix Relevance Script",
        f"// Description: {description}",
        f"// Generated on: {{now}}",
        f"// Timeout: {timeout} seconds",
        f"",
        f"// Relevance Logic",
        f"powershell script {{",
        f"{relevance_logic}",
        f"}}"
    ]
    
    relevance_script = "\n".join(relevance_script_lines)

    # Generate action script
    action_script_lines = [
        f"// BigFix Action Script",
        f"// Description: {description}",
        f"// Generated on: {{now}}",
        f"// Timeout: {timeout} seconds",
        f"",
        f"// Action Logic",
        f"delete __createfile",
        f"createfile until end[comment]",
        f"REM Execute PowerShell action script",
        f"[comment]",
        f"waithidden powershell.exe -Command \"",
        f"try {{",
        f"    // Set execution policy for this session",
        f"    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force",
        f"",
        f"    // Add BigFix-specific functions if not present",
        f"    function Write-BigFixLog {{ param($Message) Write-Host \"[BIGFIX] $Message\" }}",
        f"    function Complete-Action {{ param($Result, $Message) Write-Host \"ACTION RESULT: $Result\"; Write-Host \"ACTION MESSAGE: $Message\"; exit }}",
        f"    function Complete-Relevance {{ param($Relevant, $Message) if ($Relevant) {{ exit 0 }} else {{ exit 1 }} }}",
        f"",
        f"    // Set timeout for this script",
        f"    $timeout = {timeout}",
        f"    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()",
        f"",
        f"    // Main action logic with timeout monitoring",
        f"{action_logic.replace(chr(13), '').replace('\"', '`\"')}",
        f"}}",
        f"catch {{",
        f"    $msg = \"Unhandled exception: $($_.Exception.Message)\"",
        f"    Write-BigFixLog $msg",
        f"    Complete-Action -Result \"NonRetryableFailure\" -Message $msg",
        f"}}",
        f"\"",
        f"// End of action script"
    ]
    
    action_script = "\n".join(action_script_lines)

    # Handle output directory
    if output_dir:
        # Simulate directory creation without actually creating it
        # In a real implementation, we would validate the path is safe first
        if not isinstance(output_dir, str) or len(output_dir.strip()) == 0:
            raise ValueError("Output directory path is invalid")
            
        # Generate safe filenames from description
        safe_desc = "".join(c for c in description if c.isalnum() or c in " _-").rstrip()
        safe_desc = safe_desc.replace(" ", "_")
        
        relevance_path = f"{output_dir}/{safe_desc}_relevance.bes"
        action_path = f"{output_dir}/{safe_desc}_action.bes"
        
        # Instead of writing files, we return the simulated paths
        # In a real implementation with file I/O, we would add path validation
        # to ensure the output_dir is within allowed directories
        return {
            "relevance_script": relevance_path,
            "action_script": action_path
        }
    else:
        # Return script contents
        return {
            "relevance_script": relevance_script,
            "action_script": action_script
        }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
