
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

def weather_server_ping() -> dict:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.
    
    Returns:
        dict: A dictionary containing the server's response to the ping request,
              indicating its operational status.
        - response (str): The server's response message indicating operational status.
    """
    def _original_call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - response (str): Server response message indicating status ('OK' or similar).
        """
        return {
            "response": "OK"
        }

    try:
        # Validate tool name input for safety even though no external input is used
        if not isinstance("weather-server-ping", str):
            raise ValueError("Tool name must be a string.")

        # Fetch simulated external data
        api_data = call_external_api("weather-server-ping", **locals())

        # Construct result according to output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except Exception as e:
        # Handle any unexpected errors during execution
        return {
            "response": f"Error: {str(e)}"
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
