from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for crypto news articles.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - article_0_title (str): Title of the first article
        - article_0_link (str): URL link of the first article
        - article_0_pubDate (str): Publication date of the first article in ISO format
        - article_0_description (str): Description of the first article
        - article_1_title (str): Title of the second article
        - article_1_link (str): URL link of the second article
        - article_1_pubDate (str): Publication date of the second article in ISO format
        - article_1_description (str): Description of the second article
    """
    return {
        "article_0_title": "Deep Dive into Ethereum's Layer 2 Scaling Solutions",
        "article_0_link": "https://example.com/ethereum-l2-research",
        "article_0_pubDate": "2023-10-05T08:00:00Z",
        "article_0_description": "A comprehensive analysis of Ethereum's current Layer 2 ecosystem including Optimism, Arbitrum, and zkSync.",
        
        "article_1_title": "Bitcoin Mining Trends in 2023: Efficiency and Sustainability",
        "article_1_link": "https://example.com/bitcoin-mining-2023",
        "article_1_pubDate": "2023-10-04T12:30:00Z",
        "article_1_description": "Exploring how Bitcoin miners are adapting to rising energy costs and regulatory pressures with new efficiency measures."
    }

def news_feed_server_getArticles() -> List[Dict[str, str]]:
    """
    Get the latest crypto-related articles. Articles are always about deep research of a crypto project or company.
    They may also include analysis of the crypto market and related topics.
    
    Returns:
        List[Dict]: A list of news articles, each containing 'title', 'link', 'pubDate', and 'description' fields.
        Each article is represented as a dictionary with string values for all fields.
        
    Example:
        [
            {
                'title': 'Deep Dive into Ethereum Layer 2',
                'link': 'https://example.com/ethereum-l2',
                'pubDate': '2023-10-05T08:00:00Z',
                'description': 'Comprehensive analysis of Ethereum Layer 2 solutions...'
            }
        ]
    """
    try:
        # Fetch flattened data from simulated external API
        api_data = call_external_api("news-feed-server-getArticles")
        
        # Construct the list of articles from flattened API response
        articles = [
            {
                "title": api_data["article_0_title"],
                "link": api_data["article_0_link"],
                "pubDate": api_data["article_0_pubDate"],
                "description": api_data["article_0_description"]
            },
            {
                "title": api_data["article_1_title"],
                "link": api_data["article_1_link"],
                "pubDate": api_data["article_1_pubDate"],
                "description": api_data["article_1_description"]
            }
        ]
        
        return articles
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"Failed to retrieve articles: {str(e)}")