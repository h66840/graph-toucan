from typing import Dict, List, Any, Optional
import json

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for tool 'fetch_server_fetch_markdown'.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - content (str): Fetched website content in Markdown format
        - metadata_title (str): Page title
        - metadata_description (str): Page description
        - metadata_datePublished (str): Publication date of the page
        - metadata_author (str): Author of the page
        - metadata_interactionStatistic (str): Interaction statistic as string
        - links_0_url (str): First extracted link URL
        - links_0_text (str): First extracted link text
        - links_1_url (str): Second extracted link URL
        - links_1_text (str): Second extracted link text
        - structured_data_0_type (str): Type of first structured data item
        - structured_data_0_value (str): Value of first structured data item as JSON string
        - structured_data_1_type (str): Type of second structured data item
        - structured_data_1_value (str): Value of second structured data item as JSON string
        - images_0_src (str): Source URL of first image
        - images_0_alt (str): Alt text of first image
        - images_0_caption (str): Caption of first image
        - images_1_src (str): Source URL of second image
        - images_1_alt (str): Alt text of second image
        - images_1_caption (str): Caption of second image
        - headings_0 (str): First heading text
        - headings_1 (str): Second heading text
        - comments_0_author (str): Author of first comment
        - comments_0_text (str): Text of first comment
        - comments_0_datePublished (str): Publication date of first comment
        - comments_0_likeCount (int): Like count of first comment
        - comments_1_author (str): Author of second comment
        - comments_1_text (str): Text of second comment
        - comments_1_datePublished (str): Publication date of second comment
        - comments_1_likeCount (int): Like count of second comment
        - social_interactions_likeCount (int): Total like count
        - social_interactions_commentCount (int): Total comment count
        - social_interactions_shareCount (int): Total share count
        - keywords_0 (str): First keyword
        - keywords_1 (str): Second keyword
        - videos_0_url (str): URL of first embedded video
        - videos_0_title (str): Title of first video
        - videos_0_duration (str): Duration of first video
        - videos_0_thumbnailUrl (str): Thumbnail URL of first video
        - videos_0_description (str): Description of first video
        - videos_1_url (str): URL of second embedded video
        - videos_1_title (str): Title of second video
        - videos_1_duration (str): Duration of second video
        - videos_1_thumbnailUrl (str): Thumbnail URL of second video
        - videos_1_description (str): Description of second video
    """
    return {
        "content": "# Welcome to Example Site\n\nThis is a sample page with **Markdown** formatting.\n\n- Item one\n- Item two\n\n[Learn more](https://example.com/guide)",
        "metadata_title": "Example Homepage",
        "metadata_description": "An example website for demonstration purposes",
        "metadata_datePublished": "2023-10-15",
        "metadata_author": "John Doe",
        "metadata_interactionStatistic": "1000 views",
        "links_0_url": "https://example.com/guide",
        "links_0_text": "Learn more",
        "links_1_url": "https://example.com/about",
        "links_1_text": "About Us",
        "structured_data_0_type": "Article",
        "structured_data_0_value": '{"@type": "Article", "headline": "Example Article"}',
        "structured_data_1_type": "Organization",
        "structured_data_1_value": '{"@type": "Organization", "name": "Example Corp"}',
        "images_0_src": "https://example.com/image1.jpg",
        "images_0_alt": "Example image one",
        "images_0_caption": "First example image",
        "images_1_src": "https://example.com/image2.png",
        "images_1_alt": "Example image two",
        "images_1_caption": "Second example image",
        "headings_0": "Welcome to Example Site",
        "headings_1": "Features",
        "comments_0_author": "Alice",
        "comments_0_text": "Great article!",
        "comments_0_datePublished": "2023-10-16",
        "comments_0_likeCount": 5,
        "comments_1_author": "Bob",
        "comments_1_text": "Thanks for sharing.",
        "comments_1_datePublished": "2023-10-17",
        "comments_1_likeCount": 3,
        "social_interactions_likeCount": 8,
        "social_interactions_commentCount": 2,
        "social_interactions_shareCount": 4,
        "keywords_0": "example",
        "keywords_1": "demo",
        "videos_0_url": "https://example.com/video1.mp4",
        "videos_0_title": "Introduction Video",
        "videos_0_duration": "PT2M30S",
        "videos_0_thumbnailUrl": "https://example.com/thumb1.jpg",
        "videos_0_description": "An intro to our platform",
        "videos_1_url": "https://example.com/video2.mp4",
        "videos_1_title": "Tutorial",
        "videos_1_duration": "PT5M10S",
        "videos_1_thumbnailUrl": "https://example.com/thumb2.jpg",
        "videos_1_description": "How to use the system"
    }

def fetch_server_fetch_markdown(headers: Optional[Dict[str, str]] = None, url: str = "") -> Dict[str, Any]:
    """
    Fetch a website and return the content as Markdown.
    
    Args:
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        url (str): URL of the website to fetch (required)
    
    Returns:
        Dict containing:
        - content (str): the fetched website content converted to Markdown format
        - metadata (Dict): metadata about the fetched page (title, description, etc.)
        - links (List[Dict]): list of extracted links with 'url' and 'text'
        - structured_data (List[Dict]): list of parsed structured data objects
        - images (List[Dict]): list of images with 'src', 'alt', 'caption'
        - headings (List[str]): list of heading texts
        - comments (List[Dict]): list of user comments with author, text, date, likes
        - social_interactions (Dict): social metrics like likes, shares, comments
        - keywords (List[str]): list of keywords or hashtags
        - videos (List[Dict]): list of embedded videos with details
    
    Raises:
        ValueError: If url is not provided
    """
    if not url:
        raise ValueError("URL is required")

    # Fetch simulated external data
    api_data = call_external_api("fetch_server_fetch_markdown")
    
    # Construct metadata dictionary
    metadata = {}
    if "metadata_title" in api_data:
        metadata["title"] = api_data["metadata_title"]
    if "metadata_description" in api_data:
        metadata["description"] = api_data["metadata_description"]
    if "metadata_datePublished" in api_data:
        metadata["datePublished"] = api_data["metadata_datePublished"]
    if "metadata_author" in api_data:
        metadata["author"] = api_data["metadata_author"]
    if "metadata_interactionStatistic" in api_data:
        metadata["interactionStatistic"] = api_data["metadata_interactionStatistic"]
    
    # Construct links list
    links = []
    if all(k in api_data for k in ["links_0_url"]):
        link0 = {"url": api_data["links_0_url"]}
        if "links_0_text" in api_data:
            link0["text"] = api_data["links_0_text"]
        links.append(link0)
    
    if all(k in api_data for k in ["links_1_url"]):
        link1 = {"url": api_data["links_1_url"]}
        if "links_1_text" in api_data:
            link1["text"] = api_data["links_1_text"]
        links.append(link1)
    
    # Construct structured_data list
    structured_data = []
    if all(k in api_data for k in ["structured_data_0_type", "structured_data_0_value"]):
        try:
            value = json.loads(api_data["structured_data_0_value"])
        except:
            value = api_data["structured_data_0_value"]
        structured_data.append({
            "type": api_data["structured_data_0_type"],
            "value": value
        })
    
    if all(k in api_data for k in ["structured_data_1_type", "structured_data_1_value"]):
        try:
            value = json.loads(api_data["structured_data_1_value"])
        except:
            value = api_data["structured_data_1_value"]
        structured_data.append({
            "type": api_data["structured_data_1_type"],
            "value": value
        })
    
    # Construct images list
    images = []
    if all(k in api_data for k in ["images_0_src"]):
        image0 = {"src": api_data["images_0_src"]}
        if "images_0_alt" in api_data:
            image0["alt"] = api_data["images_0_alt"]
        if "images_0_caption" in api_data:
            image0["caption"] = api_data["images_0_caption"]
        images.append(image0)
    
    if all(k in api_data for k in ["images_1_src"]):
        image1 = {"src": api_data["images_1_src"]}
        if "images_1_alt" in api_data:
            image1["alt"] = api_data["images_1_alt"]
        if "images_1_caption" in api_data:
            image1["caption"] = api_data["images_1_caption"]
        images.append(image1)
    
    # Construct headings list
    headings = []
    if "headings_0" in api_data:
        headings.append(api_data["headings_0"])
    if "headings_1" in api_data:
        headings.append(api_data["headings_1"])
    
    # Construct comments list
    comments = []
    if all(k in api_data for k in ["comments_0_author", "comments_0_text", "comments_0_datePublished", "comments_0_likeCount"]):
        comments.append({
            "author": api_data["comments_0_author"],
            "text": api_data["comments_0_text"],
            "datePublished": api_data["comments_0_datePublished"],
            "likeCount": api_data["comments_0_likeCount"]
        })
    
    if all(k in api_data for k in ["comments_1_author", "comments_1_text", "comments_1_datePublished", "comments_1_likeCount"]):
        comments.append({
            "author": api_data["comments_1_author"],
            "text": api_data["comments_1_text"],
            "datePublished": api_data["comments_1_datePublished"],
            "likeCount": api_data["comments_1_likeCount"]
        })
    
    # Construct social_interactions dict
    social_interactions = {}
    if "social_interactions_likeCount" in api_data:
        social_interactions["likeCount"] = api_data["social_interactions_likeCount"]
    if "social_interactions_commentCount" in api_data:
        social_interactions["commentCount"] = api_data["social_interactions_commentCount"]
    if "social_interactions_shareCount" in api_data:
        social_interactions["shareCount"] = api_data["social_interactions_shareCount"]
    
    # Construct keywords list
    keywords = []
    if "keywords_0" in api_data:
        keywords.append(api_data["keywords_0"])
    if "keywords_1" in api_data:
        keywords.append(api_data["keywords_1"])
    
    # Construct videos list
    videos = []
    if all(k in api_data for k in ["videos_0_url"]):
        video0 = {
            "url": api_data["videos_0_url"],
            "title": api_data.get("videos_0_title", ""),
            "duration": api_data.get("videos_0_duration", ""),
            "thumbnailUrl": api_data.get("videos_0_thumbnailUrl", ""),
            "description": api_data.get("videos_0_description", "")
        }
        videos.append(video0)
    
    if all(k in api_data for k in ["videos_1_url"]):
        video1 = {
            "url": api_data["videos_1_url"],
            "title": api_data.get("videos_1_title", ""),
            "duration": api_data.get("videos_1_duration", ""),
            "thumbnailUrl": api_data.get("videos_1_thumbnailUrl", ""),
            "description": api_data.get("videos_1_description", "")
        }
        videos.append(video1)
    
    # Return the structured result
    result = {
        "content": api_data["content"],
        "metadata": metadata,
        "links": links,
        "structured_data": structured_data,
        "images": images,
        "headings": headings,
        "comments": comments,
        "social_interactions": social_interactions,
        "keywords": keywords,
        "videos": videos
    }
    
    return result