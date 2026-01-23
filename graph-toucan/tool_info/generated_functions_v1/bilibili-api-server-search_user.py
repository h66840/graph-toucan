from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bilibili user search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - seid (str): unique session ID for the search request
        - page (int): current page number of the search results
        - pagesize (int): number of users displayed per page
        - numResults (int): total number of user results found for the query
        - numPages (int): total number of pages available for the search query
        - suggest_keyword (str): suggested keyword if there's a spelling correction or alternative
        - rqt_type (str): type of search request, e.g., "search"
        - exp_list_show_rename (bool): experimental feature flag for rename display
        - exp_list_show_aggregation (bool): experimental feature flag for aggregation
        - egg_hit (int): internal tracking value, likely for A/B testing or Easter eggs
        - show_column (int): UI display flag indicating which columns to show in frontend
        - in_black_key (int): internal filtering flag, possibly related to blacklisted content or users
        - in_white_key (int): internal filtering flag, possibly related to whitelisted content or users
        - result_0_type (str): result type identifier, always "bili_user"
        - result_0_mid (int): unique member ID of the Bilibili user
        - result_0_uname (str): username of the user
        - result_0_usign (str): user signature or bio text
        - result_0_fans (int): number of followers the user has
        - result_0_videos (int): number of videos uploaded by the user
        - result_0_upic (str): URL to the user's avatar image
        - result_0_face_nft (int): flag indicating if the avatar is an NFT
        - result_0_face_nft_type (int): type classification of NFT avatar if applicable
        - result_0_verify_info (str): verification details or reason for verification
        - result_0_level (int): user's current level on Bilibili
        - result_0_gender (int): gender code: 0=unknown, 1=male, 2=female, 3=not specified
        - result_0_is_upuser (int): flag indicating if the user is a content creator
        - result_0_is_live (int): flag indicating if the user is currently live streaming
        - result_0_room_id (int): live room ID if the user is streaming, 0 otherwise
        - result_0_is_senior_member (int): flag indicating if the user is a senior/veteran member
        - result_0_official_verify_type (int): official verification type (-1=unverified, 0=personal, 1=organization)
        - result_0_official_verify_desc (str): official verification description
        - result_0_res_0_aid (int): article ID of the recent video
        - result_0_res_0_bvid (str): Bilibili video ID string
        - result_0_res_0_title (str): title of the recent video
        - result_0_res_0_pubdate (int): publication timestamp in Unix seconds
        - result_0_res_0_arcurl (str): full URL to the video page
        - result_0_res_0_pic (str): thumbnail image URL
        - result_0_res_0_play (str): view count as string
        - result_0_res_0_dm (int): number of danmu/comments
        - result_0_res_0_coin (int): number of coins given to the video
        - result_0_res_0_fav (int): number of favorites/bookmarks
        - result_0_res_0_desc (str): brief description or source attribution
        - result_0_res_0_duration (str): video duration in MM:SS format
        - result_0_res_0_is_pay (int): whether the video is paid content
        - result_0_res_0_is_union_video (int): whether it's part of a union/ad program
        - result_0_res_0_is_charge_video (int): whether it's a charged/premium video
        - result_0_res_0_vt (int): virtual token value
        - result_0_res_0_enable_vt (int): whether virtual token system is enabled
        - result_0_res_0_vt_display (str): display text for virtual token feature
        - result_0_hit_columns_0 (str): field that matched the search query
    """
    return {
        "seid": "abcdef1234567890",
        "page": 1,
        "pagesize": 20,
        "numResults": 156,
        "numPages": 8,
        "suggest_keyword": "",
        "rqt_type": "search",
        "exp_list_show_rename": True,
        "exp_list_show_aggregation": False,
        "egg_hit": 0,
        "show_column": 3,
        "in_black_key": 0,
        "in_white_key": 1,
        "result_0_type": "bili_user",
        "result_0_mid": 12345678,
        "result_0_uname": "ExampleUser",
        "result_0_usign": "This is a sample bio for testing.",
        "result_0_fans": 1500,
        "result_0_videos": 45,
        "result_0_upic": "https://example.com/avatar.jpg",
        "result_0_face_nft": 0,
        "result_0_face_nft_type": 0,
        "result_0_verify_info": "Verified creator",
        "result_0_level": 6,
        "result_0_gender": 1,
        "result_0_is_upuser": 1,
        "result_0_is_live": 0,
        "result_0_room_id": 0,
        "result_0_is_senior_member": 1,
        "result_0_official_verify_type": 0,
        "result_0_official_verify_desc": "Personal Verified",
        "result_0_res_0_aid": 11111111,
        "result_0_res_0_bvid": "BV1xx411c7mD",
        "result_0_res_0_title": "Sample Video Title",
        "result_0_res_0_pubdate": 1672531200,
        "result_0_res_0_arcurl": "https://www.bilibili.com/video/BV1xx411c7mD",
        "result_0_res_0_pic": "https://example.com/thumbnail.jpg",
        "result_0_res_0_play": "123456",
        "result_0_res_0_dm": 890,
        "result_0_res_0_coin": 234,
        "result_0_res_0_fav": 567,
        "result_0_res_0_desc": "Source: Original",
        "result_0_res_0_duration": "10:30",
        "result_0_res_0_is_pay": 0,
        "result_0_res_0_is_union_video": 1,
        "result_0_res_0_is_charge_video": 0,
        "result_0_res_0_vt": 0,
        "result_0_res_0_enable_vt": 0,
        "result_0_res_0_vt_display": "",
        "result_0_hit_columns_0": "uname"
    }

def bilibili_api_server_search_user(keyword: str, page: Optional[int] = 1) -> Dict[str, Any]:
    """
    搜索哔哩哔哩用户信息。
    
    Args:
        keyword (str): 用户名关键词，用于匹配用户名或相关字段
        page (int, optional): 页码，指定返回第几页的搜索结果，默认为1
        
    Returns:
        Dict[str, Any]: 包含用户搜索结果的字典数据，结构如下：
        - seid (str): unique session ID for the search request
        - page (int): current page number of the search results
        - pagesize (int): number of users displayed per page
        - numResults (int): total number of user results found for the query
        - numPages (int): total number of pages available for the search query
        - suggest_keyword (str): suggested keyword if there's a spelling correction or alternative
        - rqt_type (str): type of search request, e.g., "search"
        - exp_list (Dict[str, bool]): experimental feature flags indicating enabled features for the response
        - egg_hit (int): internal tracking value, likely for A/B testing or Easter eggs
        - result (List[Dict]): list of user objects with detailed information including:
            - type (str): result type identifier
            - mid (int): unique member ID
            - uname (str): username
            - usign (str): user signature or bio
            - fans (int): number of followers
            - videos (int): number of uploaded videos
            - upic (str): avatar image URL
            - face_nft (int): NFT avatar flag
            - face_nft_type (int): NFT avatar type
            - verify_info (str): verification details
            - level (int): user level
            - gender (int): gender code
            - is_upuser (int): content creator flag
            - is_live (int): live streaming status
            - room_id (int): live room ID
            - is_senior_member (int): senior member flag
            - official_verify (Dict): official verification status with 'type' and 'desc'
            - hit_columns (List[str]): fields that matched the search query
            - res (List[Dict]): recent video uploads with aid, bvid, title, pubdate, arcurl, pic, play, dm, coin, fav, desc, duration, and payment flags
        - show_column (int): UI display flag
        - in_black_key (int): internal filtering flag
        - in_white_key (int): internal filtering flag
    
    Raises:
        ValueError: If keyword is empty or page is less than 1
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword is required and cannot be empty.")
    if page is not None and page < 1:
        raise ValueError("Page number must be at least 1.")
    
    # Call external API to get flattened data
    api_data = call_external_api("bilibili-api-server-search_user")
    
    # Construct nested result structure
    result_item = {
        "type": api_data["result_0_type"],
        "mid": api_data["result_0_mid"],
        "uname": api_data["result_0_uname"],
        "usign": api_data["result_0_usign"],
        "fans": api_data["result_0_fans"],
        "videos": api_data["result_0_videos"],
        "upic": api_data["result_0_upic"],
        "face_nft": api_data["result_0_face_nft"],
        "face_nft_type": api_data["result_0_face_nft_type"],
        "verify_info": api_data["result_0_verify_info"],
        "level": api_data["result_0_level"],
        "gender": api_data["result_0_gender"],
        "is_upuser": api_data["result_0_is_upuser"],
        "is_live": api_data["result_0_is_live"],
        "room_id": api_data["result_0_room_id"],
        "is_senior_member": api_data["result_0_is_senior_member"],
        "official_verify": {
            "type": api_data["result_0_official_verify_type"],
            "desc": api_data["result_0_official_verify_desc"]
        },
        "hit_columns": [api_data["result_0_hit_columns_0"]] if api_data.get("result_0_hit_columns_0") else [],
        "res": [
            {
                "aid": api_data["result_0_res_0_aid"],
                "bvid": api_data["result_0_res_0_bvid"],
                "title": api_data["result_0_res_0_title"],
                "pubdate": api_data["result_0_res_0_pubdate"],
                "arcurl": api_data["result_0_res_0_arcurl"],
                "pic": api_data["result_0_res_0_pic"],
                "play": api_data["result_0_res_0_play"],
                "dm": api_data["result_0_res_0_dm"],
                "coin": api_data["result_0_res_0_coin"],
                "fav": api_data["result_0_res_0_fav"],
                "desc": api_data["result_0_res_0_desc"],
                "duration": api_data["result_0_res_0_duration"],
                "is_pay": api_data["result_0_res_0_is_pay"],
                "is_union_video": api_data["result_0_res_0_is_union_video"],
                "is_charge_video": api_data["result_0_res_0_is_charge_video"],
                "vt": api_data["result_0_res_0_vt"],
                "enable_vt": api_data["result_0_res_0_enable_vt"],
                "vt_display": api_data["result_0_res_0_vt_display"]
            }
        ]
    }
    
    # Construct final response
    response = {
        "seid": api_data["seid"],
        "page": api_data["page"],
        "pagesize": api_data["pagesize"],
        "numResults": api_data["numResults"],
        "numPages": api_data["numPages"],
        "suggest_keyword": api_data["suggest_keyword"],
        "rqt_type": api_data["rqt_type"],
        "exp_list": {
            "show_rename": api_data["exp_list_show_rename"],
            "show_aggregation": api_data["exp_list_show_aggregation"]
        },
        "egg_hit": api_data["egg_hit"],
        "show_column": api_data["show_column"],
        "in_black_key": api_data["in_black_key"],
        "in_white_key": api_data["in_white_key"],
        "result": [result_item]
    }
    
    return response