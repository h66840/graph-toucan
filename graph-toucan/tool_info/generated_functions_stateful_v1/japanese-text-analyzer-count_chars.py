from typing import Dict, Any
import re
import time

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
    Simulates fetching data from external API for Japanese text analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - characterCount (int): Count of meaningful characters (excluding spaces and newlines)
        - filePath (str): Absolute path of the analyzed file
        - analysisMetadata_encoding (str): Detected file encoding
        - analysisMetadata_processingTimeMs (float): Processing time in milliseconds
        - analysisMetadata_kanjiCount (int): Number of kanji characters
        - analysisMetadata_hiraganaCount (int): Number of hiragana characters
        - analysisMetadata_katakanaCount (int): Number of katakana characters
        - analysisMetadata_otherCount (int): Number of other characters (letters, digits, symbols)
        - success (bool): Whether the analysis was successful
        - errorMessage (str): Error message if analysis failed
    """
    return {
        "characterCount": 1247,
        "filePath": "/c/Users/test/Documents/sample.txt",
        "analysisMetadata_encoding": "utf-8",
        "analysisMetadata_processingTimeMs": 45.2,
        "analysisMetadata_kanjiCount": 342,
        "analysisMetadata_hiraganaCount": 512,
        "analysisMetadata_katakanaCount": 89,
        "analysisMetadata_otherCount": 304,
        "success": True,
        "errorMessage": ""
    }

def japanese_text_analyzer_count_chars(filePath: str) -> Dict[str, Any]:
    """
    Analyzes a text file and counts the number of meaningful characters (excluding spaces and newlines).
    Supports both Windows and WSL/Linux absolute paths.
    
    Parameters:
        filePath (str): Absolute path to the file to analyze (Windows format like C:\\Users\\... 
                       or WSL/Linux format like /c/Users/... is recommended)
    
    Returns:
        Dict containing:
        - characterCount (int): Meaningful character count (excluding spaces and newlines)
        - filePath (str): Absolute path of the analyzed file (may contain normalized input path)
        - analysisMetadata (Dict): Auxiliary information about the analysis including:
            - encoding (str): Detected file encoding
            - processingTime (float): Processing time in milliseconds
            - characterBreakdown (Dict): Breakdown of character types including:
                - kanji (int): Number of kanji characters
                - hiragana (int): Number of hiragana characters
                - katakana (int): Number of katakana characters
                - other (int): Number of other characters (letters, digits, symbols)
        - success (bool): Whether the analysis was successful
        - errorMessage (str): Detailed error message if an error occurred (e.g., file not found, no read permission)
    """
    # Validate input
    if not filePath:
        return {
            "characterCount": 0,
            "filePath": "",
            "analysisMetadata": {
                "encoding": "",
                "processingTimeMs": 0,
                "characterBreakdown": {
                    "kanji": 0,
                    "hiragana": 0,
                    "katakana": 0,
                    "other": 0
                }
            },
            "success": False,
            "errorMessage": "File path is required"
        }
    
    try:
        # Normalize path by replacing backslashes and normalizing common patterns
        # This is a safe approach that doesn't require os.path
        normalized_path = filePath.strip()
        if '\\' in normalized_path:
            # Convert Windows path separators to forward slashes
            normalized_path = normalized_path.replace('\\', '/')
            # Handle drive letter format (C:/ -> /c)
            if len(normalized_path) >= 2 and normalized_path[1] == ':' and normalized_path[0].isalpha():
                normalized_path = '/' + normalized_path[0].lower() + normalized_path[2:]
        
        # Use external API to get analysis results instead of direct file operations
        api_data = call_external_api("japanese-text_analyzer_count_chars", **locals())
        
        # Validate API response structure
        if not api_data.get("success", False):
            return {
                "characterCount": 0,
                "filePath": normalized_path,
                "analysisMetadata": {
                    "encoding": "",
                    "processingTimeMs": 0,
                    "characterBreakdown": {
                        "kanji": 0,
                        "hiragana": 0,
                        "katakana": 0,
                        "other": 0
                    }
                },
                "success": False,
                "errorMessage": api_data.get("errorMessage", "Analysis failed")
            }
        
        # Extract data from API response with proper nesting
        result = {
            "characterCount": api_data.get("characterCount", 0),
            "filePath": normalized_path,
            "analysisMetadata": {
                "encoding": api_data.get("analysisMetadata_encoding", ""),
                "processingTimeMs": api_data.get("analysisMetadata_processingTimeMs", 0),
                "characterBreakdown": {
                    "kanji": api_data.get("analysisMetadata_kanjiCount", 0),
                    "hiragana": api_data.get("analysisMetadata_hiraganaCount", 0),
                    "katakana": api_data.get("analysisMetadata_katakanaCount", 0),
                    "other": api_data.get("analysisMetadata_otherCount", 0)
                }
            },
            "success": True,
            "errorMessage": ""
        }
        
        return result
        
    except Exception as e:
        return {
            "characterCount": 0,
            "filePath": filePath,
            "analysisMetadata": {
                "encoding": "",
                "processingTimeMs": 0,
                "characterBreakdown": {
                    "kanji": 0,
                    "hiragana": 0,
                    "katakana": 0,
                    "other": 0
                }
            },
            "success": False,
            "errorMessage": f"Unexpected error occurred: {str(e)}"
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
