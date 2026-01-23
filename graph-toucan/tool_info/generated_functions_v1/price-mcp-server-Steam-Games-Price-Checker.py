from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Steam Games Price Checker.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - game_data_name (str): official title of the game
        - game_data_type (str): category of the app (e.g., "game")
        - game_data_steam_appid (int): unique Steam application ID
        - game_data_required_age (int): minimum age requirement for access; 0 if none
        - game_data_is_free (bool): indicates whether the game is free to play
        - game_data_controller_support (str): level of controller support (e.g., "full")
        - game_data_dlc_0 (int): first associated DLC appID
        - game_data_detailed_description (str): full HTML-formatted description of the game
        - game_data_about_the_game (str): concise summary of the game's premise and features
        - game_data_short_description (str): brief one-paragraph overview of gameplay
        - game_data_supported_languages (str): comma-separated list of supported languages with audio indicators
        - game_data_header_image (str): URL to the main banner image
        - game_data_capsule_image (str): URL to the store capsule image (231x87)
        - game_data_capsule_imagev5 (str): URL to an alternate capsule image (184x69)
        - game_data_website (str): official website URL or null if not available
        - game_data_pc_requirements_minimum (str): minimum system specs as formatted text
        - game_data_pc_requirements_recommended (str): recommended system specs as formatted text
        - game_data_mac_requirements_minimum (str): minimum macOS specs as formatted text
        - game_data_mac_requirements_recommended (str): recommended macOS specs as formatted text
        - game_data_linux_requirements_minimum (str): minimum Linux specs as formatted text
        - game_data_linux_requirements_recommended (str): recommended Linux specs as formatted text
        - game_data_legal_notice (str): copyright and trademark information
        - game_data_developers_0 (str): first development studio involved
        - game_data_publishers_0 (str): first publishing company
        - game_data_price_overview_currency (str): ISO currency code (e.g., "USD")
        - game_data_price_overview_initial (int): original price in cents
        - game_data_price_overview_final (int): current discounted price in cents
        - game_data_price_overview_discount_percent (int): percentage discount applied
        - game_data_price_overview_initial_formatted (str): formatted original price string (may be empty)
        - game_data_price_overview_final_formatted (str): formatted final price string (e.g., "$9.99")
        - game_data_packages_0 (int): first associated package ID on Steam
        - game_data_package_groups_0_name (str): identifier for the group (e.g., "default")
        - game_data_package_groups_0_title (str): display title for the purchase option
        - game_data_package_groups_0_description (str): additional info about the package
        - game_data_package_groups_0_selection_text (str): prompt for user selection
        - game_data_package_groups_0_subs_0_packageid (int): ID of the package
        - game_data_package_groups_0_subs_0_percent_savings (int): percentage saved
        - game_data_package_groups_0_subs_0_option_text (str): display text showing price and name
        - game_data_package_groups_0_subs_0_price_in_cents_with_discount (int): final price in cents
        - game_data_platforms_windows (bool): available on Windows
        - game_data_platforms_mac (bool): available on macOS
        - game_data_platforms_linux (bool): available on Linux
        - game_data_metacritic_score (int): critic score out of 100
        - game_data_metacritic_url (str): link to the Metacritic page
        - game_data_categories_0_id (int): category identifier
        - game_data_categories_0_description (str): human-readable category name (e.g., "Single-player")
        - game_data_genres_0_id (str): genre ID
        - game_data_genres_0_description (str): genre name (e.g., "Action")
        - game_data_screenshots_0_id (int): screenshot sequence number
        - game_data_screenshots_0_path_thumbnail (str): URL to thumbnail version
        - game_data_screenshots_0_path_full (str): URL to full-resolution image
        - game_data_movies_0_id (int): video identifier
        - game_data_movies_0_name (str): title of the video
        - game_data_movies_0_thumbnail (str): URL to preview image
        - game_data_movies_0_webm_480 (str): 480p quality stream URL
        - game_data_movies_0_webm_max (str): highest quality stream URL
        - game_data_movies_0_mp4_480 (str): 480p quality stream URL
        - game_data_movies_0_mp4_max (str): highest quality stream URL
        - game_data_movies_0_highlight (bool): whether this is a featured video
        - game_data_recommendations_total (int): number of user recommendations
        - game_data_achievements_total (int): total number of achievements
        - game_data_achievements_highlighted_0_name (str): achievement title
        - game_data_achievements_highlighted_0_path (str): URL to achievement icon image
        - game_data_release_date_coming_soon (bool): whether the game has not yet been released
        - game_data_release_date_date (str): release date in format like "Dec 5, 2013"
        - game_data_support_info_url (str): support website URL
        - game_data_support_info_email (str): contact email address
        - game_data_background (str): URL to background image used on store page
        - game_data_background_raw (str): direct URL to unprocessed background image
        - game_data_content_descriptors_ids_0 (int): numeric code for content warning
        - game_data_content_descriptors_notes (str): additional context for content ratings
        - game_data_ratings_esrb_rating (str): age rating (e.g., "e10", "m")
        - game_data_ratings_esrb_descriptors (str): list of content reasons separated by line breaks
        - game_data_ratings_esrb_use_age_gate (str): "true" if age verification required
        - game_data_ratings_esrb_required_age (str): minimum age in years
        - game_data_ratings_pegi_rating (str): e.g., "7", "18"
        - game_data_ratings_pegi_descriptors (str): content reasons
        - game_data_ratings_pegi_use_age_gate (str): "true" if gate is used
        - game_data_ratings_pegi_required_age (str): minimum age
        - game_data_ratings_usk_rating (str): e.g., "12", "18"
        - game_data_ratings_usk_use_age_gate (str): "true" if applicable
        - game_data_ratings_usk_required_age (str): minimum age
        - game_data_ratings_oflc_rating (str): e.g., "g", "ma15"
        - game_data_ratings_oflc_descriptors (str): content notes
        - game_data_ratings_oflc_use_age_gate (str): "true" if enforced
        - game_data_ratings_oflc_required_age (str): minimum age
        - game_data_ratings_nzoflc_rating (str): e.g., "r16"
        - game_data_ratings_nzoflc_descriptors (str): content reasons
        - game_data_ratings_nzoflc_use_age_gate (str): "true" if enforced
        - game_data_ratings_nzoflc_required_age (str): minimum age
        - game_data_ratings_cero_rating (str): e.g., "z"
        - game_data_ratings_cero_descriptors (str): content reasons
        - game_data_ratings_cero_use_age_gate (str): "true" if enforced
        - game_data_ratings_cero_required_age (str): minimum age
        - game_data_ratings_kgrb_rating (str): e.g., "18"
        - game_data_ratings_kgrb_descriptors (str): content reasons
        - game_data_ratings_kgrb_use_age_gate (str): "true" if enforced
        - game_data_ratings_kgrb_required_age (str): minimum age
        - game_data_ratings_dejus_rating (str): e.g., "18"
        - game_data_ratings_dejus_descriptors (str): content reasons
        - game_data_ratings_dejus_use_age_gate (str): "true" if enforced
        - game_data_ratings_dejus_required_age (str): minimum age
        - game_data_ratings_mda_rating (str): e.g., "M18"
        - game_data_ratings_mda_descriptors (str): content reasons
        - game_data_ratings_mda_use_age_gate (str): "true" if enforced
        - game_data_ratings_mda_required_age (str): minimum age
        - game_data_ratings_csrr_rating (str): e.g., "R"
        - game_data_ratings_csrr_descriptors (str): content reasons
        - game_data_ratings_csrr_use_age_gate (str): "true" if enforced
        - game_data_ratings_csrr_required_age (str): minimum age
        - game_data_ratings_crl_rating (str): e.g., "16"
        - game_data_ratings_crl_use_age_gate (str): "true" if enforced
        - game_data_ratings_crl_required_age (str): minimum age
        - success (bool): indicates whether the query was successful
    """
    return {
        "game_data_name": "Half-Life 2",
        "game_data_type": "game",
        "game_data_steam_appid": 220,
        "game_data_required_age": 16,
        "game_data_is_free": False,
        "game_data_controller_support": "full",
        "game_data_dlc_0": 300,
        "game_data_detailed_description": "<p>Half-Life 2 is a landmark in gaming...</p>",
        "game_data_about_the_game": "Half-Life 2 is a first-person shooter that redefined the genre...",
        "game_data_short_description": "A revolutionary new single-player game from Valve...",
        "game_data_supported_languages": "English, French, Italian, German, Spanish - Spain, Japanese, Korean, Portuguese - Brazil, Russian, Simplified Chinese, Traditional Chinese",
        "game_data_header_image": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/220/header.jpg",
        "game_data_capsule_image": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/220/capsule_231x87.jpg",
        "game_data_capsule_imagev5": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/220/capsule_184x69.jpg",
        "game_data_website": "http://www.half-life2.com",
        "game_data_pc_requirements_minimum": "<b>Minimum:</b><br>OS: Windows 10 (64-bit)<br>Processor: Intel Core i5-4460 or AMD FX-6300<br>Memory: 8 GB RAM<br>Graphics: NVIDIA GeForce GTX 960 or AMD Radeon R9 280<br>DirectX: Version 11<br>Storage: 30 GB available space",
        "game_data_pc_requirements_recommended": "<b>Recommended:</b><br>OS: Windows 10 (64-bit)<br>Processor: Intel Core i7-3770 or AMD FX-8350<br>Memory: 16 GB RAM<br>Graphics: NVIDIA GeForce GTX 1060 or AMD Radeon RX 580<br>DirectX: Version 11<br>Storage: 30 GB available space",
        "game_data_mac_requirements_minimum": "<b>Minimum:</b><br>OS: macOS 10.13<br>Processor: Intel Core i5<br>Memory: 8 GB RAM<br>Graphics: Intel Iris Plus Graphics 640<br>Storage: 30 GB available space",
        "game_data_mac_requirements_recommended": "<b>Recommended:</b><br>OS: macOS 10.15<br>Processor: Intel Core i7<br>Memory: 16 GB RAM<br>Graphics: AMD Radeon Pro 555X<br>Storage: 30 GB available space",
        "game_data_linux_requirements_minimum": "<b>Minimum:</b><br>OS: Ubuntu 18.04<br>Processor: Intel Core i5-4460 or AMD FX-6300<br>Memory: 8 GB RAM<br>Graphics: NVIDIA GeForce GTX 960 or AMD Radeon R9 280<br>Storage: 30 GB available space",
        "game_data_linux_requirements_recommended": "<b>Recommended:</b><br>OS: Ubuntu 20.04<br>Processor: Intel Core i7-3770 or AMD FX-8350<br>Memory: 16 GB RAM<br>Graphics: NVIDIA GeForce GTX 1060 or AMD Radeon RX 580<br>Storage: 30 GB available space",
        "game_data_legal_notice": "Valve, the Valve logo, Half-Life, the Half-Life logo, the Lambda logo, Steam, the Steam logo, Team Fortress, the Team Fortress logo, Opposing Force, Day of Defeat, the Day of Defeat logo, Counter-Strike, the Counter-Strike logo, Source, the Source logo, Counter-Strike: Condition Zero, Portal, the Portal logo, Dota, the Dota 2 logo, and Defense of the Ancients are trademarks and/or registered trademarks of Valve Corporation.",
        "game_data_developers_0": "Valve",
        "game_data_publishers_0": "Valve",
        "game_data_price_overview_currency": "USD",
        "game_data_price_overview_initial": 999,
        "game_data_price_overview_final": 999,
        "game_data_price_overview_discount_percent": 0,
        "game_data_price_overview_initial_formatted": "$9.99",
        "game_data_price_overview_final_formatted": "$9.99",
        "game_data_packages_0": 12345,
        "game_data_package_groups_0_name": "default",
        "game_data_package_groups_0_title": "Half-Life 2",
        "game_data_package_groups_0_description": "",
        "game_data_package_groups_0_selection_text": "Select a purchase option",
        "game_data_package_groups_0_subs_0_packageid": 12345,
        "game_data_package_groups_0_subs_0_percent_savings": 0,
        "game_data_package_groups_0_subs_0_option_text": "Half-Life 2 - $9.99",
        "game_data_package_groups_0_subs_0_price_in_cents_with_discount": 999,
        "game_data_platforms_windows": True,
        "game_data_platforms_mac": True,
        "game_data_platforms_linux": True,
        "game_data_metacritic_score": 96,
        "game_data_metacritic_url": "https://www.metacritic.com/game/pc/half-life-2",
        "game_data_categories_0_id": 2,
        "game_data_categories_0_description": "Single-player",
        "game_data_genres_0_id": "1",
        "game_data_genres_0_description": "Action",
        "game_data_screenshots_0_id": 1,
        "game_data_screenshots_0_path_thumbnail": "https://shared.cloudflare.steamstatic.com/steam/apps/220/0000001_thumb.jpg",
        "game_data_screenshots_0_path_full": "https://shared.cloudflare.steamstatic.com/steam/apps/220/0000001_full.jpg",
        "game_data_movies_0_id": 1,
        "game_data_movies_0_name": "Launch Trailer",
        "game_data_movies_0_thumbnail": "https://shared.cloudflare.steamstatic.com/steam/apps/220/movie.293x165.jpg",
        "game_data_movies_0_webm_480": "https://shared.cloudflare.steamstatic.com/steam/apps/220/movie480.webm",
        "game_data_movies_0_webm_max": "https://shared.cloudflare.steamstatic.com/steam/apps/220/movie_max.webm",
        "game_data_movies_0_mp4_480": "https://shared.cloudflare.steamstatic.com/steam/apps/220/movie480.mp4",
        "game_data_movies_0_mp4_max": "https://shared.cloudflare.steamstatic.com/steam/apps/220/movie_max.mp4",
        "game_data_movies_0_highlight": True,
        "game_data_recommendations_total": 150000,
        "game_data_achievements_total": 50,
        "game_data_achievements_highlighted_0_name": "Barney!",
        "game_data_achievements_highlighted_0_path": "https://shared.cloudflare.steamstatic.com/steamcommunity/public/images/apps/220/achievement_icon.jpg",
        "game_data_release_date_coming_soon": False,
        "game_data_release_date_date": "Nov 16, 2004",
        "game_data_support_info_url": "https://support.steampowered.com",
        "game_data_support_info_email": "support@steampowered.com",
        "game_data_background": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/220/page_bg.jpg",
        "game_data_background_raw": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/220/page_bg_raw.jpg",
        "game_data_content_descriptors_ids_0": 2,
        "game_data_content_descriptors_notes": "Includes intense violence and blood.",
        "game_data_ratings_esrb_rating": "m",
        "game_data_ratings_esrb_descriptors": "Violence\nBlood",
        "game_data_ratings_esrb_use_age_gate": "true",
        "game_data_ratings_esrb_required_age": "17",
        "game_data_ratings_pegi_rating": "16",
        "game_data_ratings_pegi_descriptors": "Violence",
        "game_data_ratings_pegi_use_age_gate": "true",
        "game_data_ratings_pegi_required_age": "16",
        "game_data_ratings_usk_rating": "16",
        "game_data_ratings_usk_use_age_gate": "true",
        "game_data_ratings_usk_required_age": "16",
        "game_data_ratings_oflc_rating": "ma15",
        "game_data_ratings_oflc_descriptors": "Strong violence",
        "game_data_ratings_oflc_use_age_gate": "true",
        "game_data_ratings_oflc_required_age": "15",
        "game_data_ratings_nzoflc_rating": "r16",
        "game_data_ratings_nzoflc_descriptors": "Violence",
        "game_data_ratings_nzoflc_use_age_gate": "true",
        "game_data_ratings_nzoflc_required_age": "16",
        "game_data_ratings_cero_rating": "z",
        "game_data_ratings_cero_descriptors": "Violence",
        "game_data_ratings_cero_use_age_gate": "true",
        "game_data_ratings_cero_required_age": "18",
        "game_data_ratings_kgrb_rating": "18",
        "game_data_ratings_kgrb_descriptors": "Violence",
        "game_data_ratings_kgrb_use_age_gate": "true",
        "game_data_ratings_kgrb_required_age": "18",
        "game_data_ratings_dejus_rating": "18",
        "game_data_ratings_dejus_descriptors": "Violence",
        "game_data_ratings_dejus_use_age_gate": "true",
        "game_data_ratings_dejus_required_age": "18",
        "game_data_ratings_mda_rating": "M18",
        "game_data_ratings_mda_descriptors": "Violence",
        "game_data_ratings_mda_use_age_gate": "true",
        "game_data_ratings_mda_required_age": "18",
        "game_data_ratings_csrr_rating": "R",
        "game_data_ratings_csrr_descriptors": "Violence",
        "game_data_ratings_csrr_use_age_gate": "true",
        "game_data_ratings_csrr_required_age": "18",
        "game_data_ratings_crl_rating": "16",
        "game_data_ratings_crl_use_age_gate": "true",
        "game_data_ratings_crl_required_age": "16",
        "success": True
    }

def price_mcp_server_Steam_Games_Price_Checker(appId: str, countryCode: str) -> Dict[str, Any]:
    """
    Query Steam games price based on game appID and region code.
    
    This function retrieves detailed information about a Steam game including name, pricing,
    platform support, and metadata by querying an external API using the provided appID and
    country code for regional pricing.
    
    Args:
        appId (str): The unique Steam application ID of the game (required)
        countryCode (str): The two-letter country code for regional pricing (required)
    
    Returns:
        Dict containing:
        - game_data (Dict): Comprehensive information about the game with the following structure:
            - name (str): Official title of the game
            - type (str): Category of the app (e.g., "game")
            - steam_appid (int): Unique Steam application ID
            - required_age (int): Minimum age requirement for access; 0 if none
            - is_free (bool): Indicates whether the game is free to play
            - controller_support (str): Level of controller support (e.g., "full")
            - dlc (List[int]): List of associated DLC appIDs, if any
            - detailed_description (str): Full HTML-formatted description of the game
            - about_the_game (str): Concise summary of the game's premise and features
            - short_description (str): Brief one-paragraph overview of gameplay
            - supported_languages (str): Comma-separated list of supported languages with audio indicators
            - header_image (str): URL to the main banner image
            - capsule_image (str): URL to the store capsule image (231x87)
            - capsule_imagev5 (str): URL to an alternate capsule image (184x69)
            - website (str or None): Official website URL or None if not available
            - pc_requirements (Dict): Minimum and recommended PC system requirements in HTML format
                - minimum (str): Minimum system specs as formatted text
                - recommended (str): Recommended system specs as formatted text
            - mac_requirements (Dict or List): System requirements for macOS; may be empty or absent
                - minimum (str): Minimum macOS specs as formatted text
                - recommended (str): Recommended macOS specs as formatted text
            - linux_requirements (Dict or List): System requirements for Linux; may be empty or absent
                - minimum (str): Minimum Linux specs as formatted text
                - recommended (str): Recommended Linux specs as formatted text
            - legal_notice (str): Copyright and trademark information
            - developers (List[str]): List of development studios involved
            - publishers (List[str]): List of publishing companies
            - price_overview (Dict): Current pricing details
                - currency (str): ISO currency code (e.g., "USD")
                - initial (int): Original price in cents
                - final (int): Current discounted price in cents
                - discount_percent (int): Percentage discount applied
                - initial_formatted (str): Formatted original price string (may be empty)
                - final_formatted (str): Formatted final price string (e.g., "$9.99")
            - packages (List[int]): List of associated package IDs on Steam
            - package_groups (List[Dict]): Purchase options available
                - name (str): Identifier for the group (e.g., "default")
                - title (str): Display title for the purchase option
                - description (str): Additional info about the package
                - selection_text (str): Prompt for user selection
                - subs (List[Dict]): List of purchasable items within this group
                    - packageid (int): ID of the package
                    - percent_savings (int): Percentage saved
                    - option_text (str): Display text showing price and name
                    - price_in_cents_with_discount (int): Final price in cents
            - platforms (Dict): Availability across operating systems
                - windows (bool): Available on Windows
                - mac (bool): Available on macOS
                - linux (bool): Available on Linux
            - metacritic (Dict or None): Review score from Metacritic
                - score (int): Critic score out of 100
                - url (str): Link to the Metacritic page
            - categories (List[Dict]): List of Steam category tags
                - id (int): Category identifier
                - description (str): Human-readable category name (e.g., "Single-player")
            - genres (List[Dict]): Primary genre classifications
                - id (str): Genre ID
                - description (str): Genre name (e.g., "Action")
            - screenshots (List[Dict]): Media assets showing gameplay
                - id (int): Screenshot sequence number
                - path_thumbnail (str): URL to thumbnail version
                - path_full (str): URL to full-resolution image
            - movies (List[Dict]): Promotional videos or trailers
                - id (int): Video identifier
                - name (str): Title of the video
                - thumbnail (str): URL to preview image
                - webm (Dict): WebM format streaming links
                    - 480 (str): 480p quality stream URL
                    - max (str): Highest quality stream URL
                - mp4 (Dict): MP4 format streaming links
                    - 480 (str): 480p quality stream URL
                    - max (str): Highest quality stream URL
                - highlight (bool): Whether this is a featured video
            - recommendations (Dict or None): Community recommendation stats
                - total (int): Number of user recommendations
            - achievements (Dict or None): In-game achievement data
                - total (int): Total number of achievements
                - highlighted (List[Dict]): Notable achievements with icons
                    - name (str): Achievement title
                    - path (str): URL to achievement icon image
            - release_date (Dict): Launch timeline
                - coming_soon (bool): Whether the game has not yet been released
                - date (str): Release date in format like "Dec 5, 2013"
            - support_info (Dict): Customer service contact details
                - url (str): Support website URL
                - email (str): Contact email address
            - background (str): URL to background image used on store page
            - background_raw (str): Direct URL to unprocessed background image
            - content_descriptors (Dict): Age-rating descriptors
                - ids (List[int]): Numeric codes for content warnings
                - notes (str or None): Additional context for content ratings
            - ratings (Dict or None): Various regional age rating bodies' assessments
                - esrb (Dict): ESRB rating details
                    - rating (str): Age rating (e.g., "e10", "m")
                    - descriptors (str): List of content reasons separated by line breaks
                    - use_age_gate (str): "true" if age verification required
                    - required_age (str): Minimum age in years
                - pegi (Dict): PEGI rating details
                    - rating (str): e.g., "7", "18"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if gate is used
                    - required_age (str): Minimum age
                - usk (Dict): USK (Germany) rating
                    - rating (str): e.g., "12", "18"
                    - use_age_gate (str): "true" if applicable
                    - required_age (str): Minimum age
                - oflc (Dict): OFLC (Australia) rating
                    - rating (str): e.g., "g", "ma15"
                    - descriptors (str): Content notes
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - nzoflc (Dict): NZOFLC rating
                    - rating (str): e.g., "r16"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - cero (Dict): CERO (Japan) rating
                    - rating (str): e.g., "z"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - kgrb (Dict): KGRB (South Korea) rating
                    - rating (str): e.g., "18"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - dejus (Dict): DEJUS (Brazil) rating
                    - rating (str): e.g., "18"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - mda (Dict): MDA (Singapore) rating
                    - rating (str): e.g., "M18"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - csrr (Dict): CSRR (Russia) rating
                    - rating (str): e.g., "R"
                    - descriptors (str): Content reasons
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
                - crl (Dict): CRL (Indonesia) rating
                    - rating (str): e.g., "16"
                    - use_age_gate (str): "true" if enforced
                    - required_age (str): Minimum age
        - success (bool): Indicates whether the query was successful
    
    Raises:
        ValueError: If appId or countryCode is empty or invalid
    """
    # Input validation
    if not appId or not isinstance(appId, str) or not appId.strip():
        raise ValueError("appId is required and must be a non-empty string")
    
    if not countryCode or not isinstance(countryCode, str) or not countryCode.strip():
        raise ValueError("countryCode is required and must be a non-empty string")
    
    # Clean inputs
    appId = appId.strip()
    countryCode = countryCode.strip().upper()
    
    # Validate country code format (2-letter)
    if len(countryCode) != 2:
        raise ValueError("countryCode must be a valid 2-letter country code")
    
    try:
        # Call external API to get data
        api_data = call_external_api("price-mcp-server-Steam Games Price Checker")
        
        # Construct the nested game_data structure from flat API response
        game_data = {
            "name": api_data["game_data_name"],
            "type": api_data["game_data_type"],
            "steam_appid": api_data["game_data_steam_appid"],
            "required_age": api_data["game_data_required_age"],
            "is_free": api_data["game_data_is_free"],
            "controller_support": api_data["game_data_controller_support"],
            "dlc": [api_data["game_data_dlc_0"]] if api_data.get("game_data_dlc_0") else [],
            "detailed_description": api_data["game_data_detailed_description"],
            "about_the_game": api_data["game_data_about_the_game"],
            "short_description": api_data["game_data_short_description"],
            "supported_languages": api_data["game_data_supported_languages"],
            "header_image": api_data["game_data_header_image"],
            "capsule_image": api_data["game_data_capsule_image"],
            "capsule_imagev5": api_data["game_data_capsule_imagev5"],
            "website": api_data["game_data_website"] if api_data["game_data_website"] != "null" else None,
            "pc_requirements": {
                "minimum": api_data["game_data_pc_requirements_minimum"],
                "recommended": api_data["game_data_pc_requirements_recommended"]
            },
            "mac_requirements": {
                "minimum": api_data["game_data_mac_requirements_minimum"],
                "recommended": api_data["game_data_mac_requirements_recommended"]
            } if "game_data_mac_requirements_minimum" in api_data else [],
            "linux_requirements": {
                "minimum": api_data["game_data_linux_requirements_minimum"],
                "recommended": api_data["game_data_linux_requirements_recommended"]
            } if "game_data_linux_requirements_minimum" in api_data else [],
            "legal_notice": api_data["game_data_legal_notice"],
            "developers": [api_data["game_data_developers_0"]] if api_data.get("game_data_developers_0") else [],
            "publishers": [api_data["game_data_publishers_0"]] if api_data.get("game_data_publishers_0") else [],
            "price_overview": {
                "currency": api_data["game_data_price_overview_currency"],
                "initial": api_data["game_data_price_overview_initial"],
                "final": api_data["game_data_price_overview_final"],
                "discount_percent": api_data["game_data_price_overview_discount_percent"],
                "initial_formatted": api_data["game_data_price_overview_initial_formatted"],
                "final_formatted": api_data["game_data_price_overview_final_formatted"]
            } if not api_data["game_data_is_free"] else None,
            "packages": [api_data["game_data_packages_0"]] if api_data.get("game_data_packages_0") else [],
            "package_groups": [
                {
                    "name": api_data["game_data_package_groups_0_name"],
                    "title": api_data["game_data_package_groups_0_title"],
                    "description": api_data["game_data_package_groups_0_description"],
                    "selection_text": api_data["game_data_package_groups_0_selection_text"],
                    "subs": [
                        {
                            "packageid": api_data["game_data_package_groups_0_subs_0_packageid"],
                            "percent_savings": api_data["game_data_package_groups_0_subs_0_percent_savings"],
                            "option_text": api_data["game_data_package_groups_0_subs_0_option_text"],
                            "price_in_cents_with_discount": api_data["game_data_package_groups_0_subs_0_price_in_cents_with_discount"]
                        }
                    ]
                }
            ],
            "platforms": {
                "windows": api_data["game_data_platforms_windows"],
                "mac": api_data["game_data_platforms_mac"],
                "linux": api_data["game_data_platforms_linux"]
            },
            "metacritic": {
                "score": api_data["game_data_metacritic_score"],
                "url": api_data["game_data_metacritic_url"]
            } if api_data.get("game_data_metacritic_score") else None,
            "categories": [
                {
                    "id": api_data["game_data_categories_0_id"],
                    "description": api_data["game_data_categories_0_description"]
                }
            ],
            "genres": [
                {
                    "id": api_data["game_data_genres_0_id"],
                    "description": api_data["game_data_genres_0_description"]
                }
            ],
            "screenshots": [
                {
                    "id": api_data["game_data_screenshots_0_id"],
                    "path_thumbnail": api_data["game_data_screenshots_0_path_thumbnail"],
                    "path_full": api_data["game_data_screenshots_0_path_full"]
                }
            ],
            "movies": [
                {
                    "id": api_data["game_data_movies_0_id"],
                    "name": api_data["game_data_movies_0_name"],
                    "thumbnail": api_data["game_data_movies_0_thumbnail"],
                    "webm": {
                        "480": api_data["game_data_movies_0_webm_480"],
                        "max": api_data["game_data_movies_0_webm_max"]
                    },
                    "mp4": {
                        "480": api_data["game_data_movies_0_mp4_480"],
                        "max": api_data["game_data_movies_0_mp4_max"]
                    },
                    "highlight": api_data["game_data_movies_0_highlight"]
                }
            ],
            "recommendations": {
                "total": api_data["game_data_recommendations_total"]
            } if api_data.get("game_data_recommendations_total") else None,
            "achievements": {
                "total": api_data["game_data_achievements_total"],
                "highlighted": [
                    {
                        "name": api_data["game_data_achievements_highlighted_0_name"],
                        "path": api_data["game_data_achievements_highlighted_0_path"]
                    }
                ]
            } if api_data.get("game_data_achievements_total") else None,
            "release_date": {
                "coming_soon": api_data["game_data_release_date_coming_soon"],
                "date": api_data["game_data_release_date_date"]
            },
            "support_info": {
                "url": api_data["game_data_support_info_url"],
                "email": api_data["game_data_support_info_email"]
            },
            "background": api_data["game_data_background"],
            "background_raw": api_data["game_data_background_raw"],
            "content_descriptors": {
                "ids": [api_data["game_data_content_descriptors_ids_0"]] if api_data.get("game_data_content_descriptors_ids_0") else [],
                "notes": api_data["game_data_content_descriptors_notes"] if api_data["game_data_content_descriptors_notes"] != "null" else None
            },
            "ratings": {
                "esrb": {
                    "rating": api_data["game_data_ratings_esrb_rating"],
                    "descriptors": api_data["game_data_ratings_esrb_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_esrb_use_age_gate"],
                    "required_age": api_data["game_data_ratings_esrb_required_age"]
                } if api_data.get("game_data_ratings_esrb_rating") else None,
                "pegi": {
                    "rating": api_data["game_data_ratings_pegi_rating"],
                    "descriptors": api_data["game_data_ratings_pegi_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_pegi_use_age_gate"],
                    "required_age": api_data["game_data_ratings_pegi_required_age"]
                } if api_data.get("game_data_ratings_pegi_rating") else None,
                "usk": {
                    "rating": api_data["game_data_ratings_usk_rating"],
                    "use_age_gate": api_data["game_data_ratings_usk_use_age_gate"],
                    "required_age": api_data["game_data_ratings_usk_required_age"]
                } if api_data.get("game_data_ratings_usk_rating") else None,
                "oflc": {
                    "rating": api_data["game_data_ratings_oflc_rating"],
                    "descriptors": api_data["game_data_ratings_oflc_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_oflc_use_age_gate"],
                    "required_age": api_data["game_data_ratings_oflc_required_age"]
                } if api_data.get("game_data_ratings_oflc_rating") else None,
                "nzoflc": {
                    "rating": api_data["game_data_ratings_nzoflc_rating"],
                    "descriptors": api_data["game_data_ratings_nzoflc_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_nzoflc_use_age_gate"],
                    "required_age": api_data["game_data_ratings_nzoflc_required_age"]
                } if api_data.get("game_data_ratings_nzoflc_rating") else None,
                "cero": {
                    "rating": api_data["game_data_ratings_cero_rating"],
                    "descriptors": api_data["game_data_ratings_cero_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_cero_use_age_gate"],
                    "required_age": api_data["game_data_ratings_cero_required_age"]
                } if api_data.get("game_data_ratings_cero_rating") else None,
                "kgrb": {
                    "rating": api_data["game_data_ratings_kgrb_rating"],
                    "descriptors": api_data["game_data_ratings_kgrb_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_kgrb_use_age_gate"],
                    "required_age": api_data["game_data_ratings_kgrb_required_age"]
                } if api_data.get("game_data_ratings_kgrb_rating") else None,
                "dejus": {
                    "rating": api_data["game_data_ratings_dejus_rating"],
                    "descriptors": api_data["game_data_ratings_dejus_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_dejus_use_age_gate"],
                    "required_age": api_data["game_data_ratings_dejus_required_age"]
                } if api_data.get("game_data_ratings_dejus_rating") else None,
                "mda": {
                    "rating": api_data["game_data_ratings_mda_rating"],
                    "descriptors": api_data["game_data_ratings_mda_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_mda_use_age_gate"],
                    "required_age": api_data["game_data_ratings_mda_required_age"]
                } if api_data.get("game_data_ratings_mda_rating") else None,
                "csrr": {
                    "rating": api_data["game_data_ratings_csrr_rating"],
                    "descriptors": api_data["game_data_ratings_csrr_descriptors"],
                    "use_age_gate": api_data["game_data_ratings_csrr_use_age_gate"],
                    "required_age": api_data["game_data_ratings_csrr_required_age"]
                } if api_data.get("game_data_ratings_csrr_rating") else None,
                "crl": {
                    "rating": api_data["game_data_ratings_crl_rating"],
                    "use_age_gate": api_data["game_data_ratings_crl_use_age_gate"],
                    "required_age": api_data["game_data_ratings_crl_required_age"]
                } if api_data.get("game_data_ratings_crl_rating") else None
            }
        }
        
        return {
            "game_data": game_data,
            "success": api_data["success"]
        }
        
    except Exception as e:
        return {
            "game_data": {},
            "success": False
        }