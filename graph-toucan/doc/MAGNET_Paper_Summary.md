# MAGNET: Multi-turn Tool-use Data Synthesis and Distillation

## 📄 论文基本信息

- **标题**: Magnet: Multi-turn Tool-use Data Synthesis and Distillation via Graph Translation
- **作者**: Fan Yin et al. (Google & UCLA)
- **发表时间**: 2025年3月10日
- **arXiv**: 2503.07826v1
- **代码**: 未开源（Google内部研究）

---

## 🎯 研究背景与问题

### 当前LLM在多轮工具调用中的挑战

尽管大语言模型在单轮函数调用上表现良好，但在复杂的多轮交互场景中仍然面临三大核心挑战：

#### 1. **嵌套函数调用 (Nested Function Calls)**
- **问题**: 某些操作需要多个嵌套的函数调用，但用户查询中并未明确提及
- **示例**:
  ```
  用户: "查询从旧金山到圣马特奥多少公里"
  需要: get_distance(返回miles) → convert_unit(miles→km)
  错误: 模型可能忘记调用convert_unit，直接返回miles
  ```

#### 2. **长依赖关系 (Long Dependency)**
- **问题**: 某些turn需要从对话历史中获取信息来组合函数调用
- **示例**:
  ```
  Turn 1: book_flight() → 返回booking_id=3426812
  Turn 4: "取消我的纽约行程"
  需要: cancel_booking(booking_id=3426812)  # 从Turn 1获取
  错误: 模型忘记booking_id，要求用户提供
  ```

#### 3. **信息缺失 (Irrelevance)**
- **问题**: 某些turn缺少必要的功能或参数值，需要澄清
- **示例**:
  ```
  用户: "获取我最近预订的发票"
  问题: 没有提供retrieve_invoice函数 或 缺少access_token
  正确: 模型应该询问："我没有获取发票的功能"
  ```

### 现状数据

- BFCL-v3基准测试中：
  - 最佳专有模型在多轮场景：**47.62%** 成功率
  - 部分公开模型：仅约 **10%** 成功率
- 缺乏高质量的多轮训练数据

---

## 🔬 核心方法：MAGNET框架

**MAGNET** = **M**ulti-turn function-c**A**lling data synthesis with **G**raph Tra**N**slation

### 整体Pipeline

```
① 函数收集          ② 构建依赖图        ③ 生成FSP           ④ 节点操作
  (5,011个)         (局部依赖图)      (随机游走)        (Insert/Merge/Split)
     ↓                  ↓                 ↓                  ↓
[函数池]  →  [函数关系图]  →  [初始路径]  →  [增强路径]
                                                            ↓
⑤ Back-and-Forth Translation  ←  [查询-函数对]
         ↓
⑥ Context Distillation
   ├─ 正向轨迹 (正确hints)
   └─ 负向轨迹 (错误hints)
         ↓
⑦ 训练数据
   ├─ SFT: 34,000条
   └─ mDPO: 4,556对
```

---

## 🗺️ 技术细节

### 1. 局部依赖图 (Local Dependency Graph)

#### 定义
为每个函数构建一个包含相关邻居的有向图：
- **节点**: 函数
- **边**: 当源函数的输出与目标函数的输入相关时建立有向边
- **局部性**: 每个函数只关注30个同类别的候选邻居

#### 依赖关系判断标准

两个函数存在依赖关系，当满足以下任一条件：

1. **输出作为前提**
   ```
   file_exists('file.txt') → download_file('file.txt')
   前者的结果决定是否能执行后者
   ```

2. **输出即输入**
   ```
   get_radius(obj) → calculate_area(radius)
   前者的输出正是后者需要的参数
   ```

3. **输出为部分参数**
   ```
   get_content('file.txt') → post_to_social(content, id, tags)
   前者的输出是后者的部分输入
   ```

#### 构建过程

```python
for 每个函数 vi:
    # 1. 采样候选邻居
    candidates = random_sample(
        same_category_and_class(vi),
        n=30
    )

    # 2. 使用LLM判断依赖关系
    for candidate in candidates:
        if llm_judge_dependency(vi, candidate):
            add_edge(vi, candidate)
```

#### 实际例子

```
旅行预订场景的依赖图：

cities_by_range ──→ get_distance ──→ set_navigation
                         ↓
                    convert_unit

依赖关系：
- get_distance输出distance → set_navigation需要distance
- get_distance输出miles → convert_unit转换单位
- get_distance输出distance → cities_by_range用于查找范围内城市
```

---

### 2. 函数签名路径 (FSP) 生成

#### 初始FSP：随机游走

```python
# 从依赖图中采样函数序列
start_node = random_choice(all_functions)
fsp = [start_node]

for step in range(7):  # 游走7步
    # 从当前节点的邻居中随机选择
    next_node = random_choice(current_node.neighbors)
    fsp.append(next_node)

# 初始FSP: φ̃ = (f̃₁, f̃₂, f̃₃, f̃₄, f̃₅, f̃₆, f̃₇)
# 特点：每个turn只包含1个函数
```

**关键点**：
- 每一步 = 一个turn
- 每个turn初始只有1个函数
- 沿着依赖边游走，确保函数相关性

---

### 3. 节点操作 (Node Operations)

将简单的初始FSP增强为能覆盖三大挑战的复杂FSP。

#### Node OP #1: Insert（解决嵌套调用）

**目的**: 添加隐式需要但用户未明确提及的函数

**实现**:
```python
for each turn in FSP:
    last_func = turn[-1]

    # 检查邻居中是否有嵌套函数
    for neighbor in last_func.neighbors:
        if is_nested(last_func, neighbor):
            # 方式A: 添加到当前turn（短依赖）
            turn.append(neighbor)

            # 方式B: 插入到后续turn（长依赖）
            random_later_turn.append(neighbor)
```

**嵌套判断标准** (使用LLM):
- 第二个函数的参数值可从第一个函数输出获得
- 第二个函数在查询中**未被明确提到**

**示例**:
```
查询: "查询从SF到SM多少公里"

初始FSP:
Turn 1: [get_distance]

应用Insert后:
Turn 1: [get_distance, convert_unit]
        ↓              ↓
      返回miles    miles→km
```

#### Node OP #2: Merge（解决显式多意图）

**目的**: 创建单轮中包含多个相关函数调用的场景

**实现**:
```python
for each two consecutive turns (f̃_h, f̃_{h+1}):
    if random() < 0.3:  # 30%概率
        # 合并成一个turn
        f_h = (f̃_h, f̃_{h+1})
```

**示例**:
```
查询: "查询SF到SM的距离，并用这个距离设置导航"

初始FSP:
Turn 1: [get_distance]
Turn 2: [set_navigation]

应用Merge后:
Turn 1: [get_distance, set_navigation]
```

**Merge vs. Insert 对比**:

| 特性 | Insert | Merge |
|------|--------|-------|
| 用户意图 | 单一目标 | 多个目标 |
| 第二个函数 | 隐式需要 | 显式提到 |
| 查询示例 | "查公里数" | "查距离**并且**设置导航" |

#### Node OP #3: Split（解决信息缺失）

**目的**: 创建缺少功能或参数的场景，模型需要澄清

**实现**:
```python
# 随机选择一个turn
turn_h = random_choice(FSP)

# 分裂成两个turn，中间插入空turn
f_h = turn_h
f_{h+1} = {}  # 空节点，标记为'miss_func'或'miss_params'
f_{h+2} = turn_{h+1}
```

**示例**:
```
Turn 4: 正常函数调用
Turn 5: {} 标记为'miss_func'  # 缺少retrieve_invoice函数
Turn 6: 正常函数调用

模型应该输出:
"我没有获取发票的功能，请确认..."
```

#### 操作顺序

```python
# 1. 先Merge（改变turn数量）
φ = apply_merge(φ̃, p=0.3)

# 2. 再Insert（在turn内添加函数）
φ = apply_insert(φ)

# 3. 最后Split（创建缺失场景）
φ̂ = apply_split(φ)
```

---

### 4. Back-and-Forth Translation

将增强的FSP转换为可执行的查询-函数对。

#### 迭代翻译过程

```
For each turn h in FSP:

Step 1: Back-translation (函数→查询)
---------------------------------------
输入: f_h = (func1, func2, ...)
输出: q_h = "用户查询文本"

使用LLM将函数签名转换为自然语言查询

Step 2: Forth-translation (查询→可执行函数)
---------------------------------------
输入: q_h, f_h, t_{h-1} (���一轮的输出)
输出: fc_h = "func1(arg1=val1, ...), func2(...)"

填充函数参数，确保：
- 所有必需参数都有值
- 参数值来自查询或上一轮输出
- 保持函数间依赖关系

Step 3: 执行函数获取输出
---------------------------------------
执行fc_h，获得t_h (函数输出)
```

#### 示例

```
Turn 1:
-------
FSP: [get_flight_cost, book_flight]

Back-translation:
q₁ = "预订从LA到NYC的商务舱航班，用card_123支付"

Forth-translation:
fc₁ = [
  get_flight_cost(from='LAX', to='JFK', class='business'),
  book_flight(cost=<从get_flight_cost获得>, card='card_123')
]

Execution:
t₁ = {"booking_id": "3426812", "status": true}

Turn 2:
-------
FSP: [send_message]

Back-translation:
q₂ = "告诉我朋友Joey我要去NYC"

Forth-translation:
fc₂ = [send_message(to='Joey', msg='Going to NYC...')]
```

---

### 5. Context Distillation（上下文蒸馏）

使用教师模型（Gemini-1.5-pro-002）生成正向和负向轨迹。

#### 正向轨迹（Positive Trajectories）

**目的**: 生成高质量的训练数据

**方法**: 添加正确的函数调用作为hints

```
系统提示 + 详细指令:
"你是函数调用专家..."
"以下是每个查询的[Hint]，请根据hints生成响应，但不要明确提到hint..."

用户查询 + [Hint]:
"预订航班..."
[Hint]: get_flight_cost(...), book_flight(...)

教师模型生成:
→ 完整的reasoning + 函数调用 + 结果总结
```

**关键**:
- Hints确保教师模型生成正确的函数调用
- 模型不会在响应中提到hint的存在
- 提高正向轨迹的质量和一致性

#### 负向轨迹（Negative Trajectories）

**目的**: 用于偏好优化（mDPO）

**方法**: 使用SFT模型的错误作为负向hints

```python
# 1. 收集SFT模型的错误
for each data instance:
    # 生成10条轨迹
    trajectories = sft_model.generate(query, n=10)

    # 2. 使用LLM判断器识别错误
    for turn in trajectory:
        error_type = llm_judge_error(
            turn,
            reference,
            error_types=[
                "nested_missing",
                "short_dependency",
                "long_dependency",
                "wrong_summary",
                "miss_func_or_params"
            ]
        )

        if error_type:
            wrong_hints.append(turn)

# 3. 使用错误hints生成负向轨迹
negative_trajectory = teacher_model.generate(
    query,
    hints=wrong_hints,  # 故意给错误的hints
    instruction="general"  # 使用更通用的指令
)
```

**错误类型**:
1. 嵌套函数缺失
2. 短依赖错误（turn内函数输出未正确使用）
3. 长依赖错误（未使用历史信息）
4. 错误总结（幻觉或遗漏信息）
5. 缺失函数/参数

---

### 6. 数据混合策略

#### 训练数据组成

| 类别 | SFT数量 | mDPO数量 | 说明 |
|------|---------|----------|------|
| 单轮 | 20,000 | 1,556 | 预热模型基础能力 |
| 多轮 | 7,800 | 2,250 | 核心训练数据 |
| 无关 | 6,200 | 750 | 检测能力训练 |
| **总计** | **34,000** | **4,556** | - |

#### 单轮数据类型

1. **Single**: 一个函数调用
2. **Parallel**: 同一函数，不同参数
3. **Multiple**: 多个相关函数（通过Merge生成）

#### 多轮数据统计

- 平均轮数: **4.71** turns
- 平均函数调用数: **15.13** 个
- 每turn平均: **3.2** 个函数

#### 最佳数据混合比例

通过消融实验发现：
- 单轮: 多轮: 无关 ≈ **59%: 23%: 18%**
- 无关数据在**15-17%**时平衡最好

```
无关数据过少 → 模型容易幻觉
无关数据过多 → 多轮性能下降
```

---

## 📊 实验结果

### BFCL-v3 基准测试

| 模型 | Overall | Multi-turn | 提升 |
|------|---------|------------|------|
| Qwen2.5-Coder-14B-Instruct | 51.88 | 5.38 | baseline |
| **MAGNET-14B-SFT** | 66.83 | 33.38 | **+28.0** |
| **MAGNET-14B-mDPO** | **68.01** | **37.88** | **+32.5** |
| Gemini-1.5-Pro-002 (教师) | 62.19 | 20.75 | 被学生超越 |
| GPT-4o | 69.58 | 41.00 | - |
| 排行榜第1名 | 74.31 | 58.75 | - |

**关键发现**:
- ✅ 多轮场景提升 **32.5个百分点**
- ✅ 超越教师模型Gemini-1.5-pro-002
- ✅ 排名第4（在所有模型中）
- ✅ 最佳开源模型

### ToolQuery 基准测试

| 模型 | Success Rate | Progress Rate |
|------|--------------|---------------|
| GPT-4o | 63.3 | 80.1 |
| Gemini-1.5-Pro-002 | 68.3 | 74.6 |
| xLAM-8x22b-r | 68.3 | 75.8 |
| **MAGNET-14B-mDPO** | **73.3** | **78.7** |

**零样本泛化**: ToolQuery的所有函数在训练集中**未见过**！

---

## 🔍 消融实验

### 1. Pipeline组件的贡献

| 配置 | Overall | Multi-turn | 提升 |
|------|---------|------------|------|
| Base Model | 51.88 | 5.38 | - |
| + Init Graph | 58.54 | 12.75 | +7.37 |
| + Merge | 60.83 | 20.63 | +7.88 |
| + Insert | 64.39 | 29.25 | +8.62 |
| + Split | 66.83 | 33.38 | +4.13 |
| + Context Distillation (Positive) | 66.83 | 33.38 | (必需) |
| + Context Distillation (Negative) | **68.01** | **37.88** | +4.50 |

**结论**: 每个组件都有显著贡献！

### 2. 与其他公开数据对比

| 训练数据 | Multi-turn | 数据量 |
|----------|------------|--------|
| APIGen + ToolAce | 7.13 | ~60k |
| Hammer2.1 | 23.50 | ~67k |
| **MAGNET** | **26.50** | **34k** |

**结论**: MAGNET用更少数据达到更好效果！

### 3. 泛化到不同基座模型

| 基座模型 | 原始 | +MAGNET | 提升 |
|----------|------|---------|------|
| Qwen2.5-Coder-7B | 8.25 | 26.50 | +18.25 |
| Qwen2.5-14B-Instruct | 7.25 | 21.12 | +13.87 |
| Mixtral-8x7B | 0.50 | 19.75 | +19.25 |

**结论**: 方法对不同基座模型都有效！

### 4. 不同教师模型

| 教师模型 | Multi-turn |
|----------|------------|
| Gemini-1.5-Pro-002 | 33.38 |
| GPT-4o | 30.88 |
| Qwen2.5-Coder-14B (self-improve) | 27.12 |

**结论**:
- Gemini和GPT-4o效果相当
- **自我改进也可行**（使用自己作为教师）

---

## 💡 核心洞察

### 1. 图视角的创新

**传统方法**: 随机采样同领域函数
```
❌ 函数之间缺乏明确关系
❌ 生成的序列不自然
```

**MAGNET方法**: 基于依赖图的有向采样
```
✅ 函数之间有输入-输出依赖
✅ 沿着依赖边游走，序列更合理
✅ 三种节点操作系统化地增加复杂度
```

### 2. Context Distillation的妙用

**挑战**: 教师模型在多轮场景也会出错

**解决**:
- 正向hints: 确保教师模型生成正确轨迹
- 负向hints: 利用学生模型的错误，创建对比数据
- 结果: 学生模型超越教师模型！

### 3. 节点操作的系统化

| 操作 | 挑战 | 解决方案 | 效果 |
|------|------|----------|------|
| Insert | 嵌套调用 | 添加隐式函数 | +8.62 |
| Merge | 多意图 | 合并turn | +7.88 |
| Split | 信息缺失 | 创建空节点 | +4.13 |

每个操作对应一类真实错误！

### 4. 数据效率

- MAGNET: **34K** 数据 → **26.50** 多轮性能
- APIGen+ToolAce: **60K** 数据 → **7.13** 多轮性能

**4倍数据效率提升**！

### 5. 零样本泛化能力

- BFCL-v3: 函数有重叠（但重写了名称）
- ToolQuery: 函数完全未见过
- 结果: ToolQuery上仍达到**73.3%**成功率

说明模型学到的是**函数调用的能力**，而非记忆特定函数。

---

## 🎯 方法论总结

### Pipeline的精妙设计

```
简单起点 → 系统增强 → 高质量蒸馏
    ↓           ↓           ↓
随机游走    节点操作    上下文提示
  ↓           ↓           ↓
相关序列    覆盖挑战    正负对比
```

### 三个关键创新

1. **图结构建模**: 用依赖图组织函数关系
2. **节点操作**: 系统化地创建复杂场景
3. **双向蒸馏**: 正负hints确保质量和对比

### 可复现的关键要素

如果要复现或改进此工作：

1. **函数池**: 收集可执行的函数（5K+）
2. **依赖判断器**: 用LLM判断函数间依赖（30邻居/函数）
3. **节点操作**: 实现Insert/Merge/Split
4. **翻译模型**: 用于back-and-forth translation
5. **教师模型**: Gemini/GPT-4级别的强模型
6. **判断器**: 用于识别SFT模型的错误类型

---

## 🚀 未来方向

### 论文提到的局限

1. **多语言和多模态**: 当前只支持英文文本函数
2. **知识冲突**: 工具输出与模型内部知识冲突时的处理
3. **探索能力**: 缺少反思和重新探索的能力

### 可能的改进方向

1. **更复杂的图结构**:
   - 全局依赖图（跨领域）
   - 多跳依赖关系

2. **更多节点操作**:
   - Replace: 替换错误函数
   - Reorder: 调整函数顺序

3. **动态难度控制**:
   - 根据模型能力调整FSP复杂度
   - 主动学习选择困难样本

4. **多教师蒸馏**:
   - 集成多个教师模型的优点
   - 不同模型擅长不同类型的函数

5. **强化学习**:
   - 用RL进一步优化函数选择
   - 在真实环境中在线学习

---

## 📚 相关工作对比

| 工作 | 核心思路 | 数据量 | 多轮性能 |
|------|----------|--------|----------|
| ToolFormer | 文本中插入API调用 | - | - |
| APIGen | 从API生成查询 | 60K | 低 |
| ToolLLM | 16K真实API | 大规模 | 中 |
| Hammer | 函数mask + 无关函数 | 67K | 23.50 |
| **MAGNET** | **图翻译 + 节点操作** | **34K** | **26.50** |

---

## 🏆 贡献总结

1. **理论贡献**:
   - 提出基于图的多轮函数调用数据合成框架
   - 定义三种节点操作覆盖多轮挑战
   - 双向上下文蒸馏技术

2. **实践贡献**:
   - 14B模型达到BFCL-v3排行榜第4名
   - 超越教师模型Gemini-1.5-Pro
   - ToolQuery零样本泛化达到73.3%

3. **开源贡献**:
   - 详细的方法论和实验设计
   - 完整的prompts（Appendix A）
   - 可复现的pipeline

---

## 📖 关键术语表

- **FSP**: Function Signature Path，函数签名路径
- **Node Operations**: 节点操作（Insert/Merge/Split）
- **Context Distillation**: 上下文蒸馏
- **Back-and-Forth Translation**: 双向翻译
- **Local Dependency Graph**: 局部依赖图
- **mDPO**: Multi-turn Direct Preference Optimization
- **Nested FC**: 嵌套函数调用
- **Long Dependency**: 长依赖关系

---

## 🔗 资源链接

- arXiv: https://arxiv.org/abs/2503.07826
- BFCL-v3: https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html
- Qwen2.5-Coder: https://github.com/QwenLM/Qwen2.5-Coder

---

*总结完成时间: 2026-01-07*
*总结者: Claude Sonnet 4.5*
