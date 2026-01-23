
from typing import Dict, Any, Optional, List
from contextvars import ContextVar
import copy

# Container for the actual state data
class StateData:
    def __init__(self):
        # 1. File & OS Domain (for DevTools, OS, FileMgmt)
        self.fs: Dict[str, str] = {
            "/home/user/welcome.txt": "Welcome to your virtual assistant workspace!",
            "/etc/os-release": "NAME=\"VirtualOS\"\nVERSION=\"1.0.0\""
        }
        self.env: Dict[str, str] = {
            "USER": "user",
            "HOME": "/home/user"
        }
        
        # 2. Social & Communication Domain
        self.social_graph: Dict[str, Any] = {
            "user_profile": {"id": "u1", "name": "User", "followers": 100},
            "posts": [],
            "messages": []
        }
        
        # 3. Gaming Domain
        self.game_state: Dict[str, Any] = {
            "inventory": ["starter_sword", "health_potion"],
            "achievements": [],
            "stats": {"level": 1, "xp": 0}
        }
        
        # 4. Long-term Memory Domain
        self.memory_store: Dict[str, Any] = {
            "core_memories": ["User prefers Python over Java"],
            "recall_buffer": {}
        }
        
        # 5. Generic Fallback
        self.kv: Dict[str, Any] = {}

# ContextVar to hold the StateData for the current async context
# The default is None, which triggers the fallback to a global default instance
_context_state: ContextVar[Optional[StateData]] = ContextVar("virtual_system_state", default=None)

class VirtualSystem:
    _instance = None
    _global_default = StateData() # Fallback for non-async or global usage

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VirtualSystem, cls).__new__(cls)
        return cls._instance

    @property
    def _state(self) -> StateData:
        """
        Retrieve the current context's state. 
        If no session is initialized, return the global default state.
        """
        state = _context_state.get()
        if state is None:
            return self._global_default
        return state

    def init_session(self) -> None:
        """
        Initialize a fresh, isolated state for the current async context.
        MUST be called at the start of each concurrent task/session.
        """
        _context_state.set(StateData())

    def reset_session(self) -> None:
        """Reset the *current context's* state to empty."""
        # Just overwrite with a new one
        _context_state.set(StateData())

    # --- Domain 1: File & OS Operations ---
    def write_file(self, path: str, content: str) -> None:
        self._state.fs[path] = content
        
    def read_file(self, path: str) -> Optional[str]:
        return self._state.fs.get(path, None)
    
    def delete_file(self, path: str) -> bool:
        if path in self._state.fs:
            del self._state.fs[path]
            return True
        return False

    def list_files(self) -> Dict[str, str]:
        return self._state.fs.copy()

    # --- Domain 2: Social Media Operations ---
    def get_user_profile(self) -> Dict[str, Any]:
        return self._state.social_graph["user_profile"]
        
    def post_content(self, content: str) -> None:
        self._state.social_graph["posts"].append(content)
        
    def get_feed(self) -> List[str]:
        return self._state.social_graph["posts"]

    # --- Domain 3: Gaming Operations ---
    def get_inventory(self) -> List[str]:
        return self._state.game_state["inventory"]
        
    def add_item(self, item: str) -> None:
        self._state.game_state["inventory"].append(item)
        
    def get_game_stats(self) -> Dict[str, Any]:
        return self._state.game_state["stats"]

    # --- Domain 4: Memory Operations ---
    def add_memory(self, content: str) -> None:
        self._state.memory_store["core_memories"].append(content)
        
    def search_memories(self, query: str) -> List[str]:
        # Simple keyword match
        return [m for m in self._state.memory_store["core_memories"] if query in m]

    # --- Global Reset (for testing/debug) ---
    def reset_global(self) -> None:
        """Reset the global fallback state."""
        self._global_default = StateData()

# Singleton instance
sys_state = VirtualSystem()
