from typing import Dict, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for inspirational English sentence.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - sentence (str): The inspirational English sentence
        - translation (str): Chinese translation of the sentence
        - author (str): Author or source of the sentence
        - date (str): Date associated with the sentence in YYYY-MM-DD format
        - success (bool): Whether the request was successful
        - error_message (str): Error details if the request failed
    """
    sentences = [
        {
            "sentence": "Believe you can and you're halfway there.",
            "translation": "相信你能做到，你已经成功了一半。",
            "author": "Theodore Roosevelt",
            "date": "2023-11-15"
        },
        {
            "sentence": "The only way to do great work is to love what you do.",
            "translation": "做出伟大工作的唯一方法就是热爱你所做的事。",
            "author": "Steve Jobs",
            "date": "2023-11-16"
        },
        {
            "sentence": "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "translation": "成功不是终点，失败也并非末日：最重要的是继续前进的勇气。",
            "author": "Winston Churchill",
            "date": "2023-11-17"
        },
        {
            "sentence": "Don't watch the clock; do what it does. Keep going.",
            "translation": "不要盯着时钟看，要像它一样行动：继续前进。",
            "author": "Sam Levenson",
            "date": "2023-11-18"
        },
        {
            "sentence": "The future belongs to those who believe in the beauty of their dreams.",
            "translation": "未来属于那些相信自己梦想之美的人。",
            "author": "Eleanor Roosevelt",
            "date": "2023-11-19"
        }
    ]

    # Simulate random selection if needed
    selected = random.choice(sentences) if tool_name == "pulse-cn-mcp-server-get-inspirational-english-sentence" else sentences[0]

    return {
        "sentence": selected["sentence"],
        "translation": selected["translation"],
        "author": selected["author"],
        "date": selected["date"],
        "success": True,
        "error_message": ""
    }


def pulse_cn_mcp_server_get_inspirational_english_sentence(random: Optional[bool] = None) -> Dict[str, Any]:
    """
    获取每日一句励志英语句子，返回包含句子实时数据。通过API实时获取。

    Args:
        random (bool, optional): 是否随机获取一句英语句子。如果为True，则从语录库中随机选择；
                                 如果为False或未提供，则返回默认（或当日）语录。

    Returns:
        Dict[str, Any]: 包含以下键的字典：
            - sentence (str): 励志英文句子
            - translation (str): 句子的中文翻译
            - author (str): 作者或来源（如可用）
            - date (str): 与句子关联的日期（格式：YYYY-MM-DD）
            - success (bool): 请求是否成功
            - error_message (str): 如果请求失败，包含错误详情
    """
    try:
        # Call external API simulation
        api_data = call_external_api("pulse-cn-mcp-server-get-inspirational-english-sentence")

        # If random is False, we could return a fixed sentence (e.g., based on date)
        # But since we're simulating API, we respect the API's behavior unless specified
        if random is False:
            # For deterministic behavior when random=False, use a date-based seed
            today = datetime.now().date().isoformat()
            fixed_sentences = [
                {
                    "sentence": "Every day is a new beginning.",
                    "translation": "每一天都是新的开始。",
                    "author": "Unknown",
                    "date": today
                }
            ]
            fixed = fixed_sentences[0]
            result = {
                "sentence": fixed["sentence"],
                "translation": fixed["translation"],
                "author": fixed["author"],
                "date": fixed["date"],
                "success": True,
                "error_message": ""
            }
        else:
            # Use the randomly selected one from API simulation
            result = {
                "sentence": api_data["sentence"],
                "translation": api_data["translation"],
                "author": api_data["author"],
                "date": api_data["date"],
                "success": api_data["success"],
                "error_message": api_data["error_message"]
            }

        return result

    except Exception as e:
        return {
            "sentence": "",
            "translation": "",
            "author": "",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "success": False,
            "error_message": str(e)
        }