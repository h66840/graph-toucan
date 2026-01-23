import random
import json
import ast
import copy
import datasets



def check_and_fix_format(data):
    """
    检查和修复数据格式：
    1. 确保tools字段是有效的JSON字符串
    2. 确保messages中role为'tool_call', 'tool_response', 'tool'的content都是JSON字符串
    """
    # 1. 检查和修复tools字段
    if 'tools' in data and data['tools']:
        
        assert type(data['tools']) == str
        # 尝试解析tools，如果是字符串则验证，如果不是则转换
        if isinstance(data['tools'], str):
            tools_obj = json.loads(data['tools'])
            # 重新序列化以确保格式正确
            data['tools'] = json.dumps(tools_obj, ensure_ascii=False)
        else:
            # 如果不是字符串，转换为JSON字符串
            data['tools'] = json.dumps(data['tools'], ensure_ascii=False)

            

    # 2. 检查和修复messages字段
    if 'messages' in data and data['messages']:
        try:
            # 解析messages
            if isinstance(data['messages'], str):
                messages = json.loads(data['messages'])
            else:
                messages = data['messages']
            assert type(messages) == list
            # 检查每个消息的content字段
            modified = False
            for msg in messages:
                if msg.get('role') in ['tool_call', 'tool_response', 'tool']:
                    content = msg.get('content', '')
                    if content:
                        assert type(content) == str
                        # 检查content是否是JSON字符串
                        if isinstance(content, str):
                            try:
                                # 尝试解析以验证是否是有效的JSON字符串
                                json.loads(content)
                                # 如果成功解析，说明已经是有效的JSON字符串，不需要修改
                            except (json.JSONDecodeError, ValueError):
                                # 如果解析失败，尝试用ast.literal_eval
                                try:
                                    
                                    content_obj = ast.literal_eval(content)
                                    assert type(content_obj) == dict
                                    msg['content'] = json.dumps(content_obj, ensure_ascii=False)
                                    modified = True
                                except:
                                    # 如果都失败，说明是普通字符串，将其包装成JSON字符串
                                    # 这里将普通字符串本身作为值进行JSON编码
                                    msg['content'] = json.dumps(content, ensure_ascii=False)
                                    modified = True
                                    
                                    
                        else:
                            # 如果content不是字符串，转换为JSON字符串
                            msg['content'] = json.dumps(content, ensure_ascii=False)
                            modified = True
                            assert 0
            # 如果修改了messages，更新data
            assert type(messages) == list

            data['messages'] = json.dumps(messages)

        except Exception as e:
            print(f"Warning: messages字段格式异常: {e}")
            assert 0
            return data

    return data


def process_single_sample(data):
    
    """
    处理单个样本，随机修改某个turn的数据
    """
    # 初始化新字段
    data['is_modified'] = False
    data['modification_info'] = ""  # 用空字符串表示None，因为datasets不支持None作为列值
    
    if data['subset_name'] not in ['multi-turn']:
        return data

    # 随机抽样30%进行处理
    if random.random() > 0.3:
        return data

    messages = data['messages']
    # format the message
    assert type(messages) == str
    messages = json.loads(messages)
    assert type(messages) == list

    # 找到所有user消息的位置（turn的开始）
    user_positions = []
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            user_positions.append(i)

    if not user_positions:
        return data  # 如果没有user消息，跳过

    # 随机选择一个turn
    selected_turn_start = random.choice(user_positions)

    # 确定这是第几轮（从0开始计数）
    turn_number = user_positions.index(selected_turn_start)

    # 确定这个turn的结束位置
    turn_end = len(messages)
    for pos in user_positions:
        if pos > selected_turn_start:
            turn_end = pos
            break

    # 修改这个turn中的某些消息
    # 1. 收集当前turn中所有的tool_call
    turn_tool_calls = []
    for i in range(selected_turn_start, turn_end):
        msg = messages[i]
        if msg['role'] == 'tool_call':
            # 解析content获取tool名称
            try:
                tool_info = ast.literal_eval(msg['content'])
                tool_name = tool_info.get('name')
                if tool_name:
                    turn_tool_calls.append({
                        'msg_index': i,
                        'tool_name': tool_name,
                        'msg': msg
                    })
            except:
                assert 0

    # 如果当前turn没有tool_call，跳过
    if not turn_tool_calls:
        return data

    # 2. 收集之前所有turn中调用过的tool
    previous_tools = set()
    for i in range(0, selected_turn_start):
        msg = messages[i]
        if msg['role'] == 'tool_call':
            try:
                tool_info = ast.literal_eval(msg['content'])
                tool_name = tool_info.get('name')
                if tool_name:
                    previous_tools.add(tool_name)
            except:
                assert 0

    # 3. 找到一个在之前没有调用过的tool_call
    available_tool_calls = [tc for tc in turn_tool_calls if tc['tool_name'] not in previous_tools]

    # 如果没有满足条件的tool_call，跳过这个样本
    if not available_tool_calls:
        return data

    # 随机选择一个未在之前调用过的tool_call
    selected_tool_call = random.choice(available_tool_calls)
    selected_tool_name = selected_tool_call['tool_name']

    # 4. 从tools字段中找到并pop出这个tool的信息
    tools_list = json.loads(data['tools'])
    removed_tool = None
    new_tools_list = []

    for tool in tools_list:
        if tool.get('type') == 'function' and tool['function']['name'] == selected_tool_name:
            removed_tool = tool
        else:
            new_tools_list.append(tool)

    # 如果找不到对应的tool定义，跳过
    if removed_tool is None:
        return data

    # add meta info
    data['is_modified'] = True
    data['modification_info'] = json.dumps({
        'modified_turn_index': selected_turn_start,
        'turn_number': turn_number,  # 第几轮（从0开始计数）
        'total_turns': len(user_positions),  # 总共有多少轮
        'removed_tool_name': selected_tool_name,
        'removed_tool_definition': removed_tool,
    }, ensure_ascii=False)

    # 更新tools字段
    data['tools'] = json.dumps(new_tools_list)

    # 5. 构造新的消息序列：将这一轮分为(a, b)两部分
    # a: 第一个turn - 回复说信息不足
    # b: 第二个turn - 提供缺失的函数信息，然后继续原来的操作

    # 获取原始user消息
    original_user_msg = messages[selected_turn_start]

    # 构造新的消息列表
    new_messages = []

    # 保留之前的所有消息
    new_messages.extend(messages[:selected_turn_start])

    # 添加第一个turn (a): user消息 + assistant回复信息不足
    new_messages.append(copy.deepcopy(original_user_msg))
    new_messages.append({
        'role': 'assistant',
        'content': "Sorry, I don't have enough information to answer the request. I'm missing some necessary tools to complete this task."
    })

    # 添加第二个turn (b): 提供工具信息的user消息 + 原turn的所有消息
    tool_info_message = {
        'role': 'user',
        'content': f"Here is the additional tool you can use now: {json.dumps(removed_tool, ensure_ascii=False)}"
    }
    new_messages.append(tool_info_message)

    # 添加原turn中除了user消息之外的所有消息（assistant回复、tool_call等）
    new_messages.extend(messages[selected_turn_start + 1:turn_end])

    # 添加这个turn之后的所有消息
    new_messages.extend(messages[turn_end:])

    # 更新data的messages（需要转回json字符串）
    data['messages'] = json.dumps(new_messages, ensure_ascii=False)

    return data



def process_single_sample_v2(data):
    """
    处理单个样本，找到每个函数第一次出现的位置，随机选择一个来修改
    这样可以保证每个选中的sample都会被修改，不会skip
    # todo
    加入第一次出现的函数集合（在随机抽样之前）使用user message index做切分以后的概率分布
    先切成两类（第一轮(user_messages[0]<func_index<user_messages[1])和其他轮）.
    按照反比关系动态调整每一类的抽样概率。
    """
    # 初始化新字段
    data['is_modified'] = False
    data['modification_info'] = ""  # 用空字符串表示None，因为datasets不支持None作为列值

    if data['subset_name'] not in ['multi-turn','single-turn-original']:
        return data

    

    messages = data['messages']
    # format the message
    assert type(messages) == str
    messages = json.loads(messages)
    assert type(messages) == list

    # 0. 先收集所有 user message 的位置，用于确定轮次
    user_positions = []
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            user_positions.append(i)

    if not user_positions:
        return data  # 如果没有user消息，跳过

    # 1. 找到每个函数第一次出现的位置
    first_appearance = {}  # {tool_name: {'index': msg_index, 'msg': msg}}

    for i, msg in enumerate(messages):
        if msg['role'] == 'tool_call':
            try:
                tool_info = json.loads(msg['content'])
                tool_name = tool_info.get('name')
                if tool_name and tool_name not in first_appearance:
                    first_appearance[tool_name] = {
                        'index': i,
                        'tool_name': tool_name,
                        'msg': msg
                    }
            except:
                try:
                    tool_info = ast.literal_eval(msg['content'])
                    tool_name = tool_info.get('name')
                    if tool_name and tool_name not in first_appearance:
                        first_appearance[tool_name] = {
                            'index': i,
                            'tool_name': tool_name,
                            'msg': msg
                        }
                except:
                    assert 0

    # 如果没有tool_call，跳过
    if not first_appearance:
        return data
    
    # 2. 随机选择一个第一次出现的函数
    selected_tool_info = random.choice(list(first_appearance.values()))
    selected_tool_name = selected_tool_info['tool_name']
    selected_tool_index = selected_tool_info['index']

    # 3. 往前找到离这个函数最近的user message的index
    selected_turn_start = None
    for i in range(selected_tool_index, -1, -1):
        if messages[i]['role'] == 'user':
            selected_turn_start = i
            break

    # 如果找不到user消息，跳过
    if selected_turn_start is None:
        return data

    # 确定这是第几轮（从1开始计数）
    turn_number = user_positions.index(selected_turn_start)

    # 4. 确定这个turn的结束位置
    turn_end = len(messages)
    for i in range(selected_turn_start + 1, len(messages)):
        if messages[i]['role'] == 'user':
            turn_end = i
            break

    # 5. 从tools字段中找到并pop出这个tool的信息
    tools_list = json.loads(data['tools'])
    removed_tool = None
    new_tools_list = []

    for tool in tools_list:
        if tool.get('type') == 'function' and tool['function']['name'] == selected_tool_name:
            removed_tool = tool
        else:
            new_tools_list.append(tool)

    # 如果找不到对应的tool定义，跳过
    if removed_tool is None:
        return data

    # add meta info
    data['is_modified'] = True
    data['modification_info'] = json.dumps({
        'modified_turn_index': selected_turn_start,
        'turn_number': turn_number,  # 第几轮（从1开始计数）
        'total_turns': len(user_positions),  # 总共有多少轮
        'removed_tool_name': selected_tool_name,
        'removed_tool_definition': removed_tool,
    }, ensure_ascii=False)

    # 更新tools字段
    data['tools'] = json.dumps(new_tools_list, ensure_ascii=False)

    # 6. 构造新的消息序列：将这一轮分为(a, b)两部分
    # a: 第一个turn - 回复说信息不足
    # b: 第二个turn - 提供缺失的函数信息，然后继续原来的操作

    # 获取原始user消息
    original_user_msg = messages[selected_turn_start]

    # 构造新的消息列表
    new_messages = []

    # 保留之前的所有消息
    new_messages.extend(messages[:selected_turn_start])

    # 添加第一个turn (a): user消息 + assistant回复信息不足
    new_messages.append(copy.deepcopy(original_user_msg))
    new_messages.append({
        'role': 'assistant',
        'content': "Sorry, I don't have enough information to answer the request. I'm missing some necessary tools to complete this task."
    })

    # 添加第二个turn (b): 提供工具信息的user消息 + 原turn的所有消息
    tool_info_message = {
        'role': 'user',
        'content': f"Here is the additional tool you can use now: {json.dumps(removed_tool, ensure_ascii=False)}"
    }
    new_messages.append(tool_info_message)

    # 添加原turn中除了user消息之外的所有消息（assistant回复、tool_call等）
    new_messages.extend(messages[selected_turn_start + 1:turn_end])

    # 添加这个turn之后的所有消息
    new_messages.extend(messages[turn_end:])

    # 更新data的messages（需要转回json字符串）
    data['messages'] = json.dumps(new_messages, ensure_ascii=False)

    return data


def _select_tool_with_turn_bias(first_appearance, messages, user_positions, 
                                  bias_factor=2.0, min_prob=0,max_prob=0):
    """
    🚀 高级版本：更精细的概率控制
    
    Args:
        bias_factor: 反比偏向因子，越大偏向性越强
        min_prob: 最小概率，防止某类完全被忽略
    """
    
    # 分类函数
    first_turn_tools = []
    other_turn_tools = []
    
    for tool_name, tool_info in first_appearance.items():
        tool_index = tool_info['index']
        
        turn_start_index = None
        for i in range(tool_index, -1, -1):
            if messages[i]['role'] == 'user':
                turn_start_index = i
                break
        
        if turn_start_index is not None:
            if turn_start_index == user_positions[0]:
                first_turn_tools.append(tool_info)
            else:
                other_turn_tools.append(tool_info)
    
    total_first = len(first_turn_tools)
    total_other = len(other_turn_tools)
    
    if total_first == 0:
        return random.choice(other_turn_tools)
    elif total_other == 0:
        if random.random() < 0.2: 
            return random.choice(first_turn_tools)
        return None
    else:
        # 🔥 高级概率计算
        # 使用 bias_factor 调整反比强度
        first_turn_weight = (1 / total_first) ** bias_factor
        other_turn_weight = (1 / total_other) ** bias_factor
        
        # 归一化并应用最小概率约束
        total_weight = first_turn_weight + other_turn_weight
        first_turn_prob = first_turn_weight / total_weight
        
        # 应用最大/最小概率约束
        first_turn_prob = max(min_prob, min(max_prob, first_turn_prob))
        
        if random.random() < first_turn_prob:
            return random.choice(first_turn_tools)
        else:
            return random.choice(other_turn_tools)


def _select_tool_with_turn_bias_list(call_list, messages, user_positions, 
                                     bias_factor=2.0, min_prob=0, max_prob=0):
    """
    适配 list 版 first_appearance 的 turn-bias 选择逻辑。
    call_list 中的元素是完整的 tool_call 信息：
    {'index','tool_name','msg','arguments','required_params','tool_def'}
    """
    first_turn_calls = []
    other_turn_calls = []

    for call in call_list:
        tool_index = call['index']

        turn_start_index = None
        for i in range(tool_index, -1, -1):
            if messages[i]['role'] == 'user':
                turn_start_index = i
                break

        if turn_start_index is not None:
            if turn_start_index == user_positions[0]:
                first_turn_calls.append(call)
            else:
                other_turn_calls.append(call)

    total_first = len(first_turn_calls)
    total_other = len(other_turn_calls)

    if total_first == 0 and total_other == 0:
        return None
    if total_first == 0:
        return random.choice(other_turn_calls)
    elif total_other == 0:
        if random.random() < 0:
            return random.choice(first_turn_calls)
        return None
    else:
        first_turn_weight = (1 / total_first) ** bias_factor
        other_turn_weight = (1 / total_other) ** bias_factor

        total_weight = first_turn_weight + other_turn_weight
        first_turn_prob = first_turn_weight / total_weight

        first_turn_prob = max(min_prob, min(max_prob, first_turn_prob))

        if random.random() < first_turn_prob:
            return random.choice(first_turn_calls)
        else:
            return random.choice(other_turn_calls)

def _select_tool_with_turn_bias_list_plus(call_list, messages, user_positions, 
                                         turn_probs=None, default_prob=0.0, seed=None):
    """
    增强版：可以分别控制前5个轮次的抽样概率
    
    Args:
        call_list: tool_call 列表，元素格式：{'index','tool_name','msg','arguments','required_params','tool_def'}
        messages: 消息列表
        user_positions: user消息的位置列表
        turn_probs: 轮次抽样概率配置，可以是：
            - dict: {1: 0.3, 2: 0.2, 3: 0.15, 4: 0.1, 5: 0.05} 表示各轮次的抽样概率
            - list: [0.3, 0.2, 0.15, 0.1, 0.05] 表示第1-5轮的概率（索引0对应第1轮）
        default_prob: 第6轮及以后的默认抽样概率（默认0.0，即不抽样）
        seed: 随机种子
    
    Returns:
        选中的tool_call，如果没有满足条件的则返回None
    """
    if seed is not None:
        random.seed(seed)
    
    # 解析turn_probs参数
    if turn_probs is None:
        # 默认配置：第1轮概率较高，后续递减
        turn_probs = {1: 0.1, 2: 0.4, 3: 0.2, 4: 0.1, 5: 0.05}
    
    if isinstance(turn_probs, list):
        # 将列表转换为字典
        turn_probs = {i+1: prob for i, prob in enumerate(turn_probs) if i < 5}
    
    # 确保turn_probs是字典格式
    if not isinstance(turn_probs, dict):
        turn_probs = {}
    
    # 按轮次分组
    turn_groups = {}  # {turn_number: [calls]}
    
    for call in call_list:
        tool_index = call['index']
        
        # 找到这个tool_call属于哪个轮次
        turn_start_index = None
        for i in range(tool_index, -1, -1):
            if messages[i]['role'] == 'user':
                turn_start_index = i
                break
        
        if turn_start_index is not None:
            # 确定这是第几轮（从1开始计数）
            try:
                turn_number = user_positions.index(turn_start_index) + 1
            except ValueError:
                # 如果找不到，跳过
                continue
            
            if turn_number not in turn_groups:
                turn_groups[turn_number] = []
            turn_groups[turn_number].append(call)
    
    if not turn_groups:
        return None
    
    # 计算每个轮次的权重（基于概率和数量）
    turn_weights = {}
    for turn_num, calls in turn_groups.items():
        count = len(calls)
        if count == 0:
            continue
        
        # 获取该轮次的抽样概率
        prob = turn_probs.get(turn_num, default_prob if turn_num > 5 else 0.0)
        
        # 如果概率为0，跳过该轮次
        if prob <= 0:
            continue
        
        # 权重计算方式：
        # 方式1: prob / count - 数量越少，权重越高（偏向样本少的轮次）
        # 方式2: prob * count - 数量越多，权重越高（偏向样本多的轮次）
        # 方式3: prob - 直接使用概率，不考虑数量
        # 这里使用方式1，因为通常我们希望平衡各轮次的样本分布
        turn_weights[turn_num] = prob 
    
    if not turn_weights:
        return None
    
    # 归一化权重
    total_weight = sum(turn_weights.values())
    if total_weight == 0:
        return None
    
    # 根据权重进行加权随机选择
    rand_val = random.random() * total_weight
    cumulative = 0
    
    for turn_num, weight in sorted(turn_weights.items()):
        cumulative += weight
        if rand_val <= cumulative:
            # 从该轮次中随机选择一个
            return random.choice(turn_groups[turn_num])
    
    # 如果由于浮点数精度问题没有选中，返回权重最大的轮次中的一个
    max_turn = max(turn_weights.items(), key=lambda x: x[1])[0]
    return random.choice(turn_groups[max_turn])

def process_single_sample_v3(data):
    """
    处理单个样本，基于轮次分布的动态概率抽样
    改进策略：
    1. 按第一轮和其他轮分类
    2. 使用反比关系动态调整抽样概率
    3. 基于user message index切分后的概率分布
    """
    
    if data['subset_name'] not in ['multi-turn','single-turn-original']:
        return data

    messages = data['messages']
    assert type(messages) == str
    messages = json.loads(messages)
    assert type(messages) == list
    # 0. 先收集所有 user message 的位置，用于确定轮次
    user_positions = []
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            user_positions.append(i)
    if not user_positions:
        return data
    # 1. 找到每个函数第一次出现的位置
    first_appearance = {}
    for i, msg in enumerate(messages):
        if msg['role'] == 'tool_call':
            try:
                tool_info = json.loads(msg['content'])
                tool_name = tool_info.get('name')
                if tool_name and tool_name not in first_appearance:
                    first_appearance[tool_name] = {
                        'index': i,
                        'tool_name': tool_name,
                        'msg': msg
                    }
            except:
                try:
                    tool_info = ast.literal_eval(msg['content'])
                    tool_name = tool_info.get('name')
                    if tool_name and tool_name not in first_appearance:
                        first_appearance[tool_name] = {
                            'index': i,
                            'tool_name': tool_name,
                            'msg': msg
                        }
                except:
                    assert 0
    if not first_appearance:
        return data
    # 🚀 **核心改进：基于轮次分布的动态概率抽样**
    # 基于sub-category 选择采样策略
    selected_tool_info = None
    if data['subset_name'] == 'multi-turn':
        if random.random() < 0:
            selected_tool_info = _select_tool_with_turn_bias(
                first_appearance, messages, user_positions
            )
    elif data['subset_name'] in ['single-turn-original']:
        if random.random() < 0:
            selected_tool_info = random.choice(list(first_appearance.values())) 
        else:
            selected_tool_info = None
    if not selected_tool_info:
        return data
    selected_tool_name = selected_tool_info['tool_name']
    selected_tool_index = selected_tool_info['index']
    # 后续处理逻辑保持不变...
    # 3. 往前找到离这个函数最近的user message的index
    selected_turn_start = None
    for i in range(selected_tool_index, -1, -1):
        if messages[i]['role'] == 'user':
            selected_turn_start = i
            break
    if selected_turn_start is None:
        return data
    # 确定这是第几轮
    turn_number = user_positions.index(selected_turn_start)
    # 4. 确定turn结束位置
    turn_end = len(messages)
    for i in range(selected_turn_start + 1, len(messages)):
        if messages[i]['role'] == 'user':
            turn_end = i
            break
    # 5. 处理tools信息
    tools_list = json.loads(data['tools'])
    removed_tool = None
    new_tools_list = []
    for tool in tools_list:
        if tool.get('type') == 'function' and tool['function']['name'] == selected_tool_name:
            removed_tool = tool
        else:
            new_tools_list.append(tool)
    if removed_tool is None:
        return data
    # 添加元信息
    data['is_modified'] = True
    data['modification_info'] = json.dumps({
        'modified_turn_index': selected_turn_start,
        'turn_number': turn_number,
        'total_turns': len(user_positions),
        'removed_tool_name': selected_tool_name,
        'removed_tool_definition': removed_tool,
        'selection_method': 'turn_biased',  # 标记使用了新的选择方法
    }, ensure_ascii=False)
    # 更新tools字段
    data['tools'] = json.dumps(new_tools_list, ensure_ascii=False)
    # 6. 构造新消息序列
    original_user_msg = messages[selected_turn_start]
    new_messages = []
    # 保留之前的消息
    new_messages.extend(messages[:selected_turn_start])
    # 添加第一个turn
    new_messages.append(copy.deepcopy(original_user_msg))
    new_messages.append({
        'role': 'assistant',
        'content': "Sorry, I don't have enough information to answer the request. I'm missing some necessary tools to complete this task."
    })
    # 添加第二个turn
    tool_info_message = {
        'role': 'user',
        'content': f"Here is the additional tool you can use now: {json.dumps(removed_tool, ensure_ascii=False)}"
    }
    new_messages.append(tool_info_message)
    new_messages.extend(messages[selected_turn_start + 1:turn_end])
    new_messages.extend(messages[turn_end:])
    data['messages'] = json.dumps(new_messages, ensure_ascii=False)
    return data
def analyze_modified_samples(modified_samples):
    """
    统计修改样本的详细信息

    Args:
        modified_samples: 被修改的样本数据集

    Returns:
        dict: 包含各种统计信息的字典
    """
    from collections import Counter

    stats = {
        'total_modified': len(modified_samples),
        'turn_number_distribution': Counter(),  # 每个轮次被修改的次数
        'removed_tools': Counter(),  # 被移除的工具名称及其次数
        'total_turns_distribution': Counter(),  # 样本总轮次的分布
        'turn_percentage_distribution': [],  # 修改发生在样本中的相对位置（百分比）
        'function_call_count_distribution': Counter(),  # 每个样本的function call数量分布
    }

    for sample in modified_samples:
        if sample['is_modified'] and sample['modification_info'] and sample['subset_name'] in ['multi-turn','single-turn-original']:
            try:
                mod_info = json.loads(sample['modification_info'])

                # 统计轮次分布
                turn_number = mod_info.get('turn_number', -1)
                stats['turn_number_distribution'][turn_number] += 1

                # 统计被移除的工具
                removed_tool_name = mod_info.get('removed_tool_name', 'unknown')
                stats['removed_tools'][removed_tool_name] += 1

                # 统计总轮次分布
                total_turns = mod_info.get('total_turns', 0)
                stats['total_turns_distribution'][total_turns] += 1

                # 计算修改发生的相对位置（百分比）
                if total_turns > 0:
                    percentage = (turn_number / total_turns) * 100
                    stats['turn_percentage_distribution'].append(percentage)

                # 统计样本有多少个function call
                messages = sample.get('messages', '[]')
                if isinstance(messages, str):
                    messages = json.loads(messages)

                function_call_count = sum(1 for msg in messages if msg.get('role') == 'tool_call')
                stats['function_call_count_distribution'][function_call_count] += 1

            except json.JSONDecodeError:
                continue

    return stats



def print_statistics(stats):
    """
    打印统计信息

    Args:
        stats: analyze_modified_samples返回的统计字典
    """
    print("\n" + "="*60)
    print("Modified Samples Statistics")
    print("="*60)

    print(f"\n📊 Total modified samples: {stats['total_modified']}")

    # 打印轮次分布
    print("\n🔢 Turn Number Distribution (which turn was modified):")
    turn_numbers = sorted(stats['turn_number_distribution'].items())
    for turn_num, count in turn_numbers:
        percentage = (count / stats['total_modified']) * 100
        print(f"  Turn {turn_num}: {count} samples ({percentage:.2f}%)")

    # 打印总轮次分布
    print("\n📈 Total Turns Distribution (how many turns in sample):")
    total_turns = sorted(stats['total_turns_distribution'].items())
    for turns, count in total_turns:
        percentage = (count / stats['total_modified']) * 100
        print(f"  {turns} turns: {count} samples ({percentage:.2f}%)")

    # 打印被移除工具的统计（只显示前20个）
    print("\n🔧 Top 20 Removed Tools:")
    top_tools = stats['removed_tools'].most_common(20)
    for tool_name, count in top_tools:
        percentage = (count / stats['total_modified']) * 100
        print(f"  {tool_name}: {count} times ({percentage:.2f}%)")

    # 打印function call数量分布
    print("\n📞 Function Call Count Distribution:")
    function_call_counts = sorted(stats['function_call_count_distribution'].items())

    # 计算平均function call数量
    total_function_calls = sum(count * samples for count, samples in function_call_counts)
    avg_function_calls = total_function_calls / stats['total_modified'] if stats['total_modified'] > 0 else 0
    print(f"  Average function calls per sample: {avg_function_calls:.2f}")
    print()

    for count, samples in function_call_counts:
        percentage = (samples / stats['total_modified']) * 100
        print(f"  {count} function calls: {samples} samples ({percentage:.2f}%)")

    # 打印相对位置统计
    if stats['turn_percentage_distribution']:
        import statistics
        percentages = stats['turn_percentage_distribution']
        print("\n📍 Modification Position (as percentage of total turns):")
        print(f"  Mean: {statistics.mean(percentages):.2f}%")
        print(f"  Median: {statistics.median(percentages):.2f}%")
        print(f"  Min: {min(percentages):.2f}%")
        print(f"  Max: {max(percentages):.2f}%")

        # 分段统计
        early = sum(1 for p in percentages if p < 33.33)
        middle = sum(1 for p in percentages if 33.33 <= p < 66.67)
        late = sum(1 for p in percentages if p >= 66.67)
        total = len(percentages)

        print(f"\n  Early turns (0-33%): {early} ({early/total*100:.2f}%)")
        print(f"  Middle turns (33-67%): {middle} ({middle/total*100:.2f}%)")
        print(f"  Late turns (67-100%): {late} ({late/total*100:.2f}%)")

    print("\n" + "="*60 + "\n")

def filter_by_ratio(dataset, field_name, target_value, remove_ratio=0.5):
    """
    按比例剔除匹配的数据
    remove_ratio: 0.0-1.0，表示剔除匹配数据的比例
    """
    import random
    
    def ratio_filter(example, idx):
        if example[field_name] == target_value:
            # 根据索引和比例决定是否保留
            random.seed(idx)  # 确保结果可重现
            return random.random() > remove_ratio
        return True
    
    return dataset.filter(ratio_filter, with_indices=True)

def filter_by_turn_number_with_sampling(dataset, turn_number=1, max_count=None, sampling_ratio=None, seed=42):
    """
    按照turn_number对数据集进行过滤和抽样
    
    Args:
        dataset: 数据集，每个样本的modification_info字段包含turn_number信息
        turn_number: 要控制的turn_number值（默认为1）
        max_count: 对于指定turn_number的样本，最多保留的数量（None表示不限制）
        sampling_ratio: 对于指定turn_number的样本，保留的比例（0.0-1.0，None表示不限制）
                       max_count和sampling_ratio同时指定时，优先使用max_count
        seed: 随机种子，确保结果可重现
    
    Returns:
        filtered_dataset: 过滤后的数据集
        stats: 统计信息字典
    """
    from collections import Counter
    import random
    
    random.seed(seed)
    
    # 先按turn_number分组
    turn_number_samples = []  # 指定turn_number的样本
    other_samples = []  # 其他turn_number的样本
    
    for sample in dataset:
        try:
            if sample.get('modification_info'):
                mod_info = json.loads(sample['modification_info'])
                sample_turn_number = mod_info.get('turn_number')
                
                if sample_turn_number == turn_number:
                    turn_number_samples.append(sample)
                else:
                    other_samples.append(sample)
            else:
                # 如果没有modification_info，保留
                other_samples.append(sample)
        except (json.JSONDecodeError, TypeError):
            # 如果解析失败，保留
            other_samples.append(sample)
    
    # 对指定turn_number的样本进行抽样
    original_count = len(turn_number_samples)
    
    if max_count is not None:
        # 使用max_count限制数量
        if len(turn_number_samples) > max_count:
            # 随机抽样
            turn_number_samples = random.sample(turn_number_samples, max_count)
            print(f"Sampled {max_count} samples from {original_count} samples with turn_number={turn_number}")
        else:
            print(f"All {original_count} samples with turn_number={turn_number} are kept (requested {max_count})")
    elif sampling_ratio is not None:
        # 使用sampling_ratio限制比例
        target_count = int(len(turn_number_samples) * sampling_ratio)
        if target_count < len(turn_number_samples):
            turn_number_samples = random.sample(turn_number_samples, target_count)
            print(f"Sampled {target_count} samples ({sampling_ratio*100:.1f}%) from {original_count} samples with turn_number={turn_number}")
        else:
            print(f"All {original_count} samples with turn_number={turn_number} are kept (requested {sampling_ratio*100:.1f}%)")
    else:
        print(f"All {original_count} samples with turn_number={turn_number} are kept (no sampling)")
    
    # 合并结果
    filtered_samples = turn_number_samples + other_samples
    
    # 统计信息
    turn_number_distribution = Counter()
    for sample in filtered_samples:
        try:
            if sample.get('modification_info'):
                mod_info = json.loads(sample['modification_info'])
                sample_turn_number = mod_info.get('turn_number')
                if sample_turn_number is not None:
                    turn_number_distribution[sample_turn_number] += 1
        except (json.JSONDecodeError, TypeError):
            pass
    
    stats = {
        'original_total': len(dataset),
        'filtered_total': len(filtered_samples),
        'turn_number_distribution': turn_number_distribution,
        'target_turn_number': turn_number,
        'target_turn_original_count': original_count,
        'target_turn_filtered_count': len(turn_number_samples),
    }
    
    # 将列表转换回数据集
    # 使用datasets库的Dataset.from_list方法
    filtered_dataset = datasets.Dataset.from_list(filtered_samples)
    
    return filtered_dataset, stats

def init_single_sample(data):
    """
    处理单个样本，基于轮次分布的动态概率抽样
    改进策略：
    1. 按第一轮和其他轮分类
    2. 使用反比关系动态调整抽样概率
    3. 基于user message index切分后的概率分布
    """
    # 初始化新字段
    data['is_modified'] = False
    data['modification_info'] = ""
    
    return data

def shuffle_sample_tool_list(data):
    """
    shuffle the tool list
    """
    tools_list = json.loads(data['tools'])
    random.shuffle(tools_list)
    data['tools'] = json.dumps(tools_list, ensure_ascii=False)
    return data

def extract_processed_uuids(dataset):
    """
    从数据集中提取所有 modified 样本的 uuid。
    这些 uuid 对应的原始样本（is_modified == False）不应该再次被处理。
    
    Args:
        dataset: 数据集
    
    Returns:
        set: 已处理的 uuid 集合
    """
    processed_uuids = set()
    
    for sample in dataset:
        if sample.get('is_modified', False) and 'uuid' in sample:
            processed_uuids.add(sample['uuid'])
    
    return processed_uuids

def find_common_uuids(dataset1, dataset2, dataset1_name="Dataset1", dataset2_name="Dataset2"):
    """
    查找两个数据集中uuid相同的样本
    
    Args:
        dataset1: 第一个数据集
        dataset2: 第二个数据集
        dataset1_name: 第一个数据集的名称（用于打印）
        dataset2_name: 第二个数据集的名称（用于打印）
    
    Returns:
        dict: 包含统计信息的字典，包括：
            - common_uuids: 两个数据集中相同的uuid集合
            - dataset1_uuids: 第一个数据集中的所有uuid集合
            - dataset2_uuids: 第二个数据集中的所有uuid集合
            - dataset1_only: 只在第一个数据集中存在的uuid集合
            - dataset2_only: 只在第二个数据集中存在的uuid集合
            - stats: 统计信息字典
    """
    # 提取两个数据集中的所有uuid
    dataset1_uuids = set()
    dataset2_uuids = set()
    
    for sample in dataset1:
        if 'uuid' in sample and sample['uuid']:
            dataset1_uuids.add(sample['uuid'])
    
    for sample in dataset2:
        if 'uuid' in sample and sample['uuid']:
            dataset2_uuids.add(sample['uuid'])
    
    # 找出相同的uuid
    common_uuids = dataset1_uuids & dataset2_uuids
    
    # 找出只在各自数据集中存在的uuid
    dataset1_only = dataset1_uuids - dataset2_uuids
    dataset2_only = dataset2_uuids - dataset1_uuids
    
    # 统计信息
    stats = {
        'dataset1_total': len(dataset1),
        'dataset2_total': len(dataset2),
        'dataset1_uuids_count': len(dataset1_uuids),
        'dataset2_uuids_count': len(dataset2_uuids),
        'common_uuids_count': len(common_uuids),
        'dataset1_only_count': len(dataset1_only),
        'dataset2_only_count': len(dataset2_only),
    }
    
    return {
        'common_uuids': common_uuids,
        'dataset1_uuids': dataset1_uuids,
        'dataset2_uuids': dataset2_uuids,
        'dataset1_only': dataset1_only,
        'dataset2_only': dataset2_only,
        'stats': stats,
    }

def print_common_uuids_info(common_info, dataset1_name="Dataset1", dataset2_name="Dataset2"):
    """
    打印两个数据集uuid比较的统计信息
    
    Args:
        common_info: find_common_uuids返回的字典
        dataset1_name: 第一个数据集的名称
        dataset2_name: 第二个数据集的名称
    """
    stats = common_info['stats']
    
    print("\n" + "="*60)
    print(f"UUID Comparison: {dataset1_name} vs {dataset2_name}")
    print("="*60)
    
    print(f"\n📊 Dataset Statistics:")
    print(f"  {dataset1_name}:")
    print(f"    Total samples: {stats['dataset1_total']}")
    print(f"    Samples with uuid: {stats['dataset1_uuids_count']}")
    print(f"  {dataset2_name}:")
    print(f"    Total samples: {stats['dataset2_total']}")
    print(f"    Samples with uuid: {stats['dataset2_uuids_count']}")
    
    print(f"\n🔍 Comparison Results:")
    print(f"  Common uuids: {stats['common_uuids_count']}")
    if stats['dataset1_uuids_count'] > 0:
        common_percentage_1 = (stats['common_uuids_count'] / stats['dataset1_uuids_count']) * 100
        print(f"    ({common_percentage_1:.2f}% of {dataset1_name} samples)")
    if stats['dataset2_uuids_count'] > 0:
        common_percentage_2 = (stats['common_uuids_count'] / stats['dataset2_uuids_count']) * 100
        print(f"    ({common_percentage_2:.2f}% of {dataset2_name} samples)")
    
    print(f"  Only in {dataset1_name}: {stats['dataset1_only_count']}")
    print(f"  Only in {dataset2_name}: {stats['dataset2_only_count']}")
    
    # 如果相同的uuid数量较少，可以打印出来
    if stats['common_uuids_count'] > 0 and stats['common_uuids_count'] <= 50:
        print(f"\n📋 Common UUIDs (showing all {stats['common_uuids_count']}):")
        for uuid in sorted(common_info['common_uuids']):
            print(f"    {uuid}")
    elif stats['common_uuids_count'] > 50:
        print(f"\n📋 Common UUIDs (showing first 20 of {stats['common_uuids_count']}):")
        for uuid in sorted(list(common_info['common_uuids']))[:20]:
            print(f"    {uuid}")
        print(f"    ... and {stats['common_uuids_count'] - 20} more")
    
    print("\n" + "="*60 + "\n")

def remove_common_uuids_from_dataset(dataset1, dataset2):
    """
    从dataset1中移除与dataset2有相同UUID的样本
    
    Args:
        dataset1: 第一个数据集（需要被过滤的数据集）
        dataset2: 第二个数据集（用于比较的数据集）
    
    Returns:
        tuple: (filtered_dataset, removed_count, common_uuids)
            - filtered_dataset: 过滤后的数据集
            - removed_count: 被移除的样本数量
            - common_uuids: 重合的UUID集合
    """
    # 首先找出两个数据集中相同的UUID
    common_info = find_common_uuids(dataset1, dataset2)
    common_uuids = common_info['common_uuids']
    
    if not common_uuids:
        print("No common UUIDs found. Returning original dataset1.")
        return dataset1, 0, common_uuids
    
    print(f"Found {len(common_uuids)} common UUIDs. Filtering dataset1...")
    
    # 过滤dataset1，移除UUID在common_uuids中的样本
    def filter_func(example):
        if 'uuid' in example and example['uuid']:
            return example['uuid'] not in common_uuids
        # 如果没有uuid字段，保留该样本
        return True
    
    filtered_dataset = dataset1.filter(filter_func)
    removed_count = len(dataset1) - len(filtered_dataset)
    
    print(f"Removed {removed_count} samples from dataset1.")
    print(f"Original dataset1 size: {len(dataset1)}")
    print(f"Filtered dataset1 size: {len(filtered_dataset)}")
    
    return filtered_dataset, removed_count, common_uuids

def process_single_sample_v4(data, processed_uuids=None):
    """
    this function is used to process sample to miss param situation.
    random sample one function call(fc A) need have params in tool_call step in one random select turn.
    find the before and after nearest user message index(index_b,index_c) ,we copy this turn at the begining of the index_b, and 其余的index依次向后, then we get needed to rewrite user message and target tool, then we can based on
    the target tool call required func param to rewrite user message to contruct the lack param info turn. 
    
    Args:
        data: 数据集样本
        processed_uuids: set, 已处理的 uuid 集合，用于避免重复处理同一原始样本
    """
    
    # 仅处理 subset_name 在目标集合中，且当前还未被标记修改的数据
    # 即：subset_name in ['multi-turn','single-turn-original'] 且 data['is_modified'] == False
    if data['subset_name'] not in ['multi-turn'] or data.get('is_modified', False):
        return data
    
    # 检查当前样本的 uuid 是否已经被处理过（即存在相同 uuid 且 is_modified == True 的样本）
    if processed_uuids is not None and 'uuid' in data:
        if data['uuid'] in processed_uuids:
            # 这个原始样本已经被用来生成过 modified 样本了，跳过
            return data

    messages = data['messages']
    assert type(messages) == str
    messages = json.loads(messages)
    assert type(messages) == list
    # 0. 先收集所有 user message 的位置，用于确定轮次
    user_positions = []
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            user_positions.append(i)
    if not user_positions:
        return data
    # 1. collect tool call index set with full param info
    #    first_appearance 在这里表示“所有满足条件的 tool_call 集合”，元素是完整的调用信息
    tools_list = json.loads(data['tools'])
    tools_dict = {}
    for tool in tools_list:
        if tool.get('type') == 'function':
            tools_dict[tool['function']['name']] = tool

    first_appearance = []  # list of call_info: {'index','tool_name','msg','arguments','required_params','tool_def'}
    for i, msg in enumerate(messages):
        if msg['role'] != 'tool_call':
            continue

        # 解析 tool_call 内容
        try:
            tool_info = json.loads(msg['content'])
        except Exception:
            try:
                tool_info = ast.literal_eval(msg['content'])
            except Exception:
                continue

        if not isinstance(tool_info, dict):
            continue

        tool_name = tool_info.get('name')
        tool_args = tool_info.get('arguments', {})

        # judge tool_arge type
        assert type(tool_args) == str
        try:
            tool_args = json.loads(tool_args)
        except Exception:
            continue
        if type(tool_args) == str:
            tool_args = json.loads(tool_args)
        assert type(tool_args) == dict
        # 要求：有参数且为 dict，且非空
        if not (tool_name and isinstance(tool_args, dict) and tool_args):
            continue

        # 根据 schema 检查 required 参数是否都在 arguments 中
        tool_def = tools_dict.get(tool_name)
        if not tool_def:
            continue

        required_params = tool_def.get('function', {}).get('parameters', {}).get('required', [])
        # 如果 schema 没有 required 或 required 为空，则认为不满足“缺参数”任务的前提，直接跳过
        if not required_params:
            continue

        if not all(req in tool_args for req in required_params):
            # 参数没有完全覆盖 required，就跳过
            continue

        call_info = {
            'index': i,
            'tool_name': tool_name,
            'msg': msg,
            'arguments': tool_args,
            'required_params': required_params,
            'tool_def': tool_def,
        }

        # 保证集合中不出现完全相同的调用（同名 + 相同参数）
        if not any(
            c['tool_name'] == call_info['tool_name'] and c['arguments'] == call_info['arguments']
            for c in first_appearance
        ):
            first_appearance.append(call_info)

    if not first_appearance:
        return data

    # 2. 在 first_appearance(list) 中做基于轮次的偏置采样
    selected_tool_info = None
    if data['subset_name'] == 'multi-turn':
        if random.random() < 0.5:
            # 方式1: 使用原始版本（只区分first turn和other turn）
            # selected_tool_info = _select_tool_with_turn_bias_list(
            #     first_appearance, messages, user_positions
            # )
            
            # 方式2: 使用增强版（可以分别控制前5个轮次的概率）
            # 配置示例：第1轮30%，第2轮20%，第3轮15%，第4轮10%，第5轮5%，其他轮次不抽样
            turn_probs = {
                1: 0,   # 第1轮抽样概率
                2: 0.2,   # 第2轮抽样概率
                3: 0.4,  # 第3轮抽样概率
                4: 0.6,   # 第4轮抽样概率
                5: 0.8,  # 第5轮抽样概率
            }
            # 或者使用列表格式：[0.3, 0.2, 0.15, 0.1, 0.05]
            # turn_probs = [0.3, 0.2, 0.15, 0.1, 0.05]
            
            selected_tool_info = _select_tool_with_turn_bias_list_plus(
                first_appearance, 
                messages, 
                user_positions,
                turn_probs=turn_probs,
                default_prob=0,  # 第6轮及以后的默认概率（0.0表示不抽样）
                seed=42  # 可以设置随机种子确保可重现
            )
    elif data['subset_name'] in ['single-turn-original']:
        if random.random() < 0.3:
            selected_tool_info = random.choice(first_appearance)
        else:
            selected_tool_info = None
    if not selected_tool_info:
        return data

    selected_tool_name = selected_tool_info['tool_name']
    selected_tool_index = selected_tool_info['index']

    # 2. 解析选中 tool_call 的参数，用于 miss-param 元信息
    tool_call_args = selected_tool_info['arguments']
    
    

    # 如果没有参数，就不构造 miss-param 场景
    if not isinstance(tool_call_args, dict) or not tool_call_args:
        return data

    # 3. 往前找到离这个函数最近的user message的index
    selected_turn_start = None
    for i in range(selected_tool_index, -1, -1):
        if messages[i]['role'] == 'user':
            selected_turn_start = i
            break
    if selected_turn_start is None:
        return data

    # 确定这是第几轮
    turn_number = user_positions.index(selected_turn_start)

    # 4. 确定turn结束位置
    turn_end = len(messages)
    for i in range(selected_turn_start + 1, len(messages)):
        if messages[i]['role'] == 'user':
            turn_end = i
            break

    # 5. 处理tools信息（保持与原逻辑一致）
    tools_list = json.loads(data['tools'])
    target_tool_def = None

    for tool in tools_list:
        if tool.get('type') == 'function' and tool['function']['name'] == selected_tool_name:
            target_tool_def = tool

    if target_tool_def is None:
        return data

    # 添加元信息，补充 target tool call 的参数信息
    base_mod_info = {}
    if data.get('modification_info'):
        try:
            base_mod_info = json.loads(data['modification_info'])
        except Exception:
            base_mod_info = {}
    
    base_mod_info.update({
        'modified_type': 'miss-param',
        'modified_turn_index': selected_turn_start,
        'turn_number': turn_number,
        'total_turns': len(user_positions),
        'target_tool_name': selected_tool_name,
        'target_tool_definition': target_tool_def,
        'selection_method': 'turn_biased',  # 标记使用了新的选择方法
        'target_tool_call_arguments': tool_call_args,
        'target_tool_call_index': selected_tool_index,
    })

    data['is_modified'] = True
    data['modification_info'] = json.dumps(base_mod_info, ensure_ascii=False)


    # # 6. 构造新消息序列（复用原逻辑，只在第二个 turn 使用 raw user message）
    # original_user_msg = messages[selected_turn_start]
    # new_messages = []
    # # 保留之前的消息
    # new_messages.extend(messages[:selected_turn_start])
    # # 添加第一个turn：原始 user + 缺信息的 assistant
    # new_messages.append(copy.deepcopy(original_user_msg))
    # new_messages.append({
    #     'role': 'assistant',
    #     'content': "Sorry, I don't have enough information to answer the request. I'm missing some necessary parameters to complete this task."
    # })
    # # 添加第二个turn：使用 raw user message，而不是工具说明包装
    # new_messages.append(copy.deepcopy(original_user_msg))

    # # 添加原turn中除了最初 user 消息之外的所有消息（assistant 回复、tool_call 等）
    # new_messages.extend(messages[selected_turn_start + 1:turn_end])
    # # 添加这个turn之后的所有消息
    # new_messages.extend(messages[turn_end:])

    # data['messages'] = json.dumps(new_messages, ensure_ascii=False)
    return data

# 使用示例
if __name__ == '__main__':
    # 检查两个数据集的UUID重合情况，分析miss func 和 miss param
    # 然后找到重合的UUID,把datasets1 也就是miss param里的数据剔掉
    # dataset1 = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v4')
    # dataset2 = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v1/multi-turn-miss-func-subset')
    
    # # 先查看重合情况
    # stats = find_common_uuids(dataset1, dataset2, "miss-param", "miss-func")
    # print_common_uuids_info(stats, "miss-param", "miss-func")
    
    # # 从dataset1中移除与dataset2有相同UUID的样本
    # filtered_dataset1, removed_count, common_uuids = remove_common_uuids_from_dataset(
    #     dataset1, dataset2
    # )
    
    # # 保存过滤后的数据集（可选）
    # filtered_dataset1.save_to_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v2-filtered')
    # print(f"Filtered dataset saved successfully!")
    
    #assert 0
    # 分析turns,
    # from datasets import concatenate_datasets
    # dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v2-filtered')
    # dataset1 = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v4')
    # total_dataset = concatenate_datasets([dataset,dataset1])

    # stats = analyze_modified_samples(total_dataset)
    # print_statistics(stats)
    # assert 0
    # 设置随机种子以确保可复现性
    random.seed(42)

    # 加载数据集
    dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v1/total')
    #dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/totalv3')
    print(f"Original dataset size: {len(dataset)}")
    
    raw_count = sum(1 for sample in dataset if sample.get('is_modified') is not None)
    print(f"Raw modify sample: {raw_count}")

    # filtered_dataset = dataset.shuffle(seed=42).select(range(1740))
    # filtered_dataset.save_to_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/single-turn-miss-param-subset-1740')
    # assert 0
    # step 0: 过滤部分subset == irrelevant数据
    filtered_dataset = filter_by_ratio(dataset,'subset_name','irrelevant',1)
    filtered_dataset = filtered_dataset.filter(lambda x: not x['is_modified'])
    #filtered_dataset = filtered_dataset.map(init_single_sample)
    #filtered_dataset = filtered_dataset.map(shuffle_sample_tool_list)
    print(f"Original samples: {len(dataset)}")
    print(f"filtered samples: {len(filtered_dataset)}")
    
    # Step 0.5: 提取已处理的 uuid，避免重复处理同一原始样本
    print("Step 0.5: Extracting processed uuids...")
    processed_uuids = extract_processed_uuids(filtered_dataset)
    
    # Step 0.8: 提取已处理的一批样本的uuid(一个新的dataset),添加到processed_uuids里
    print("Step 0.8: Extracting processed uuids from additional datasets...")
    additional_datasets = [
        '/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v2-filtered',
        '/data/lhy/datasets/1202/Toucan-SFT-v1/multi-turn-miss-func-subset',
        '/data/lhy/datasets/1202/Toucan-SFT-v1/single-turn-miss-func-subset'
        # 可以添加更多数据集路径
    ]
    
    for dataset_path in additional_datasets:
        try:
            additional_dataset = datasets.load_from_disk(dataset_path)
            additional_uuids = extract_processed_uuids(additional_dataset)
            processed_uuids.update(additional_uuids)
            print(f"  Loaded {len(additional_uuids)} uuids from {dataset_path}")
        except Exception as e:
            print(f"  Warning: Failed to load dataset from {dataset_path}: {e}")
    
    print(f"Found {len(processed_uuids)} already-processed original samples (by uuid)")
    
    #Step 1: 处理数据集，生成增强样本
    print("Step 1: Processing samples to create augmented data...")
    # 使用闭包传递 processed_uuids
    def process_with_uuids(data):
        return process_single_sample_v4(data, processed_uuids=processed_uuids)
    
    augmented_dataset = filtered_dataset.map(process_with_uuids)

    #augmented_dataset = filtered_dataset
    #Step 2: 筛选出被修改的样本（这些是增强数据）
    # print("Step 2: Filtering modified samples...")
    
    # modified_samples = augmented_dataset.filter(lambda x:  x['is_modified']  and json.loads(x['modification_info']).get('modified_type') == 'miss-param' and x['subset_name'] == 'multi-turn')

    # # 统计处理结果
    # print(f"augmented samples: {len(augmented_dataset)}")
    # print(f"modified samples: {len(modified_samples)}")

    # #统计修改的样本和修改的turn信息
    # print("\nAnalyzing modified samples...")
    # stats = analyze_modified_samples(modified_samples)
    # print_statistics(stats)

    # modified_samples我需要按照字段modification_info的turn_number进行filter，我想自由控制turn_number==1的数量，也就是再抽样一个子集
    #print("\nFiltering modified_samples by turn_number...")
    # 方式1: 使用max_count控制turn_number==1的数量（例如最多保留500个）
    # modified_samples, filter_stats = filter_by_turn_number_with_sampling(
    #     modified_samples, 
    #     turn_number=1, 
    #     max_count=5000,  # 最多保留500个turn_number==1的样本
    #     seed=42
    # )
    
    # 方式2: 使用sampling_ratio控制turn_number==1的比例（例如保留50%）
    # modified_samples, filter_stats = filter_by_turn_number_with_sampling(
    #     modified_samples, 
    #     turn_number=1, 
    #     sampling_ratio=0.5,  # 保留50%的turn_number==1的样本
    #     seed=42
    # )
    
    # 方式3: 不进行抽样，保留所有样本
    # modified_samples, filter_stats = filter_by_turn_number_with_sampling(
    #     modified_samples, 
    #     turn_number=1
    # )
    
    # 打印过滤后的统计信息
    # print(f"\nFilter Statistics:")
    # print(f"  Original total: {filter_stats['original_total']}")
    # print(f"  Filtered total: {filter_stats['filtered_total']}")
    # print(f"  Turn number distribution: {dict(filter_stats['turn_number_distribution'])}")
    # print(f"  Turn {filter_stats['target_turn_number']} samples: {filter_stats['target_turn_original_count']} -> {filter_stats['target_turn_filtered_count']}")
    
    #Step 3: 合并原始数据和增强数据
    print("Step 3: Concatenating original and augmented data...")
    
    from datasets import concatenate_datasets
    
    # modified_multi_turn_dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v8')
    #modified_multi_turn_dataset = modified_multi_turn_dataset.shuffle(seed=42).select(range(1000))
    modified_single_turn_dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/single-turn-miss-param')
    #modified_single_turn_dataset = modified_single_turn_dataset.shuffle(seed=42).select(range(2500))
    # miss_func_multi_turn_subset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v1/multi-turn-miss-func-subset')
    miss_func_single_turn_subset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v1/single-turn')
    
    #final_dataset = concatenate_datasets([modified_multi_turn_dataset, modified_single_turn_dataset,filtered_dataset])
    final_dataset = concatenate_datasets([modified_single_turn_dataset,filtered_dataset,miss_func_single_turn_subset])
    #final_dataset = modified_samples
    final_dataset = final_dataset.map(shuffle_sample_tool_list)
    #final_dataset = concatenate_datasets([filtered_dataset, modified_samples])

    print(f"Final dataset size: {len(final_dataset)}")

    #Step 4: fix 数据格式
    print("Step 4: Checking and fixing format...")
    formated_dataset = final_dataset.map(check_and_fix_format)

    print("Format check completed!")
    
    # 保存处理后的数据集
    formated_dataset.save_to_disk('/data/lhy/datasets/1211/Toucan-SFT')
    print("Dataset saved successfully!")
