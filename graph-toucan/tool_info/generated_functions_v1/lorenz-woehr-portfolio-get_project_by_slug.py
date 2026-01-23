from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Lorenz Woehr portfolio project by slug.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coverImage_url (str): URL to the cover image of the project
        - credits_0__key (str): Key identifier for the first credit entry
        - credits_0_role (str): Role in the first credit entry
        - credits_0_names_0__key (str): Key identifier for the first contributor name in the first credit
        - credits_0_names_0_name (str): Name of the first contributor in the first credit
        - credits_0_names_0_url (str): URL associated with the first contributor in the first credit (optional)
        - gallery_0_alt (str): Alt text for the first gallery item
        - gallery_0_caption (str): Caption for the first gallery item
        - gallery_0_media_asset_url (str): URL of the asset for the first gallery item if it's an image
        - gallery_0_media_asset_secure_url (str): Secure URL of the asset for the first gallery item if it's a video
        - gallery_0_media_type (str): Type of media ('image' or 'video') for the first gallery item
        - link (str): URL to the live project if available, otherwise None
        - scope_0__key (str): Key identifier for the first scope tag
        - scope_0_highlighted (bool): Whether the first scope tag is highlighted
        - scope_0_text (str): Skill/technology name for the first scope tag
        - subtitle (str): Brief descriptive subtitle of the project
        - title (str): Main title/name of the project
        - whatIDid_0__key (str): Key identifier for the first 'what I did' block
        - whatIDid_0__type (str): Type of the first 'what I did' block
        - whatIDid_0_children_0__key (str): Key identifier for the first child span in the first 'what I did' block
        - whatIDid_0_children_0__type (str): Type of the first child span in the first 'what I did' block
        - whatIDid_0_children_0_marks (str): JSON string representing marks (e.g., formatting) for the first child span
        - whatIDid_0_children_0_text (str): Text content of the first child span in the first 'what I did' block
        - whatIDid_0_markDefs (str): JSON string representing mark definitions for the first 'what I did' block
        - whatIDid_0_style (str): Style of the first 'what I did' block (e.g., 'normal', 'h3')
        - whereIStarted_0__key (str): Key identifier for the first 'where I started' block
        - whereIStarted_0__type (str): Type of the first 'where I started' block
        - whereIStarted_0_children_0__key (str): Key identifier for the first child span in the first 'where I started' block
        - whereIStarted_0_children_0__type (str): Type of the first child span in the first 'where I started' block
        - whereIStarted_0_children_0_marks (str): JSON string representing marks for the first child span in the first 'where I started' block
        - whereIStarted_0_children_0_text (str): Text content of the first child span in the first 'where I started' block
        - whereIStarted_0_markDefs (str): JSON string representing mark definitions for the first 'where I started' block
        - whereIStarted_0_style (str): Style of the first 'where I started' block
    """
    return {
        "coverImage_url": "https://example.com/images/project-cover.jpg",
        "credits_0__key": "credit-01",
        "credits_0_role": "Lead Developer",
        "credits_0_names_0__key": "name-01",
        "credits_0_names_0_name": "Lorenz Woehr",
        "credits_0_names_0_url": "https://lorenzwoehr.com",
        "gallery_0_alt": "Project screenshot",
        "gallery_0_caption": "Main interface view",
        "gallery_0_media_asset_url": "https://example.com/gallery/image.jpg",
        "gallery_0_media_asset_secure_url": "https://secure.example.com/gallery/video.mp4",
        "gallery_0_media_type": "image",
        "link": "https://example.com/live-project",
        "scope_0__key": "scope-01",
        "scope_0_highlighted": True,
        "scope_0_text": "React",
        "subtitle": "A modern web application built with cutting-edge technologies",
        "title": "Innovative Dashboard App",
        "whatIDid_0__key": "work-01",
        "whatIDid_0__type": "block",
        "whatIDid_0_children_0__key": "span-01",
        "whatIDid_0_children_0__type": "span",
        "whatIDid_0_children_0_marks": "[]",
        "whatIDid_0_children_0_text": "Developed the frontend using React and TypeScript.",
        "whatIDid_0_markDefs": "[]",
        "whatIDid_0_style": "normal",
        "whereIStarted_0__key": "narrative-01",
        "whereIStarted_0__type": "block",
        "whereIStarted_0_children_0__key": "span-02",
        "whereIStarted_0_children_0__type": "span",
        "whereIStarted_0_children_0_marks": "[]",
        "whereIStarted_0_children_0_text": "The project started as a concept during a hackathon in Berlin.",
        "whereIStarted_0_markDefs": "[]",
        "whereIStarted_0_style": "normal"
    }

def lorenz_woehr_portfolio_get_project_by_slug(slug: str) -> Dict[str, Any]:
    """
    Get a project from Lorenz Woehr by its slug.
    
    This function retrieves detailed information about a specific project
    from Lorenz Woehr's portfolio using the project's unique slug identifier.
    
    Args:
        slug (str): The slug of Lorenz Woehr's project to retrieve. Required.
        
    Returns:
        Dict containing the following fields:
        - coverImage (Dict): contains 'url' field pointing to the cover image
        - credits (List[Dict]): list of credit entries with '_key', 'role', 'names'
        - gallery (List[Dict]): list of media items with 'alt', 'caption', 'media'
        - link (str): URL to the live project or None
        - scope (List[Dict]): list of project scope tags with '_key', 'highlighted', 'text'
        - subtitle (str): brief descriptive subtitle
        - title (str): main title of the project
        - whatIDid (List[Dict]): detailed description of work performed
        - whereIStarted (List[Dict]): narrative on how the project began
        
    Raises:
        ValueError: If slug is empty or not a string
    """
    if not isinstance(slug, str):
        raise ValueError("Slug must be a string")
    if not slug.strip():
        raise ValueError("Slug cannot be empty")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("lorenz-woehr-portfolio-get_project_by_slug")
    
    # Construct coverImage object
    coverImage = {
        "url": api_data["coverImage_url"]
    } if api_data.get("coverImage_url") else None
    
    # Construct credits list (only one item generated as per requirements)
    credits_entry_names = [
        {
            "_key": api_data["credits_0_names_0__key"],
            "name": api_data["credits_0_names_0_name"],
            "url": api_data.get("credits_0_names_0_url")
        }
    ]
    credits = [
        {
            "_key": api_data["credits_0__key"],
            "role": api_data["credits_0_role"],
            "names": credits_entry_names
        }
    ]
    
    # Construct media asset object based on type
    media_asset = {}
    if api_data["gallery_0_media_type"] == "image":
        media_asset["url"] = api_data["gallery_0_media_asset_url"]
    else:
        media_asset["secure_url"] = api_data["gallery_0_media_asset_secure_url"]
    
    # Construct gallery list
    gallery = [
        {
            "alt": api_data["gallery_0_alt"],
            "caption": api_data["gallery_0_caption"],
            "media": {
                "asset": media_asset,
                "type": api_data["gallery_0_media_type"]
            }
        }
    ]
    
    # Construct scope list
    scope = [
        {
            "_key": api_data["scope_0__key"],
            "highlighted": api_data["scope_0_highlighted"],
            "text": api_data["scope_0_text"]
        }
    ]
    
    # Construct whatIDid list
    whatIDid_children = [
        {
            "_key": api_data["whatIDid_0_children_0__key"],
            "_type": api_data["whatIDid_0_children_0__type"],
            "marks": api_data["whatIDid_0_children_0_marks"],
            "text": api_data["whatIDid_0_children_0_text"]
        }
    ]
    whatIDid = [
        {
            "_key": api_data["whatIDid_0__key"],
            "_type": api_data["whatIDid_0__type"],
            "children": whatIDid_children,
            "markDefs": api_data["whatIDid_0_markDefs"],
            "style": api_data["whatIDid_0_style"]
        }
    ]
    
    # Construct whereIStarted list
    whereIStarted_children = [
        {
            "_key": api_data["whereIStarted_0_children_0__key"],
            "_type": api_data["whereIStarted_0_children_0__type"],
            "marks": api_data["whereIStarted_0_children_0_marks"],
            "text": api_data["whereIStarted_0_children_0_text"]
        }
    ]
    whereIStarted = [
        {
            "_key": api_data["whereIStarted_0__key"],
            "_type": api_data["whereIStarted_0__type"],
            "children": whereIStarted_children,
            "markDefs": api_data["whereIStarted_0_markDefs"],
            "style": api_data["whereIStarted_0_style"]
        }
    ]
    
    # Assemble final result
    result = {
        "coverImage": coverImage,
        "credits": credits,
        "gallery": gallery,
        "link": api_data.get("link"),
        "scope": scope,
        "subtitle": api_data["subtitle"],
        "title": api_data["title"],
        "whatIDid": whatIDid,
        "whereIStarted": whereIStarted
    }
    
    return result