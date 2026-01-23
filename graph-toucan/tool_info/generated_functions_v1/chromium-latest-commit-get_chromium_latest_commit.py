from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Chromium latest commit.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - commit_hash (str): Full SHA-1 hash of the commit
        - author (str): Author name and email in "Name <email>" format
        - committer (str): Committer name and email in "Name <email>" format
        - commit_time (str): Human-readable timestamp of the commit
        - commit_message (str): Full commit message including metadata
        - modified_files_0 (str): First modified file with action prefix
        - modified_files_1 (str): Second modified file with action prefix
        - diff_details (str): Raw unified diff showing code changes
    """
    return {
        "commit_hash": "a1b2c3d4e5f678901234567890abcdef12345678",
        "author": "John Doe <johndoe@example.com>",
        "committer": "Jane Smith <janesmith@example.com>",
        "commit_time": "Fri Apr 05 13:40:25 2024",
        "commit_message": "Fix null pointer dereference in sync service\n\nThis fixes a crash when processing empty sync data.\n\nBug: chromium:123456\nChange-Id: I123456789abcdef123456789abcdef123456789ab\nReviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1234567\nCr-Commit-Position: refs/heads/main@{#123456}",
        "modified_files_0": "[MODIFIED] components/sync/service/data_type_manager.cc",
        "modified_files_1": "[MODIFIED] components/sync/test/fake_data_type_manager.cc",
        "diff_details": "@@ -45,6 +45,9 @@ class DataTypeManager {\n public:\n   void ProcessData();\n+  bool HasValidData() const;\n+\n private:\n   std::unique_ptr<Data> data_;\n+  bool is_initialized_ = false;\n };\n \n@@ -100,6 +103,11 @@ void DataTypeManager::ProcessData() {\n   if (!data_) return;\n+  if (!is_initialized_) {\n+    LOG(ERROR) << \"DataTypeManager not initialized\";\n+    return;\n+  }\n+\n   // Process the data\n   data_->Process();\n }"
    }

def chromium_latest_commit_get_chromium_latest_commit(file_path: str) -> str:
    """
    MCP handler to get the latest commit information for a specified file in Chromium repository.

    Args:
        file_path (str): Relative path of the file in Chromium repository (e.g., "components/sync/service/data_type_manager.cc")

    Returns:
        str: Formatted commit information including hash, author, message, modified files list, and diff details

    Output fields:
        - commit_hash (str): the full SHA-1 hash of the commit
        - author (str): name and email of the commit author in "Name <email>" format
        - committer (str): name and email of the committer in "Name <email>" format
        - commit_time (str): timestamp of the commit in human-readable format
        - commit_message (str): full commit message including description, bug references, Change-Id, review metadata, and Cr-Commit-Position
        - modified_files (List[str]): list of file paths modified in this commit, each prefixed with action like "[MODIFIED]"
        - diff_details (str): raw unified diff (patch) showing code changes per file

    Raises:
        ValueError: If file_path is empty or not a string
    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError("file_path must be a non-empty string")

    # Call external API to get data (simulated)
    api_data = call_external_api("chromium-latest-commit-get_chromium_latest_commit")

    # Construct output structure from flat API data
    commit_hash = api_data["commit_hash"]
    author = api_data["author"]
    committer = api_data["committer"]
    commit_time = api_data["commit_time"]
    commit_message = api_data["commit_message"]
    diff_details = api_data["diff_details"]

    # Reconstruct list of modified files from indexed fields
    modified_files = [
        api_data["modified_files_0"],
        api_data["modified_files_1"]
    ]

    # Format the final output string
    formatted_output = f"""Commit Hash: {commit_hash}
Author: {author}
Committer: {committer}
Commit Time: {commit_time}

Commit Message:
{commit_message}

Modified Files:
"""
    for file in modified_files:
        formatted_output += f"{file}\n"

    formatted_output += f"\nDiff Details:\n{diff_details}"

    return formatted_output