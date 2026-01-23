from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play app details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): App name as listed on Google Play
        - description (str): Full app description in plain text
        - descriptionHTML (str): Full app description with HTML formatting preserved
        - summary (str): Short one-line description of the app
        - installs (str): Install count range (e.g., '10,000+', '1M+')
        - minInstalls (int): Minimum number of installs (lower bound of range)
        - maxInstalls (int): Maximum number of installs (upper bound of range, or exact if capped)
        - score (float): Average user rating from 0 to 5
        - scoreText (str): Formatted rating display text (e.g., '4.5')
        - ratings (int): Total number of user ratings
        - reviews (int): Total number of user reviews
        - histogram_1 (int): Number of 1-star ratings
        - histogram_2 (int): Number of 2-star ratings
        - histogram_3 (int): Number of 3-star ratings
        - histogram_4 (int): Number of 4-star ratings
        - histogram_5 (int): Number of 5-star ratings
        - price (float): Price of the app in local currency (0 if free)
        - free (bool): True if the app is free to download
        - currency (str): Currency code for the price (e.g., 'USD', 'EUR')
        - priceText (str): Formatted price string (e.g., '$0.99', 'Free')
        - offersIAP (bool): True if the app offers in-app purchases
        - IAPRange (str): Price range for in-app purchases (e.g., '$0.99 - $99.99')
        - androidVersion (str): Minimum Android version required (e.g., '5.0')
        - androidVersionText (str): Formatted version requirement text (e.g., 'Varies with device', '5.0 and up')
        - developer (str): Name of the app developer
        - developerId (str): Unique identifier for the developer on Google Play
        - developerEmail (str): Contact email address for the developer
        - developerWebsite (str): Official website URL of the developer
        - developerAddress (str): Physical address of the developer (if provided)
        - genre (str): Primary category/genre of the app (e.g., 'Tools', 'Games')
        - genreId (str): Internal Google Play ID for the genre
        - icon (str): URL to the app's main icon image
        - headerImage (str): URL to the app's header/feature graphic
        - screenshot_0 (str): URL of first screenshot
        - screenshot_1 (str): URL of second screenshot
        - contentRating (str): Content rating assigned (e.g., 'Everyone', 'Teen', 'Mature')
        - contentRatingDescription (str): Detailed explanation of content rating (e.g., 'Contains violence')
        - adSupported (bool): True if the app displays advertisements
        - released (str): Release date of the app in ISO format (e.g., '2020-01-15')
        - updated (int): Timestamp of last update in milliseconds since epoch
        - version (str): Current version string of the app (e.g., '1.23.0')
        - recentChanges (str): Changelog details for the latest version
        - preregister (bool): True if the app is available for pre-registration
        - editorsChoice (bool): True if the app is marked as an Editor's Choice
        - feature_0 (str): First special feature of the app
        - feature_1 (str): Second special feature of the app
    """
    return {
        "title": "Google Translate",
        "description": "Translate between 108 languages by typing or using the camera to translate printed and handwritten text. You can also translate speech in real time and offline.",
        "descriptionHTML": "Translate between 108 languages by typing or using the camera to translate printed and handwritten text. You can also translate speech in real time and offline.",
        "summary": "Translate in real time, offline, and with camera",
        "installs": "1,000,000,000+",
        "minInstalls": 1000000000,
        "maxInstalls": 5000000000,
        "score": 4.5,
        "scoreText": "4.5",
        "ratings": 12500000,
        "reviews": 8500000,
        "histogram_1": 1200000,
        "histogram_2": 800000,
        "histogram_3": 1500000,
        "histogram_4": 3000000,
        "histogram_5": 6000000,
        "price": 0.0,
        "free": True,
        "currency": "USD",
        "priceText": "Free",
        "offersIAP": False,
        "IAPRange": "",
        "androidVersion": "5.0",
        "androidVersionText": "5.0 and up",
        "developer": "Google LLC",
        "developerId": "5700313618786177705",
        "developerEmail": "translate-android@google.com",
        "developerWebsite": "https://support.google.com/translate",
        "developerAddress": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
        "genre": "Tools",
        "genreId": "TOOLS",
        "icon": "https://play-lh.googleusercontent.com/9jwVH5bWJk7ZvQfV8Y6X7GzZqZtZrZsZpZoZnZmZlZkZjZiZhZgZfZeZdZcZbZaZ9Z8Z7Z6Z5Z4Z3Z2Z1Z0",
        "headerImage": "https://play-lh.googleusercontent.com/8iU8jK7lM6kN5jL4mO3nP2oQ1pR0qS9tU8vW7xY6zA5bB4cC3dD2eE1fF0gG9hH8iI7jJ6kK5lL4mM3nN2oO1pP",
        "screenshot_0": "https://play-lh.googleusercontent.com/screenshot1.jpg",
        "screenshot_1": "https://play-lh.googleusercontent.com/screenshot2.jpg",
        "contentRating": "Everyone",
        "contentRatingDescription": "Mild Language",
        "adSupported": False,
        "released": "2011-04-12",
        "updated": 1678886400000,
        "version": "7.23.0",
        "recentChanges": "Improved translation accuracy and performance.",
        "preregister": False,
        "editorsChoice": True,
        "feature_0": "Available on tablets",
        "feature_1": "In-app events"
    }

def app_market_intelligence_google_play_details(appId: str, country: Optional[str] = "us", lang: Optional[str] = "en") -> Dict[str, Any]:
    """
    Get detailed information about a Google Play app.
    
    Args:
        appId (str): Google Play package name (e.g., 'com.google.android.apps.translate')
        country (str, optional): Country code to check app availability (default: us)
        lang (str, optional): Language code for result text (default: en)
    
    Returns:
        Dict containing detailed app information with the following structure:
        - title (str): App name as listed on Google Play
        - description (str): Full app description in plain text
        - descriptionHTML (str): Full app description with HTML formatting preserved
        - summary (str): Short one-line description of the app
        - installs (str): Install count range (e.g., '10,000+', '1M+')
        - minInstalls (int): Minimum number of installs
        - maxInstalls (int): Maximum number of installs
        - score (float): Average user rating from 0 to 5
        - scoreText (str): Formatted rating display text
        - ratings (int): Total number of user ratings
        - reviews (int): Total number of user reviews
        - histogram (Dict): Rating distribution by star level with keys '1', '2', '3', '4', '5'
        - price (float): Price of the app in local currency (0 if free)
        - free (bool): True if the app is free to download
        - currency (str): Currency code for the price (e.g., 'USD', 'EUR')
        - priceText (str): Formatted price string (e.g., '$0.99', 'Free')
        - offersIAP (bool): True if the app offers in-app purchases
        - IAPRange (str): Price range for in-app purchases (e.g., '$0.99 - $99.99')
        - androidVersion (str): Minimum Android version required (e.g., '5.0')
        - androidVersionText (str): Formatted version requirement text (e.g., 'Varies with device', '5.0 and up')
        - developer (str): Name of the app developer
        - developerId (str): Unique identifier for the developer on Google Play
        - developerEmail (str): Contact email address for the developer
        - developerWebsite (str): Official website URL of the developer
        - developerAddress (str): Physical address of the developer (if provided)
        - genre (str): Primary category/genre of the app (e.g., 'Tools', 'Games')
        - genreId (str): Internal Google Play ID for the genre
        - icon (str): URL to the app's main icon image
        - headerImage (str): URL to the app's header/feature graphic
        - screenshots (List[str]): List of screenshot URLs
        - contentRating (str): Content rating assigned (e.g., 'Everyone', 'Teen', 'Mature')
        - contentRatingDescription (str): Detailed explanation of content rating (e.g., 'Contains violence')
        - adSupported (bool): True if the app displays advertisements
        - released (str): Release date of the app in ISO format (e.g., '2020-01-15')
        - updated (int): Timestamp of last update in milliseconds since epoch
        - version (str): Current version string of the app (e.g., '1.23.0')
        - recentChanges (str): Changelog details for the latest version
        - preregister (bool): True if the app is available for pre-registration
        - editorsChoice (bool): True if the app is marked as an Editor's Choice
        - features (List[str]): List of special features offered by the app
    """
    raw_data = call_external_api("google_play_details")
    
    # Transform histogram data into a nested dictionary
    histogram = {
        "1": raw_data["histogram_1"],
        "2": raw_data["histogram_2"],
        "3": raw_data["histogram_3"],
        "4": raw_data["histogram_4"],
        "5": raw_data["histogram_5"]
    }
    
    # Extract screenshots into a list
    screenshots = []
    for i in range(2):
        key = f"screenshot_{i}"
        if key in raw_data and raw_data[key]:
            screenshots.append(raw_data[key])
    
    # Extract features into a list
    features = []
    for i in range(2):
        key = f"feature_{i}"
        if key in raw_data and raw_data[key]:
            features.append(raw_data[key])
    
    # Build final result with transformed structures
    result = {
        "title": raw_data["title"],
        "description": raw_data["description"],
        "descriptionHTML": raw_data["descriptionHTML"],
        "summary": raw_data["summary"],
        "installs": raw_data["installs"],
        "minInstalls": raw_data["minInstalls"],
        "maxInstalls": raw_data["maxInstalls"],
        "score": raw_data["score"],
        "scoreText": raw_data["scoreText"],
        "ratings": raw_data["ratings"],
        "reviews": raw_data["reviews"],
        "histogram": histogram,
        "price": raw_data["price"],
        "free": raw_data["free"],
        "currency": raw_data["currency"],
        "priceText": raw_data["priceText"],
        "offersIAP": raw_data["offersIAP"],
        "IAPRange": raw_data["IAPRange"],
        "androidVersion": raw_data["androidVersion"],
        "androidVersionText": raw_data["androidVersionText"],
        "developer": raw_data["developer"],
        "developerId": raw_data["developerId"],
        "developerEmail": raw_data["developerEmail"],
        "developerWebsite": raw_data["developerWebsite"],
        "developerAddress": raw_data["developerAddress"],
        "genre": raw_data["genre"],
        "genreId": raw_data["genreId"],
        "icon": raw_data["icon"],
        "headerImage": raw_data["headerImage"],
        "screenshots": screenshots,
        "contentRating": raw_data["contentRating"],
        "contentRatingDescription": raw_data["contentRatingDescription"],
        "adSupported": raw_data["adSupported"],
        "released": raw_data["released"],
        "updated": raw_data["updated"],
        "version": raw_data["version"],
        "recentChanges": raw_data["recentChanges"],
        "preregister": raw_data["preregister"],
        "editorsChoice": raw_data["editorsChoice"],
        "features": features
    }
    
    return result