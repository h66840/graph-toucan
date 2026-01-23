
import json
import os
import re

# =================================================================================
# 1. Domain Access Protocol Definition
# =================================================================================
DOMAIN_PROTOCOLS = {
    # --- Domain 1: File & OS ---
    "File Management": {
        "access_methods": ["read_file", "write_file", "delete_file", "list_files", "print_env"],
        "import_statement": "from state_manager import sys_state"
    },
    "Operating System": {
        "access_methods": ["read_file", "write_file", "delete_file", "list_files", "print_env"],
        "import_statement": "from state_manager import sys_state"
    },
    "Development Tools": {
        "access_methods": ["read_file", "write_file", "delete_file", "list_files"],
        "import_statement": "from state_manager import sys_state"
    },

    # --- Domain 2: Social ---
    "Social Media": {
        "access_methods": ["get_user_profile", "post_content", "get_feed"],
        "import_statement": "from state_manager import sys_state"
    },
    "Communication Tools": {
        "access_methods": ["get_user_profile", "post_content", "get_feed"],
        "import_statement": "from state_manager import sys_state"
    },

    # --- Domain 3: Gaming ---
    "Gaming": {
        "access_methods": ["get_inventory", "add_item", "get_game_stats"],
        "import_statement": "from state_manager import sys_state"
    },

    # --- Domain 4: Memory ---
    "Memory Management": {
        "access_methods": ["add_memory", "search_memories"],
        "import_statement": "from state_manager import sys_state"
    }
}

# Code Template for State Injection
INJECTION_TEMPLATE = """
import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    {import_stmt}
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock
"""

def migrate_tools():
    # 1. Load Distribution
    base_dir = "/Users/plastic/Documents/code/biyesheji/graph-toucan/tool_info"
    dist_path = os.path.join(base_dir, "stateful_tools_distribution.json")
    generated_dir = os.path.join(base_dir, "generated_functions_v1")
    
    # NEW Output Directory
    output_dir = os.path.join(base_dir, "generated_functions_stateful_v1")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    with open(dist_path, 'r') as f:
        tools_list = json.load(f)

    print(f"Loaded {len(tools_list)} tools for migration.")

    migrated_count = 0
    for tool_entry in tools_list:
        tool_name = tool_entry["name"]
        category = tool_entry["category"]
        
        # 2. Check Protocol
        if category not in DOMAIN_PROTOCOLS:
            continue
            
        protocol = DOMAIN_PROTOCOLS[category]
        source_path = os.path.join(generated_dir, f"{tool_name}.py")
        dest_path = os.path.join(output_dir, f"{tool_name}.py")
        
        if not os.path.exists(source_path):
            print(f"Skipping {tool_name}: Source file not found.")
            continue

        # 3. Read Content
        with open(source_path, 'r') as f:
            content = f.read()
            
        # 4. Inject Import
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                insert_idx = i + 1
        
        injection_code = INJECTION_TEMPLATE.format(import_stmt=protocol["import_statement"])
        lines.insert(insert_idx, injection_code)
        
        # 5. Inject Logic Wrapper (Hook Strategy)
        content_str = "\n".join(lines)

        # 4.5. Patch Call Site (CRITICAL FIX) 
        # Robustly inject `**locals()` into call_external_api to pass arguments to wrapper.
        params_pattern = re.compile(r'call_external_api\s*\(\s*(?P<quote>[\'"])(?P<name>[^#\r\n]+?)(?P=quote)\s*\)')
        if params_pattern.search(content_str):
             content_str = params_pattern.sub(r'call_external_api(\g<quote>\g<name>\g<quote>, **locals())', content_str)
        else:
             print(f"  [Warning] Call site regex failed for {tool_name}")

        if "def call_external_api" not in content_str:
            # Skip wrapping if no main entry found
            with open(dest_path, 'w') as f:
                f.write(content_str)
            continue
            
        # RENAME original
        content_str = content_str.replace("def call_external_api", "def _original_call_external_api")
        
        wrapper_code = ""
        wrapper_preamble = """
# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name
"""

        if "File Management" in category or "Development Tools" in category or "Operating System" in category:
             wrapper_code = wrapper_preamble + """
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
"""
        elif "Social Media" in category or "Communication" in category:
            wrapper_code = wrapper_preamble + """
        # POST
        if "post" in tool_name or "send" in tool_name:
            content = kwargs.get("content") or kwargs.get("text") or kwargs.get("message")
            if content:
                sys_state.post_content(content)
                
        # FEED
        if "get" in tool_name or "feed" in tool_name or "timeline" in tool_name:
            posts = sys_state.get_feed()
            if posts:
                 result["content"] = posts
    except Exception:
        pass
    return result
"""
        elif "Gaming" in category:
            wrapper_code = wrapper_preamble + """
        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
"""
        else:
             wrapper_code = wrapper_preamble + """
        pass
    except Exception:
        pass
    return result
"""

        if wrapper_code:
            content_str += "\n" + wrapper_code

        # Write to NEW destination
        with open(dest_path, 'w') as f:
            f.write(content_str)
        
        migrated_count += 1
            
    print(f"Migration Complete. {migrated_count} tools written to {output_dir}")

if __name__ == "__main__":
    migrate_tools()
