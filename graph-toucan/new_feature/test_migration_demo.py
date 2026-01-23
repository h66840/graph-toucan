
import sys
import os

# 1. Setup Paths
# We need to import from the NEW generated folder
base_dir = "/Users/plastic/Documents/code/biyesheji/graph-toucan/tool_info"
stateful_dir = os.path.join(base_dir, "generated_functions_stateful_v1")

# Add parent dir (for state_manager) and stateful dir (for the tool) to sys.path
sys.path.append(base_dir)
sys.path.append(stateful_dir)

from state_manager import sys_state

# Dynamic import of the migrated tool
# (We could essentially just import it if the file name is known)
try:
    from importlib import import_module
    # Note: Python module names might have dashes repalced by underscores or similar if they are packages
    # But here they are standalone files. Import by filename.
    # The file is: text-editor-mcp-server-text_editor.py -> module name: text-editor-mcp-server-text_editor
    # Python generally disallows dashes in module names for normal imports.
    # However, use importlib machinery to load it directly.
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "text_editor_module", 
        os.path.join(stateful_dir, "text-editor-mcp-server-text_editor.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["text_editor_module"] = module
    spec.loader.exec_module(module)
    text_editor_fn = module.text_editor_mcp_server_text_editor
    
    print("Successfully imported migrated tool.")

except Exception as e:
    print(f"Import Failed: {e}")
    sys.exit(1)


def run_demo():
    print("=== Starting Stateful Migration Test ===\n")
    
    # 2. Initialize Session (Context Isolation)
    sys_state.init_session()
    print(f"[System] Session Initialized.")

    # 3. Test WRITE (Action)
    print("\n--- Step 1: Writing File 'demo.txt' ---")
    write_result = text_editor_fn(
        command="create",
        path="/home/user/demo.txt",
        file_text="Hello from the Stateful World!",
        description="Creating a test file"
    )
    print(f"Write Result: {write_result}")
    
    # 4. Test READ (Verification)
    # If migration worked, 'content' should come from our write, NOT the hardcoded mock.
    print("\n--- Step 2: Reading File 'demo.txt' ---")
    read_result = text_editor_fn(
        command="view",
        path="/home/user/demo.txt",
        description="Reading the file back"
    )
    print(f"Read Result: {read_result}")
    
    # Validation logic
    actual_content = read_result.get("content", "")
    expected = "Hello from the Stateful World!"
    
    if actual_content == expected:
        print("\n✅ SUCCESS: Content matches! The tool is reading from the Virtual State.")
    else:
        print("\n❌ FAILURE: Content mismatch.")
        print(f"Expected: {expected}")
        print(f"Got:      {actual_content}")
        print("(This likely means the tool returned the hardcoded mock instead of injected state.)")

    # 5. Test ISOLATION (Sanity Check)
    # Check if file exists in the underlying system state
    # (Should return the content directly)
    raw_content = sys_state.read_file("/home/user/demo.txt")
    print(f"\n[Debug] Direct SysState Access: {raw_content}")

if __name__ == "__main__":
    run_demo()
