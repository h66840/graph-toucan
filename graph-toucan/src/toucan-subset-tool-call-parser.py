"""
该文件的目的是抽取single-turn-subset-common-mcp数据的messages的tool call chain.
tool call chain 可以分为几种形式： single turn single step tool call. single turn multi step tool call.
其中 每个step 又可以同时进行 parallel tool call. 对于连续的 role: tool_call , 可以认为是single step 里的 parallel call
如果是role : tool_call , role: tool_response, role: tool_call ,role: tool_response交替出现，则是multi step.
我需要你写一个逻辑，能把我提到的这些关键信息表示出来,可能的格式有: turn 0: step 0: tool call A, tool call B. step 1: toll call A, tool call C.
"""

import json
import datasets
from typing import List, Dict, Any
from tqdm import tqdm


def parse_tool_call_content(content: str) -> Dict[str, Any]:
    """
    解析 tool_call 的 content 字段，提取 tool name
    
    Args:
        content: tool_call 消息的 content 字段
        
    Returns:
        dict: 包含 name 和 arguments 的字典，如果解析失败返回 None
    """
    try:
        # 尝试直接解析 JSON
        if isinstance(content, str):

            try:
                tool_data = json.loads(content)
            except json.JSONDecodeError:
                # 如果 JSON 解析失败，尝试使用 ast.literal_eval
                import ast
                tool_data = ast.literal_eval(content)
        else:
            tool_data = content
        
        if isinstance(tool_data, dict):
            return {
                'name': tool_data.get('name', 'unknown'),
                'arguments': tool_data.get('arguments', '')
            }
    except Exception as e:
        assert 0
    
    assert 0


def parse_tool_call_chain(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    解析 messages 中的 tool call chain
    
    Args:
        messages: 消息列表
        
    Returns:
        dict: 包含 tool call chain 信息的字典
            - turns: list, 每个 turn 的信息
            - summary: dict, 统计信息
    """
    turns = []
    current_turn = None
    current_step = None
    
    i = 0
    while i < len(messages):
        msg = messages[i]
        role = msg.get('role', '')
        
        # 检测新的 turn（通常以 user 消息开始）
        if role == 'user':
            # 如果之前有 turn，先保存
            if current_turn is not None:
                if current_step is not None and current_step['tool_calls']:
                    current_turn['steps'].append(current_step)
                turns.append(current_turn)
            
            # 开始新的 turn
            current_turn = {
                'turn_index': len(turns),
                'steps': []
            }
            current_step = None
        
        # 处理 tool_call
        elif role == 'tool_call':
            # 解析 tool call
            tool_info = parse_tool_call_content(msg.get('content', ''))
            if tool_info:
                tool_name = tool_info['name']
                
                # 检查前一个消息的类型（用于判断是否开始新 step）
                prev_role = messages[i - 1].get('role') if i > 0 else None
                prev_is_response = (prev_role == 'tool_response')
                prev_is_assistant = (prev_role == 'assistant')
                
                # 检查下一个消息是否是 tool_response
                next_is_response = (i + 1 < len(messages) and 
                                  messages[i + 1].get('role') == 'tool_response')
                
                # 开始新 step 的条件：
                # 1. 当前 step 不存在
                # 2. 前一个消息是 tool_response（说明上一个 step 已完成）
                # 3. 前一个消息是 assistant（assistant 消息后通常开始新的操作）
                # 连续的 tool_call（前面是 tool_call）属于同一个 step（parallel call）
                should_start_new_step = (current_step is None or 
                                        prev_is_response or 
                                        prev_is_assistant)
                
                if should_start_new_step:
                    # 保存上一个 step（如果有）
                    if current_step is not None and current_step['tool_calls']:
                        current_turn['steps'].append(current_step)
                    
                    # 开始新的 step
                    current_step = {
                        'step_index': len(current_turn['steps']) if current_turn else 0,
                        'tool_calls': [],
                        'has_response': next_is_response
                    }
                
                # 添加到当前 step
                current_step['tool_calls'].append(tool_name)
                current_step['has_response'] = next_is_response
        
        # 处理 tool_response（标记当前 step 有 response）
        elif role == 'tool_response':
            if current_step is not None:
                current_step['has_response'] = True
        
        i += 1
    
    # 保存最后一个 turn 和 step
    if current_turn is not None:
        if current_step is not None and current_step['tool_calls']:
            current_turn['steps'].append(current_step)
        turns.append(current_turn)
    
    # 统计信息
    total_turns = len(turns)
    total_steps = sum(len(turn['steps']) for turn in turns)
    total_tool_calls = sum(len(step['tool_calls']) for turn in turns for step in turn['steps'])
    
    # 统计 single step 和 multi step 的 turn 数量
    single_step_turns = sum(1 for turn in turns if len(turn['steps']) == 1)
    multi_step_turns = sum(1 for turn in turns if len(turn['steps']) > 1)
    
    # 统计 parallel tool calls（step 中有多个 tool call）
    parallel_steps = sum(1 for turn in turns for step in turn['steps'] if len(step['tool_calls']) > 1)
    
    return {
        'turns': turns,
        'summary': {
            'total_turns': total_turns,
            'total_steps': total_steps,
            'total_tool_calls': total_tool_calls,
            'single_step_turns': single_step_turns,
            'multi_step_turns': multi_step_turns,
            'parallel_steps': parallel_steps,
            'avg_steps_per_turn': total_steps / total_turns if total_turns > 0 else 0,
            'avg_tool_calls_per_step': total_tool_calls / total_steps if total_steps > 0 else 0
        }
    }


def format_tool_call_chain(chain_info: Dict[str, Any]) -> str:
    """
    格式化 tool call chain 为可读的字符串
    
    Args:
        chain_info: parse_tool_call_chain 返回的字典
        
    Returns:
        str: 格式化的字符串
    """
    lines = []
    for turn in chain_info['turns']:
        turn_index = turn['turn_index']
        step_strs = []
        
        for step in turn['steps']:
            step_index = step['step_index']
            tool_calls = step['tool_calls']
            tool_calls_str = ', '.join(tool_calls)
            step_strs.append(f"step {step_index}: {tool_calls_str}")
        
        if step_strs:
            lines.append(f"turn {turn_index}: {' '.join(step_strs)}.")
    
    return '\n'.join(lines)


def process_dataset(dataset_path: str, output_path: str = None):
    """
    处理整个数据集，提取所有样本的 tool call chain
    
    Args:
        dataset_path: str, 数据集路径
        output_path: str or None, 输出 JSON 文件路径
        
    Returns:
        list: 包含所有样本 tool call chain 信息的列表
    """
    print(f"Loading dataset from {dataset_path}...")
    dataset = datasets.load_from_disk(dataset_path)
    print(f"Loaded {len(dataset)} samples")
    
    results = []
    
    for idx, sample in enumerate(tqdm(dataset, desc="Parsing tool call chains")):
        # 解析 messages
        messages_str = sample.get('messages', '[]')
        try:
            messages = json.loads(messages_str) if isinstance(messages_str, str) else messages_str
        except json.JSONDecodeError:
            continue
        
        # 解析 tool call chain
        chain_info = parse_tool_call_chain(messages)
        
        # 格式化输出
        formatted_chain = format_tool_call_chain(chain_info)
        
        result = {
            'uuid': sample.get('uuid', f'sample_{idx}'),
            'chain_info': chain_info,
            'formatted_chain': formatted_chain
        }
        
        results.append(result)
    
    # 保存结果
    if output_path:
        print(f"\nSaving results to {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved successfully!")
    
    # 打印总体统计
    print("\n" + "="*80)
    print("Overall Statistics")
    print("="*80)
    
    total_turns = sum(r['chain_info']['summary']['total_turns'] for r in results)
    total_steps = sum(r['chain_info']['summary']['total_steps'] for r in results)
    total_tool_calls = sum(r['chain_info']['summary']['total_tool_calls'] for r in results)
    single_step_turns = sum(r['chain_info']['summary']['single_step_turns'] for r in results)
    multi_step_turns = sum(r['chain_info']['summary']['multi_step_turns'] for r in results)
    parallel_steps = sum(r['chain_info']['summary']['parallel_steps'] for r in results)
    
    print(f"Total samples: {len(results)}")
    print(f"Total turns: {total_turns}")
    print(f"Total steps: {total_steps}")
    print(f"Total tool calls: {total_tool_calls}")
    print(f"Single-step turns: {single_step_turns}")
    print(f"Multi-step turns: {multi_step_turns}")
    print(f"Steps with parallel tool calls: {parallel_steps}")
    if total_turns > 0:
        print(f"Average steps per turn: {total_steps / total_turns:.2f}")
    if total_steps > 0:
        print(f"Average tool calls per step: {total_tool_calls / total_steps:.2f}")
    print("="*80)
    
    return results

def check_single_turn_no_parallel(messages: List[Dict[str, Any]]) -> bool:
    """
    检查样本是否是 single turn 且没有 parallel tool call
    
    Args:
        messages: 消息列表
        
    Returns:
        bool: True 如果是 single turn 且没有 parallel tool call（需要排除），False 否则
    """
    # 使用已有的 parse_tool_call_chain 函数来解析
    chain_info = parse_tool_call_chain(messages)
    
    # 判断是否是 single turn
    is_single_turn = chain_info['summary']['total_turns'] == 1
    
    # 判断是否有 parallel tool call（某个 step 中有多个 tool call）
    has_parallel = chain_info['summary']['parallel_steps'] > 0
    
    # 如果是 single turn 且没有 parallel tool call，返回 True（需要排除）
    return is_single_turn and not has_parallel


def filter_out_single_turn_no_parallel(dataset_path: str, output_path: str = None):
    """
    用来排除single turn and no parallel tool call的样本
    
    Args:
        dataset_path: str, 输入数据集路径
        output_path: str or None, 如果提供则保存过滤后的数据集
        
    Returns:
        datasets.Dataset: 过滤后的数据集（排除了 single turn 且没有 parallel tool call 的样本）
    """
    print(f"Loading dataset from {dataset_path}...")
    dataset = datasets.load_from_disk(dataset_path)
    print(f"Original dataset size: {len(dataset)}")
    
    def should_keep_sample(sample):
        """判断样本是否应该保留"""
        messages_str = sample.get('messages', '[]')
        try:
            messages = json.loads(messages_str) if isinstance(messages_str, str) else messages_str
        except json.JSONDecodeError:
            # 如果解析失败，保留样本（让用户自己决定）
            return True
        
        # 检查是否是 single turn 且没有 parallel tool call
        is_single_turn_no_parallel = check_single_turn_no_parallel(messages)
        
        # 如果是 single turn 且没有 parallel tool call，则排除（返回 False）
        return not is_single_turn_no_parallel
    
    # 过滤数据集
    print("Filtering out single turn and no parallel tool call samples...")
    filtered_dataset = dataset.filter(should_keep_sample, desc="Filtering samples")
    
    print(f"Filtered dataset size: {len(filtered_dataset)}")
    print(f"Excluded samples: {len(dataset) - len(filtered_dataset)}")
    print(f"Exclusion rate: {(len(dataset) - len(filtered_dataset)) / len(dataset) * 100:.2f}%")
    
    # 保存数据集
    if output_path:
        print(f"\nSaving filtered dataset to {output_path}...")
        filtered_dataset.save_to_disk(output_path)
        print(f"Dataset saved successfully!")
    
    return filtered_dataset


# 用来排除single turn and no parallel tool call的样本
def main():
    """
    主函数
    """
    #dataset_path = '/data/lhy/datasets/graph-Toucan/Toucan-single-turn-with-mcp-field'
    output_path = '/data/lhy/datasets/graph-Toucan/tool_call_chains_v2.json'
    
    # 过滤掉 single turn and no parallel tool call sample
    # dataset = filter_out_single_turn_no_parallel(dataset_path)
    # dataset.save_to_disk('/data/lhy/datasets/graph-Toucan/TOucan-single-turn-with-mcp-field-filtered-out')

    results = process_dataset('/data/lhy/datasets/graph-Toucan/Toucan-single-turn-subset-common-mcp-v1',output_path)
    
    #打印前几个样本的 tool call chain 作为示例
    print("\n" + "="*80)
    print("Sample Tool Call Chains (first 5)")
    print("="*80)
    for i, result in enumerate(results[:5]):
        print(f"\nSample {i+1} (UUID: {result['uuid']}):")
        print(result['formatted_chain'])
        print(f"Summary: {result['chain_info']['summary']}")
    print("="*80)


if __name__ == "__main__":
    main()
