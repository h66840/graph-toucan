基于toucan和magnet，这就是工作量。参考GitHub repo： 1、toucan的开源项目 2、（待定）graph-toucan的代码
理想情况下我需要的，把datasets和模型挂在hugging face上，把graph-toucan这个项目直接传到GitHub上（去除APIKEY后）。然后回去补充实验，
toucan是一个大规模的tool use的数据集，magnet是一个用graph合成tool use数据的系统。
我的创新点1:
我们把toucan复现了，然后针对其在bfcl上miss info情况下的表现不佳的情况，我们合成了一批拒绝策略的数据，并且在其余指标不掉的情况下提升了miss info的指标。
QA:
对于miss func的情况，是怎么合成数据的？
对于miss params的情况，是怎么合成数据的？
训练框架用的是什么？
合成了多少条数据？
创新点2:
toucan的数据依赖于调用真实MCP合成数据，很费钱，而且依赖于random select，此处要解释toucan生成数据集的流程。并且toucan数据集的multi-turn数据质量低，此处分析toucan的多轮对话数据集的avg turns, per turns avg steps，avg turn tool call counts，这三个指标。因此我们想在保留真实MCP tool的前提下，合成一批比toucan的多轮对话数据质量更高的数据。此处介绍一些数据合成的办法，比如APIGEN，在magnet论文里提到的一些数据合成方法。然后介绍我们的数据合成系统：
QA：
为什么要做一个数据合成的系统？
解决多轮对话数据质量不高的问题，并且更加方便（不需要调用真实的MCP）
这个数据合成系统A相比于APIGEN、TOUCAN的优点在哪？
相比于这两个系统，A更有可解释性，因为它是基于图游走的方法，每条轨迹的生成都依赖于一条可以解释的节点游走路径。A生成的数据的复杂度更高，可以在生成的节点游走路径上使用各种自定义的操作，来模拟多轮对话中存在的并行调用、长短依赖、信息缺失的真实情况。
解释一下系统的细节？

是不是要补充实验？应该就是去t-bench上跑一下，
论文结构是啥？
如果是小论文的话：
1、introduction
2、related work
3、your method
4、experiment
5、conclusion and future work
magnet和toucan的结构都是这样的
我的思路：先基于这两篇论文写出来两个结构，然后把它们合在一起
1、introduction
写大语言模型的发展现状，现在agent的作用，尤其是Claude code。写这些agent是怎么被训练出来的，参考kimi和glm的技术报告，肯定是用大规模的agentic数据做了增量训练，因此如果想激发开源模型的agentic潜能，就离不开高质量、大规模的agentic数据。写一下agentic数据和tool use数据的关系，然后引到我的工作重点（tool use）。
写一下什么是tool use数据，参考bfcl benchmark。agentic数据可以由几类构成，single turn数据、multi-turn数据。
single turn数据又可以拆分为single step数据、multi step数据。写一下这三种模式的定义，参考bfcl blog。其中single step数据我理解的是用来做warm up模型的function call能力，这是最基础的tool call能力。multi step数据表示模型把一个large task逐步拆分为atomic task，展示模型的planning能力。multi-turn数据模拟了真实情况下用户和模型进行back and forth的交互流程。

写当前仍缺少一种scalable、open-source、high-quality的datasets.能够针对这三种情况合成高质量的数据。写一些开源的tool use数据集，要找一种指标表示我的数据集比它们的都好。（这也是个工作量。）对比Toucan、APIGen、ToolACE、action98k,先就这四个数据集吧，我觉得要对比的指标就是 single turn 数据量，multi turn数据量，single turn数据的avg tool calls，avg steps、
multi turn数据的avg steps，avg tool calls。
需要搞一个表。
然后介绍一下数据来源，因为我的数据来源于Toucan和合成数据，可以说来自两个scenario，一个来自于smithery上真实的MCP，吹一下Toucan github上的MCP种类和数量，水字数的话可以介绍下MCP。因为原来也做过类似的工作，可以说一下来自real MCP的数据合成pipeline（随机采样MCP，再随机采样MCP里的函数，给Gemini2.5-pro生成query，然后给Claude-4-sonnet连上真实MCP采样轨迹。然后用trl做训练，当然这是我的流程，不等同于toucan）

2、related work
这个直接抄吧，写一些benchmark和datasets，bfcl t-bench 、开源tool use数据集
3、method
3.1 data generation pipeline
这部分感觉要缝合toucan和magnet的工作，先说从smithery上选了几百个高质量的MCP server，（感觉可以抄一下toucan的repo，把它的MCP info抄过来），可以说用python把smithery ai的mcp都爬下来了，然后做一波数据分析，别和toucan一样比较好。然后就是对MCP过滤，需要第三方认证的都过滤，最后保留的是可以remote和stdio的。准备从tool的角度来写，假设得到M个mcp servers,N个tools，每个MCP servers在smithery上有一个tag，最后得到K个tag。然后给这N个tools用大模型进行打标，每个tool上打3个tag。
最后得到的数据结构：
tools list:[{toolA:[{function_schema,tags}]}],然后合成query的阶段，每次指定生成query时必须要参考N个tools（这N个tools是一个neighbor的），neighbor的逻辑是两个tools至少有一个tag是重合的。N的数量从1～3不等。然后再实际合成query的时候会把每个tools对应的MCP里的tool list给LLM，让其随机参考M个MCP server tool list的tools。最后生成一个query，目标是能调用M+N个tools。
最后得到A个QA对，[query,target_tool_list],都是single turn multi-step data 或者single turn single-step data。
然后使用langgraph构建一个rollout流程，实际跑A条数据，得到A个trajecotry。然后可以说借鉴toucan的生成多轮对话数据的方法，生成了B条multi-turn traj。开源分析一波这种数据的缺点，从上文里提到的指标，这其实就是toucan里multi-turn类型的数据。
然后指出这个数据的缺点是缺少拒绝样本。
先增加miss-info类型的数据，对于miss func类型的数据，算法是找到每个在轨迹中用到的tools第一次出现的位置，得到一个集合，然后随机抽样一个tool，从这个集合里选到tool index,然后映射到对应的turn index，然后把这个tool从tool schema里mask掉，修改这个turn index的回答，让其输出拒绝原因，然后插入一个QA，Q是提供这个函数的schema。相当于从原来的QA in turn A，变成了 Q A1 Q1 A。
对于miss params类型的数据，首先对multi turn的数据进行打标，抽样出一批数据需要进行数据增强，然后对找到要改的turn的query，重写它让他缺少调用目标函数的必要信息，得到Q1，然后重写这个answer，让其解释为什么不能调用，然后加一个Q2，去补充这个缺失的参数信息，然后正常继续调用。从[Q,A] -> [Q1,A1,Q2,A]。
然后缝合magnet，增加multi-turn类型的数据，说一波它的multi-turn数据仍然有缺陷，我们参考了magnet,environment scaling，t-bench，做了一个新的数据生成方法。仍然保留以tool为最小atomic 单位的做法，并且沿用之间已经构建的tool relationship关系图。
我们based on LLM judge的方法，对于两个tool(toolA 和 toolB)，如果tool A的输出能够作为toolB的部分输入，完整输入，作为其前提，举几个例子，那么可以构建有向边(A -> B)。
数据预处理
因为MCP里的真实tools很多情况下都只有tool input params，而没有tool output schema，所以我们基于方法1合成得来的数据(data1)，对每个tool选择3~4个实际调用的example，该example来源于data1，并且有tool的调用，让llm based on these example design tool output schema（并且忽略掉从input schema field 传递而来的output schema field）。得到tools_output_schema作为前置条件。
并且依赖于之前已经得到的tool_classification_result，同样作为前置条件。最后取这两个tool集合的交集，得到最终用来建立图的所有tool节点。
建图算法：
Step1: 输出参数过滤
过滤规则：1、输出参数名称==输入参数名称，直接过滤 2、输出参数描述和输入参数描述的语义完全相同，过滤（LLM判断）
做这个过滤的原因是如果function A(userId) -> (userId), function B(userId),那么如果建立了a->b，那么说明调a的时候同时可以调b。
Step2: 边判断
使用LLM作为判断器，分析是否应该建立有向边node -> candidate。依赖类型判断：
依赖类型 描述 示例
full node输出可以作为candidate的完整输入 get_user_info ->(id,name) <br> send_email(id,name,msg)
partial node输出可作为candidate的部分输入 get_file_path ->(path) <br> read_file(path,encoding)
prerequisite node输出决定是否应该调用candidate check_file_exists -> (exists) <br> download_file(url)
none 无依赖关系
需要补充prompt在附录。
得到了工具依赖图后，接着实现基于工具依赖图的随机游走算法 + 数据增强动作，用来生成多样化的函数调用路径。
1、以每个节点为起点，设置max_steps(最大游走次数)，采样出DAG
2、对单节点进行多次的路径游走，然后对路径进行去重
3、对全图进行遍历，得到初始的函数调用路径(FSP path list)，结构为(每个turn一个节点)，相当于每一轮对话只有一个函数调用意图
4、设计数据增强操作，merge、split、nested，目的是合成具有依赖关系并且多函数意图的数据
merge操作：合并连续turn，turn1(func1) -> turn2(func2), 得到turn(func1,func2)，模拟单论对话包含多个函数调用的场景。
apply_merge_option(fsp,merge_prob)
输入FSP
    turn0:[get_distance]
    turn1:[set_navigation]
输出FSP
    turn0:[get_distance,set_navigation]
insert操作：创建有依赖关系的函数调用场景
short dependency:同一个turn中的[funcA,funcB]存在数据依赖，
long dependency：跨turn之间存在数据依赖[funcA] [funcB]
split操作：创建缺失信息，模型应该拒绝回答的场景
turn1[],此时模型应当表示拒绝调用的意图，因为缺失了信息
整体流程：
graph
    A[加载工具依赖图] -->B[随机游走生成路径]
    B -->C[路径去重]
    C -->D[初始FSP]
    D -->E[FSP数据增强]
    E -->E1[Merge:合并连续turn]
    E -->E2[Insert:创建数据依赖场景]
    E -->E3[Split:创建信息缺失场景]
    E -->F[保存Json]

模拟数据执行环境
1、首先对tool进行分类(computation、query、action),让大模型进行分类
    1.computation:不依赖外部信息源，只依赖tool的参数并且执行函数内部运算逻辑，例如计算器，单位转换，解析json
    2.query：依赖外部信息源检索数据，从外部系统读取数据但是不修改外部状态，例如：搜索数据库，抓取天气信息，检索文件内容
    3.action：依赖外部信息源，并且执行该工具会修改外部状态，比如创建文件（修改文件系统），执行脚本
<tool类型分类结果分析>
2、把tool从tool with input output schema translate into python code format
对于computation类型的tool，使用函数的input output params实现纯计算逻辑，不允许出现额外的API call和网络请求。
对于query和action类型的tool，创建一个额外的helper函数<call_external_api(tool_name:str) -> Dict[str,Any]>返回来自外部信息源的数据，并且这个函数只能返回被flat后的simple字段(str,int,bool,float),不允许返回nested结构的字段。
    定义<call_external_api>
    对output schema的复杂嵌套结构字段进行展平，比如对于nested object:user.name -> user_name，对于list or array:
    items[].name -> item_0_name and item_1_name
    每个被flat后的字段只能是str int float bool
    每个call_external_api函数的入参事tool_name，返回一个dict contain flatted field，对于list/array fields，使用indexed field name eg.item_0_name item_1_name，对于list fields，generate 2items for a list。
    document all fields in the function docstring.
    定义<main_function>
    调用call_external_api to get external data，write code to construct nested complex structure,把从<call_external_api>得到的flat field 在主函数里reconstruct为nested structure，对应于output schema，
    包含错误处理和input参数校验
<python code>
下一步是对生成的FSP做后向-前向翻译算法，用来从FSP -> query。
对于每个FSP，检测FSP的每个turn的类型，
<detect turn type>
turn定义了6种类型：
normal |没有进行任何变换操作 | 根据turn的函数生成满足调用函数的请求
empty | 进行了split操作 | 生成无法满足本轮函数调用条件的请求
merge | 进行了merge操作 | 生成多意图请求
insert short dependency | 这个turn内insert了函数 | 只提最终目标
insert long dependency | 跨turn引用了历史 | query需要进行代词引用,用that distance指代上文提到的25.4km
insert mixed | 同时用long / short dependency
merge with insert | 混合 | 多意图并行+代词引用/隐式helper函数
<build prompt for turn>
对每种turn类型构建prompt，
You are a role-playing as a user in a multi-turn conversation with a function-calling agent.This is Turn {turn_idx}.
empty turn prompt:
     The use will make a request, but there is NO suitable function available to fulfill it, or the request is missing critical parameters.
     You must generate the user query in English, regardless of function names or descritions.
    {error_feedback_prompt}
    {history_block}
    {last_round_block}
    Your task:
    Generate a natural user query that woould require a function that doesn't exist, or that is missing critical information.
merged turn prompt:
    This is a MERGED scenario where you express multiple lintents in a single query.
    MERGED Definition:
    Multiple functions in the SAME turn with potential SHORT DEPENDENCY.
    Output of one function may feed as input to the next (within same turn)
    User EXPLICITLY mentions ALL actions/intents (unlike insert where some are implicit)
    Use connecting words to link multiple intents: "and","then"...
    ** All functions to call** (turn_functions)
    You must generate the user query in English, regardless of function names or descritions.
    {error_feedback_prompt}
    {history_block}
    {last_round_block}
    CRITIAL Instructions
    1.Explicitly mention all {len(turn_functions)} intents/actions in your query.
    2.Use connecting words: and, then,after that
    3.Make the data flow clear in function has dependency
    4.Each function should be reflected in the query
    5.Natural combination of multiple explicit intents
    Contrast with insert short:
    insert short: Navigate to San Mateo(only final goal,distance is implicit)
    merged: Find the distance to San mateo and set up navigation(both are explicit)
    # 不同query的风格instruction
    {style_instruction}
    # 少样本
    {examples_block}
    Candidate Functions:
    # 这一轮的候选函数文档
    {candidate_block}    
merge with insert prompt:
    This is a Merge + Insert scenario with multiple types of functions.
    Function Classification
    MERGED function (explicit intents){merged_funcs_str}
    LONG-DEPENDENCY functions (explicit,reference history){log_dep_funcs_str}:
    SHORT-DEPENDENCY helpers (imolicit, do NOT mention)
    **ALL functions call

    <dependency info>
    short dependency info:
        {source_func} -> {target_func}
        {source_func} output:
        {target_func} input schema,see params in Candidate functions below
    long dependency info:
        Turn {dependency['source_turn']}: <source_func> -> Turn {dependency['target_turn']}:
        {target_func}
        {source_func} output:
        {target_func} input:
    
    {dependency_info}
    {history_block}
    {last_round_block}
    CRITIAL INSTRUCTION
    MERGED functions: Express threse explicit intents clearly
    Long-dependency functions
        -Express these intents BUT use pronous to reference previous outputs
        -DO NOT repeat specific values from history
        -Understand the cross-turn data flow

...每种类型都有对应的prompt，再构建完毕后，call llm 得到query result
接下来顺序执行这一轮的函数，首先要拿到这一轮的query和turn functions，因为没有构建并行调用的函数，所以执行顺序就是按照顺序（nested函数一定在primary函数后面）。
    for func in execution_order:
        # generate param for each function
        param_result = generate_single_func_params(turn_qery,function_name,context,tool_schemas)
        # generate_single_func_params的逻辑，要求llm输出每个参数值的来源，context or query。
        如果不能找到，拒绝填参数。
        # execute function
        exec_result = execute_function_call(function_name,param_result,tool_schema)
        # execution逻辑
        首先判断当前函数是否依赖外部信息，也就是有没有call_external_api函数，如果有的话，
        先执行simulate_call_external_api函数，得到simulate_result。
        simulate_call_external_api的逻辑，给这个函数的主函数，以及call_external_api函数的docstring，让llm 模拟其输出。
        然后把函数代码里的call_external_api也就是placeholder，动态替换成另一个函数mock_api，它直接return这个simulate_result。然后运行这个函数，函数运行完毕后再替换回来。
        turn_output.append(exec_result)
    这个forward过程模拟了single turn的函数执行情况，假设函数调用顺序是funcA -> funcB,funcB调用的时候能看见funcA的调用历史。
    然后外层的循环处理每个turn，整体逻辑是
        for single_turn in turns:
            detect_turn_type
            construct_turn_prompt_for_each_turn
            generate_each_turn_query
            forward_to_turn_params(里面有single turn的循环)
    
    这是整体造数据的过程。


然后要对这些数据做数据分析，感觉后面对toucan的数据做个分析

做实验的部分
补充实验，现在只有bfcl，补充一个t-bench，一个