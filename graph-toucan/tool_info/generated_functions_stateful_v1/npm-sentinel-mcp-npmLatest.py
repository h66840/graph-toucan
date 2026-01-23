from typing import Dict, List, Any, Optional

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
    Simulates fetching data from external API for NPM package details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_packageInput (str): Original input string for the first package
        - result_0_packageName (str): Canonical name of the first package
        - result_0_versionQueried (str): Version specifier queried for the first package
        - result_0_status (str): Status of the first query
        - result_0_error (str or None): Error message if failed, else None
        - result_0_message (str): Human-readable message for the first result
        - result_0_data_name (str): Name of the first package
        - result_0_data_version (str): Latest version number of the first package
        - result_0_data_description (str): Description of the first package
        - result_0_data_author (str): Author of the first package
        - result_0_data_license (str): License type of the first package
        - result_0_data_homepage (str): Homepage URL of the first package
        - result_0_data_repositoryUrl (str): Repository URL of the first package
        - result_0_data_bugsUrl (str): Bug tracker URL of the first package
        - result_0_data_dependenciesCount (int): Number of runtime dependencies
        - result_0_data_devDependenciesCount (int): Number of dev dependencies
        - result_0_data_peerDependenciesCount (int): Number of peer dependencies
        - result_0_data_types (str or None): Type definition info or None
        - result_0_data_dist_shasum (str): SHA-1 checksum of tarball
        - result_0_data_dist_tarball (str): Download URL of tarball
        - result_0_data_dist_fileCount (int): Number of files in unpacked package
        - result_0_data_dist_integrity (str): Subresource Integrity string
        - result_0_data_dist_unpackedSize (int): Unpacked size in bytes
        - result_0_data_dist_npm_signature (str): PGP signature of publication
        - result_0_data_dist_signatures_0_sig (str): First signature (base64)
        - result_0_data_dist_signatures_0_keyid (str): First signing key ID
        - result_0_data_dist_signatures_1_sig (str): Second signature (base64)
        - result_0_data_dist_signatures_1_keyid (str): Second signing key ID
        - result_1_packageInput (str): Original input string for the second package
        - result_1_packageName (str): Canonical name of the second package
        - result_1_versionQueried (str): Version specifier queried for the second package
        - result_1_status (str): Status of the second query
        - result_1_error (str or None): Error message if failed, else None
        - result_1_message (str): Human-readable message for the second result
        - result_1_data_name (str): Name of the second package
        - result_1_data_version (str): Latest version number of the second package
        - result_1_data_description (str): Description of the second package
        - result_1_data_author (str): Author of the second package
        - result_1_data_license (str): License type of the second package
        - result_1_data_homepage (str): Homepage URL of the second package
        - result_1_data_repositoryUrl (str): Repository URL of the second package
        - result_1_data_bugsUrl (str): Bug tracker URL of the second package
        - result_1_data_dependenciesCount (int): Number of runtime dependencies
        - result_1_data_devDependenciesCount (int): Number of dev dependencies
        - result_1_data_peerDependenciesCount (int): Number of peer dependencies
        - result_1_data_types (str or None): Type definition info or None
        - result_1_data_dist_shasum (str): SHA-1 checksum of tarball
        - result_1_data_dist_tarball (str): Download URL of tarball
        - result_1_data_dist_fileCount (int): Number of files in unpacked package
        - result_1_data_dist_integrity (str): Subresource Integrity string
        - result_1_data_dist_unpackedSize (int): Unpacked size in bytes
        - result_1_data_dist_npm_signature (str): PGP signature of publication
        - result_1_data_dist_signatures_0_sig (str): First signature (base64)
        - result_1_data_dist_signatures_0_keyid (str): First signing key ID
        - result_1_data_dist_signatures_1_sig (str): Second signature (base64)
        - result_1_data_dist_signatures_1_keyid (str): Second signing key ID
    """
    return {
        "result_0_packageInput": "express",
        "result_0_packageName": "express",
        "result_0_versionQueried": "latest",
        "result_0_status": "success",
        "result_0_error": None,
        "result_0_message": "Successfully retrieved latest version",
        "result_0_data_name": "express",
        "result_0_data_version": "4.18.2",
        "result_0_data_description": "Fast, unopinionated, minimalist web framework",
        "result_0_data_author": "TJ Holowaychuk <tj@vision-media.ca>",
        "result_0_data_license": "MIT",
        "result_0_data_homepage": "https://expressjs.com",
        "result_0_data_repositoryUrl": "https://github.com/expressjs/express",
        "result_0_data_bugsUrl": "https://github.com/expressjs/express/issues",
        "result_0_data_dependenciesCount": 9,
        "result_0_data_devDependenciesCount": 27,
        "result_0_data_peerDependenciesCount": 0,
        "result_0_data_types": "@types/express",
        "result_0_data_dist_shasum": "e5c7a846028baa5156366d7b40f54e6b5d58e3c2",
        "result_0_data_dist_tarball": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
        "result_0_data_dist_fileCount": 128,
        "result_0_data_dist_integrity": "sha512-312lKT+I4mWYXl1RZk+Ug7ZLhCgDvLZ2dOqR1kMQ6lX3GYDzjJw4DlPmUWBM2cJZzChBxKC6uKCBR2iD13qQ==",
        "result_0_data_dist_unpackedSize": 1857624,
        "result_0_data_dist_npm_signature": "-----BEGIN PGP SIGNATURE-----...",
        "result_0_data_dist_signatures_0_sig": "MEUCIQD...AB",
        "result_0_data_dist_signatures_0_keyid": "ABC123DEF456",
        "result_0_data_dist_signatures_1_sig": "MEUCIQD...CD",
        "result_0_data_dist_signatures_1_keyid": "GHI789JKL012",
        
        "result_1_packageInput": "nonexistent-package-xyz",
        "result_1_packageName": "nonexistent-package-xyz",
        "result_1_versionQueried": "latest",
        "result_1_status": "error",
        "result_1_error": "Package not found",
        "result_1_message": "Failed to retrieve package: not found in registry",
        "result_1_data_name": "nonexistent-package-xyz",
        "result_1_data_version": "",
        "result_1_data_description": "",
        "result_1_data_author": "",
        "result_1_data_license": "",
        "result_1_data_homepage": "",
        "result_1_data_repositoryUrl": "",
        "result_1_data_bugsUrl": "",
        "result_1_data_dependenciesCount": 0,
        "result_1_data_devDependenciesCount": 0,
        "result_1_data_peerDependenciesCount": 0,
        "result_1_data_types": None,
        "result_1_data_dist_shasum": "",
        "result_1_data_dist_tarball": "",
        "result_1_data_dist_fileCount": 0,
        "result_1_data_dist_integrity": "",
        "result_1_data_dist_unpackedSize": 0,
        "result_1_data_dist_npm_signature": "",
        "result_1_data_dist_signatures_0_sig": "",
        "result_1_data_dist_signatures_0_keyid": "",
        "result_1_data_dist_signatures_1_sig": "",
        "result_1_data_dist_signatures_1_keyid": "",
    }

def npm_sentinel_mcp_npmLatest(packages: List[str]) -> Dict[str, Any]:
    return call_external_api("npmLatest", **locals())

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
