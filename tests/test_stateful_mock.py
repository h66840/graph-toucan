
import unittest
import sys
import os
import importlib.util

# Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
tool_info_dir = os.path.join(project_root, "graph-toucan", "tool_info")
poc_dir = os.path.join(tool_info_dir, "poc_stateful_tools")

# Ensure state_manager is importable
if tool_info_dir not in sys.path:
    sys.path.append(tool_info_dir)

from state_manager import sys_state

# Dynamic import of the POC tool
def import_tool_module(file_path):
    spec = importlib.util.spec_from_file_location("poc_text_editor", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

tool_path = os.path.join(poc_dir, "text_editor.py")
text_editor = import_tool_module(tool_path)

class TestStatefulTextEditor(unittest.TestCase):
    
    def setUp(self):
        sys_state.reset()
        
    def test_create_and_view(self):
        print("\nTesting Create and View (POC)...")
        # 1. Create file
        response = text_editor.text_editor_mcp_server_text_editor(
            command="create",
            description="test creation",
            path="/tmp/hello.txt",
            file_text="Hello World"
        )
        self.assertTrue(response['success'])
        
        # 2. View file
        response = text_editor.text_editor_mcp_server_text_editor(
            command="view",
            description="verifying content",
            path="/tmp/hello.txt"
        )
        self.assertTrue(response['success'])
        self.assertEqual(response['content'], "Hello World")
        print("Success: Content persisted in POC!")

    def test_persistence_across_Reset(self):
        print("\nTesting Reset (POC)...")
        # 1. Create
        text_editor.text_editor_mcp_server_text_editor(
            command="create",
            description="test",
            path="/tmp/temp.txt",
            file_text="Ephemeral"
        )
        # 2. Reset
        sys_state.reset()
        
        # 3. View -> Should fail
        response = text_editor.text_editor_mcp_server_text_editor(
            command="view",
            description="check after reset",
            path="/tmp/temp.txt"
        )
        self.assertFalse(response['success'])
        print("Success: State cleared after reset!")

    def test_complex_operations(self):
        print("\nTesting Complex Ops (Insert in POC)...")
        path = "/tmp/code.py"
        init_code = "def main():\n    pass"
        
        # 1. Create
        text_editor.text_editor_mcp_server_text_editor("create", "init", path, file_text=init_code)
        
        # 2. Insert
        text_editor.text_editor_mcp_server_text_editor(
            "insert", "add print", path, 
            insert_line=1, new_str="    print('hi')"
        )
        
        # 3. View
        resp = text_editor.text_editor_mcp_server_text_editor("view", "check", path)
        expected = "def main():\n    print('hi')\n    pass"
        self.assertEqual(resp['content'], expected)
        print("Success: Modifications applied correctly!")

if __name__ == '__main__':
    unittest.main()
