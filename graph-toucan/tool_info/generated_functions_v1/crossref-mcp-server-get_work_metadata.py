from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Crossref work metadata.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): status of the response (e.g., "ok")
        - message_type (str): type of message returned, e.g., "work"
        - message_version (str): version of the message format
        - doi (str): digital object identifier for the work
        - title_0 (str): main title of the work
        - subtitle_0 (str): subtitle of the work, if any
        - published_date_parts_0_0 (int): year of publication
        - published_date_parts_0_1 (int): month of publication
        - published_date_parts_0_2 (int): day of publication
        - created_date_parts_0_0 (int): year when record was created
        - created_date_parts_0_1 (int): month when record was created
        - created_date_parts_0_2 (int): day when record was created
        - created_date_time (str): ISO timestamp when record was created
        - created_timestamp (int): Unix timestamp when record was created
        - indexed_date_parts_0_0 (int): year of indexing
        - indexed_date_parts_0_1 (int): month of indexing
        - indexed_date_parts_0_2 (int): day of indexing
        - indexed_date_time (str): ISO timestamp of indexing
        - indexed_timestamp (int): Unix timestamp of indexing
        - updated_date_parts_0_0 (int): year of last update
        - updated_date_parts_0_1 (int): month of last update
        - updated_date_parts_0_2 (int): day of last update
        - updated_date_time (str): ISO timestamp of last update
        - updated_timestamp (int): Unix timestamp of last update
        - publisher (str): name of the publisher
        - container_title_0 (str): title of the journal or container
        - short_container_title_0 (str): abbreviated journal or container title
        - volume (str): volume number of the journal
        - issue (str): issue number within the volume
        - page (str): page range of the article
        - URL (str): human-readable URL to the work
        - resource_primary_URL (str): primary access link to the work
        - ISSN_0 (str): first ISSN value (e.g., print)
        - ISSN_1 (str): second ISSN value (e.g., electronic)
        - issn_type_0_type (str): type of first ISSN ("print" or "electronic")
        - issn_type_0_value (str): value of first ISSN
        - issn_type_1_type (str): type of second ISSN ("print" or "electronic")
        - issn_type_1_value (str): value of second ISSN
        - author_0_given (str): first name of first author
        - author_0_family (str): last name of first author
        - author_0_sequence (str): sequence ("first" or "additional") of first author
        - author_0_ORCID (str): ORCID of first author
        - reference_count (int): number of references cited by the work
        - references_0_DOI (str): DOI of first reference
        - references_0_author (str): author of first reference
        - references_0_year (int): year of first reference
        - references_0_journal_title (str): journal title of first reference
        - references_0_unstructured (str): unstructured citation string for first reference
        - license_0_start_date_parts_0_0 (int): year license starts
        - license_0_start_date_parts_0_1 (int): month license starts
        - license_0_start_date_parts_0_2 (int): day license starts
        - license_0_content_version (str): content version under license
        - license_0_delay_in_days (int): embargo delay in days
        - license_0_URL (str): URL to license terms
        - subject_0 (str): first subject category or keyword
        - subject_1 (str): second subject category or keyword
        - language (str): language of the work (e.g., "en")
        - link_0_URL (str): URL of first full-text link
        - link_0_content_type (str): content type of first link
        - link_0_content_version (str): content version of first link
        - link_0_intended_application (str): intended application of first link
        - deposited_date_parts_0_0 (int): year metadata was deposited
        - deposited_date_parts_0_1 (int): month metadata was deposited
        - deposited_date_parts_0_2 (int): day metadata was deposited
        - deposited_timestamp (int): Unix timestamp when metadata was deposited
        - score (float): relevance score assigned by Crossref
        - type (str): type of work (e.g., "journal-article")
        - prefix (str): DOI prefix (e.g., "10.1038")
        - member (str): Crossref member ID of the publisher
        - is_referenced_by_count (int): number of works that cite this article
        - alternative_id_0 (str): first alternative identifier for the article
        - assertion_0_name (str): name of first editorial assertion
        - assertion_0_value (str): value of first editorial assertion
        - assertion_0_group_name (str): group name of first editorial assertion
        - assertion_0_group_title (str): group title of first editorial assertion
        - relation_is_preprint_of_DOI (str): DOI of preprint relationship
        - update_policy (str): URL to the update policy for the record
        - source (str): source system (e.g., "Crossref")
        - content_domain_domain_0 (str): first domain in content domain
        - content_domain_crossmark_restriction (bool): whether crossmark restriction applies
    """
    return {
        "status": "ok",
        "message_type": "work",
        "message_version": "1.0",
        "doi": "10.1038/nature12373",
        "title_0": "A highly potent and selective VISTA antagonist antibody",
        "subtitle_0": "Development and characterization of anti-VISTA antibodies",
        "published_date_parts_0_0": 2023,
        "published_date_parts_0_1": 5,
        "published_date_parts_0_2": 15,
        "created_date_parts_0_0": 2023,
        "created_date_parts_0_1": 4,
        "created_date_parts_0_2": 10,
        "created_date_time": "2023-04-10T12:30:45Z",
        "created_timestamp": 1681129845,
        "indexed_date_parts_0_0": 2023,
        "indexed_date_parts_0_1": 4,
        "indexed_date_parts_0_2": 12,
        "indexed_date_time": "2023-04-12T08:15:30Z",
        "indexed_timestamp": 1681296930,
        "updated_date_parts_0_0": 2023,
        "updated_date_parts_0_1": 5,
        "updated_date_parts_0_2": 1,
        "updated_date_time": "2023-05-01T14:20:10Z",
        "updated_timestamp": 1682953210,
        "publisher": "Nature Publishing Group",
        "container_title_0": "Nature",
        "short_container_title_0": "Nature",
        "volume": "617",
        "issue": "7961",
        "page": "567-572",
        "URL": "https://doi.org/10.1038/nature12373",
        "resource_primary_URL": "https://www.nature.com/articles/nature12373",
        "ISSN_0": "0028-0836",
        "ISSN_1": "1476-4687",
        "issn_type_0_type": "print",
        "issn_type_0_value": "0028-0836",
        "issn_type_1_type": "electronic",
        "issn_type_1_value": "1476-4687",
        "author_0_given": "John",
        "author_0_family": "Doe",
        "author_0_sequence": "first",
        "author_0_ORCID": "https://orcid.org/0000-0002-1825-0097",
        "reference_count": 45,
        "references_0_DOI": "10.1038/nature12374",
        "references_0_author": "Jane Smith",
        "references_0_year": 2022,
        "references_0_journal_title": "Nature",
        "references_0_unstructured": "Smith, J. et al. Discovery of VISTA inhibitors. Nature 615, 345–350 (2022).",
        "license_0_start_date_parts_0_0": 2023,
        "license_0_start_date_parts_0_1": 5,
        "license_0_start_date_parts_0_2": 15,
        "license_0_content_version": "vor",
        "license_0_delay_in_days": 0,
        "license_0_URL": "https://creativecommons.org/licenses/by/4.0/",
        "subject_0": "Immunology",
        "subject_1": "Cancer Research",
        "language": "en",
        "link_0_URL": "https://www.nature.com/articles/nature12373.pdf",
        "link_0_content_type": "application/pdf",
        "link_0_content_version": "vor",
        "link_0_intended_application": "text-mining",
        "deposited_date_parts_0_0": 2023,
        "deposited_date_parts_0_1": 4,
        "deposited_date_parts_0_2": 10,
        "deposited_timestamp": 1681129845,
        "score": 1.0,
        "type": "journal-article",
        "prefix": "10.1038",
        "member": "7812",
        "is_referenced_by_count": 12,
        "alternative_id_0": "NATURE-12373",
        "assertion_0_name": "received",
        "assertion_0_value": "2022-10-15",
        "assertion_0_group_name": "publication_history",
        "assertion_0_group_title": "Publication History",
        "relation_is_preprint_of_DOI": "10.1101/2023.01.01.498273",
        "update_policy": "https://doi.org/10.1038/update-policy",
        "source": "Crossref",
        "content_domain_domain_0": "www.nature.com",
        "content_domain_crossmark_restriction": True
    }

def crossref_mcp_server_get_work_metadata(doi: str, mailto: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve metadata for a scholarly work using its DOI from Crossref.
    
    This function simulates querying the Crossref API to get detailed metadata
    about a journal article or other scholarly work, including title, authors,
    publication details, references, licenses, and more.
    
    Args:
        doi (str): Digital Object Identifier (DOI) of the work to retrieve.
        mailto (Optional[str]): Email address for API request identification (optional).
    
    Returns:
        Dict containing the full metadata structure with nested objects and lists
        as defined by the Crossref API schema, including:
        - status: response status
        - message_type: type of message ("work")
        - message_version: format version
        - doi: the requested DOI
        - title: list of titles
        - subtitle: list of subtitles
        - published: publication date information
        - created: record creation timestamp
        - indexed: indexing information
        - updated: last update timestamp
        - publisher: publisher name
        - container_title: journal/container title
        - short_container_title: abbreviated container title
        - volume: journal volume
        - issue: journal issue
        - page: page range
        - URL: human-readable URL
        - resource_primary_URL: primary access link
        - ISSN: list of ISSN values
        - issn_type: list of ISSN type objects
        - author: list of author objects
        - reference_count: number of references
        - references: list of reference objects
        - license: list of license objects
        - subject: list of subject categories
        - language: language code
        - link: list of access links
        - deposited: metadata deposit information
        - score: relevance score
        - type: work type
        - prefix: DOI prefix
        - member: Crossref member ID
        - is_referenced_by_count: citation count
        - alternative_id: list of alternative identifiers
        - assertion: list of editorial assertions
        - relation: relationships to other works
        - update_policy: update policy URL
        - source: source system
        - content_domain: content hosting domain information
    """
    # Input validation
    if not doi:
        raise ValueError("DOI is required and cannot be empty")
    
    if not isinstance(doi, str):
        raise TypeError("DOI must be a string")
    
    if mailto is not None and not isinstance(mailto, str):
        raise TypeError("mailto must be a string or None")
    
    # Call external API to get flattened data
    api_data = call_external_api("crossref-mcp-server-get_work_metadata")
    
    # Construct nested output structure
    result = {
        "status": api_data["status"],
        "message_type": api_data["message_type"],
        "message_version": api_data["message_version"],
        "doi": api_data["doi"],
        "title": [api_data["title_0"]] if api_data["title_0"] else [],
        "subtitle": [api_data["subtitle_0"]] if api_data["subtitle_0"] else [],
        "published": {
            "date-parts": [[
                api_data["published_date_parts_0_0"],
                api_data["published_date_parts_0_1"],
                api_data["published_date_parts_0_2"]
            ]]
        },
        "created": {
            "date-parts": [[
                api_data["created_date_parts_0_0"],
                api_data["created_date_parts_0_1"],
                api_data["created_date_parts_0_2"]
            ]],
            "date-time": api_data["created_date_time"],
            "timestamp": api_data["created_timestamp"]
        },
        "indexed": {
            "date-parts": [[
                api_data["indexed_date_parts_0_0"],
                api_data["indexed_date_parts_0_1"],
                api_data["indexed_date_parts_0_2"]
            ]],
            "date-time": api_data["indexed_date_time"],
            "timestamp": api_data["indexed_timestamp"]
        },
        "updated": {
            "date-parts": [[
                api_data["updated_date_parts_0_0"],
                api_data["updated_date_parts_0_1"],
                api_data["updated_date_parts_0_2"]
            ]],
            "date-time": api_data["updated_date_time"],
            "timestamp": api_data["updated_timestamp"]
        },
        "publisher": api_data["publisher"],
        "container_title": [api_data["container_title_0"]] if api_data["container_title_0"] else [],
        "short_container_title": [api_data["short_container_title_0"]] if api_data["short_container_title_0"] else [],
        "volume": api_data["volume"],
        "issue": api_data["issue"],
        "page": api_data["page"],
        "URL": api_data["URL"],
        "resource_primary_URL": api_data["resource_primary_URL"],
        "ISSN": [],
        "issn_type": [],
        "author": [],
        "reference_count": api_data["reference_count"],
        "references": [],
        "license": [],
        "subject": [],
        "language": api_data["language"],
        "link": [],
        "deposited": {
            "date-parts": [[
                api_data["deposited_date_parts_0_0"],
                api_data["deposited_date_parts_0_1"],
                api_data["deposited_date_parts_0_2"]
            ]],
            "timestamp": api_data["deposited_timestamp"]
        },
        "score": api_data["score"],
        "type": api_data["type"],
        "prefix": api_data["prefix"],
        "member": api_data["member"],
        "is_referenced_by_count": api_data["is_referenced_by_count"],
        "alternative_id": [api_data["alternative_id_0"]] if api_data["alternative_id_0"] else [],
        "assertion": [],
        "relation": {},
        "update_policy": api_data["update_policy"],
        "source": api_data["source"],
        "content_domain": {
            "domain": [],
            "crossmark_restriction": api_data["content_domain_crossmark_restriction"]
        }
    }
    
    # Handle ISSN lists
    if api_data["ISSN_0"]:
        result["ISSN"].append(api_data["ISSN_0"])
    if api_data["ISSN_1"]:
        result["ISSN"].append(api_data["ISSN_1"])
    
    # Handle issn_type list
    if api_data["issn_type_0_type"] and api_data["issn_type_0_value"]:
        result["issn_type"].append({
            "type": api_data["issn_type_0_type"],
            "value": api_data["issn_type_0_value"]
        })
    if api_data["issn_type_1_type"] and api_data["issn_type_1_value"]:
        result["issn_type"].append({
            "type": api_data["issn_type_1_type"],
            "value": api_data["issn_type_1_value"]
        })
    
    # Handle author list
    if api_data["author_0_given"] or api_data["author_0_family"]:
        author = {
            "given": api_data["author_0_given"],
            "family": api_data["author_0_family"],
            "sequence": api_data["author_0_sequence"]
        }
        if api_data["author_0_ORCID"]:
            author["ORCID"] = api_data["author_0_ORCID"]
        result["author"].append(author)
    
    # Handle references list
    if api_data["references_0_DOI"]:
        reference = {
            "DOI": api_data["references_0_DOI"],
            "author": api_data["references_0_author"],
            "year": api_data["references_0_year"],
            "journal-title": api_data["references_0_journal_title"],
            "unstructured": api_data["references_0_unstructured"]
        }
        result["references"].append(reference)
    
    # Handle license list
    if api_data["license_0_URL"]:
        license_obj = {
            "start": {
                "date-parts": [[
                    api_data["license_0_start_date_parts_0_0"],
                    api_data["license_0_start_date_parts_0_1"],
                    api_data["license_0_start_date_parts_0_2"]
                ]]
            },
            "content-version": api_data["license_0_content_version"],
            "delay-in-days": api_data["license_0_delay_in_days"],
            "URL": api_data["license_0_URL"]
        }
        result["license"].append(license_obj)
    
    # Handle subject list
    if api_data["subject_0"]:
        result["subject"].append(api_data["subject_0"])
    if api_data["subject_1"]:
        result["subject"].append(api_data["subject_1"])
    
    # Handle link list
    if api_data["link_0_URL"]:
        link_obj = {
            "URL": api_data["link_0_URL"],
            "content-type": api_data["link_0_content_type"],
            "content-version": api_data["link_0_content_version"],
            "intended-application": api_data["link_0_intended_application"]
        }
        result["link"].append(link_obj)
    
    # Handle assertion list
    if api_data["assertion_0_name"]:
        assertion_obj = {
            "name": api_data["assertion_0_name"],
            "value": api_data["assertion_0_value"],
            "group_name": api_data["assertion_0_group_name"],
            "group_title": api_data["assertion_0_group_title"]
        }
        result["assertion"].append(assertion_obj)
    
    # Handle relation object
    if api_data["relation_is_preprint_of_DOI"]:
        result["relation"] = {
            "is-preprint-of": {
                "DOI": api_data["relation_is_preprint_of_DOI"]
            }
        }
    
    # Handle content_domain domain list
    if api_data["content_domain_domain_0"]:
        result["content_domain"]["domain"].append(api_data["content_domain_domain_0"])
    
    return result