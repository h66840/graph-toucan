#!/usr/bin/env python3
"""
将 path_v1.json 转换为 random_walk_paths12_25.json 格式
"""

import json
from pathlib import Path


def convert_path_format(input_file, output_file):
    """
    将path_v1.json格式转换为random_walk_paths12_25.json格式
    
    Args:
        input_file: 输入的path_v1.json文件路径
        output_file: 输出的random_walk_paths格式文件路径
    """
    # 读取输入文件
    print(f"正在读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取meta信息并转换格式
    meta = data['meta']
    max_steps = meta['max_steps']
    
    new_meta = {
        "graph_path": meta['graph_path'],
        "max_steps": max_steps,
        "walks_per_node": meta['num_walks_per_node'],
        "num_nodes": meta['num_nodes'],
        "total_walks": 0,  # 稍后计算
        "seed": meta['seed']
    }
    
    # 转换paths
    paths = []
    node_results = data['node_results']
    
    print("正在转换路径数据...")
    for node_index_str, node_data in node_results.items():
        node_index = int(node_index_str)
        node_name = node_data['name']
        
        # 优先使用merged_paths（包含merge信息的路径）
        if 'merged_paths' in node_data and len(node_data['merged_paths']) > 0:
            merged_paths_list = node_data['merged_paths']
            
            for merged_path_data in merged_paths_list:
                # 使用merged_path作为主要路径
                merged_path = merged_path_data['merged_path']
                merged_path_names = merged_path_data['merged_path_names']
                merged_path_length = len(merged_path)
                
                # 获取对应的walk_id（从原始path匹配到paths_after_dedup）
                original_path = merged_path_data['path']
                walk_id = None
                
                # 尝试从paths_after_dedup中找到匹配的walk_id
                if 'paths_after_dedup' in node_data:
                    for path_item in node_data['paths_after_dedup']:
                        if path_item['node_indices'] == original_path:
                            walk_id = path_item['walk_id']
                            break
                
                # 如果找不到，使用merged_paths中的索引+1作为walk_id
                if walk_id is None:
                    walk_id = merged_paths_list.index(merged_path_data) + 1
                
                new_path = {
                    "start_index": node_index,
                    "start_name": node_name,
                    "walk_id": walk_id,
                    "node_indices": merged_path,
                    "node_names": merged_path_names,
                    "path_length": merged_path_length,
                    "max_steps": max_steps,
                    "early_stopped": merged_path_length < max_steps,
                    # 保留merge相关信息
                    "original_path": merged_path_data['path'],
                    "original_path_names": merged_path_data['path_names'],
                    "merge_info": merged_path_data['merge_info'],
                    "num_merges": merged_path_data['num_merges']
                }
                paths.append(new_path)
        
        # 如果没有merged_paths，回退到paths_after_dedup
        elif 'paths_after_dedup' in node_data:
            paths_list = node_data['paths_after_dedup']
            
            for path_data in paths_list:
                path_length = path_data['path_length']
                
                new_path = {
                    "start_index": node_index,
                    "start_name": node_name,
                    "walk_id": path_data['walk_id'],
                    "node_indices": path_data['node_indices'],
                    "node_names": path_data['node_names'],
                    "path_length": path_length,
                    "max_steps": max_steps,
                    "early_stopped": path_length < max_steps
                }
                paths.append(new_path)
        
        # 最后回退到paths_before_dedup
        else:
            paths_list = node_data.get('paths_before_dedup', [])
            
            for path_data in paths_list:
                path_length = path_data['path_length']
                
                new_path = {
                    "start_index": node_index,
                    "start_name": node_name,
                    "walk_id": path_data['walk_id'],
                    "node_indices": path_data['node_indices'],
                    "node_names": path_data['node_names'],
                    "path_length": path_length,
                    "max_steps": max_steps,
                    "early_stopped": path_length < max_steps
                }
                paths.append(new_path)
    
    # 更新total_walks
    new_meta['total_walks'] = len(paths)
    
    # 计算平均路径长度
    if paths:
        avg_path_length = sum(p['path_length'] for p in paths) / len(paths)
    else:
        avg_path_length = 0.0
    
    # 构建输出数据结构
    output_data = {
        "meta": new_meta,
        "paths": paths,
        "avg_path_length": avg_path_length
    }
    
    # 保存输出文件
    print(f"正在保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"转换完成！")
    print(f"  - 总路径数: {len(paths)}")
    print(f"  - 平均路径长度: {avg_path_length:.6f}")
    print(f"  - 最大步数: {max_steps}")


if __name__ == "__main__":
    # 设置输入输出文件路径
    input_file = "/data/lhy/datasets/graph-Toucan/walker_path/path_v1.json"
    output_file = "/data/lhy/datasets/graph-Toucan/walker_path/path_v1_converted.json"
    
    convert_path_format(input_file, output_file)

