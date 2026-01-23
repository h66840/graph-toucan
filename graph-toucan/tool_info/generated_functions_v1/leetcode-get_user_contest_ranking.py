def leetcode_get_user_contest_ranking(attended: bool = True, username: str = None) -> dict:
    """
    Retrieves a user's contest ranking information on LeetCode, including overall ranking, participation history, and performance metrics across contests.
    
    Args:
        attended (bool, optional): Whether to include only the contests the user has participated in. Defaults to True.
        username (str, required): LeetCode username to retrieve contest ranking information for.
    
    Returns:
        dict: A dictionary containing the user's contest ranking information with the following structure:
            - username (str): The username of the LeetCode user.
            - contestRanking (dict): Contains detailed contest ranking data including:
                - userContestRanking (dict or None): Current ranking details if available.
                - userContestRankingHistory (list of dict or None): List of past contest performances (at least 2 entries).
    """
    if not username:
        raise ValueError("Username is required.")

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API for LeetCode user contest ranking.

        Returns:
            Dict with simple scalar fields only (str, int, float, bool):
            - username (str): User's LeetCode username
            - userContestRanking_rating (float): Current rating of the user
            - userContestRanking_rank (int): Global rank of the user
            - userContestRanking_level (str): Rank level (e.g., "Knight")
            - userContestRanking_badge (bool): Whether user has a badge
            - userContestRanking_attended (int): Number of contests attended
            - userContestRanking_participated (int): Number of contests participated
            - userContestRanking_finishes (int): Number of finishes
            - userContestRanking_maxRating (float): Maximum rating achieved
            - userContestRanking_maxRank (int): Best global rank achieved
            - userContestRanking_maxRankDisplay (str): Display version of best rank
            - item_0_contestId (int): First contest ID
            - item_0_contestTitle (str): Title of first contest
            - item_0_rating (float): Rating change in first contest
            - item_0_rank (int): Rank in first contest
            - item_0_score (int): Score in first contest
            - item_0_finishTime (str): Finish time for first contest
            - item_0_attended (bool): Whether user attended first contest
            - item_1_contestId (int): Second contest ID
            - item_1_contestTitle (str): Title of second contest
            - item_1_rating (float): Rating change in second contest
            - item_1_rank (int): Rank in second contest
            - item_1_score (int): Score in second contest
            - item_1_finishTime (str): Finish time for second contest
            - item_1_attended (bool): Whether user attended second contest
        """
        return {
            "username": username,
            "userContestRanking_rating": 1850.0,
            "userContestRanking_rank": 4500,
            "userContestRanking_level": "Knight",
            "userContestRanking_badge": True,
            "userContestRanking_attended": 35,
            "userContestRanking_participated": 30,
            "userContestRanking_finishes": 30,
            "userContestRanking_maxRating": 1920.0,
            "userContestRanking_maxRank": 3200,
            "userContestRanking_maxRankDisplay": "Top 0.5%",
            "item_0_contestId": 101,
            "item_0_contestTitle": "Weekly Contest 300",
            "item_0_rating": 1870.5,
            "item_0_rank": 2800,
            "item_0_score": 16,
            "item_0_finishTime": "1:45:30",
            "item_0_attended": True,
            "item_1_contestId": 102,
            "item_1_contestTitle": "Biweekly Contest 88",
            "item_1_rating": 1840.0,
            "item_1_rank": 3500,
            "item_1_score": 12,
            "item_1_finishTime": "2:00:15",
            "item_1_attended": True,
        }

    # Fetch simulated external data
    api_data = call_external_api("leetcode-get_user_contest_ranking")

    # Construct userContestRanking object
    user_contest_ranking = {
        "rating": api_data["userContestRanking_rating"],
        "rank": api_data["userContestRanking_rank"],
        "level": api_data["userContestRanking_level"],
        "badge": api_data["userContestRanking_badge"],
        "attended": api_data["userContestRanking_attended"],
        "participated": api_data["userContestRanking_participated"],
        "finishes": api_data["userContestRanking_finishes"],
        "maxRating": api_data["userContestRanking_maxRating"],
        "maxRank": api_data["userContestRanking_maxRank"],
        "maxRankDisplay": api_data["userContestRanking_maxRankDisplay"]
    }

    # Construct userContestRankingHistory list
    user_contest_history = [
        {
            "contestId": api_data["item_0_contestId"],
            "contestTitle": api_data["item_0_contestTitle"],
            "rating": api_data["item_0_rating"],
            "rank": api_data["item_0_rank"],
            "score": api_data["item_0_score"],
            "finishTime": api_data["item_0_finishTime"],
            "attended": api_data["item_0_attended"]
        },
        {
            "contestId": api_data["item_1_contestId"],
            "contestTitle": api_data["item_1_contestTitle"],
            "rating": api_data["item_1_rating"],
            "rank": api_data["item_1_rank"],
            "score": api_data["item_1_score"],
            "finishTime": api_data["item_1_finishTime"],
            "attended": api_data["item_1_attended"]
        }
    ]

    # Apply filtering based on 'attended' parameter
    if attended:
        user_contest_history = [record for record in user_contest_history if record["attended"]]

    # Final result construction
    result = {
        "username": api_data["username"],
        "contestRanking": {
            "userContestRanking": user_contest_ranking,
            "userContestRankingHistory": user_contest_history if len(user_contest_history) > 0 else None
        }
    }

    return result