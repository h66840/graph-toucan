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
        - name (str): Name of the NPM package
        - description (str): Description of the package functionality and purpose
        - latestVersion (str): Version string of the latest release
        - license (str): License type under which the package is distributed
        - homepage (str): URL to the package's homepage or documentation site
        - repository_type (str): Type of repository (e.g., "git")
        - repository_url (str): Repository location URL
        - author_name (str): Name of the author
        - author_email (str): Email of the author
        - author_url (str): Optional URL associated with the author
        - maintainer_0_name (str): First maintainer name
        - maintainer_0_email (str): First maintainer email
        - maintainer_1_name (str): Second maintainer name
        - maintainer_1_email (str): Second maintainer email
        - keyword_0 (str): First keyword
        - keyword_1 (str): Second keyword
        - dependency_0_name (str): First runtime dependency name
        - dependency_0_version (str): Required version for first runtime dependency
        - dependency_1_name (str): Second runtime dependency name
        - dependency_1_version (str): Required version for second runtime dependency
        - devDependency_0_name (str): First development dependency name
        - devDependency_0_version (str): Required version for first dev dependency
        - devDependency_1_name (str): Second development dependency name
        - devDependency_1_version (str): Required version for second dev dependency
        - peerDependency_0_name (str): First peer dependency name
        - peerDependency_0_version (str): Required version for first peer dependency
        - peerDependency_1_name (str): Second peer dependency name
        - peerDependency_1_version (str): Required version for second peer dependency
        - engine_node (str): Compatible Node.js version
        - script_test (str): Test script command
        - script_build (str): Build script command
        - main (str): Entry point file path
        - bugs_url (str): URL to the issue tracker
        - version_0 (str): First available version string
        - version_1 (str): Second available version string
        - totalVersions (int): Total number of versions published
    """
    return {
        "name": "express",
        "description": "Fast, unopinionated, minimalist web framework for Node.js",
        "latestVersion": "4.18.2",
        "license": "MIT",
        "homepage": "http://expressjs.com",
        "repository_type": "git",
        "repository_url": "https://github.com/expressjs/express.git",
        "author_name": "TJ Holowaychuk",
        "author_email": "tj@vision-media.ca",
        "author_url": "http://tjholowaychuk.com",
        "maintainer_0_name": "Douglas Christopher Wilson",
        "maintainer_0_email": "doug@somethingdoug.com",
        "maintainer_1_name": "Jonathan Ong",
        "maintainer_1_email": "me@jongleberry.com",
        "keyword_0": "web",
        "keyword_1": "framework",
        "dependency_0_name": "accepts",
        "dependency_0_version": "~1.3.8",
        "dependency_1_name": "array-flatten",
        "dependency_1_version": "1.1.1",
        "devDependency_0_name": "after",
        "devDependency_0_version": "0.8.2",
        "devDependency_1_name": "benchmark",
        "devDependency_1_version": "2.1.4",
        "peerDependency_0_name": "optional-peer1",
        "peerDependency_0_version": "1.0.0",
        "peerDependency_1_name": "optional-peer2",
        "peerDependency_1_version": "2.0.0",
        "engine_node": ">= 0.10.0",
        "script_test": "mocha --reporter spec --bail --check-leaks test/",
        "script_build": "echo 'No build step needed'",
        "main": "lib/express.js",
        "bugs_url": "https://github.com/expressjs/express/issues",
        "version_0": "4.18.2",
        "version_1": "4.18.1",
        "totalVersions": 150
    }

def package_registry_server_get_npm_package_details(name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific NPM package.
    
    Args:
        name (str): Name of the NPM package to retrieve details for
        
    Returns:
        Dict containing detailed information about the NPM package with the following structure:
        - name (str): name of the NPM package
        - description (str): description of the package functionality and purpose
        - latestVersion (str): version string of the latest release of the package
        - license (str): license type under which the package is distributed
        - homepage (str): URL to the package's homepage or documentation site
        - repository (Dict): contains 'type' (e.g., "git") and 'url' (repository location)
        - author (Dict): contains author details including 'name', 'email', and optionally 'url'
        - maintainers (List[Dict]): list of maintainer objects, each with 'name' and 'email'
        - keywords (List[str]): list of keywords associated with the package for discoverability
        - dependencies (Dict): mapping of runtime dependency names to their required version strings
        - devDependencies (Dict): mapping of development dependency names to their required version strings
        - peerDependencies (Dict): mapping of peer dependency names to their required version strings (if present)
        - engines (Dict): specifies compatible Node.js versions or other execution environments (if present)
        - scripts (Dict): npm script definitions such as 'test', 'build', etc.
        - main (str): entry point file path for the package when imported
        - bugs (Dict): contains 'url' pointing to the issue tracker for the package
        - versions (List[str]): list of available version strings for the package, typically recent ones
        - totalVersions (int): total number of versions published for this package
        
    Raises:
        ValueError: If the name parameter is empty or None
    """
    if not name:
        raise ValueError("Package name is required")
        
    # Call external API to get flattened data
    api_data = call_external_api("package-registry-server-get-npm-package-details", **locals())
    
    # Construct repository object
    repository = {
        "type": api_data["repository_type"],
        "url": api_data["repository_url"]
    }
    
    # Construct author object
    author = {
        "name": api_data["author_name"],
        "email": api_data["author_email"]
    }
    
    # Add optional url if present
    if "author_url" in api_data and api_data["author_url"]:
        author["url"] = api_data["author_url"]
    
    # Construct maintainers list
    maintainers = [
        {
            "name": api_data["maintainer_0_name"],
            "email": api_data["maintainer_0_email"]
        },
        {
            "name": api_data["maintainer_1_name"],
            "email": api_data["maintainer_1_email"]
        }
    ]
    
    # Construct keywords list
    keywords = [
        api_data["keyword_0"],
        api_data["keyword_1"]
    ]
    
    # Construct dependencies
    dependencies = {
        api_data["dependency_0_name"]: api_data["dependency_0_version"],
        api_data["dependency_1_name"]: api_data["dependency_1_version"]
    }
    
    # Construct devDependencies
    devDependencies = {
        api_data["devDependency_0_name"]: api_data["devDependency_0_version"],
        api_data["devDependency_1_name"]: api_data["devDependency_1_version"]
    }
    
    # Construct peerDependencies
    peerDependencies = {
        api_data["peerDependency_0_name"]: api_data["peerDependency_0_version"],
        api_data["peerDependency_1_name"]: api_data["peerDependency_1_version"]
    }
    
    # Construct engines
    engines = {
        "node": api_data["engine_node"]
    }
    
    # Construct scripts
    scripts = {
        "test": api_data["script_test"],
        "build": api_data["script_build"]
    }
    
    # Construct bugs
    bugs = {
        "url": api_data["bugs_url"]
    }
    
    # Construct versions list
    versions = [
        api_data["version_0"],
        api_data["version_1"]
    ]
    
    # Build final result structure
    result = {
        "name": api_data["name"],
        "description": api_data["description"],
        "latestVersion": api_data["latestVersion"],
        "license": api_data["license"],
        "homepage": api_data["homepage"],
        "repository": repository,
        "author": author,
        "maintainers": maintainers,
        "keywords": keywords,
        "dependencies": dependencies,
        "devDependencies": devDependencies,
        "peerDependencies": peerDependencies,
        "engines": engines,
        "scripts": scripts,
        "main": api_data["main"],
        "bugs": bugs,
        "versions": versions,
        "totalVersions": api_data["totalVersions"]
    }
    
    return result

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
