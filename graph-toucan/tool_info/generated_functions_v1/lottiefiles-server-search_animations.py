from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Lottie animations search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - count (int): Total number of animations matching the search query
        - animations_0_id (str): Unique identifier for the animation
        - animations_0_name (str): Display name of the animation
        - animations_0_slug (str): URL-friendly version of the name
        - animations_0_type (str): License type of the animation (e.g., "FREE", "PREMIUM")
        - animations_0_status (str): Publication status (e.g., "PUBLISHED")
        - animations_0_description (str): Brief description of the animation
        - animations_0_createdAt (int): Unix timestamp when the animation was created
        - animations_0_updatedAt (int): Unix timestamp when the animation was last updated
        - animations_0_publishedAt (int): Unix timestamp when the animation was published
        - animations_0_bgColor (str): Background color in hex format
        - animations_0_speed (str): Playback speed setting
        - animations_0_isSticker (bool): Whether the animation is a sticker format
        - animations_0_downloadCount (int): Number of times the animation has been downloaded
        - animations_0_aepAvailable (bool): Whether After Effects project is available
        - animations_0_isAnimatorHireable (bool): Whether the creator is available for hire
        - animations_0_gifUrl (str): URL to animated GIF preview
        - animations_0_imageSource (str): URL to static image preview
        - animations_0_jsonSource (str): URL to JSON file (Lottie format)
        - animations_0_lottieSource (str): URL to .lottie binary file
        - animations_0_videoSource (str): URL to video preview (MP4)
        - animations_0_tags_0 (str): First tag associated with the animation
        - animations_0_userTags_0 (str): First user-provided tag
        - animations_0_mlTags_0 (str): First machine-learning generated tag
        - animations_0_metaDataV2_animations_0_id (str): Internal ID of the animation track
        - animations_0_metaDataV2_animations_0_width (int): Width in pixels
        - animations_0_metaDataV2_animations_0_height (int): Height in pixels
        - animations_0_metaDataV2_animations_0_frames (float): Total number of frames
        - animations_0_metaDataV2_animations_0_frameRate (float): Frames per second
        - animations_0_metaDataV2_animations_0_layers (int): Number of layers in the animation
        - animations_0_metaDataV2_animations_0_colors_0_0 (float): First R value of first color
        - animations_0_metaDataV2_animations_0_colors_0_1 (float): First G value of first color
        - animations_0_metaDataV2_animations_0_colors_0_2 (float): First B value of first color
        - animations_0_metaDataV2_animations_0_colors_0_3 (float): First A value of first color
        - animations_0_metaDataV2_animations_0_fileSize (int): Size of the animation data in bytes
        - animations_0_metaDataV2_animations_0_generator (str): Tool used to generate the animation
        - animations_0_metaDataV2_animations_0_version (str): Version of the generator
        - animations_0_metaDataV2_animations_0_inPoint (float): Start frame of the visible animation
        - animations_0_metaDataV2_animations_0_outPoint (float): End frame of the visible animation
        - animations_0_user_id (str): Unique identifier of the user
        - animations_0_user_name (str): Full name of the user
        - animations_0_user_username (str): Username/handle
        - animations_0_user_avatarUrl (str): URL to user's avatar image
        - animations_0_user_isHireable (bool): Whether the user is open to freelance work
        - animations_0_user_legacyWebUserId (str): Legacy user ID
        - animations_0_user_state (str): Account state
        - animations_0_user_preference_preferredLang (str): Preferred language code
        - animations_0_user_preference_hasWorkspace (bool): Whether user has a workspace
        - animations_0_user_preference_hasPaidWorkspace (bool): Whether user has a paid plan
        - animations_0_user_preference_animationAutoplayProfile (bool): Autoplay preference
        - animations_0_user_preference_fileCount (int): Number of files uploaded by user
        - animations_0_user_preference_isLottieExpert (bool): Whether user is marked as expert
        - animations_0_user_preference_courses_0_id (str): First course ID
        - animations_0_user_preference_courses_0_slug (str): First course slug
        - animations_0_user_preference_courses_0_name (str): First course name
        - animations_0_user_preference_courses_0_shortName (str): First course short name
        - animations_0_user_preference_courses_0_courseUrl (str): First course URL
        - animations_0_user_preference_courses_0_isActive (bool): Whether first course is active
        - animations_0_user_preference_courses_0_tool_name (str): First course tool name
        - animations_0_user_preference_courses_0_tool_slug (str): First course tool slug
        - animations_0_fileVariations_0 (str): First file variation (placeholder)
        - animations_0_tools_0 (str): First tool used (placeholder)
    """
    return {
        "count": 125,
        "animations_0_id": "anim123",
        "animations_0_name": "Loading Spinner",
        "animations_0_slug": "loading-spinner",
        "animations_0_type": "FREE",
        "animations_0_status": "PUBLISHED",
        "animations_0_description": "A smooth circular loading animation",
        "animations_0_createdAt": 1620000000,
        "animations_0_updatedAt": 1625000000,
        "animations_0_publishedAt": 1622000000,
        "animations_0_bgColor": "#FFFFFF",
        "animations_0_speed": "1",
        "animations_0_isSticker": False,
        "animations_0_downloadCount": 1500,
        "animations_0_aepAvailable": True,
        "animations_0_isAnimatorHireable": True,
        "animations_0_gifUrl": "https://example.com/anim123.gif",
        "animations_0_imageSource": "https://example.com/anim123.png",
        "animations_0_jsonSource": "https://example.com/anim123.json",
        "animations_0_lottieSource": "https://example.com/anim123.lottie",
        "animations_0_videoSource": "https://example.com/anim123.mp4",
        "animations_0_tags_0": "loading",
        "animations_0_userTags_0": "spinner",
        "animations_0_mlTags_0": "circle",
        "animations_0_metaDataV2_animations_0_id": "track1",
        "animations_0_metaDataV2_animations_0_width": 200,
        "animations_0_metaDataV2_animations_0_height": 200,
        "animations_0_metaDataV2_animations_0_frames": 30.0,
        "animations_0_metaDataV2_animations_0_frameRate": 30.0,
        "animations_0_metaDataV2_animations_0_layers": 5,
        "animations_0_metaDataV2_animations_0_colors_0_0": 0.0,
        "animations_0_metaDataV2_animations_0_colors_0_1": 0.5,
        "animations_0_metaDataV2_animations_0_colors_0_2": 1.0,
        "animations_0_metaDataV2_animations_0_colors_0_3": 1.0,
        "animations_0_metaDataV2_animations_0_fileSize": 15320,
        "animations_0_metaDataV2_animations_0_generator": "LottieFiles AE Plugin",
        "animations_0_metaDataV2_animations_0_version": "3.5.1",
        "animations_0_metaDataV2_animations_0_inPoint": 0.0,
        "animations_0_metaDataV2_animations_0_outPoint": 30.0,
        "animations_0_user_id": "user456",
        "animations_0_user_name": "John Doe",
        "animations_0_user_username": "johndoe",
        "animations_0_user_avatarUrl": "https://example.com/avatar.jpg",
        "animations_0_user_isHireable": True,
        "animations_0_user_legacyWebUserId": "web789",
        "animations_0_user_state": "active",
        "animations_0_user_preference_preferredLang": "EN",
        "animations_0_user_preference_hasWorkspace": True,
        "animations_0_user_preference_hasPaidWorkspace": False,
        "animations_0_user_preference_animationAutoplayProfile": True,
        "animations_0_user_preference_fileCount": 45,
        "animations_0_user_preference_isLottieExpert": False,
        "animations_0_user_preference_courses_0_id": "course001",
        "animations_0_user_preference_courses_0_slug": "intro-lottie",
        "animations_0_user_preference_courses_0_name": "Introduction to Lottie",
        "animations_0_user_preference_courses_0_shortName": "Intro",
        "animations_0_user_preference_courses_0_courseUrl": "https://example.com/course001",
        "animations_0_user_preference_courses_0_isActive": True,
        "animations_0_user_preference_courses_0_tool_name": "Figma",
        "animations_0_user_preference_courses_0_tool_slug": "figma",
        "animations_0_fileVariations_0": "variation1",
        "animations_0_tools_0": "After Effects"
    }


def lottiefiles_server_search_animations(limit: Optional[int] = None, page: Optional[int] = None, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for Lottie animations by keywords, tags, and other criteria. Supports pagination.

    Args:
        limit (int, optional): Number of items per page. Defaults to None.
        page (int, optional): Page number, starting from 1. Defaults to None.
        query (str, optional): Search keywords that match animation names, descriptions, tags, etc. Defaults to None.

    Returns:
        Dict containing:
        - count (int): total number of animations matching the search query
        - animations (List[Dict]): list of animation objects containing details such as name, ID, source URLs, tags, metadata, and user information
          Each animation dict includes:
          - id (str): unique identifier
          - name (str): display name
          - slug (str): URL-friendly name
          - type (str): license type ("FREE", "PREMIUM")
          - status (str): publication status
          - description (str): brief description
          - createdAt (int): creation timestamp
          - updatedAt (int): last update timestamp
          - publishedAt (int): publication timestamp
          - bgColor (str): background color in hex
          - speed (str): playback speed
          - isSticker (bool): whether it's a sticker
          - downloadCount (int): number of downloads
          - aepAvailable (bool): whether AE project is available
          - isAnimatorHireable (bool): whether creator is hireable
          - gifUrl (str): GIF preview URL
          - imageSource (str): static image URL
          - jsonSource (str): JSON file URL
          - lottieSource (str): .lottie file URL
          - videoSource (str): video preview URL
          - tags (List[str]): list of tags
          - userTags (List[str]): user-provided tags
          - mlTags (List[str]): ML-generated tags
          - metaDataV2 (Dict): extended metadata
          - user (Dict): creator info
          - fileVariations (List): alternative file versions
          - tools (List): tools used

    Raises:
        ValueError: If page or limit is less than 1
    """
    # Input validation
    if page is not None and page < 1:
        raise ValueError("Page number must be at least 1")
    if limit is not None and limit < 1:
        raise ValueError("Limit must be at least 1")

    # Call external API to get flattened data
    api_data = call_external_api("lottiefiles_server_search_animations")

    # Construct nested animation object
    animation = {
        "id": api_data["animations_0_id"],
        "name": api_data["animations_0_name"],
        "slug": api_data["animations_0_slug"],
        "type": api_data["animations_0_type"],
        "status": api_data["animations_0_status"],
        "description": api_data["animations_0_description"],
        "createdAt": api_data["animations_0_createdAt"],
        "updatedAt": api_data["animations_0_updatedAt"],
        "publishedAt": api_data["animations_0_publishedAt"],
        "bgColor": api_data["animations_0_bgColor"],
        "speed": api_data["animations_0_speed"],
        "isSticker": api_data["animations_0_isSticker"],
        "downloadCount": api_data["animations_0_downloadCount"],
        "aepAvailable": api_data["animations_0_aepAvailable"],
        "isAnimatorHireable": api_data["animations_0_isAnimatorHireable"],
        "gifUrl": api_data["animations_0_gifUrl"],
        "imageSource": api_data["animations_0_imageSource"],
        "jsonSource": api_data["animations_0_jsonSource"],
        "lottieSource": api_data["animations_0_lottieSource"],
        "videoSource": api_data["animations_0_videoSource"],
        "tags": [api_data["animations_0_tags_0"]],
        "userTags": [api_data["animations_0_userTags_0"]],
        "mlTags": [api_data["animations_0_mlTags_0"]],
        "metaDataV2": {
            "animations": [
                {
                    "id": api_data["animations_0_metaDataV2_animations_0_id"],
                    "width": api_data["animations_0_metaDataV2_animations_0_width"],
                    "height": api_data["animations_0_metaDataV2_animations_0_height"],
                    "frames": api_data["animations_0_metaDataV2_animations_0_frames"],
                    "frameRate": api_data["animations_0_metaDataV2_animations_0_frameRate"],
                    "layers": api_data["animations_0_metaDataV2_animations_0_layers"],
                    "colors": [
                        [
                            api_data["animations_0_metaDataV2_animations_0_colors_0_0"],
                            api_data["animations_0_metaDataV2_animations_0_colors_0_1"],
                            api_data["animations_0_metaDataV2_animations_0_colors_0_2"],
                            api_data["animations_0_metaDataV2_animations_0_colors_0_3"]
                        ]
                    ],
                    "fileSize": api_data["animations_0_metaDataV2_animations_0_fileSize"],
                    "generator": api_data["animations_0_metaDataV2_animations_0_generator"],
                    "version": api_data["animations_0_metaDataV2_animations_0_version"],
                    "inPoint": api_data["animations_0_metaDataV2_animations_0_inPoint"],
                    "outPoint": api_data["animations_0_metaDataV2_animations_0_outPoint"]
                }
            ]
        },
        "user": {
            "id": api_data["animations_0_user_id"],
            "name": api_data["animations_0_user_name"],
            "username": api_data["animations_0_user_username"],
            "avatarUrl": api_data["animations_0_user_avatarUrl"],
            "isHireable": api_data["animations_0_user_isHireable"],
            "legacyWebUserId": api_data["animations_0_user_legacyWebUserId"],
            "state": api_data["animations_0_user_state"],
            "preference": {
                "preferredLang": api_data["animations_0_user_preference_preferredLang"],
                "hasWorkspace": api_data["animations_0_user_preference_hasWorkspace"],
                "hasPaidWorkspace": api_data["animations_0_user_preference_hasPaidWorkspace"],
                "animationAutoplayProfile": api_data["animations_0_user_preference_animationAutoplayProfile"],
                "fileCount": api_data["animations_0_user_preference_fileCount"],
                "isLottieExpert": api_data["animations_0_user_preference_isLottieExpert"],
                "courses": [
                    {
                        "id": api_data["animations_0_user_preference_courses_0_id"],
                        "slug": api_data["animations_0_user_preference_courses_0_slug"],
                        "name": api_data["animations_0_user_preference_courses_0_name"],
                        "shortName": api_data["animations_0_user_preference_courses_0_shortName"],
                        "courseUrl": api_data["animations_0_user_preference_courses_0_courseUrl"],
                        "isActive": api_data["animations_0_user_preference_courses_0_isActive"],
                        "tool": {
                            "name": api_data["animations_0_user_preference_courses_0_tool_name"],
                            "slug": api_data["animations_0_user_preference_courses_0_tool_slug"]
                        }
                    }
                ]
            }
        },
        "fileVariations": [api_data["animations_0_fileVariations_0"]],
        "tools": [api_data["animations_0_tools_0"]]
    }

    # Construct final result
    result = {
        "count": api_data["count"],
        "animations": [animation]
    }

    return result