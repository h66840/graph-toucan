from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching AI daily news data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - news_item_0_index (int): Rank/index of the first news item
        - news_item_0_title (str): Headline of the first news item
        - news_item_0_summary (str): Detailed summary of the first news item
        - news_item_1_index (int): Rank/index of the second news item
        - news_item_1_title (str): Headline of the second news item
        - news_item_1_summary (str): Detailed summary of the second news item
    """
    return {
        "news_item_0_index": 1,
        "news_item_0_title": "Google Unveils New Multimodal AI Model",
        "news_item_0_summary": "Google has introduced a new multimodal AI model capable of processing text, images, and audio simultaneously. The model, named Gemini Advanced, demonstrates state-of-the-art performance across multiple benchmarks and is expected to power future applications in search, content creation, and accessibility tools.",
        "news_item_1_index": 2,
        "news_item_1_title": "OpenAI Launches GPT-4o with Real-Time Voice Capabilities",
        "news_item_1_summary": "OpenAI has released GPT-4o, an optimized version of GPT-4 with enhanced real-time voice interaction capabilities. The new model supports natural-sounding conversations with low latency, enabling applications in customer service, language learning, and personal assistants."
    }

def aidaily_spider_ai_daily() -> Dict[str, Any]:
    """
    Fetches and structures AI daily news items from external source.
    
    This function retrieves AI-related news from a simulated external API and formats
    it into a structured list of news items containing index, title, and summary.
    
    Returns:
        Dict containing:
            - news_items (List[Dict]): List of news items with 'index', 'title', and 'summary' fields
              where each item represents a significant AI development.
    
    Raises:
        KeyError: If expected fields are missing from the API response
        ValueError: If data types are invalid or inconsistent
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("aidaily-spider_ai_daily")
        
        # Validate required fields are present
        required_fields = [
            "news_item_0_index", "news_item_0_title", "news_item_0_summary",
            "news_item_1_index", "news_item_1_title", "news_item_1_summary"
        ]
        
        for field in required_fields:
            if field not in api_data:
                raise KeyError(f"Missing required field: {field}")
        
        # Construct news items list from flat API data
        news_items: List[Dict[str, Any]] = [
            {
                "index": int(api_data["news_item_0_index"]),
                "title": str(api_data["news_item_0_title"]),
                "summary": str(api_data["news_item_0_summary"])
            },
            {
                "index": int(api_data["news_item_1_index"]),
                "title": str(api_data["news_item_1_title"]),
                "summary": str(api_data["news_item_1_summary"])
            }
        ]
        
        # Sort by index to ensure correct ordering
        news_items.sort(key=lambda x: x["index"])
        
        # Return structured result
        return {
            "news_items": news_items
        }
        
    except (TypeError, ValueError) as e:
        raise ValueError(f"Data type error in processing news items: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error in aidaily_spider_ai_daily: {str(e)}")