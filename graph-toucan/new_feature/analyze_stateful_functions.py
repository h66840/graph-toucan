
import json
import os

# Define categories that imply statefulness
STATEFUL_CATEGORIES = {
    "File Management",
    "Operating System",
    "Memory Management",
    "Social Media",
    "Development Tools",
    "Communication Tools",
    "Database", # If exists
    "Gaming" # Sometimes has state like inventory, but maybe less critical for this thesis
}

def analyze_tools():
    file_path = "/Users/plastic/Documents/code/biyesheji/graph-toucan/tool_info/tool_classification_results_v1.json"
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    stateful_tools = []
    stateless_tools = []
    
    print(f"Total tools analyzed: {len(data)}")
    
    for item in data:
        tool_name = item['function_schema']['function']['name']
        classification = item.get('classification', {})
        primary = classification.get('primary_label', '').strip('*') # Remove potential markdown bolding
        secondary = [s.strip('*') for s in classification.get('secondary_labels', [])]
        
        is_stateful = False
        reason = ""
        
        if primary in STATEFUL_CATEGORIES:
            is_stateful = True
            reason = f"Primary label: {primary}"
        # Check secondary labels if primary isn't enough (optional, maybe stick to primary for simplicity first)
        elif any(s in STATEFUL_CATEGORIES for s in secondary):
            # For now, let's be conservative and only count if primary is stateful, 
            # or if it's a specific known stateful pattern (like "create", "update", "delete", "post")
            # But let's just list them as 'Potential' for now
            pass

        if is_stateful:
            stateful_tools.append({
                "name": tool_name,
                "category": primary,
                "reason": reason
            })
        else:
            stateless_tools.append({
                "name": tool_name,
                "category": primary
            })
            
    
    # 3. Filter by Graph Existence (Validation Step)
    graph_path = "/Users/plastic/Documents/code/biyesheji/graph-toucan/graph/graph_v1.json"
    if os.path.exists(graph_path):
        print(f"Validating against {graph_path}...")
        with open(graph_path, 'r') as f:
            graph_data = json.load(f)
        
        # Extract active tool names from graph
        active_tool_names = set()
        for node in graph_data.get("nodes", []):
            try:
                active_tool_names.add(node["function_schema"]["function"]["name"])
            except KeyError:
                pass
        
        # Filter
        original_count = len(stateful_tools)
        stateful_tools = [t for t in stateful_tools if t['name'] in active_tool_names]
        print(f"Filtered {original_count} -> {len(stateful_tools)} tools (matched with graph_v1.json).")
    else:
        print("Warning: graph_v1.json not found, skipping validation.")

    print(f"\nFinal Count: {len(stateful_tools)} verified stateful tools.")
    print("-" * 30)
    
    # Export to JSON
    output_path = "/Users/plastic/Documents/code/biyesheji/graph-toucan/tool_info/stateful_tools_distribution.json"
    with open(output_path, 'w') as f:
        json.dump(stateful_tools, f, indent=2)
    print(f"Exported list to {output_path}")

    # Group by category for display
    by_category = {}
    for tool in stateful_tools:
        cat = tool['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(tool['name'])
        
    for cat, tools in by_category.items():
        print(f"\ncategory: {cat} ({len(tools)} tools)")
        for t in tools[:5]: # Show first 5 examples
            print(f"  - {t}")
        if len(tools) > 5:
            print(f"  ... and {len(tools)-5} more")

if __name__ == "__main__":
    analyze_tools()
