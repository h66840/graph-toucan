from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching contact data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - email (str): Professional email address for Lorenz Woehr
        - social_0_platform (str): First social media platform name
        - social_0_url (str): First social media profile URL
        - social_1_platform (str): Second social media platform name
        - social_1_url (str): Second social media profile URL
        - website (str): Personal/portfolio website URL
    """
    return {
        "email": "lorenz.woehr@portfolio.com",
        "social_0_platform": "LinkedIn",
        "social_0_url": "https://linkedin.com/in/lorenzwoehr",
        "social_1_platform": "GitHub",
        "social_1_url": "https://github.com/lorenzwoehr",
        "website": "https://lorenzwoehr.me"
    }

def lorenz_woehr_portfolio_get_contact() -> Dict[str, Any]:
    """
    Get Lorenz Woehr's contact information.
    
    Returns:
        Dict containing:
        - email (str): Professional email address for Lorenz Woehr
        - socialLinks (List[Dict]): List of social media profiles, each with 'platform' (str) and 'url' (str)
        - website (str): Personal/portfolio website URL
    """
    try:
        # Validate tool name (defensive programming, though not strictly necessary here)
        if not isinstance("lorenz-woehr-portfolio-get_contact", str):
            raise ValueError("Tool name must be a string")
            
        # Fetch data from simulated external API
        api_data = call_external_api("lorenz-woehr-portfolio-get_contact")
        
        # Construct social links list from indexed fields
        social_links = [
            {
                "platform": api_data["social_0_platform"],
                "url": api_data["social_0_url"]
            },
            {
                "platform": api_data["social_1_platform"],
                "url": api_data["social_1_url"]
            }
        ]
        
        # Build final result matching output schema
        result = {
            "email": api_data["email"],
            "socialLinks": social_links,
            "website": api_data["website"]
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve contact information: {str(e)}")