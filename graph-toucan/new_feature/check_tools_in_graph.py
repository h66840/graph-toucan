
import json
import os

def check_tools():
    base_dir = "/Users/plastic/Documents/code/biyesheji/graph-toucan"
    dist_path = os.path.join(base_dir, "tool_info/stateful_tools_distribution.json")
    graph_path = os.path.join(base_dir, "graph/graph_v1.json")
    
    # 1. Load Expected Stateful Tools
    if not os.path.exists(dist_path):
        print(f"Error: {dist_path} not found.")
        return

    with open(dist_path, 'r') as f:
        stateful_tools = json.load(f)
        expected_names = {t['name'] for t in stateful_tools}
    
    print(f"Loaded {len(expected_names)} expected stateful tools from distribution.")

    # 2. Load Graph Tools
    if not os.path.exists(graph_path):
        print(f"Error: {graph_path} not found.")
        return

    print("Loading graph_v1.json (this might take a moment)...")
    with open(graph_path, 'r') as f:
        graph_data = json.load(f)
        
    graph_nodes = graph_data.get("nodes", [])
    graph_tool_names = set()
    for node in graph_nodes:
        # Access nested name: function_schema -> function -> name
        try:
            name = node["function_schema"]["function"]["name"]
            graph_tool_names.add(name)
        except KeyError:
            continue
            
    print(f"Loaded {len(graph_tool_names)} total tools from graph_v1.json.")

    # 3. Compare
    found = expected_names.intersection(graph_tool_names)
    missing = expected_names - graph_tool_names
    
    print("-" * 40)
    print(f"Match Count: {len(found)} / {len(expected_names)}")
    print(f"Missing Count: {len(missing)}")
    
    if missing:
        print("\nExamples of missing tools:")
        for t in list(missing)[:10]:
            print(f" - {t}")
    else:
        print("\nSUCCESS: All stateful tools are present in the graph!")

if __name__ == "__main__":
    check_tools()
