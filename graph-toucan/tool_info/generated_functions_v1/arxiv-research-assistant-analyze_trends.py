from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for arxiv-research-assistant-analyze_trends.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - trend_analysis_title (str): Title of the trend analysis report including category and time period
        - popular_keyword_0 (str): First popular keyword in recent papers
        - popular_keyword_1 (str): Second popular keyword in recent papers
        - popular_topic_0 (str): First trending research topic
        - popular_topic_1 (str): Second trending research topic
    """
    return {
        "trend_analysis_title": "Trend Analysis for Machine Learning - Last 7 Days",
        "popular_keyword_0": "deep learning",
        "popular_keyword_1": "neural networks",
        "popular_topic_0": "Efficient Transformers for NLP",
        "popular_topic_1": "Self-supervised Learning in Computer Vision"
    }


def arxiv_research_assistant_analyze_trends(category: Optional[str] = None, days: Optional[int] = None) -> Dict[str, Any]:
    """
    Analyzes recent trends in a specific ArXiv category over a given number of days.

    Args:
        category (Optional[str]): The ArXiv category to analyze (e.g., 'cs.LG', 'physics.optics'). Defaults to 'cs.LG' if not provided.
        days (Optional[int]): Number of recent days to include in the analysis. Defaults to 7 if not provided.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - trend_analysis_title (str): Title of the trend analysis report
            - popular_keywords (List[str]): List of popular keywords identified
            - popular_paper_topics (List[str]): List of trending research topics
    """
    # Set default values if not provided
    category = category or "cs.LG"
    days = days or 7

    # Fetch simulated external data
    api_data = call_external_api("arxiv-research-assistant-analyze_trends")

    # Construct output structure from flat API response
    result = {
        "trend_analysis_title": api_data["trend_analysis_title"],
        "popular_keywords": [
            api_data["popular_keyword_0"],
            api_data["popular_keyword_1"]
        ],
        "popular_paper_topics": [
            api_data["popular_topic_0"],
            api_data["popular_topic_1"]
        ]
    }

    # Optionally update title based on actual inputs (more realistic simulation)
    result["trend_analysis_title"] = f"Trend Analysis for {category} - Last {days} Days"

    # For demonstration, adjust keywords and topics slightly based on category
    if "nlp" in category.lower() or "language" in category.lower():
        result["popular_keywords"] = ["transformers", "large language models"]
        result["popular_paper_topics"] = ["Multilingual Pretraining", "Prompt Engineering"]
    elif "vision" in category.lower() or "cv" in category.lower():
        result["popular_keywords"] = ["convolutional networks", "object detection"]
        result["popular_paper_topics"] = ["Vision Transformers", "Few-shot Image Classification"]
    elif "quantum" in category.lower():
        result["popular_keywords"] = ["quantum computing", "entanglement"]
        result["popular_paper_topics"] = ["Quantum Error Correction", "NISQ Devices"]

    return result