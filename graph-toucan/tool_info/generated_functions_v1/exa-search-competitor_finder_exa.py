from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching competitor data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - competitor_0_name (str): Name of the first competitor
        - competitor_0_similarity_reason (str): Reason why this company is a competitor
        - competitor_0_market_positioning (str): Market positioning of the first competitor
        - competitor_0_key_attributes (str): Key attributes of the first competitor
        - competitor_1_name (str): Name of the second competitor
        - competitor_1_similarity_reason (str): Reason why this company is a competitor
        - competitor_1_market_positioning (str): Market positioning of the second competitor
        - competitor_1_key_attributes (str): Key attributes of the second competitor
        - analysis_summary_market_segmentation (str): Overview of market segmentation
        - analysis_summary_direct_vs_indirect (str): Analysis of direct vs indirect competitors
        - analysis_summary_industry_trends (str): Current industry trends
        - total_count (int): Total number of competitors identified
        - query_metadata_timestamp (str): Timestamp of the query
        - query_metadata_confidence_score (float): Confidence score of the results
        - query_metadata_source_references (str): Source references used in the search
    """
    return {
        "competitor_0_name": "TechNova Inc.",
        "competitor_0_similarity_reason": "Offers similar AI-powered analytics platform targeting enterprise clients.",
        "competitor_0_market_positioning": "Premium pricing, enterprise-focused, global reach",
        "competitor_0_key_attributes": "Cloud-native, real-time processing, strong security compliance",
        "competitor_1_name": "DataSphere Labs",
        "competitor_1_similarity_reason": "Provides competing data visualization and business intelligence tools.",
        "competitor_1_market_positioning": "Mid-market focus, subscription-based pricing",
        "competitor_1_key_attributes": "User-friendly interface, integrations with major CRM platforms",
        "analysis_summary_market_segmentation": "Market segmented by enterprise, mid-market, and SMBs; enterprise segment growing fastest.",
        "analysis_summary_direct_vs_indirect": "Direct competitors focus on analytics platforms; indirect include broader BI suites.",
        "analysis_summary_industry_trends": "Increasing demand for real-time analytics, AI integration, and data governance features.",
        "total_count": 7,
        "query_metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "query_metadata_confidence_score": 0.92,
        "query_metadata_source_references": "Exa proprietary index, Crunchbase, G2, industry reports"
    }


def exa_search_competitor_finder_exa(companyName: str, industry: Optional[str] = None, numResults: Optional[int] = 5) -> Dict[str, Any]:
    """
    Find competitors for a business using Exa AI - identifies similar companies, competitive landscape analysis, and market positioning.
    Helps discover direct and indirect competitors in any industry.

    Args:
        companyName (str): Name of the company to find competitors for
        industry (Optional[str]): Industry sector (optional, helps narrow search)
        numResults (Optional[int]): Number of competitors to find (default: 5)

    Returns:
        Dict containing:
        - competitors (List[Dict]): List of competitor companies with details such as name, similarity reason, market positioning, and key attributes
        - analysis_summary (Dict): High-level insights about the competitive landscape including market segmentation, direct vs. indirect competitors, and industry trends
        - total_count (int): Total number of competitors identified
        - query_metadata (Dict): Metadata about the search query including timestamp, confidence scores, and source references

    Raises:
        ValueError: If companyName is empty or invalid
    """
    if not companyName or not companyName.strip():
        raise ValueError("companyName is required and cannot be empty")

    if numResults is None:
        numResults = 5
    if numResults <= 0:
        raise ValueError("numResults must be a positive integer")

    # Fetch simulated external data
    api_data = call_external_api("exa-search-competitor_finder_exa")

    # Construct competitors list from indexed fields
    competitors = []
    for i in range(min(numResults, 2)):  # Only 2 simulated competitors available
        competitor = {
            "name": api_data.get(f"competitor_{i}_name", ""),
            "similarity_reason": api_data.get(f"competitor_{i}_similarity_reason", ""),
            "market_positioning": api_data.get(f"competitor_{i}_market_positioning", ""),
            "key_attributes": api_data.get(f"competitor_{i}_key_attributes", "")
        }
        competitors.append(competitor)

    # Construct analysis summary
    analysis_summary = {
        "market_segmentation": api_data["analysis_summary_market_segmentation"],
        "direct_vs_indirect": api_data["analysis_summary_direct_vs_indirect"],
        "industry_trends": api_data["analysis_summary_industry_trends"]
    }

    # Construct query metadata
    query_metadata = {
        "timestamp": api_data["query_metadata_timestamp"],
        "confidence_score": api_data["query_metadata_confidence_score"],
        "source_references": api_data["query_metadata_source_references"]
    }

    # Final result structure
    result = {
        "competitors": competitors,
        "analysis_summary": analysis_summary,
        "total_count": api_data["total_count"],
        "query_metadata": query_metadata
    }

    return result