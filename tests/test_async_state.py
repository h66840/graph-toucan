
import unittest
import asyncio
import sys
import os

# Paths setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
tool_info_dir = os.path.join(project_root, "graph-toucan", "tool_info")
sys.path.append(tool_info_dir)

from state_manager import sys_state

# We define a helper async function that simulates a session
async def session_task(name: str, file_path: str, content: str, delay: float):
    # 1. Initialize context for this task
    sys_state.init_session()
    
    # 2. Write file
    print(f"[{name}] Writing {content} to {file_path}")
    sys_state.write_file(file_path, content)
    
    # 3. Sleep to let other tasks run (simulating network io)
    await asyncio.sleep(delay)
    
    # 4. Read file back and verify integrity
    read_content = sys_state.read_file(file_path)
    print(f"[{name}] Read back: {read_content}")
    
    # 5. Verify NO leakage: check if the other task's file exists?
    # To test isolation strictly: Task A should NOT see Task B's files.
    # We'll return (my_content, full_file_list)
    return read_content, sys_state.list_files()

class TestAsyncStateIsolation(unittest.TestCase):
    
    def test_concurrent_sessions(self):
        async def run_test():
            # Task A: Writes "DataA" to "fileA"
            # Task B: Writes "DataB" to "fileB"
            # If isolated, Task A's file list should ONLY contain "fileA"
            
            task_a = asyncio.create_task(session_task("SessionA", "fileA", "DataA", 0.1))
            task_b = asyncio.create_task(session_task("SessionB", "fileB", "DataB", 0.1))
            
            res_a, files_a = await task_a
            res_b, files_b = await task_b
            
            # Assertions
            self.assertEqual(res_a, "DataA")
            self.assertEqual(res_b, "DataB")
            
            # Isolation Check: A should only see fileA
            self.assertIn("fileA", files_a)
            self.assertNotIn("fileB", files_a, "Session A leaked into Session B!")
            
            # Isolation Check: B should only see fileB
            self.assertIn("fileB", files_b)
            self.assertNotIn("fileA", files_b, "Session B leaked into Session A!")
            
            print("\nSUCCESS: Sessions are perfectly isolated!")

        # Run the async test structure
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
