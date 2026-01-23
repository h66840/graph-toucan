from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OSRS Wiki page parsing.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content_html (str): Raw HTML content of the parsed wiki page
        - page_title (str): Title of the wiki page as extracted from content
        - is_disambiguation_page (bool): Whether the page is a disambiguation page
        - messagebox_type (str): Type of messagebox (e.g., 'disambig')
        - messagebox_title (str): Title of the messagebox
        - messagebox_text (str): Text content of the messagebox
        - disambiguation_entries_0_title (str): Title of first disambiguation entry
        - disambiguation_entries_0_description (str): Description of first entry
        - disambiguation_entries_1_title (str): Title of second disambiguation entry
        - disambiguation_entries_1_subentries_0 (str): First subentry of second disambiguation entry
        - disambiguation_entries_1_subentries_1 (str): Second subentry of second disambiguation entry
        - links_0_url (str): URL of first link
        - links_0_text (str): Text of first link
        - links_0_section (str): Section of first link (if applicable)
        - links_1_url (str): URL of second link
        - links_1_text (str): Text of second link
        - links_1_section (str): Section of second link (if applicable)
    """
    return {
        "content_html": "<p>This is the simulated HTML content for Dragon scimitar.</p>",
        "page_title": "Dragon scimitar",
        "is_disambiguation_page": False,
        "messagebox_type": "info",
        "messagebox_title": "Note",
        "messagebox_text": "This page is about the weapon.",
        "disambiguation_entries_0_title": "Dragon scimitar (uncharged)",
        "disambiguation_entries_0_description": "A melee weapon requiring 60 Attack.",
        "disambiguation_entries_1_title": "Dragon scimitar (charged)",
        "disambiguation_entries_1_subentries_0": "With 10 charges",
        "disambiguation_entries_1_subentries_1": "With 5 charges",
        "links_0_url": "/wiki/Dragon_sword",
        "links_0_text": "Dragon sword",
        "links_0_section": "Related items",
        "links_1_url": "/wiki/Superior_scimitar",
        "links_1_text": "Superior scimitar",
        "links_1_section": "Drop sources"
    }

def old_school_runescape_wiki_and_data_server_osrs_wiki_parse_page(page: str) -> Dict[str, Any]:
    """
    Get the parsed HTML content of a specific OSRS Wiki page.
    
    Args:
        page (str): The exact title of the wiki page to parse (e.g., 'Dragon scimitar', 'Abyssal whip'). Case-sensitive.
    
    Returns:
        Dict containing:
        - content_html (str): The raw HTML content of the parsed wiki page as a string
        - disambiguation_entries (List[Dict]): List of disambiguation entries with 'title', and optional 'description' or 'subentries'
        - page_title (str): The title of the wiki page as extracted from the content
        - is_disambiguation_page (bool): Whether the page is a disambiguation page
        - messagebox (Dict): Structured info about notice boxes with 'type', 'title', and 'text'
        - links (List[Dict]): List of all anchor links with 'url', 'text', and optional 'section'
    
    Raises:
        ValueError: If the 'page' parameter is empty or not a string
    """
    if not page:
        raise ValueError("Parameter 'page' is required and cannot be empty.")
    if not isinstance(page, str):
        raise ValueError("Parameter 'page' must be a string.")

    # Fetch data from simulated external API
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-osrs_wiki_parse_page")

    # Construct disambiguation entries
    disambiguation_entries: List[Dict[str, Any]] = []
    
    if "disambiguation_entries_0_title" in api_data:
        entry_0: Dict[str, Any] = {
            "title": api_data["disambiguation_entries_0_title"]
        }
        if "disambiguation_entries_0_description" in api_data:
            entry_0["description"] = api_data["disambiguation_entries_0_description"]
        disambiguation_entries.append(entry_0)

    if "disambiguation_entries_1_title" in api_data:
        entry_1: Dict[str, Any] = {
            "title": api_data["disambiguation_entries_1_title"]
        }
        subentries = []
        if "disambiguation_entries_1_subentries_0" in api_data:
            subentries.append(api_data["disambiguation_entries_1_subentries_0"])
        if "disambiguation_entries_1_subentries_1" in api_data:
            subentries.append(api_data["disambiguation_entries_1_subentries_1"])
        if subentries:
            entry_1["subentries"] = subentries
        disambiguation_entries.append(entry_1)

    # Construct messagebox
    messagebox: Dict[str, str] = {}
    if "messagebox_type" in api_data:
        messagebox["type"] = api_data["messagebox_type"]
    if "messagebox_title" in api_data:
        messagebox["title"] = api_data["messagebox_title"]
    if "messagebox_text" in api_data:
        messagebox["text"] = api_data["messagebox_text"]

    # Construct links
    links: List[Dict[str, str]] = []
    
    if "links_0_url" in api_data:
        link_0: Dict[str, str] = {
            "url": api_data["links_0_url"],
            "text": api_data["links_0_text"]
        }
        if "links_0_section" in api_data:
            link_0["section"] = api_data["links_0_section"]
        links.append(link_0)

    if "links_1_url" in api_data:
        link_1: Dict[str, str] = {
            "url": api_data["links_1_url"],
            "text": api_data["links_1_text"]
        }
        if "links_1_section" in api_data:
            link_1["section"] = api_data["links_1_section"]
        links.append(link_1)

    # Construct final result
    result: Dict[str, Any] = {
        "content_html": api_data["content_html"],
        "page_title": api_data["page_title"],
        "is_disambiguation_page": api_data["is_disambiguation_page"],
        "messagebox": messagebox,
        "disambiguation_entries": disambiguation_entries,
        "links": links
    }

    return result