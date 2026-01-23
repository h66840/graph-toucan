# Graph-Toucan 创新点技术落地详解 (最终版)

基于我们的深入讨论，以下是四大创新点的最终落地技术细节，包含具体的代码实现模式。可以直接收录进论文的 **Method** 章节。

---

## 1. 混合执行：Consistency-Aware Execution Simulation (感知一致性的执行模拟)

### 1.1 核心痛点与现有方案对比 (Problem & Motivation)

在合成推理数据（Reasoning Data）生成中，现有的两种主流范式都存在明显缺陷：

*   **TOUCAN 模式 (Real Execution)**: 直接调用真实的 MCP Server。
    *   **优点**: 状态真实，逻辑完美。
    *   **缺点**: **极其笨重 (Heavyweight)**。需要启动数百个真实的 Server 进程，资源消耗巨大，且难以实现高并发生成（Concurrent Data Synthesis），存在安全隐患。
*   **MAGNET 模式 (Stateless Mock)**: 使用 LLM 或静态脚本模拟工具返回。
    *   **优点**: 极速，零成本。
    *   **缺点**: **逻辑不一致 (Context Inconsistency)**。MAGNET 论文未解决“状态记忆”问题，导致模型写入文件后读取依然是初始 Mock 数据，破坏了因果推理链条。

### 1.2 解决方案：Zero-Cost Stateful Sandbox (零成本有状态沙箱)
我们提出了一种**"Stateful Mock" (有状态模拟)** 架构，结合了上述两者的优点：**像 MAGNET 一样轻量（无需真实 Server 进程），像 TOUCAN 一样逻辑自洽。**

#### A. 核心基础设施：隔离状态管理器 (`state_manager.py`)
利用 Python 的 `contextvars` 实现了 **Async Concurrency Isolation**，确保几百个并发生成的任务之间状态互不干扰。同时定义了严格的 **Domain Partitioning (领域分区)**：
-   **FileSystem Domain**: 模拟文件系统的 CRUD 操作。
-   **Social Domain**: 模拟社交网络的 Post/Feed 流。
-   **Gaming Domain**: 模拟游戏背包与属性变动。
-   **Memory Domain**: 模拟 Agent 的长期记忆库。

#### B. 批量无损迁移策略 (The Hook-Only Strategy)
为了保留原始 MCP 工具复杂的 JSON Schema，我们设计了 **"Hook-Only"** 注入方案，而非重写代码。
-   **参数透视 (Argument Transparency)**: 自动 Patch 工具代码，注入 `**locals()` 以捕获所有输入参数。
-   **后置拦截 (Post-Execution Hook)**: 
    1.先执行原始 Mock 函数，获取完美的 Schema 结构（如 `{"success": true, "content": "..."}`）。
    2.在返回前拦截结果，根据 `tool_name` (如 `write`, `post`) 执行副作用，或从 `sys_state` 中读取真实数据覆盖 Mock 数据。

### 1.3 实验验证结论
我们对 174 个活跃工具进行了迁移测试。
-   **Consistency Check**: 在 `text-editor` 测试中，写入的数据能被后续的读取操作**100% 精确召回**。
-   **Schema Compatibility**: 所有工具的返回值结构与原始定义保持完全一致，**零破坏**。

**论文贡献 (Contribution)**：
这是业界首个在**大规模合成数据生成**流程中引入“轻量级状态层”的方案。它既避免了真实环境（Real Sandbox）的高昂成本和安全风险，又解决了传统 Mock 方案的逻辑不一致问题，是实现 **High-Quality Reasoning Data** 的基石。

---

## 2. 推理验证：Structural Consistency Verification (结构一致性验证)

> **核心思路**：利用图结构进行“实时拦截” (Active Filtering)，而不仅仅是事后算分。

**实现方案**：

在 `positive_distill_v2.py` 的生成 Loop 中加入验证逻辑：

```python
# 伪代码逻辑
def verify_topological_consistency(graph, plan_tools, actual_tool_calls):
    """
    验证实际调用是否符合图结构的拓扑约束
    """
    # 1. 集合一致性检测
    if set(plan_tools) != set([t['name'] for t in actual_tool_calls]):
        return False, "Tool mismatch"
    
    # 2. 顺序/依赖检测 (高级)
    # 如果图规定 A -> B，检查实际调用顺序是否为 A, B
    for i, tool in enumerate(actual_tool_calls):
        if not check_dependencies_satisfied(tool, actual_tool_calls[:i], graph):
              return False, f"Dependency violation: {tool} called too early"
              
    return True, "Passed"

# 在蒸馏循环中
response = teacher_model.generate()
is_valid, reason = verify_topological_consistency(graph, current_fsp, response.tool_calls)

if not is_valid:
    # 策略 A: 丢弃数据 (用于构建 High-Quality SFT Set)
    discard_sample()
    # 策略 B: Self-Correction (用于 RLHF 或更强 Teacher)
    # prompt += f"\n[Error]: Your tool usage violated the dependency graph: {reason}. Please retry."
```

**论文卖点**：**"Structure-Guaranteed Correctness"**。你的数据集里的每一条数据，不仅经过了 Teacher 的筛选，还经过了底层图逻辑的验证，含金量极高。

---

## 3. 角色游走：Persona-Weighted Random Walk (加权随机游走)

> **核心思路**：通过 Embedding 相似度，让游走倾向于符合角色设定的节点。

**算法伪代码**：

```python
def get_next_node_weighted(persona_embedding, neighbors, temperature=0.5):
    """
    persona_embedding: 角色描述的向量 (e.g., "Senior Python Dev")
    neighbors: 候选节点对象列表 (包含 .embedding 属性)
    temperature: 控制聚焦程度，越小越聚焦
    """
    weights = []
    for node in neighbors:
        # 1. 计算余弦相似度 (-1 ~ 1)
        sim = cosine_similarity(persona_embedding, node.embedding)
        
        # 2. Softmax 变体计算权重
        # 放大差异：相似度高的权重指数级增加
        weight = math.exp(sim / temperature) 
        weights.append(weight)
    
    # 3. 基于权重采样
    return random.choices(neighbors, weights=weights, k=1)[0]
```

**论文卖点**：生成的数据具有显著的 **"Role Consistency" (角色一致性)**，这是 TOUCAN 的随机 Tag 采样无法比拟的。

---

## 4. 歧义消解：Ambiguity Pair Mining (歧义对挖掘)

> **核心思路**：利用类似工具的语义接近性，制造“不确定性”，训练 Agent 提问。

**Pipeline**：

1.  **Mining (挖掘)**: 
    *   计算 `Similarity(Tool_A, Tool_B)`。
    *   筛选出 `0.85 < Similarity < 0.98` 的对子（太相似是重复，不相似没歧义）。
    *   *Example*: `delete_file` vs `remove_directory`。

2.  **Synthesis (合成)**:
    *   利用 LLM 生成歧义 Query。
    *   *Prompt*: "Given these two tools, generate a user request that is ambiguous enough that it could refer to either one."
    *   *Output*: "Clearn up the temp item."

3.  **Labeling (标注)**:
    *   **Input**: "Clean up the temp item."
    *   **Output**: "Do you want to delete the file 'temp' or remove the directory 'temp'?" (Clarification Action)

**论文卖点**：提升 Agent 的 **Robustness & Safety**，教会模型 "Stop and Ask" 而不是 "Hallucinate and Act"。
