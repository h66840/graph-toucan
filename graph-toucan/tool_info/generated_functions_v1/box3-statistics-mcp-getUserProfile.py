from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for user profile.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - profileId (str): User profile unique identifier
        - userId (str): User ID
        - username (str): User's nickname or login name
        - displayName (str): User display name
        - avatarUrl (str): URL of user's avatar image
        - bio (str): User's biography or self-description
        - level (int): User's platform level
        - experience (int): User's current experience points
        - registrationDate (str): User registration date in ISO 8601 format
        - lastLoginTime (str): Last login time in ISO 8601 format
        - status (str): User status (e.g., active, inactive, banned)
        - verified (bool): Whether the user is verified
        - statistics_postsCount (int): Number of posts made by user
        - statistics_likesReceived (int): Number of likes received
        - statistics_followersCount (int): Number of followers
        - statistics_followingCount (int): Number of users followed
        - customFields_memberType (str): Member type (e.g., premium, basic)
        - customFields_specialTag (str): Special tag assigned to user
        - success (bool): Whether the request was successful
        - errorMessage (str): Error message if request failed, else null
    """
    return {
        "profileId": "prof_12345",
        "userId": "user_67890",
        "username": "neko_sakura",
        "displayName": "Sakura",
        "avatarUrl": "https://example.com/avatar/sakura.jpg",
        "bio": "Hello, I'm Sakura! Love cats and coding.",
        "level": 15,
        "experience": 23400,
        "registrationDate": "2022-01-15T08:30:00Z",
        "lastLoginTime": "2023-10-05T14:22:10Z",
        "status": "active",
        "verified": True,
        "statistics_postsCount": 124,
        "statistics_likesReceived": 890,
        "statistics_followersCount": 345,
        "statistics_followingCount": 210,
        "customFields_memberType": "premium",
        "customFields_specialTag": "top_contributor",
        "success": True,
        "errorMessage": None
    }

def box3_statistics_mcp_getUserProfile(userId: str) -> Dict[str, Any]:
    """
    获取神岛平台用户的个人资料数据。

    参数:
        userId (str): 用户ID

    返回:
        Dict[str, Any]: 包含用户个人资料信息的字典，结构如下：
        - profileId (str): 用户资料的唯一标识符
        - userId (str): 用户ID，与输入一致
        - username (str): 用户的昵称或登录名
        - displayName (str): 用户显示名称
        - avatarUrl (str): 用户头像图片的URL地址
        - bio (str): 用户的个人简介
        - level (int): 用户在平台中的等级
        - experience (int): 用户当前的经验值
        - registrationDate (str): 用户注册时间，ISO 8601格式
        - lastLoginTime (str): 用户最后一次登录时间，ISO 8601格式
        - status (str): 用户当前状态（如：active, inactive, banned）
        - verified (bool): 是否为认证用户
        - statistics (Dict): 用户的行为统计数据，包含：
            - postsCount (int)
            - likesReceived (int)
            - followersCount (int)
            - followingCount (int)
        - customFields (Dict): 平台自定义扩展字段，包含：
            - memberType (str)
            - specialTag (str)
        - success (bool): 请求是否成功
        - errorMessage (str): 错误信息，成功时为 None
    """
    if not userId or not isinstance(userId, str):
        return {
            "profileId": None,
            "userId": userId,
            "username": None,
            "displayName": None,
            "avatarUrl": None,
            "bio": None,
            "level": None,
            "experience": None,
            "registrationDate": None,
            "lastLoginTime": None,
            "status": None,
            "verified": False,
            "statistics": {
                "postsCount": 0,
                "likesReceived": 0,
                "followersCount": 0,
                "followingCount": 0
            },
            "customFields": {
                "memberType": None,
                "specialTag": None
            },
            "success": False,
            "errorMessage": "Invalid userId provided. Must be a non-empty string."
        }

    api_data = call_external_api("box3-statistics-mcp-getUserProfile")

    # 构造 statistics 字典
    statistics = {
        "postsCount": api_data.get("statistics_postsCount"),
        "likesReceived": api_data.get("statistics_likesReceived"),
        "followersCount": api_data.get("statistics_followersCount"),
        "followingCount": api_data.get("statistics_followingCount")
    }

    # 构造 customFields 字典
    customFields = {
        "memberType": api_data.get("customFields_memberType"),
        "specialTag": api_data.get("customFields_specialTag")
    }

    # 构造最终结果
    result = {
        "profileId": api_data.get("profileId"),
        "userId": userId,  # 使用输入的 userId 保持一致
        "username": api_data.get("username"),
        "displayName": api_data.get("displayName"),
        "avatarUrl": api_data.get("avatarUrl"),
        "bio": api_data.get("bio"),
        "level": api_data.get("level"),
        "experience": api_data.get("experience"),
        "registrationDate": api_data.get("registrationDate"),
        "lastLoginTime": api_data.get("lastLoginTime"),
        "status": api_data.get("status"),
        "verified": api_data.get("verified"),
        "statistics": statistics,
        "customFields": customFields,
        "success": api_data.get("success"),
        "errorMessage": api_data.get("errorMessage")
    }

    return result