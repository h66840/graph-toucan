from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for train ticket search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - train_0_车次 (str): Train number for the first train
        - train_0_出发站 (str): Departure station for the first train
        - train_0_到达站 (str): Arrival station for the first train
        - train_0_出发时间 (str): Departure time for the first train
        - train_0_到达时间 (str): Arrival time for the first train
        - train_0_历时 (str): Duration of the first train journey
        - train_0_备注 (str): Remarks for the first train
        - train_0_ticket_0_类型 (str): First ticket type for the first train
        - train_0_ticket_0_余票 (str): Remaining tickets for the first ticket type of the first train
        - train_0_ticket_0_价格 (str): Price for the first ticket type of the first train
        - train_0_ticket_1_类型 (str): Second ticket type for the first train
        - train_0_ticket_1_余票 (str): Remaining tickets for the second ticket type of the first train
        - train_0_ticket_1_价格 (str): Price for the second ticket type of the first train
        - train_1_车次 (str): Train number for the second train
        - train_1_出发站 (str): Departure station for the second train
        - train_1_到达站 (str): Arrival station for the second train
        - train_1_出发时间 (str): Departure time for the second train
        - train_1_到达时间 (str): Arrival time for the second train
        - train_1_历时 (str): Duration of the second train journey
        - train_1_备注 (str): Remarks for the second train
        - train_1_ticket_0_类型 (str): First ticket type for the second train
        - train_1_ticket_0_余票 (str): Remaining tickets for the first ticket type of the second train
        - train_1_ticket_0_价格 (str): Price for the first ticket type of the second train
        - train_1_ticket_1_类型 (str): Second ticket type for the second train
        - train_1_ticket_1_余票 (str): Remaining tickets for the second ticket type of the second train
        - train_1_ticket_1_价格 (str): Price for the second ticket type of the second train
        - error_message (str): Error message if query fails, otherwise empty string
    """
    return {
        "train_0_车次": "G1",
        "train_0_出发站": "北京南",
        "train_0_到达站": "上海虹桥",
        "train_0_出发时间": "09:00",
        "train_0_到达时间": "13:30",
        "train_0_历时": "4小时30分",
        "train_0_备注": "正点",
        "train_0_ticket_0_类型": "二等座",
        "train_0_ticket_0_余票": "有票",
        "train_0_ticket_0_价格": "¥553",
        "train_0_ticket_1_类型": "一等座",
        "train_0_ticket_1_余票": "有票",
        "train_0_ticket_1_价格": "¥933",
        "train_1_车次": "G2",
        "train_1_出发站": "北京南",
        "train_1_到达站": "上海虹桥",
        "train_1_出发时间": "10:00",
        "train_1_到达时间": "14:30",
        "train_1_历时": "4小时30分",
        "train_1_备注": "正点",
        "train_1_ticket_0_类型": "二等座",
        "train_1_ticket_0_余票": "候补",
        "train_1_ticket_0_价格": "¥553",
        "train_1_ticket_1_类型": "一等座",
        "train_1_ticket_1_余票": "有票",
        "train_1_ticket_1_价格": "¥933",
        "error_message": ""
    }


def chinarailway_mcp_服务端_search(date: str, fromCity: str, toCity: str) -> Dict[str, Any]:
    """
    查询12306火车票信息。

    Args:
        date (str): 出发日期，格式为 YYYY-MM-DD
        fromCity (str): 出发城市
        toCity (str): 到达城市

    Returns:
        Dict containing:
        - trains (List[Dict]): List of train services with details including '车次', '出发站', '到达站',
          '出发时间', '到达时间', '历时', '备注', and '票列表'
        - error_message (str): Error message if the query fails (e.g., invalid date), otherwise None

    Raises:
        ValueError: If the date format is invalid or date is outside valid range
    """
    # Validate date format and range
    try:
        departure_date = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.today()
        max_date = today.replace(year=today.year + 1)
        # Fix: Use timedelta for proper date arithmetic
        min_date = today.replace(hour=0, minute=0, second=0, microsecond=0) - (today - datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
        min_date = min_date - timedelta(days=2)  # Allow slight past dates

        if not (min_date <= departure_date <= max_date):
            return {
                "trains": [],
                "error_message": "查询日期超出有效范围，仅支持近2天至1年内车票查询"
            }
    except ValueError as e:
        return {
            "trains": [],
            "error_message": "日期格式错误，请使用 YYYY-MM-DD 格式"
        }
    
    # Import timedelta here to ensure it's available
    from datetime import timedelta

    # Validate date format and range
    try:
        departure_date = datetime.strptime(date, "%Y-%m-%d")
        today = datetime.today()
        max_date = today.replace(year=today.year + 1)
        # Use timedelta for proper date arithmetic
        min_date = today - timedelta(days=2)  # Allow slight past dates

        if not (min_date <= departure_date <= max_date):
            return {
                "trains": [],
                "error_message": "查询日期超出有效范围，仅支持近2天至1年内车票查询"
            }
    except ValueError:
        return {
            "trains": [],
            "error_message": "日期格式错误，请使用 YYYY-MM-DD 格式"
        }

    # Call external API to get flat data
    api_data = call_external_api("chinarailway-mcp-服务端-search")

    # Check for error from API
    if api_data.get("error_message"):
        return {
            "trains": [],
            "error_message": api_data["error_message"]
        }

    # Construct trains list from flat API data
    trains = []

    for i in range(2):  # Process two trains (0 and 1)
        train_key_prefix = f"train_{i}"
        if not api_data.get(f"{train_key_prefix}_车次"):
            continue

        # Extract ticket information
        tickets = []
        for j in range(2):  # Each train has two ticket types
            ticket_type_key = f"{train_key_prefix}_ticket_{j}_类型"
            ticket_stock_key = f"{train_key_prefix}_ticket_{j}_余票"
            ticket_price_key = f"{train_key_prefix}_ticket_{j}_价格"

            if api_data.get(ticket_type_key):
                tickets.append({
                    "类型": api_data[ticket_type_key],
                    "余票": api_data[ticket_stock_key],
                    "价格": api_data[ticket_price_key]
                })

        # Create train dictionary
        train = {
            "车次": api_data[f"{train_key_prefix}_车次"],
            "出发站": api_data[f"{train_key_prefix}_出发站"],
            "到达站": api_data[f"{train_key_prefix}_到达站"],
            "出发时间": api_data[f"{train_key_prefix}_出发时间"],
            "到达时间": api_data[f"{train_key_prefix}_到达时间"],
            "历时": api_data[f"{train_key_prefix}_历时"],
            "备注": api_data[f"{train_key_prefix}_备注"],
            "票列表": tickets
        }
        trains.append(train)

    return {
        "trains": trains,
        "error_message": None
    }