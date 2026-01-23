from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for arXiv research assistant.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - search_query (str): The original keyword query used for searching papers
        - result_0_title (str): Title of the first paper result
        - result_0_authors (str): Authors of the first paper (comma-separated)
        - result_0_id (str): arXiv ID of the first paper
        - result_0_categories (str): Categories of the first paper (comma-separated)
        - result_0_abstract (str): Abstract of the first paper
        - result_0_published_date (str): Published date of the first paper (ISO format)
        - result_1_title (str): Title of the second paper result
        - result_1_authors (str): Authors of the second paper (comma-separated)
        - result_1_id (str): arXiv ID of the second paper
        - result_1_categories (str): Categories of the second paper (comma-separated)
        - result_1_abstract (str): Abstract of the second paper
        - result_1_published_date (str): Published date of the second paper (ISO format)
    """
    return {
        "search_query": "machine learning",
        "result_0_title": "A Deep Learning Approach to Neural Networks",
        "result_0_authors": "John Doe, Jane Smith",
        "result_0_id": "2301.04567",
        "result_0_categories": "cs.LG, stat.ML",
        "result_0_abstract": "This paper presents a novel approach to deep learning using advanced neural network architectures.",
        "result_0_published_date": "2023-01-15T12:34:56Z",
        "result_1_title": "Transformers in Natural Language Processing",
        "result_1_authors": "Alice Johnson, Bob Lee",
        "result_1_id": "2302.08765",
        "result_1_categories": "cs.CL, cs.AI",
        "result_1_abstract": "We explore the application of transformer models to improve language understanding tasks.",
        "result_1_published_date": "2023-02-20T08:22:33Z"
    }

def arxiv_research_assistant_search_papers(keyword: str, max_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    키워드로 arXiv 논문을 검색합니다.

    Parameters:
        keyword (str): 검색할 키워드 (필수)
        max_results (Optional[int]): 반환할 최대 결과 수 (기본값: 10, 선택 사항)

    Returns:
        Dict containing:
            - results (List[Dict]): 논문 항목 리스트. 각 항목은 'title', 'authors', 'id', 'categories', 'abstract', 'published_date' 포함
            - search_query (str): 논문 검색에 사용된 원래 키워드 쿼리

    Raises:
        ValueError: keyword가 빈 문자열인 경우
    """
    if not keyword or not keyword.strip():
        raise ValueError("keyword must be a non-empty string")

    # 외부 API 호출 (가상)
    api_data = call_external_api("arxiv-research-assistant-search_papers")

    # 결과 리스트 구성
    results = [
        {
            "title": api_data["result_0_title"],
            "authors": api_data["result_0_authors"],
            "id": api_data["result_0_id"],
            "categories": api_data["result_0_categories"],
            "abstract": api_data["result_0_abstract"],
            "published_date": api_data["result_0_published_date"]
        },
        {
            "title": api_data["result_1_title"],
            "authors": api_data["result_1_authors"],
            "id": api_data["result_1_id"],
            "categories": api_data["result_1_categories"],
            "abstract": api_data["result_1_abstract"],
            "published_date": api_data["result_1_published_date"]
        }
    ]

    # max_results 적용
    limited_results = results[:max_results] if max_results is not None else results

    return {
        "results": limited_results,
        "search_query": keyword.strip()
    }