from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar paper recommendations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - paperId (str): unique identifier of the recommended paper in Semantic Scholar
        - corpusId (int): unique corpus identifier assigned by Semantic Scholar
        - externalIds_DOI (str): DOI identifier of the paper
        - externalIds_ArXiv (str): ArXiv identifier of the paper
        - externalIds_DBLP (str): DBLP identifier of the paper
        - externalIds_CorpusId (str): CorpusId as external identifier
        - url (str): direct URL to the paper on Semantic Scholar
        - title (str): title of the recommended paper
        - abstract (str): abstract or summary of the paper
        - venue (str): abbreviated venue name where the paper was published
        - publicationVenue (str): ID of the publication venue
        - year (int): year of publication
        - referenceCount (int): number of references cited in the paper
        - citationCount (int): total number of citations the paper has received
        - influentialCitationCount (int): count of influential citations
        - isOpenAccess (bool): indicates whether the paper is open access
        - openAccessPdf_url (str): URL to the open access PDF
        - openAccessPdf_status (str): status of the open access PDF
        - openAccessPdf_license (str): license type for the open access content
        - openAccessPdf_disclaimer (str): disclaimer about usage rights
        - fieldsOfStudy_0 (str): first research field associated with the paper
        - s2FieldsOfStudy_0_category (str): category of the first S2 field of study
        - s2FieldsOfStudy_0_source (str): source of the first S2 field of study
        - publicationTypes_0 (str): first type of publication (e.g., JournalArticle)
        - publicationDate (str): ISO-formatted publication date (YYYY-MM-DD)
        - journal_name (str): name of the journal
        - journal_volume (str): volume number of the journal
        - citationStyles_bibtex (str): BibTeX citation format
        - authors_0_authorId (str): ID of the first author
        - authors_0_name (str): name of the first author
    """
    return {
        "paperId": "1234567890abcdef1234567890abcdef",
        "corpusId": 123456789,
        "externalIds_DOI": "10.1234/example.doi",
        "externalIds_ArXiv": "2101.12345",
        "externalIds_DBLP": "conf/example/Author21",
        "externalIds_CorpusId": "123456789",
        "url": "https://www.semanticscholar.org/paper/1234567890abcdef",
        "title": "A Study on Artificial Intelligence and Machine Learning",
        "abstract": "This paper explores recent advances in artificial intelligence and machine learning, focusing on deep neural networks and their applications in natural language processing.",
        "venue": "AAAI",
        "publicationVenue": "aaai2021",
        "year": 2021,
        "referenceCount": 45,
        "citationCount": 123,
        "influentialCitationCount": 15,
        "isOpenAccess": True,
        "openAccessPdf_url": "https://arxiv.org/pdf/2101.12345.pdf",
        "openAccessPdf_status": "active",
        "openAccessPdf_license": "CC-BY-4.0",
        "openAccessPdf_disclaimer": "Usage subject to license terms.",
        "fieldsOfStudy_0": "Artificial Intelligence",
        "s2FieldsOfStudy_0_category": "Computer Science",
        "s2FieldsOfStudy_0_source": "s2-fos-model",
        "publicationTypes_0": "JournalArticle",
        "publicationDate": "2021-03-15",
        "journal_name": "Journal of Artificial Intelligence Research",
        "journal_volume": "70",
        "citationStyles_bibtex": "@article{example2021ai, author={John Doe and Jane Smith}, title={A Study on Artificial Intelligence and Machine Learning}, journal={Journal of Artificial Intelligence Research}, year={2021}, volume={70}, pages={1--20}}",
        "authors_0_authorId": "987654321",
        "authors_0_name": "John Doe"
    }

def semantic_scholar_academic_research_mcp_get_semantic_scholar_paper_recommendations(paper_id: str, limit: Optional[int] = 10) -> List[Dict[str, Any]]:
    """
    Get recommended papers for a single positive example paper from Semantic Scholar.
    
    Args:
        paper_id (str): ID of the paper to get recommendations for (positive example)
        limit (int, optional): Number of recommendations to return (default: 10, max: 500)
    
    Returns:
        List of dictionaries containing recommended papers similar to the input paper.
        Each dictionary contains the following fields:
        - paperId (str): unique identifier of the recommended paper in Semantic Scholar
        - corpusId (int): unique corpus identifier assigned by Semantic Scholar
        - externalIds (Dict): external identifiers such as DOI, ArXiv, DBLP, and CorpusId
        - url (str): direct URL to the paper on Semantic Scholar
        - title (str): title of the recommended paper
        - abstract (str): abstract or summary of the paper
        - venue (str): abbreviated venue name where the paper was published
        - publicationVenue (str or None): ID of the publication venue if available
        - year (int): year of publication
        - referenceCount (int): number of references cited in the paper
        - citationCount (int): total number of citations the paper has received
        - influentialCitationCount (int): count of influential citations
        - isOpenAccess (bool): indicates whether the paper is open access
        - openAccessPdf (Dict): contains 'url', 'status', 'license', and 'disclaimer'
        - fieldsOfStudy (List[str] or None): list of research fields associated with the paper
        - s2FieldsOfStudy (List[Dict]): list of fields of study with 'category' and 'source'
        - publicationTypes (List[str] or None): types of publication such as JournalArticle
        - publicationDate (str): ISO-formatted publication date (YYYY-MM-DD)
        - journal (Dict or None): journal information including 'name' and 'volume'
        - citationStyles (Dict): citation formats; currently includes 'bibtex'
        - authors (List[Dict]): list of author objects with 'authorId' and 'name'
    
    Raises:
        ValueError: If paper_id is empty or limit is not within valid range
    """
    if not paper_id or not paper_id.strip():
        raise ValueError("paper_id is required and cannot be empty")
    
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")
    
    if limit > 500:
        raise ValueError("limit cannot exceed 500")
    
    # Fetch simulated external data
    api_data = call_external_api("semantic-scholar-academic-research-mcp-get_semantic_scholar_paper_recommendations")
    
    # Construct externalIds dictionary
    external_ids = {
        "DOI": api_data["externalIds_DOI"],
        "ArXiv": api_data["externalIds_ArXiv"],
        "DBLP": api_data["externalIds_DBLP"],
        "CorpusId": api_data["externalIds_CorpusId"]
    }
    
    # Construct openAccessPdf dictionary
    open_access_pdf = {
        "url": api_data["openAccessPdf_url"],
        "status": api_data["openAccessPdf_status"],
        "license": api_data["openAccessPdf_license"],
        "disclaimer": api_data["openAccessPdf_disclaimer"]
    } if api_data["openAccessPdf_url"] else None
    
    # Construct fieldsOfStudy list
    fields_of_study = [api_data["fieldsOfStudy_0"]] if api_data["fieldsOfStudy_0"] else []
    
    # Construct s2FieldsOfStudy list
    s2_fields_of_study = [{
        "category": api_data["s2FieldsOfStudy_0_category"],
        "source": api_data["s2FieldsOfStudy_0_source"]
    }] if api_data["s2FieldsOfStudy_0_category"] else []
    
    # Construct publicationTypes list
    publication_types = [api_data["publicationTypes_0"]] if api_data["publicationTypes_0"] else []
    
    # Construct journal dictionary
    journal = {
        "name": api_data["journal_name"],
        "volume": api_data["journal_volume"]
    } if api_data["journal_name"] else None
    
    # Construct citationStyles dictionary
    citation_styles = {
        "bibtex": api_data["citationStyles_bibtex"]
    }
    
    # Construct authors list
    authors = [{
        "authorId": api_data["authors_0_authorId"],
        "name": api_data["authors_0_name"]
    }] if api_data["authors_0_name"] else []
    
    # Construct the recommended paper object
    recommended_paper = {
        "paperId": api_data["paperId"],
        "corpusId": api_data["corpusId"],
        "externalIds": external_ids,
        "url": api_data["url"],
        "title": api_data["title"],
        "abstract": api_data["abstract"],
        "venue": api_data["venue"],
        "publicationVenue": api_data["publicationVenue"] if api_data["publicationVenue"] else None,
        "year": api_data["year"],
        "referenceCount": api_data["referenceCount"],
        "citationCount": api_data["citationCount"],
        "influentialCitationCount": api_data["influentialCitationCount"],
        "isOpenAccess": api_data["isOpenAccess"],
        "openAccessPdf": open_access_pdf,
        "fieldsOfStudy": fields_of_study,
        "s2FieldsOfStudy": s2_fields_of_study,
        "publicationTypes": publication_types,
        "publicationDate": api_data["publicationDate"],
        "journal": journal,
        "citationStyles": citation_styles,
        "authors": authors
    }
    
    # Return list of recommended papers (limit determines count, all identical for simulation)
    return [recommended_paper for _ in range(limit)]