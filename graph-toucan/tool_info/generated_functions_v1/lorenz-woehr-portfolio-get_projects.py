from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Lorenz Woehr's portfolio projects.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - project_0_title (str): Title of the first project
        - project_0_subtitle (str): Subtitle of the first project
        - project_0_slug (str): URL slug of the first project
        - project_0_link (str): Direct link to the first project
        - project_0_coverImage_url (str): Cover image URL of the first project
        - project_0_orderRank (int): Order rank of the first project
        - project_0_scope_0__key (str): Key of the first scope item in the first project
        - project_0_scope_0_highlighted (bool): Whether the first scope item is highlighted in the first project
        - project_0_scope_0_text (str): Text of the first scope item in the first project
        - project_0_scope_1__key (str): Key of the second scope item in the first project
        - project_0_scope_1_highlighted (bool): Whether the second scope item is highlighted in the first project
        - project_0_scope_1_text (str): Text of the second scope item in the first project
        - project_1_title (str): Title of the second project
        - project_1_subtitle (str): Subtitle of the second project
        - project_1_slug (str): URL slug of the second project
        - project_1_link (str): Direct link to the second project
        - project_1_coverImage_url (str): Cover image URL of the second project
        - project_1_orderRank (int): Order rank of the second project
        - project_1_scope_0__key (str): Key of the first scope item in the second project
        - project_1_scope_0_highlighted (bool): Whether the first scope item is highlighted in the second project
        - project_1_scope_0_text (str): Text of the first scope item in the second project
        - project_1_scope_1__key (str): Key of the second scope item in the second project
        - project_1_scope_1_highlighted (bool): Whether the second scope item is highlighted in the second project
        - project_1_scope_1_text (str): Text of the second scope item in the second project
    """
    return {
        "project_0_title": "Interactive Data Dashboard",
        "project_0_subtitle": "A real-time analytics platform for business insights",
        "project_0_slug": "interactive-data-dashboard",
        "project_0_link": "https://lorenzwoehr.com/projects/interactive-data-dashboard",
        "project_0_coverImage_url": "https://lorenzwoehr.com/images/dashboard-cover.jpg",
        "project_0_orderRank": 1,
        "project_0_scope_0__key": "design",
        "project_0_scope_0_highlighted": True,
        "project_0_scope_0_text": "UI/UX Design",
        "project_0_scope_1__key": "development",
        "project_0_scope_1_highlighted": True,
        "project_0_scope_1_text": "Frontend Development",
        
        "project_1_title": "E-Commerce Mobile App",
        "project_1_subtitle": "A cross-platform shopping experience",
        "project_1_slug": "ecommerce-mobile-app",
        "project_1_link": "https://lorenzwoehr.com/projects/ecommerce-mobile-app",
        "project_1_coverImage_url": "https://lorenzwoehr.com/images/ecommerce-cover.jpg",
        "project_1_orderRank": 2,
        "project_1_scope_0__key": "strategy",
        "project_1_scope_0_highlighted": False,
        "project_1_scope_0_text": "Product Strategy",
        "project_1_scope_1__key": "development",
        "project_1_scope_1_highlighted": True,
        "project_1_scope_1_text": "Full Stack Development"
    }

def lorenz_woehr_portfolio_get_projects() -> List[Dict[str, Any]]:
    """
    Fetches and returns a list of Lorenz Woehr's portfolio projects.
    
    This function simulates retrieving project data from an external source
    and formats it according to the required schema. Each project includes
    metadata such as title, subtitle, URL identifiers, cover image, ranking,
    and scope details.
    
    Returns:
        List[Dict[str, Any]]: A list of project dictionaries, each containing:
            - title (str): Project title
            - subtitle (str): Project subtitle or description
            - slug (str): URL-friendly identifier
            - link (str): Full URL to the project
            - coverImage (Dict[str, str]): Image object with 'url' field
            - orderRank (int): Numerical rank for ordering
            - scope (List[Dict[str, Any]]): List of scope items, each with:
                - _key (str): Scope category key
                - highlighted (bool): Whether the scope item is featured
                - text (str): Human-readable scope description
    """
    try:
        api_data = call_external_api("lorenz-woehr-portfolio-get_projects")
        
        projects = []
        
        # Process first project
        project_0_scope = [
            {
                "_key": api_data["project_0_scope_0__key"],
                "highlighted": api_data["project_0_scope_0_highlighted"],
                "text": api_data["project_0_scope_0_text"]
            },
            {
                "_key": api_data["project_0_scope_1__key"],
                "highlighted": api_data["project_0_scope_1_highlighted"],
                "text": api_data["project_0_scope_1_text"]
            }
        ]
        
        project_0 = {
            "title": api_data["project_0_title"],
            "subtitle": api_data["project_0_subtitle"],
            "slug": api_data["project_0_slug"],
            "link": api_data["project_0_link"],
            "coverImage": {
                "url": api_data["project_0_coverImage_url"]
            },
            "orderRank": api_data["project_0_orderRank"],
            "scope": project_0_scope
        }
        
        # Process second project
        project_1_scope = [
            {
                "_key": api_data["project_1_scope_0__key"],
                "highlighted": api_data["project_1_scope_0_highlighted"],
                "text": api_data["project_1_scope_0_text"]
            },
            {
                "_key": api_data["project_1_scope_1__key"],
                "highlighted": api_data["project_1_scope_1_highlighted"],
                "text": api_data["project_1_scope_1_text"]
            }
        ]
        
        project_1 = {
            "title": api_data["project_1_title"],
            "subtitle": api_data["project_1_subtitle"],
            "slug": api_data["project_1_slug"],
            "link": api_data["project_1_link"],
            "coverImage": {
                "url": api_data["project_1_coverImage_url"]
            },
            "orderRank": api_data["project_1_orderRank"],
            "scope": project_1_scope
        }
        
        projects.append(project_0)
        projects.append(project_1)
        
        return projects
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve projects: {str(e)}")