from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OSRS Wiki page info.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page_0_pageid (int): Page ID of the first page
        - page_0_ns (int): Namespace ID of the first page
        - page_0_title (str): Title of the first page
        - page_0_contentmodel (str): Content model of the first page
        - page_0_pagelanguage (str): Language code of the first page
        - page_0_pagelanguagehtmlcode (str): HTML language code of the first page
        - page_0_pagelanguagedir (str): Text direction of the first page ('ltr' or 'rtl')
        - page_0_touched (str): ISO timestamp when the first page was last updated
        - page_0_lastrevid (int): Last revision ID of the first page
        - page_0_length (int): Length of the first page content in bytes
        - page_1_pageid (int): Page ID of the second page
        - page_1_ns (int): Namespace ID of the second page
        - page_1_title (str): Title of the second page
        - page_1_contentmodel (str): Content model of the second page
        - page_1_pagelanguage (str): Language code of the second page
        - page_1_pagelanguagehtmlcode (str): HTML language code of the second page
        - page_1_pagelanguagedir (str): Text direction of the second page ('ltr' or 'rtl')
        - page_1_touched (str): ISO timestamp when the second page was last updated
        - page_1_lastrevid (int): Last revision ID of the second page
        - page_1_length (int): Length of the second page content in bytes
        - normalized_0_from (str): Original title that was normalized (first)
        - normalized_0_to (str): Normalized title (first)
        - normalized_1_from (str): Original title that was normalized (second)
        - normalized_1_to (str): Normalized title (second)
    """
    return {
        "page_0_pageid": 12345,
        "page_0_ns": 0,
        "page_0_title": "Dragon Scimitar",
        "page_0_contentmodel": "wikitext",
        "page_0_pagelanguage": "en",
        "page_0_pagelanguagehtmlcode": "en",
        "page_0_pagelanguagedir": "ltr",
        "page_0_touched": "2023-10-05T08:45:30Z",
        "page_0_lastrevid": 987654321,
        "page_0_length": 4500,
        "page_1_pageid": 67890,
        "page_1_ns": 0,
        "page_1_title": "Abyssal Whip",
        "page_1_contentmodel": "wikitext",
        "page_1_pagelanguage": "en",
        "page_1_pagelanguagehtmlcode": "en",
        "page_1_pagelanguagedir": "ltr",
        "page_1_touched": "2023-09-28T14:20:15Z",
        "page_1_lastrevid": 987650000,
        "page_1_length": 5200,
        "normalized_0_from": "dragon_scimitar",
        "normalized_0_to": "Dragon Scimitar",
        "normalized_1_from": "abyssal_whip",
        "normalized_1_to": "Abyssal Whip"
    }

def old_school_runescape_wiki_and_data_server_osrs_wiki_get_page_info(titles: str) -> Dict[str, Any]:
    """
    Get information about specific pages on the OSRS Wiki.

    Args:
        titles (str): Comma-separated list of page titles to get info for (e.g., Dragon_scimitar,Abyssal_whip)

    Returns:
        Dict containing:
        - pages (List[Dict]): List of page objects with keys 'pageid', 'ns', 'title', 'contentmodel',
          'pagelanguage', 'pagelanguagehtmlcode', 'pagelanguagedir', 'touched', 'lastrevid', 'length'
        - normalized (List[Dict]): Optional list of normalization mappings with 'from' and 'to' keys

    Raises:
        ValueError: If titles parameter is empty or not a string
    """
    if not titles or not isinstance(titles, str):
        raise ValueError("Parameter 'titles' must be a non-empty string")

    # Simulate calling external API
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-osrs_wiki_get_page_info")

    # Construct pages list from indexed fields
    pages: List[Dict[str, Any]] = [
        {
            "pageid": api_data["page_0_pageid"],
            "ns": api_data["page_0_ns"],
            "title": api_data["page_0_title"],
            "contentmodel": api_data["page_0_contentmodel"],
            "pagelanguage": api_data["page_0_pagelanguage"],
            "pagelanguagehtmlcode": api_data["page_0_pagelanguagehtmlcode"],
            "pagelanguagedir": api_data["page_0_pagelanguagedir"],
            "touched": api_data["page_0_touched"],
            "lastrevid": api_data["page_0_lastrevid"],
            "length": api_data["page_0_length"]
        },
        {
            "pageid": api_data["page_1_pageid"],
            "ns": api_data["page_1_ns"],
            "title": api_data["page_1_title"],
            "contentmodel": api_data["page_1_contentmodel"],
            "pagelanguage": api_data["page_1_pagelanguage"],
            "pagelanguagehtmlcode": api_data["page_1_pagelanguagehtmlcode"],
            "pagelanguagedir": api_data["page_1_pagelanguagedir"],
            "touched": api_data["page_1_touched"],
            "lastrevid": api_data["page_1_lastrevid"],
            "length": api_data["page_1_length"]
        }
    ]

    # Construct normalized list if present
    normalized: List[Dict[str, str]] = [
        {
            "from": api_data["normalized_0_from"],
            "to": api_data["normalized_0_to"]
        },
        {
            "from": api_data["normalized_1_from"],
            "to": api_data["normalized_1_to"]
        }
    ]

    return {
        "pages": pages,
        "normalized": normalized
    }