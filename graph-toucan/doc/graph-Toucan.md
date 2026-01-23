1 we need analysis Toucan tool schema, we need this ,and need category ,we can
  use mcp to be category. and we can get real category and real edge ,it is
from the real data tool call chain. so we can use the Toucan data to construct
a graph A as our baseline.
2 for the diversity, we can use cos similarity to add edges(env scale) and use magnet
  method (random select some node within same domain as candidate ,and use llm
to construct edge.) 
after we get initial graph, we can use random walker to get func call path.
and convert fcp into traj. but it need tool result,
how can we get tool result?
truly execuate python code.
use a dataset, use logic convert all func to read/write operation

version 0.0.1
以函数为节点，对函数A先抽样一个子集合，在子集合里和函数A做判断，函数A的输出是否能作为函数B（func in subset）的输入或者前置依赖。
建完图后，假设用magnet的方法，采出一条FSP（funcA -> funcB -funcC），funA属于stateful MCP，则其有状态，funcB,funcC无状态则直接变成python code。而funcA是一个类的函数，并且有对应的database。
对函数A抽样一个子集合的方法：
1、random sample
2、根据toolA 和 toolB的parameters的余弦相似度
3、先让llm 给每个func打1～3个label，如果funcA和funcB的label有一个重合，作为edge的候选。

version 0.0.2
现在改变了策略，需要根据toucan原始数据以及建的图进行比较，首先要证明toucan原始数据提取出来的tool call chain，在我们建的图上是联通的，或者在我们的图上判断是否是一个DAG。
那么我今天干了一些事情，1是首先我过滤了toucan single turn original的数据，我把single turn and no parallel的数据过滤掉了，这种数据在图上就是一个点。
然后为了控制成本，在过滤后的数据上统计了出现次数大于sample 数量 1%的mcp，我们把这些mcp称为常用的mcp，并且我们进一步过滤出来了只包含common mcp的数据，
然后在这些mcp 对应的tool上建图，看看是否联通。但是有个问题是绝大部分的common mcp都是无状态的，无状态的mcp使用现在的建边规则可能是建不出来（也不一定，反正要修改这个规则，我的假设是有状态的mcp的tool关联性更强）
然后就是建边的规则，它首先是根据label的相似逻辑拿到一个可能的node pair，然后把node pair全都给大模型，让他过滤，看看到底能留多少

find problem: tool schema no contain tool output, llm based on tool description guess one.so result in some edge is not constructed...
some tool call chain can not be form as input output relationship..
so this method can be more edges than Toucan ?
we can see there be many new edges but not be confident , the reason is still we do not design func output format, llm judge the input output relationship sometimes just guess
so we need to design the tool schema
two func category, output is natural language, output is json format
for the former, need to extract key info, and better use re to extract
for the another one, need to json loads and extrace key info , for the nested field, throw it

whatever now we have one DAG, and its edge is 强依赖, so we want to backward get user query first.
and when we random walk we can get function signature paths. we use this to first get the one turn multi steps data. so a user query is needed in the forward process
而且我们要迭代的生成user query? 因为第二轮之后的user query生成是要依赖于last round的func output的。
所以应该是先把fsp按照turn分好，然后对于turn 1 假设有两个函数，然后让大模型生成一个user query能够调用turn 1里的函数的至少一个，
这也就是candidate functions.然后需要进行forward，让大模型填参数，并且进行函数的执行。在第二轮backward的时候，是根据last round的tool output和这一轮的candidate来生成user query的，条件是这个query要motivated by last round tool output, 完美情况下这些output要能作为下一轮选的函数的input（至少一个）,这也是能成立的，然后在决定了要选哪个函数后，确保query要能包含调用函数的全部信息，虽然有些信息是可以通过last round tool output推断出来，你可以对这些进行指代，如果少了信息 需要在query里补充.

给定一条链，如何转换成单轮对话下的多轮调用形式？
首先我先用merge获得一条fsp，相当于我把magnet对应的多轮变成一轮的多step，然后我基于每一个step生成一个atomic query，并且我要要求生成的第二个step以及之后的query要用到last step的tool output,并且要调用这一步的candidate函数，最好是选择的函数的输入至少有一个能from last round tool output.相当于最后我生成了one turn multi step,每个step 都有一个atomic query。然后最后我把这些atomic query合成为一个大的query。 
rule:
- The preferred next round query should be motivated by the outputs from the last round function output. Preferably, those outputs are used as the input parameters for as least one of the functions being called at this round.
- You should NOT mention which functions to use in your query explicitly.
- After you decide on which function to use, make sure your new query contains information for all the required parameters of the functions you want to call, although some information may be referred to implicitly as the outputs from the last round. If the value for some required parameters are not clear given the context, you may want to create a value for that required parameter but just remember, have information for all required parameters.
- Use no parameters besides the parameters indicated in the required and optional fields of the function documentation.
- For outputs from the last round, try not to mention the exact parameters that you will use. Instead, use references such as 'the location you just found', 'With the listed items'... to refer to the output of last round that will be leveraged next.
- Do not repeat any queries in the conversation history. This means your new query should not call the same function with the same set of parameters as any of the queries in the conversation, even the function exists in the adjacent list.
现在需要去生成tool result,根据tool input schema 和output schema.
1. 要不要分类来设计tool的code 2. 分析是否需要引入额外的mock数据
首先要明确一点我们现在通过对mcp是否有状态已经做了分类，假设mcp为无状态则mcp tool也无状态，这表明一个mcp tool A的调用 不会影响到another mcp tool B的结果。但是这只是在单个mcp级别可以这么划分，如果考虑跨mcp的情况，则可能可以把stateless 的 mcp tool 强行组合成有状态。
假设我们先不考虑建立database的情况，但仍需要对工具进行分类：
1.计算类
2.查询类（查询源来自外部API）
3.执行类（需要依赖外部API）
func doc -> python code的时候，对于 query 和 action,把依赖于外部API的地方抽象为 call external API placeholder函数, place holder func 的return data 应该是一个dict.先把 place holder 函数的input 定义为none
是否要写单元测试
首先写出来的python code都要通过语法检查，然后后面再考虑写ut
先为每个tool 设计python code，然后依据分类，有些tool有一个call_external_api函数，且每个函数都有独特的docstring。所以一个最简单的做法是每次调用这个python code的时候，
如果该python code里有call_external_api，那么调用该函数时，把doc string给llm,让llm模拟一个call_external_api的结果。模拟得到结果后，再继续执行完python code.
得到query and fc reference后，最后一步是做蒸馏

