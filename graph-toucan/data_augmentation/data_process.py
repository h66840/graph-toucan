import datasets,argparse
import json,os,asyncio,logging,time,re
from openai import AsyncOpenAI
from tqdm import tqdm
async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

logger = logging.getLogger("toucan_data_process")
logger.setLevel(logging.INFO)
if not logger.handlers:
    log_dir = os.path.dirname(__file__)
    log_path = os.path.join(log_dir, "process_batch_v3.log")
    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


async def rewrite_sample_async(history, tools):
    """
    explain the user query why can not be achieved .

    Args:
        history: conversation history list, where history[-1] is the user query
        tools: list of available tool schemas

    Returns:
        model natural language explanation
    """
    # Extract the user query that needs to be rewritten
    user_query = history[-1]['content']

    # Build the context from previous conversation
    context_messages = []
    for msg in history[:-1]:
        context_messages.append(msg)

    # Create the prompt for LLM
    prompt = f"""Given the following conversation history and available tools, the user's last query cannot be solved because a necessary tool/function is missing.

Available tools:
{json.dumps(tools, indent=2)}

Conversation history:
{json.dumps(context_messages, indent=2)}

User's query that cannot be solved:
{user_query}

Based on the available tools and conversation history, the uesr query can not be solved because of miss necessery tool. Not simply point out missing func,Your task is to try to use natural language to answer query, and describe the situation and what functionality is missed. 

"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=1024 
    )

    model_explanation = completion.choices[0].message.content
    return model_explanation

async def rewrite_sample_v1(history, tools,target_tool):
    """
    explain the user query why can not be achieved .

    Args:
        history: conversation history list, where history[-1] is the user query
        tools: list of available tool schemas
        target_tool: the missing tool that is needed to solve the query

    Returns:
        tuple: (model natural language explanation, token usage dict)
    """
    # Extract the user query that needs to be rewritten
    user_query = history[-1]['content']

    # Build the context from previous conversation
    context_messages = []
    for msg in history[:-1]:
        context_messages.append(msg)

    # Create the prompt for LLM
    prompt = f"""Given the following conversation history and available tools, the user's last query cannot be solved because a necessary tool/function is missing.

Available tools:
{json.dumps(tools, indent=2)}

Conversation history:
{json.dumps(context_messages, indent=2)}

User's query that cannot be solved:
{user_query}

Additional information - The missing tool that would be needed:
{json.dumps(target_tool, indent=2)}

Based on the available tools and conversation history, the uesr query can not be solved because of miss necessery tool. 
Not simply point out missing func,Your task is to try to use natural language to answer query and describe the current situation and based on user_query conversation_history additional target tool information,analyse what functionality is missed. 
Important: in your answer, do not directly mention the missing tool info,the missing tool info i provide is just for you to better complete the task.


"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=1024
    )

    model_explanation = completion.choices[0].message.content

    # Extract token usage information
    token_usage = {
        'prompt_tokens': completion.usage.prompt_tokens,
        'completion_tokens': completion.usage.completion_tokens,
        'total_tokens': completion.usage.total_tokens
    }

    return model_explanation, token_usage

async def rewrite_sample_v2(history, tools,target_tool,missing_params):
    """

    1.explain the user query why can not be achieved for miss-param situation.

    Args:
        history: conversation history list, where history[-1] is the user query
        tools: list of available tool schemas
        target_tool: the missing tool that is needed to solve the query
        missing_params: the required params that are missing in the rewritten query
    Returns:
        tuple: (model natural language explanation, token usage dict)
    """
    # Extract the user query that is rewritten
    user_query = history[-1]['content']

    # Build the context from previous conversation
    context_messages = []
    for msg in history[:-1]:
        context_messages.append(msg)

    # Create the prompt for LLM
    prompt = f"""Given the following conversation history and available tools, the user's last query cannot be solved because solve the problem need to call one target function while some required parameters for the function is not mentioned in the query.

Available tools:
{json.dumps(tools, indent=2)}

Conversation history:
{json.dumps(context_messages, indent=2)}

User's query that cannot be solved:
{user_query}

target function definition that is missing info to call:
{json.dumps(target_tool, indent=2)}
additional helpful information - required params that are missing in the rewritten query:
{json.dumps(missing_params, indent=2)}

Based on the available tools ,conversation history and target function definition, the uesr query can not be solved because of some required params does not mentioned in the query. 
Your task is to output some pure texts to ask for the lacking information.
important: in your answer, do not directly mention the required params i provide,the required params i provide is just for you to better complete the task.
"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=1024
    )

    model_explanation = completion.choices[0].message.content

    # Extract token usage information
    token_usage = {
        'prompt_tokens': completion.usage.prompt_tokens,
        'completion_tokens': completion.usage.completion_tokens,
        'total_tokens': completion.usage.total_tokens
    }

    return model_explanation, token_usage

async def rewrite_user_query_for_miss_param(history, tools, target_tool):
    """
    Rewrite user query to create a QA flow with missing parameters:
    Q1' (missing params) -> A1' (explain missing params) -> Q2 (supplement params) -> A1 (original answer)
    
    CRITICAL: This function checks if missing parameters can be inferred from conversation history.
    If missing params can be found in history, returns "NONE" for rewritten_query (cannot safely rewrite).
    Note: Cases where required params are not directly mentioned in user_query are also covered by 
    the history check, as they would be considered inferable from history.
    
    Args:
        history: conversation history list, where history[-1] is the user query
        tools: list of available tool schemas
        target_tool: the target tool definition that needs to be called
    
    Returns:
        tuple: (rewritten_query, explanation_answer, supplement_query, missing_params, token_usage, rule_0_satisfied)
            - rewritten_query: str, Q1' - the rewritten user query that lacks some required params, 
                              or "NONE" if missing params can be inferred from conversation history
            - explanation_answer: str, A1' - explanation of what parameters are missing, or why cannot rewrite
            - supplement_query: str, Q2 - a statement that supplements the missing parameters (empty if NONE)
            - missing_params: list, the required params that are missing in the rewritten query (empty if NONE)
            - token_usage: dict, token usage information
            - rule_0_satisfied: bool, True if cannot rewrite (missing params can be inferred from history)
    """
    # Extract the rewritten query
    rewritten_query = history[-1]['content']
    
    # Build the context from previous conversation
    context_messages = []
    for msg in history[:-1]:
        context_messages.append(msg)
    
    # Extract required parameters from target_tool
    # Handle case where target_tool might be a string
    if isinstance(target_tool, str):
        try:
            target_tool = json.loads(target_tool)
        except json.JSONDecodeError:
            # If it's not JSON, log warning and continue
            logger.warning(f"target_tool is a string but not valid JSON: {target_tool[:100]}")
    
    required_params = []
    if isinstance(target_tool, dict):
        function_def = target_tool.get('function', {})
        parameters = function_def.get('parameters', {})
        required_params = parameters.get('required', [])
    else:
        logger.warning(f"target_tool is not a dict: {type(target_tool)}")
    
    # Format conversation history for the prompt
    history_text = ""
    if context_messages:
        history_text = "\nConversation history (previous turns):\n"
        for i, msg in enumerate(context_messages):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            history_text += f"  {role}: {content}\n"
    else:
        history_text = "\nConversation history: (No previous conversation)\n"
    
    # Create the prompt for LLM - NOW INCLUDING HISTORY CHECK
    prompt = f"""Given the following conversation history and available tools, the user's last query may not be solved because solve the problem need to call one target function while some required parameters for the function is probably not mentioned in the query or can not be infered through the conversation history.

{history_text}

Current user query : {rewritten_query}

Available tools:
{json.dumps(tools, indent=2, ensure_ascii=False)}

Target function definition:
{json.dumps(target_tool, indent=2, ensure_ascii=False)}


So your task is Not simply point out whether or not missing param,but also try to use natural language to answer query and explain the required params for calling the target function is complete or not,you should analyze the required params can be inferred or find from the history and user query or not , and if you think current info indeed not satisfy user query, you need to explain what is the lack params, and explain you can not get these params info through the history and user query. 



"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0.3,  # Increased from 0 to encourage more diverse rewrites
        max_completion_tokens=1024
    )
    
    response_text = completion.choices[0].message.content
    

    # Extract token usage information
    token_usage = {
        'prompt_tokens': completion.usage.prompt_tokens,
        'completion_tokens': completion.usage.completion_tokens,
        'total_tokens': completion.usage.total_tokens
    }
    
    return response_text, token_usage

async def filter_user_query_for_miss_param(history, tools, target_tool):
    """
    Filter rewritten queries by checking if the missing parameters mentioned in assistant's response (A1')
    can be found in conversation history. If the missing parameters can be inferred from history, 
    the sample should be skipped.
    
    Args:
        history: conversation history list, where:
                 - history[-2] is the rewritten user query (Q1')
                 - history[-1] is the assistant's response (A1') explaining what parameters are missing
        tools: list of available tool schemas
        target_tool: the target tool definition that needs to be called
    
    Returns:
        tuple: (should_keep: bool, judgment: str, token_usage: dict)
            - should_keep: True if the sample should be kept (missing params are truly missing), 
                          False if should be skipped (missing params can be found in history)
            - judgment: str, LLM's explanation of the judgment
            - token_usage: dict, token usage information
    """
    # Validate history structure
    if len(history) < 2:
        logger.warning(f"History too short: {len(history)} messages, expected at least 2")
        return True, "History too short, keeping sample", {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    # Extract Q1' and A1'
    rewritten_query = history[-2]['content'] if history[-2]['role'] == 'user' else None
    assistant_response = history[-1]['content'] if history[-1]['role'] == 'assistant' else None
    
    if not rewritten_query or not assistant_response:
        logger.warning(f"Invalid history structure: last two messages should be user query and assistant response")
        return True, "Invalid history structure, keeping sample", {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    # Build the full conversation history (including all previous turns before Q1' and A1')
    context_messages = []
    for msg in history[:-2]:  # All messages before Q1' and A1'
        context_messages.append(msg)
    
    # Extract required parameters from target_tool
    if isinstance(target_tool, str):
        try:
            target_tool = json.loads(target_tool)
        except json.JSONDecodeError:
            logger.warning(f"target_tool is a string but not valid JSON: {target_tool[:100]}")
    
    # Extract required parameters list for reference
    required_params = []
    if isinstance(target_tool, dict):
        function_def = target_tool.get('function', {})
        parameters = function_def.get('parameters', {})
        required_params = parameters.get('required', [])
    
    # Create the prompt for LLM to check if missing params can be found in history
    prompt = f"""You are a judge evaluating whether the missing parameters mentioned in the assistant's response can be found or inferred from the conversation history.

Conversation history (context before the current QA turn):
{json.dumps(context_messages, indent=2, ensure_ascii=False)}

Current QA turn:
User query (Q1'): {rewritten_query}
Assistant response (A1'): {assistant_response}

Target function definition:
{json.dumps(target_tool, indent=2, ensure_ascii=False)}

Available tools:
{json.dumps(tools, indent=2, ensure_ascii=False)}

Required parameters for the target function:
{json.dumps(required_params, indent=2, ensure_ascii=False)}

Your task is to:
1. **Identify what parameters the assistant (A1') thinks are missing**
   - Analyze the assistant's response (A1') to understand what parameters or information it claims are missing or needed.
   - The assistant may mention missing parameters explicitly or implicitly (e.g., "I need the width and height", "could you specify the background type").

2. **Check if these missing parameters can be found in the conversation history**
   - Check if the values for the missing parameters can be clearly inferred or found in the conversation history (including previous user queries, assistant responses, or function call results).
   - Consider both explicit mentions and implicit references (e.g., "as we discussed before", "the previous result", "what we retrieved earlier").
   - Look for parameter values that were mentioned in earlier turns of the conversation.

3. **Make a judgment**
   - If ANY of the missing parameters mentioned by the assistant CAN be found or inferred from the conversation history, then the sample should be SKIPPED (output JUDGMENT: SKIP).
   - Only if ALL missing parameters mentioned by the assistant CANNOT be found in the history, the sample should be KEPT (output JUDGMENT: KEEP).

CRITICAL RULES:
- Be strict: if there's any reasonable way to infer a parameter value from the conversation history, consider it as "can be found".
- The assistant's response (A1') is asking for information that should be missing. Your job is to check if that information actually exists in the earlier conversation history.
- If the missing information can be found in history, it means the rewritten query (Q1') is not truly missing the parameters (it can rely on context), so skip this sample.

Your output format MUST be:
JUDGMENT: KEEP or SKIP
EXPLANATION: [brief explanation of:
  1. What parameters the assistant thinks are missing (based on A1')
  2. Whether these parameters can be found in the conversation history
  3. Why you made this judgment]

Where:
- JUDGMENT: KEEP  means the sample should be kept (all missing params mentioned by assistant are truly missing, cannot be found in history)
- JUDGMENT: SKIP  means the sample should be skipped (at least one missing param mentioned by assistant can be found or inferred from history)
"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a careful judge that evaluates whether missing parameters mentioned in assistant responses can be found in conversation history."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=512
    )
    
    judgment_text = completion.choices[0].message.content
    
    # Parse the judgment
    should_keep = True  # Default to keep if parsing fails
    judgment_upper = judgment_text.upper()
    
    if "JUDGMENT:" in judgment_upper:
        for line in judgment_text.split("\n"):
            if "JUDGMENT:" in line.upper():
                if "KEEP" in line.upper():
                    should_keep = True
                elif "SKIP" in line.upper():
                    should_keep = False
                break
    else:
        # Fallback: look for KEEP/SKIP keywords
        if "SKIP" in judgment_upper and "KEEP" not in judgment_upper:
            should_keep = False
        elif "KEEP" in judgment_upper:
            should_keep = True
    
    # Extract token usage information
    token_usage = {
        'prompt_tokens': completion.usage.prompt_tokens,
        'completion_tokens': completion.usage.completion_tokens,
        'total_tokens': completion.usage.total_tokens
    }
    
    return should_keep, judgment_text, token_usage

async def filter_sample_async(data):
    """
    Filter a single rewritten sample by checking if the missing parameters mentioned in assistant's response (A1')
    can be found in conversation history.
    
    Args:
        data: dataset sample containing tools, messages (already rewritten with Q1' -> A1' -> Q2' -> A1)
    
    Returns:
        tuple: (data or None, token_usage dict)
            - If should keep: (data, token_usage)
            - If should skip: (None, token_usage)
    """
    tools_schema = json.loads(data['tools'])
    messages = json.loads(data['messages'])
    modified_info = json.loads(data['modification_info'])
    modified_turn_index = modified_info.get('modified_turn_index')
    
    if modified_turn_index == 0:
        logger.warning(f"modified_turn_index is 0, skipping filter")
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    # Get target_tool, handle both string and dict cases
    target_tool = modified_info.get('target_tool_definition')
    if target_tool is None:
        logger.warning(f"target_tool_definition not found, skipping filter")
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    if isinstance(target_tool, str):
        try:
            target_tool = json.loads(target_tool)
        except json.JSONDecodeError:
            pass
    
    # Find Q1' and A1' in the rewritten messages
    # After rewrite, the structure is: messages[:modified_turn_index] + Q1' + A1' + Q2' + A1
    # We need to find Q1' and A1' which should be at positions modified_turn_index and modified_turn_index+1
    if modified_turn_index + 1 >= len(messages):
        logger.warning(f"Invalid message structure, cannot find Q1' and A1'")
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    # Build history for filtering: all previous messages + Q1' + A1'
    history_for_filter = messages[:modified_turn_index + 2].copy()
    
    # Validate that the last two messages are Q1' (user) and A1' (assistant)
    if len(history_for_filter) < 2:
        logger.warning(f"History too short for filtering")
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    if history_for_filter[-2]['role'] != 'user' or history_for_filter[-1]['role'] != 'assistant':
        logger.warning(f"Invalid history structure: expected user then assistant, got {history_for_filter[-2]['role']} then {history_for_filter[-1]['role']}")
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    
    try:
        should_keep, filter_judgment, token_usage_filter = await filter_user_query_for_miss_param(
            history_for_filter, tools_schema, target_tool
        )
        
        if not should_keep:
            # Skip this sample if missing params can be found in history
            # logger.info(f"Skipping sample: missing params can be found in history. UUID INFO{data['uuid']}")
            # tqdm.write(f"Skipping sample: missing params can be found in history. UUID INFO{data['uuid']}")
            return None, token_usage_filter
        
        return data, token_usage_filter
        
    except Exception as e:
        logger.error(f"Error in filter_user_query_for_miss_param: {str(e)}")
        logger.error(f"messages length: {len(messages)}, modified_turn_index: {modified_turn_index}")
        # If filtering fails, log but keep the sample (default to keep)
        return data, {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}

def validate_rewritten_query(original_query, rewritten_query, missing_params, similarity_threshold=0.85):
    """
    Lightweight heuristic validator kept for quick local checks.

    NOTE: For stronger semantic validation using LLM, use
    `validate_rewritten_query_with_llm` instead.
    
    Args:
        original_query: str, the original user query
        rewritten_query: str, the rewritten query
        missing_params: list, the claimed missing parameters
        similarity_threshold: float, maximum allowed similarity (0-1)
    
    Returns:
        tuple: (is_valid: bool, reason: str)
    """
    # Check 1: Ensure rewritten query is different from original
    # Simple similarity check based on word overlap
    original_words = set(original_query.lower().split())
    rewritten_words = set(rewritten_query.lower().split())
    
    if len(original_words) == 0 or len(rewritten_words) == 0:
        return False, "Empty query detected"
    
    # Calculate Jaccard similarity (intersection over union)
    intersection = len(original_words & rewritten_words)
    union = len(original_words | rewritten_words)
    similarity = intersection / union if union > 0 else 0.0
    
    if similarity > similarity_threshold:
        return False, f"Rewritten query too similar to original (similarity: {similarity:.2f} > {similarity_threshold})"
    
    # Check 2: Ensure missing_params is not empty
    if not missing_params or len(missing_params) == 0:
        return False, "No missing parameters specified"
    
    # Check 3: Ensure rewritten query is not identical to original
    if original_query.strip().lower() == rewritten_query.strip().lower():
        return False, "Rewritten query is identical to original"
    
    # Check 4: Ensure rewritten query is not trivially similar in length and content
    length_ratio = len(rewritten_query) / len(original_query) if len(original_query) > 0 else 1.0
    if length_ratio > 0.98 and similarity > 0.8:
        return False, f"Rewritten query too similar in length and content (length_ratio: {length_ratio:.2f}, similarity: {similarity:.2f})"
    
    return True, "Validation passed"


async def validate_rewritten_query_with_llm(
    original_query,
    rewritten_query,
    missing_params,
    required_params=None,
    conversation_history=None,
    target_tool=None,
    available_tools=None,
):
    """
    Use LLM as a judge to validate whether the rewritten query truly
    (1) lacks the claimed required parameters and
    (2) is not just a trivial paraphrase of the original.

    Args:
        original_query: str, the original user query
        rewritten_query: str, the rewritten query produced by rewrite_user_query_for_miss_param
        missing_params: list[str], parameter names the rewriter claims are missing
        required_params: list[str] or None, all required parameters of the target tool (optional but helpful)
        conversation_history: list[dict] or None, previous turns before the original query
        target_tool: dict or None, target tool definition (optional, for context only)
        available_tools: list or None, available tools (optional, for context only)

    Returns:
        dict: {
            "satisfied": bool,      # whether validation passed
            "judgment": str,        # raw LLM judgment text
            "token_usage": dict,    # prompt/completion/total tokens
        }
    """
    # Build compact context snippets (avoid huge prompts)
    history_snippet = ""
    if conversation_history:
        try:
            history_snippet = json.dumps(conversation_history[-5:], ensure_ascii=False, indent=2)
        except Exception:
            history_snippet = str(conversation_history)

    target_tool_snippet = ""
    if target_tool:
        try:
            target_tool_snippet = json.dumps(target_tool, ensure_ascii=False, indent=2)
        except Exception:
            target_tool_snippet = str(target_tool)

    available_tools_snippet = ""
    if available_tools:
        try:
            available_tools_snippet = json.dumps(available_tools, ensure_ascii=False, indent=2)
        except Exception:
            available_tools_snippet = str(available_tools)

    required_params = required_params or []

    judge_prompt = f"""You are a strict judge. Your task is to check whether a rewritten user query
correctly simulates a "missing required parameters" situation for a target tool/function.

Conversation history (recent turns only, may be empty):
{history_snippet}

Original user query (this one CAN correctly call the function, possibly with implicit parameters):
{original_query}

Rewritten user query (this one SHOULD NOT have enough info to call the function):
{rewritten_query}

Target tool (for your understanding only, do NOT mention it explicitly in your judgment):
{target_tool_snippet}

Available tools (for context only, optional):
{available_tools_snippet}

All required parameters of the target function (if provided):
{json.dumps(required_params, ensure_ascii=False)}

Parameters that the rewriter claims are missing in the rewritten query:
{json.dumps(missing_params, ensure_ascii=False)}

You must carefully check the following:
1. **Missing information correctness**:
   - For each parameter in `missing_params`, the rewritten query must NOT contain a concrete value
     or enough information to reliably fill that parameter.
   - It is OK if the general concept appears, but the specific value must be missing.

2. **Not just a paraphrase**:
   - The rewritten query must NOT simply restate the same concrete parameter values using
     synonyms or slightly different wording.
   - If the rewritten query still clearly implies the same concrete values, this is a failure.

3. **Intent and naturalness**:
   - The rewritten query should keep a similar overall intent and remain natural and coherent.
   - It is acceptable (and even good) to keep or add contextual/background information as long
     as it does not re-introduce the concrete parameter values.

Your output format MUST be:
JUDGMENT: YES or NO
EXPLANATION: a brief explanation of why it passed or failed

Where:
- JUDGMENT: YES  means the rewritten query is a valid "missing required parameters" version.
- JUDGMENT: NO   means the rewritten query is invalid (e.g., still has concrete values, or is just a paraphrase).
"""

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {
                "role": "system",
                "content": "You are a careful, strict, and concise judge that evaluates rewritten user queries for missing-parameter scenarios.",
            },
            {"role": "user", "content": judge_prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=512,
    )

    judgment_text = completion.choices[0].message.content

    # Parse JUDGMENT: YES/NO
    satisfied = False
    upper = judgment_text.upper()
    if "JUDGMENT:" in upper:
        for line in judgment_text.split("\n"):
            if "JUDGMENT:" in line.upper():
                if "YES" in line.upper():
                    satisfied = True
                elif "NO" in line.upper():
                    satisfied = False
                break
    else:
        # Fallback: look for YES/NO at start
        if upper.strip().startswith("YES"):
            satisfied = True
        elif upper.strip().startswith("NO"):
            satisfied = False

    token_usage = {
        "prompt_tokens": completion.usage.prompt_tokens,
        "completion_tokens": completion.usage.completion_tokens,
        "total_tokens": completion.usage.total_tokens,
    }

    return {
        "satisfied": satisfied,
        "judgment": judgment_text,
        "token_usage": token_usage,
    }

def generate_default_rule(user_query, conversation_history=None, target_tool=None, available_tools=None):
    """
    Generate a default rule for checking if model response satisfies key requirements.
    
    Args:
        user_query: str, the user's query that needs to be answered
        conversation_history: list or str, the conversation history before the user query (optional)
        target_tool: dict or str, the target tool information that should NOT be directly mentioned (optional)
        available_tools: list or str, the available tools in the context (optional)
    
    Returns:
        str, the generated rule text for evaluation
    """
    rule_parts = []
    
    # Build context information
    context_info = []
    if conversation_history:
        if isinstance(conversation_history, list):
            context_str = json.dumps(conversation_history, indent=2, ensure_ascii=False)
        else:
            context_str = str(conversation_history)
        context_info.append(f"Conversation history: {context_str}")
    
    if available_tools:
        if isinstance(available_tools, list):
            tools_str = json.dumps(available_tools, indent=2, ensure_ascii=False)
        else:
            tools_str = str(available_tools)
        context_info.append(f"Available tools: {tools_str}")
    
    context_section = "\n".join(context_info) if context_info else "No additional context provided."
    
    # Build target tool restriction
    target_tool_restriction = ""
    if target_tool:
        if isinstance(target_tool, dict):
            target_tool_str = json.dumps(target_tool, indent=2, ensure_ascii=False)
        else:
            target_tool_str = str(target_tool)
        target_tool_restriction = f"""
    IMPORTANT RESTRICTION: The response must NOT directly mention or reference the following target tool information:
    {target_tool_str}

    The target tool information is provided only for your reference to understand what functionality is missing, but you should NOT explicitly mention it in your evaluation. Instead, check if the response describes the missing functionality in a natural way without directly referencing the tool details above.
    """
    
    rule = f"""You are evaluating whether a model's response satisfies the following requirements. The response must meet ALL of the following criteria:

    1. **Answer the user query**: The response should attempt to address or answer the user's query, even if it cannot be fully completed due to missing functionality.

    User query to be answered:
    {user_query}

    2. **Describe the current situation**: The response should clearly describe the current situation, explaining what can and cannot be done with the available resources.

    3. **Explain missing functionality based on context**: The response should explain what functionality is missing, based on the conversation history and available tools context. The explanation should be natural and contextual. 
    can not be halucination.

    Context information:
    {context_section}

    4. **No direct mention of target tool**: The response should NOT directly mention, quote, or explicitly reference the specific target tool details. Instead, it should describe the missing functionality in natural language without revealing the exact tool information.
    {target_tool_restriction}

    Evaluation criteria:
    - The response satisfies ALL four requirements above: YES
    - The response fails to meet any of the four requirements: NO
    - Then provide a brief explanation of your judgment.
    Please evaluate each requirement carefully and provide your judgment."""
    
    return rule

async def rule_based_judge(response, rule):
    """
    Check if LLM's response satisfies the provided rule using LLM API.

    Args:
        response: str, the LLM's response text to be checked
        rule: str, the rule to check against

    Returns:
        dict: {
            'satisfied': bool, whether the response satisfies the rule
            'judgment': str, LLM's judgment explanation
            'token_usage': dict, token usage information
        }
    """
    prompt = f"""You are a judge evaluating whether a response satisfies a given rule.

    Rule to check:
    {rule}

    Response to evaluate:
    {response}

    Please carefully evaluate whether the response satisfies the rule. Your judgment should be:
    1. First, output "YES" or "NO" to indicate whether the response satisfies the rule
    2. Then provide a brief explanation of your judgment

    Format your response as:
    JUDGMENT: YES/NO
    EXPLANATION: [your explanation here]
    """

    completion = await async_client.chat.completions.create(
        model="qwen3-235b-a22b-instruct-2507",
        messages=[
            {"role": "system", "content": "You are a helpful and precise judge that evaluates responses against rules."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0,
        max_completion_tokens=512
    )

    judgment_text = completion.choices[0].message.content
    
    # Parse the judgment
    satisfied = False
    if "JUDGMENT:" in judgment_text:
        judgment_line = [line for line in judgment_text.split('\n') if 'JUDGMENT:' in line.upper()][0]
        satisfied = 'YES' in judgment_line.upper()
    else:
        # Fallback: check if the response contains YES/NO
        judgment_upper = judgment_text.upper()
        if judgment_upper.startswith('YES') or ' JUDGMENT: YES' in judgment_upper:
            satisfied = True
        elif judgment_upper.startswith('NO') or ' JUDGMENT: NO' in judgment_upper:
            satisfied = False

    # Extract token usage information
    token_usage = {
        'prompt_tokens': completion.usage.prompt_tokens,
        'completion_tokens': completion.usage.completion_tokens,
        'total_tokens': completion.usage.total_tokens
    }

    return {
        'satisfied': satisfied,
        'judgment': judgment_text,
        'token_usage': token_usage
    }

def extract_info(data):
    """
    Extract user query, conversation history, target tool, and available tools from data sample.
    
    Args:
        data: dataset sample containing tools, messages, and modification_info
    
    Returns:
        tuple: (user_query, conversation_history, target_tool, available_tools, response)
    """
    messages = json.loads(data['messages'])
    tools_schema = json.loads(data['tools'])
    modified_info = json.loads(data['modification_info'])
    modified_turn_index = modified_info.get('modified_turn_index')
    
    # Extract user query (the query at modified_turn_index)
    user_query = messages[modified_turn_index]['content']
    
    # Extract conversation history (messages before the user query)
    conversation_history = messages[0:modified_turn_index]
    
    # Extract target tool - it might be a JSON string or already a dict
    removed_tool_def = modified_info.get('removed_tool_definition')
    if isinstance(removed_tool_def, str):
        target_tool = json.loads(removed_tool_def)
    else:
        target_tool = removed_tool_def or {}
    
    # Available tools
    available_tools = tools_schema
    
    # Extract the response to judge (assistant's response after user query)
    response = messages[modified_turn_index + 1]['content']
    
    return user_query, conversation_history, target_tool, available_tools, response

def process_sample(data):
    """
    Process a single data sample and rewrite the user query if a necessary tool is missing.

    Args:
        data: dataset sample containing tools, messages, and modification_info

    Returns:
        updated data sample with rewritten message
    """
    tools_schema = json.loads(data['tools'])
    messages = json.loads(data['messages'])
    modified_info = json.loads(data['modification_info'])
    modified_turn_index = modified_info.get('modified_turn_index')

    assert messages[modified_turn_index]['role'] == 'user'
    history = messages[0:modified_turn_index+1]

    target_tool = json.loads(data['modification_info'])['removed_tool_definition']
    # make explain to describe missing functionality
    #model_explain = rewrite_sample(history, tools_schema)
    model_explain = rewrite_sample_v1(history, tools_schema,target_tool)

    # Update the message with the rewritten content
    assert messages[modified_turn_index+1]['content'] == "Sorry, I don't have enough information to answer the request. I'm missing some necessary tools to complete this task."
    messages[modified_turn_index+1]['content'] = model_explain

    # Update the data sample
    data['messages'] = json.dumps(messages)

    return data

async def process_sample_async(data):
    """
    Process a single data sample and rewrite the user query if a necessary tool is missing.

    Args:
        data: dataset sample containing tools, messages, and modification_info

    Returns:
        tuple: (updated data sample with rewritten message, token usage dict)
    """
    tools_schema = json.loads(data['tools'])
    messages = json.loads(data['messages'])
    modified_info = json.loads(data['modification_info'])
    modified_turn_index = modified_info.get('modified_turn_index')

    assert messages[modified_turn_index]['role'] == 'user'
    history = messages[0:modified_turn_index+1]

    target_tool = json.loads(data['modification_info'])['removed_tool_definition']
    # make explain to describe missing functionality
    model_explain, token_usage = await rewrite_sample_v1(history, tools_schema, target_tool)

    # Update the message with the rewritten content
    assert messages[modified_turn_index+1]['content'] == "Sorry, I don't have enough information to answer the request. I'm missing some necessary tools to complete this task."
    messages[modified_turn_index+1]['content'] = model_explain

    # Update the data sample
    data['messages'] = json.dumps(messages)

    return data, token_usage

async def process_sample_v1_async(data):
    """
    Process a single data sample and create a QA flow:
    Q1' (missing params) -> A1' (explain missing) -> Q2' (supplement) -> A1 (original answer)

    Args:
        data: dataset sample containing tools, messages, and modification_info

    Returns:
        tuple: (updated data sample with rewritten message, token usage dict)
    """
    tools_schema = json.loads(data['tools'])
    messages = json.loads(data['messages'])
    modified_info = json.loads(data['modification_info'])
    modified_turn_index = modified_info.get('modified_turn_index')

    # Debug: Check if modified_turn_index is valid
    if modified_turn_index is None:
        raise ValueError(f"modified_turn_index is None in modification_info: {modified_info}")
    if modified_turn_index >= len(messages):
        raise ValueError(f"modified_turn_index {modified_turn_index} >= len(messages) {len(messages)}")
    
    assert messages[modified_turn_index]['role'] == 'user', f"Expected user role at index {modified_turn_index}, got {messages[modified_turn_index].get('role')}"
    

    # this history contain the needed modified query
    history = messages[0:modified_turn_index+1]

    # Get target_tool, handle both string and dict cases
    target_tool = modified_info.get('target_tool_definition')
    if target_tool is None:
        raise ValueError(f"target_tool_definition not found in modification_info: {modified_info}")
    if isinstance(target_tool, str):
        try:
            target_tool = json.loads(target_tool)
        except json.JSONDecodeError:
            # If it's not JSON, keep as string
            pass
    
    
    # rewrite_answer
    try:
        response_text, token_usage1= await rewrite_user_query_for_miss_param(history, tools_schema, target_tool)
    except Exception as e:
        logger.error(f"Error in rewrite_user_query_for_miss_param: {str(e)}")
        logger.error(f"target_tool type: {type(target_tool)}, value: {str(target_tool)[:200]}")
        logger.error(f"history length: {len(history)}, last message: {history[-1] if history else 'None'}")
        raise
    

    # Keep messages before modified_turn_index
    new_messages = messages[:modified_turn_index+1].copy()
    
    # Q1': rewritten query without parameters (or "NONE" if rule 0 is satisfied)
    new_messages.append({
        'role': 'assistant',
        'content': response_text
    })
    
    # A1: original assistant response
   
    # If no original response, keep the placeholder
    if modified_turn_index + 2 < len(messages):
        new_messages.extend(messages[modified_turn_index + 2:])
    else:
        assert 0
    
    # Update the data sample
    data['messages'] = json.dumps(new_messages)

    return data, token_usage1

def calculate_token_statistics(batch_results):
    """
    Calculate token usage statistics from batch processing results

    Args:
        batch_results: list of (data, token_usage) tuples or Exception objects

    Returns:
        dict containing token usage statistics
    """
    successful_results = []
    failed_count = 0
    skip_count = 0
    # Separate successful and failed results
    for result in batch_results:
        if isinstance(result, Exception):
            failed_count += 1
        elif not result:
            skip_count += 1
        else:
            data, token_usage = result
            successful_results.append(token_usage)

    if not successful_results:
        return {
            'successful_samples': 0,
            'failed_samples': failed_count,
            'skiped_samples': skip_count,
            'avg_prompt_tokens': 0,
            'avg_completion_tokens': 0,
            'avg_total_tokens': 0,
            'total_prompt_tokens': 0,
            'total_completion_tokens': 0,
            'total_tokens': 0
        }

    # Calculate statistics
    total_prompt_tokens = sum(t['prompt_tokens'] for t in successful_results)
    total_completion_tokens = sum(t['completion_tokens'] for t in successful_results)
    total_tokens = sum(t['total_tokens'] for t in successful_results)
    num_successful = len(successful_results)

    return {
        'successful_samples': num_successful,
        'failed_samples': failed_count,
        'skiped_samples': skip_count,
        'avg_prompt_tokens': total_prompt_tokens / num_successful,
        'avg_completion_tokens': total_completion_tokens / num_successful,
        'avg_total_tokens': total_tokens / num_successful,
        'total_prompt_tokens': total_prompt_tokens,
        'total_completion_tokens': total_completion_tokens,
        'total_tokens': total_tokens
    }

def print_token_statistics(token_stats):
    """
    Print formatted token usage statistics

    Args:
        token_stats: dict containing token usage statistics from calculate_token_statistics
    """
    print("\n" + "="*60)
    print("Token Usage Statistics:")
    print("="*60)
    print(f"Successful samples: {token_stats['successful_samples']}")
    print(f"Failed samples: {token_stats['failed_samples']}")
    print(f"Skiped samples: {token_stats['skiped_samples']}")
    print(f"\nAverage per sample:")
    print(f"  - Prompt tokens: {token_stats['avg_prompt_tokens']:.2f}")
    print(f"  - Completion tokens: {token_stats['avg_completion_tokens']:.2f}")
    print(f"  - Total tokens: {token_stats['avg_total_tokens']:.2f}")
    print(f"\nTotal consumption:")
    print(f"  - Total prompt tokens: {token_stats['total_prompt_tokens']}")
    print(f"  - Total completion tokens: {token_stats['total_completion_tokens']}")
    print(f"  - Total tokens: {token_stats['total_tokens']}")
    print("="*60)

async def filter_batch(samples, batch_size=5):
    """
    Filter rewritten samples in batches by checking if missing parameters can be found in history.

    Features:
        1. tqdm progress bar for batch processing visibility.
        2. Failed samples are logged via the configured logger, skipped, and stored for later reporting.
        3. Prints processing time for each batch.

    Args:
        samples: list of dataset samples to filter (should already be rewritten)
        batch_size: number of concurrent API calls per batch

    Returns:
        tuple: (list of filtered data samples, overall token statistics dict, failed_samples list, skipped_samples list)
    """
    results = []
    failed_samples = []
    skipped_samples = []
    all_batch_results = []
    total_batches = (len(samples) + batch_size - 1) // batch_size
    start_total_time = time.time()

    batch_iterator = tqdm(
        range(0, len(samples), batch_size),
        total=total_batches if total_batches else None,
        desc="Filtering batches",
        unit="batch"
    )

    for i in batch_iterator:
        batch = samples[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        # Record batch start time
        batch_start_time = time.time()
        
        batch_iterator.set_postfix_str(f"size={len(batch)}")

        tasks = [filter_sample_async(s) for s in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Record batch end time and calculate duration
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
        
        # Collect results and handle errors
        for idx, result in enumerate(batch_results):
            sample_index = i + idx
            if isinstance(result, Exception):
                error_msg = str(result)
                log_msg = f"Error filtering sample {sample_index} (batch {batch_num}): {error_msg}"
                tqdm.write(f"  {log_msg}")
                logger.error(log_msg)
                failed_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'error': error_msg
                })
                # Add exception to all_batch_results for consistent handling
                all_batch_results.append(result)
                continue
            
            # filter_sample_async returns (data or None, token_usage)
            if result is None:
                log_msg = f"Skip filtering sample {sample_index} (batch {batch_num}): unexpected None result"
                tqdm.write(f"  {log_msg}")
                logger.warning(log_msg)
                skipped_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'reason': 'unexpected None result'
                })
                # Add None to all_batch_results for consistent handling
                all_batch_results.append(None)
                continue
            
            data, token_usage = result
            
            # If data is None, it means the sample should be skipped
            if data is None:
                log_msg = f"Skip filtering sample {sample_index} (batch {batch_num}): missing params found in history"
                tqdm.write(f"  {log_msg}")
                logger.info(log_msg)
                skipped_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'reason': 'missing params found in history'
                })
                # Still add to all_batch_results for token statistics
                all_batch_results.append((None, token_usage))
                continue
            
            # Sample passed the filter
            results.append(data)
            all_batch_results.append((data, token_usage))

        # Update postfix with batch processing time
        batch_iterator.set_postfix_str(f"size={len(batch)}, time={batch_duration:.2f}s")

    batch_iterator.close()
    
    # Calculate and print total processing time
    total_duration = time.time() - start_total_time
    avg_batch_time = total_duration / total_batches if total_batches > 0 else 0
    print(f"\nTotal filtering time: {total_duration:.2f}s")
    print(f"Average batch time: {avg_batch_time:.2f}s")

    # Calculate overall statistics
    overall_stats = calculate_token_statistics(all_batch_results)

    return results, overall_stats, failed_samples, skipped_samples

async def process_batch(samples, batch_size=5):
    """
    Process samples in batches to avoid overwhelming the API with concurrent requests.

    Features:
        1. tqdm progress bar for batch processing visibility.
        2. Failed samples are logged via the configured logger, skipped, and stored for later reporting.
        3. Prints processing time for each batch.

    Args:
        samples: list of dataset samples to process
        batch_size: number of concurrent API calls per batch

    Returns:
        tuple: (list of processed data samples, overall token statistics dict, failed_samples list, skipped_samples list)
    """
    results = []
    failed_samples = []
    skipped_samples = []
    all_batch_results = []
    total_batches = (len(samples) + batch_size - 1) // batch_size
    start_total_time = time.time()

    batch_iterator = tqdm(
        range(0, len(samples), batch_size),
        total=total_batches if total_batches else None,
        desc="Processing batches",
        unit="batch"
    )

    for i in batch_iterator:
        batch = samples[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        # Record batch start time
        batch_start_time = time.time()
        
        batch_iterator.set_postfix_str(f"size={len(batch)}")

        tasks = [process_sample_v1_async(s) for s in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Record batch end time and calculate duration
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
        
        # Collect results and handle errors
        for idx, result in enumerate(batch_results):
            sample_index = i + idx
            if isinstance(result, Exception):
                error_msg = str(result)
                log_msg = f"Error processing sample {sample_index} (batch {batch_num}): {error_msg}"
                tqdm.write(f"  {log_msg}")
                logger.error(log_msg)
                failed_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'error': error_msg
                })
                continue
            if not result:
                log_msg = f"Skip processing sample {sample_index} (batch {batch_num})"
                tqdm.write(f"  {log_msg}")
                logger.info(log_msg)
                skipped_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'error': log_msg
                })
                continue
            data, token_usage = result
            results.append(data)

        all_batch_results.extend(batch_results)
        
        # Update postfix with batch processing time
        batch_iterator.set_postfix_str(f"size={len(batch)}, time={batch_duration:.2f}s")

    batch_iterator.close()
    
    # Calculate and print total processing time
    total_duration = time.time() - start_total_time
    avg_batch_time = total_duration / total_batches if total_batches > 0 else 0
    print(f"\nTotal processing time: {total_duration:.2f}s")
    print(f"Average batch time: {avg_batch_time:.2f}s")

    # Calculate overall statistics
    overall_stats = calculate_token_statistics(all_batch_results)

    return results, overall_stats, failed_samples,skipped_samples

def get_batch_info_from_sample_indices(sample_indices, batch_size):
    """
    Convert sample indices (from process_batch) to batch_index and sample_ids_in_batch.
    
    Args:
        sample_indices: list of int, global sample indices (0-based, same as sample_index in process_batch)
        batch_size: int, batch size used in process_batch
    
    Returns:
        dict: {
            batch_index: [sample_ids_in_batch, ...]
        }
        Example: {1: [0, 2], 2: [1, 3]} means batch 1 has samples 0,2 and batch 2 has samples 1,3
    """
    batch_info = {}
    
    for sample_index in sample_indices:
        # Calculate batch_index (1-based) from sample_index
        batch_index = (sample_index // batch_size) + 1
        # Calculate sample_id_in_batch (0-based)
        sample_id_in_batch = sample_index % batch_size
        
        if batch_index not in batch_info:
            batch_info[batch_index] = []
        
        if sample_id_in_batch not in batch_info[batch_index]:
            batch_info[batch_index].append(sample_id_in_batch)
    
    # Sort sample_ids_in_batch for each batch
    for batch_index in batch_info:
        batch_info[batch_index].sort()
    
    return batch_info

def query_samples_by_batch_and_ids(samples, batch_size, batch_index, sample_ids_in_batch):
    """
    Query problematic samples based on batch index and in-batch sample ids.

    Args:
        samples: list of dataset samples (same list passed into process_batch)
        batch_size: int, batch size used in process_batch
        batch_index: int, 1-based batch index (same as logged in failed_samples['batch_index'])
        sample_ids_in_batch: list of int, indices within the batch (0-based, 0..batch_size-1)

    Returns:
        list of samples corresponding to the specified batch and in-batch ids
    """
    if batch_index <= 0:
        raise ValueError("batch_index should be 1-based and >= 1")

    start = (batch_index - 1) * batch_size
    problem_samples = []

    for in_batch_id in sample_ids_in_batch:
        if in_batch_id < 0:
            continue
        global_idx = start + in_batch_id
        if 0 <= global_idx < len(samples):
            problem_samples.append(samples[global_idx])

    return problem_samples
async def main():
    """
    Main async function to process the dataset
    """
    # parser = argparse.ArgumentParser(description="process dataset")
    # parser.add_argument('--dataset_path',type=str,required=True,help='Path to the dataset directory')
    # args = parser.parse_args()

    sample_size = 50
    batch_size = 10  # Number of concurrent API calls

    print("Loading dataset...")
    #dataset = datasets.load_from_disk('/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-need-rewrite')
    dataset = datasets.load_from_disk('/data/lhy/datasets/1210/Toucan-SFT-v4/multi-turn-miss-param-data')
    print("Filtering modified samples...")
    modified_samples = dataset.filter(lambda x: x['is_modified'] and json.loads(x['modification_info']).get('modified_type') == 'miss-param'and x['subset_name'] == 'multi-turn')
    print(f"Found {len(modified_samples)} modified samples")

    # Random sample target subset
    print(f"Sampling {sample_size} samples...")
    #sampled_modified_samples = modified_samples.shuffle(seed=42).select(range(sample_size))
    sampled_modified_samples = modified_samples
    # Convert to list for async processing
    samples_list = [sampled_modified_samples[i] for i in range(len(sampled_modified_samples))]

    # check problem samples
    # batch_info = get_batch_info_from_sample_indices([5611,5612,5616], batch_size)
    # for batch_index, sample_ids_in_batch in batch_info.items():
    #     problematic_samples = query_samples_by_batch_and_ids(samples_list, batch_size, batch_index, sample_ids_in_batch)
    #     print(f"Found {len(problematic_samples)} problematic samples")
    #     for sample in problematic_samples:
    #         print(sample)
    #         print("******************")
    #         # print(sample['messages'])
    #         # print(sample['tools'])
    #         # print(sample['modification_info'])
    # assert 0
    # Process samples in batches
    print(f"\nStarting async processing with batch_size={batch_size}...")
    processed_results,token_stats,failed_samples,skip_samples = await process_batch(samples_list, batch_size=batch_size)


    # filter
    #processed_results, token_stats, failed_samples, skip_samples = await filter_batch(samples_list, batch_size=batch_size)
    failed_count = len(failed_samples)
    if failed_count > 0:
        print(f"\nWarning: {failed_count} samples failed to process")
        for failed in failed_samples:
            msg = f"  - Batch {failed['batch_index']}, sample {failed['sample_index']}: {failed['error']}"
            print(msg)
            logger.error(msg)

    skiped_count = len(skip_samples)
    if skiped_count > 0:
        print(f"\nWarning: {skiped_count} samples skiped to process")
        for skip in skip_samples:
            msg = f"  - Batch {skip['batch_index']}, sample {skip['sample_index']}"
            print(msg)
            logger.info(msg)
    successful_results = processed_results

    print(f"\nSuccessfully processed {len(successful_results)}/{len(samples_list)} samples")

    # print token usage info
    print_token_statistics(token_stats)
    
    # judge the result
    # tasks = []
    # for result in successful_results:
    #     user_query, conversation_history, target_tool, available_tools, response = extract_info(result)
    #     rule = generate_default_rule(user_query, conversation_history, target_tool, available_tools)
    #     tasks.append(rule_based_judge(response, rule))
    # judgments = await asyncio.gather(*tasks)

    # for index, judgment in enumerate(judgments):
    #     if not judgment['satisfied']:
    #         print(f"Judgment failed: {index}")
    #         print(judgment)
    #         raise ValueError(f"Judgment failed: {judgment}")
            

    # Convert back to dataset format
    if successful_results:
        # Create a new dataset from the processed results
        from datasets import Dataset
        test_data = Dataset.from_list(successful_results)

        # Save the processed dataset
        output_path = '/data/lhy/datasets/1202/Toucan-SFT-v3/multi-turn-miss-param-v8'
        print(f"\nSaving processed data to {output_path}...")
        test_data.save_to_disk(output_path)
        print("Done!")

        return test_data
    else:
        print("No samples were successfully processed!")
        return None

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
    