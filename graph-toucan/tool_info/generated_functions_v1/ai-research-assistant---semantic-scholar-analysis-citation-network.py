from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for semantic scholar analysis.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - main_paper_title (str): Title of the main paper
        - main_paper_year (int): Publication year of the main paper
        - main_paper_authors (str): Comma-separated authors of the main paper
        - main_paper_venue (str): Venue where the main paper was published
        - main_paper_citation_count (int): Number of citations for the main paper
        - cited_paper_0_title (str): Title of the first cited paper
        - cited_paper_0_year (int): Year of the first cited paper
        - cited_paper_0_authors (str): Authors of the first cited paper
        - cited_paper_0_citation_count (int): Citation count of the first cited paper
        - cited_paper_0_influential (bool): Whether the first cited paper is influential
        - cited_paper_1_title (str): Title of the second cited paper
        - cited_paper_1_year (int): Year of the second cited paper
        - cited_paper_1_authors (str): Authors of the second cited paper
        - cited_paper_1_citation_count (int): Citation count of the second cited paper
        - cited_paper_1_influential (bool): Whether the second cited paper is influential
        - citing_paper_0_title (str): Title of the first citing paper
        - citing_paper_0_year (int): Year of the first citing paper
        - citing_paper_0_authors (str): Authors of the first citing paper
        - citing_paper_0_citation_count (int): Citation count of the first citing paper
        - citing_paper_1_title (str): Title of the second citing paper
        - citing_paper_1_year (int): Year of the second citing paper
        - citing_paper_1_authors (str): Authors of the second citing paper
        - citing_paper_1_citation_count (int): Citation count of the second citing paper
        - influential_citations_count (int): Number of influential citing papers
        - total_citations_displayed (int): Total number of citing papers returned
        - influential_references_count (int): Number of influential cited papers
        - total_references_displayed (int): Total number of cited papers returned
    """
    return {
        "main_paper_title": "Attention Is All You Need",
        "main_paper_year": 2017,
        "main_paper_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin",
        "main_paper_venue": "NeurIPS",
        "main_paper_citation_count": 45000,
        "cited_paper_0_title": "Neural Machine Translation by Jointly Learning to Align and Translate",
        "cited_paper_0_year": 2015,
        "cited_paper_0_authors": "Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio",
        "cited_paper_0_citation_count": 28000,
        "cited_paper_0_influential": True,
        "cited_paper_1_title": "Deep Residual Learning for Image Recognition",
        "cited_paper_1_year": 2016,
        "cited_paper_1_authors": "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun",
        "cited_paper_1_citation_count": 120000,
        "cited_paper_1_influential": True,
        "citing_paper_0_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "citing_paper_0_year": 2018,
        "citing_paper_0_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "citing_paper_0_citation_count": 60000,
        "citing_paper_1_title": "GPT-3: Language Models are Few-Shot Learners",
        "citing_paper_1_year": 2020,
        "citing_paper_1_authors": "Tom B. Brown, Benjamin Mann, Nick Ryder, et al.",
        "citing_paper_1_citation_count": 25000,
        "influential_citations_count": 2,
        "total_citations_displayed": 2,
        "influential_references_count": 2,
        "total_references_displayed": 2
    }

def ai_research_assistant_semantic_scholar_analysis_citation_network(
    paperId: str,
    citationsLimit: Optional[int] = None,
    depth: Optional[str] = None,
    referencesLimit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Analyze the citation network for a specific paper using Semantic Scholar data.

    Args:
        paperId (str): Paper ID (Semantic Scholar ID, arXiv ID, DOI, etc.) - required
        citationsLimit (Optional[int]): Maximum number of citations to analyze per paper
        depth (Optional[str]): Depth of citation network ("1" or "2")
        referencesLimit (Optional[int]): Maximum number of references to analyze per paper

    Returns:
        Dict containing:
        - main_paper (Dict): Basic info about the central paper
        - cited_papers (List[Dict]): Papers directly cited by the main paper
        - citing_papers (List[Dict]): Papers that cite the main paper
        - influential_citations_count (int): Number of influential papers among those citing the main paper
        - total_citations_displayed (int): Total number of citing papers returned
        - influential_references_count (int): Number of influential papers among those cited by the main paper
        - total_references_displayed (int): Total number of cited papers returned

    Raises:
        ValueError: If paperId is empty or invalid
    """
    if not paperId or not paperId.strip():
        raise ValueError("paperId is required and cannot be empty")

    if depth and depth not in ["1", "2"]:
        raise ValueError("depth must be '1' or '2'")

    if citationsLimit is not None and citationsLimit < 0:
        raise ValueError("citationsLimit must be non-negative")

    if referencesLimit is not None and referencesLimit < 0:
        raise ValueError("referencesLimit must be non-negative")

    # Fetch simulated external data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-analysis-citation-network")

    # Construct main_paper object
    main_paper = {
        "title": api_data["main_paper_title"],
        "year": api_data["main_paper_year"],
        "authors": api_data["main_paper_authors"],
        "venue": api_data["main_paper_venue"],
        "citation_count": api_data["main_paper_citation_count"]
    }

    # Construct cited_papers list
    cited_papers = [
        {
            "title": api_data["cited_paper_0_title"],
            "year": api_data["cited_paper_0_year"],
            "authors": api_data["cited_paper_0_authors"],
            "citation_count": api_data["cited_paper_0_citation_count"],
            "influential": api_data["cited_paper_0_influential"]
        },
        {
            "title": api_data["cited_paper_1_title"],
            "year": api_data["cited_paper_1_year"],
            "authors": api_data["cited_paper_1_authors"],
            "citation_count": api_data["cited_paper_1_citation_count"],
            "influential": api_data["cited_paper_1_influential"]
        }
    ]

    # Apply referencesLimit if specified
    if referencesLimit is not None:
        cited_papers = cited_papers[:referencesLimit]

    # Construct citing_papers list
    citing_papers = [
        {
            "title": api_data["citing_paper_0_title"],
            "year": api_data["citing_paper_0_year"],
            "authors": api_data["citing_paper_0_authors"],
            "citation_count": api_data["citing_paper_0_citation_count"]
        },
        {
            "title": api_data["citing_paper_1_title"],
            "year": api_data["citing_paper_1_year"],
            "authors": api_data["citing_paper_1_authors"],
            "citation_count": api_data["citing_paper_1_citation_count"]
        }
    ]

    # Apply citationsLimit if specified
    if citationsLimit is not None:
        citing_papers = citing_papers[:citationsLimit]

    # Build final result
    result = {
        "main_paper": main_paper,
        "cited_papers": cited_papers,
        "citing_papers": citing_papers,
        "influential_citations_count": api_data["influential_citations_count"],
        "total_citations_displayed": len(citing_papers),
        "influential_references_count": api_data["influential_references_count"],
        "total_references_displayed": len(cited_papers)
    }

    return result