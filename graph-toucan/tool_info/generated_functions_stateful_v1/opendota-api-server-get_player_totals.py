from typing import Dict, Any

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for player totals.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - kills_total (float): total number of kills across all games
        - kills_per_min (float): average kills per minute
        - deaths_total (float): total number of deaths across all games
        - deaths_per_min (float): average deaths per minute
        - assists_total (float): total number of assists across all games
        - assists_per_min (float): average assists per minute
        - kda (float): total or average KDA (Kills + Assists) / Deaths
        - gold_per_min (float): average gold earned per minute
        - xp_per_min (float): average experience gained per minute
        - last_hits (float): total last hits landed
        - last_hits_per_min (float): average last hits per minute
        - denies (float): total denies
        - denies_per_min (float): average denies per minute
        - lane_efficiency_pct (float): lane efficiency as a percentage
        - duration_total (float): total game duration in seconds
        - duration_per_min (float): average game duration in minutes
        - level_total (float): total hero level sum across games
        - level_per_min (float): average hero level per minute
        - hero_damage_total (float): total damage dealt to heroes
        - hero_damage_per_min (float): average hero damage per minute
        - tower_damage_total (float): total damage dealt to towers
        - tower_damage_per_min (float): average tower damage per minute
        - hero_healing_total (float): total health healed on allies
        - hero_healing_per_min (float): average hero healing per minute
        - stuns_total (float): total stun duration in seconds
        - stuns_per_min (float): average stun duration per minute
        - tower_kills (float): total number of towers killed
        - neutral_kills (float): total number of neutral creeps killed
        - courier_kills (float): total number of couriers killed
        - purchase_tpscroll (float): total number of Town Portal Scrolls purchased
        - purchase_ward_observer (float): total number of Observer Wards purchased
        - purchase_ward_sentry (float): total number of Sentry Wards purchased
        - purchase_gem (float): total number of Gem of True Sight purchases
        - purchase_rapier (float): total number of Divine Rapiers purchased
        - pings (float): total number of pings sent
        - throw (float): metric indicating games thrown (sum or count)
        - comeback (float): metric indicating successful comebacks (count or sum)
        - stomp (float): metric indicating dominant/stomp victories (count or sum)
        - loss (float): total number of losses recorded
        - actions_per_min (float): average actions (clicks/commands) per minute
    """
    return {
        "kills_total": 2450.0,
        "kills_per_min": 0.42,
        "deaths_total": 1830.0,
        "deaths_per_min": 0.31,
        "assists_total": 4120.0,
        "assists_per_min": 0.71,
        "kda": 3.56,
        "gold_per_min": 385.5,
        "xp_per_min": 520.3,
        "last_hits": 18700.0,
        "last_hits_per_min": 32.1,
        "denies": 1250.0,
        "denies_per_min": 2.15,
        "lane_efficiency_pct": 78.4,
        "duration_total": 86400.0,
        "duration_per_min": 38.5,
        "level_total": 1240.0,
        "level_per_min": 0.55,
        "hero_damage_total": 4850000.0,
        "hero_damage_per_min": 8320.0,
        "tower_damage_total": 1250000.0,
        "tower_damage_per_min": 2145.0,
        "hero_healing_total": 320000.0,
        "hero_healing_per_min": 550.0,
        "stuns_total": 480.0,
        "stuns_per_min": 8.2,
        "tower_kills": 145.0,
        "neutral_kills": 3200.0,
        "courier_kills": 65.0,
        "purchase_tpscroll": 210.0,
        "purchase_ward_observer": 380.0,
        "purchase_ward_sentry": 190.0,
        "purchase_gem": 12.0,
        "purchase_rapier": 7.0,
        "pings": 2400.0,
        "throw": 3.0,
        "comeback": 15.0,
        "stomp": 22.0,
        "loss": 89.0,
        "actions_per_min": 125.7
    }

def opendota_api_server_get_player_totals(account_id: int) -> Dict[str, Any]:
    """
    Get player's overall stats totals from OpenDota API.
    
    Args:
        account_id (int): Steam32 account ID of the player
    
    Returns:
        Dict[str, Any]: Summary of player's total stats with the following fields:
        - kills_total (float): total number of kills across all games
        - kills_per_min (float): average kills per minute
        - deaths_total (float): total number of deaths across all games
        - deaths_per_min (float): average deaths per minute
        - assists_total (float): total number of assists across all games
        - assists_per_min (float): average assists per minute
        - kda (float): total or average KDA (Kills + Assists) / Deaths
        - gold_per_min (float): average gold earned per minute
        - xp_per_min (float): average experience gained per minute
        - last_hits (float): total last hits landed
        - last_hits_per_min (float): average last hits per minute
        - denies (float): total denies
        - denies_per_min (float): average denies per minute
        - lane_efficiency_pct (float): lane efficiency as a percentage
        - duration_total (float): total game duration in seconds
        - duration_per_min (float): average game duration in minutes
        - level_total (float): total hero level sum across games
        - level_per_min (float): average hero level per minute
        - hero_damage_total (float): total damage dealt to heroes
        - hero_damage_per_min (float): average hero damage per minute
        - tower_damage_total (float): total damage dealt to towers
        - tower_damage_per_min (float): average tower damage per minute
        - hero_healing_total (float): total health healed on allies
        - hero_healing_per_min (float): average hero healing per minute
        - stuns_total (float): total stun duration in seconds
        - stuns_per_min (float): average stun duration per minute
        - tower_kills (float): total number of towers killed
        - neutral_kills (float): total number of neutral creeps killed
        - courier_kills (float): total number of couriers killed
        - purchase_tpscroll (float): total number of Town Portal Scrolls purchased
        - purchase_ward_observer (float): total number of Observer Wards purchased
        - purchase_ward_sentry (float): total number of Sentry Wards purchased
        - purchase_gem (float): total number of Gem of True Sight purchases
        - purchase_rapier (float): total number of Divine Rapiers purchased
        - pings (float): total number of pings sent
        - throw (float): metric indicating games thrown (sum or count)
        - comeback (float): metric indicating successful comebacks (count or sum)
        - stomp (float): metric indicating dominant/stomp victories (count or sum)
        - loss (float): total number of losses recorded
        - actions_per_min (float): average actions (clicks/commands) per minute
    """
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")
    
    api_data = call_external_api("opendota-api-server-get_player_totals", **locals())
    
    result = {
        "kills_total": api_data["kills_total"],
        "kills_per_min": api_data["kills_per_min"],
        "deaths_total": api_data["deaths_total"],
        "deaths_per_min": api_data["deaths_per_min"],
        "assists_total": api_data["assists_total"],
        "assists_per_min": api_data["assists_per_min"],
        "kda": api_data["kda"],
        "gold_per_min": api_data["gold_per_min"],
        "xp_per_min": api_data["xp_per_min"],
        "last_hits": api_data["last_hits"],
        "last_hits_per_min": api_data["last_hits_per_min"],
        "denies": api_data["denies"],
        "denies_per_min": api_data["denies_per_min"],
        "lane_efficiency_pct": api_data["lane_efficiency_pct"],
        "duration_total": api_data["duration_total"],
        "duration_per_min": api_data["duration_per_min"],
        "level_total": api_data["level_total"],
        "level_per_min": api_data["level_per_min"],
        "hero_damage_total": api_data["hero_damage_total"],
        "hero_damage_per_min": api_data["hero_damage_per_min"],
        "tower_damage_total": api_data["tower_damage_total"],
        "tower_damage_per_min": api_data["tower_damage_per_min"],
        "hero_healing_total": api_data["hero_healing_total"],
        "hero_healing_per_min": api_data["hero_healing_per_min"],
        "stuns_total": api_data["stuns_total"],
        "stuns_per_min": api_data["stuns_per_min"],
        "tower_kills": api_data["tower_kills"],
        "neutral_kills": api_data["neutral_kills"],
        "courier_kills": api_data["courier_kills"],
        "purchase_tpscroll": api_data["purchase_tpscroll"],
        "purchase_ward_observer": api_data["purchase_ward_observer"],
        "purchase_ward_sentry": api_data["purchase_ward_sentry"],
        "purchase_gem": api_data["purchase_gem"],
        "purchase_rapier": api_data["purchase_rapier"],
        "pings": api_data["pings"],
        "throw": api_data["throw"],
        "comeback": api_data["comeback"],
        "stomp": api_data["stomp"],
        "loss": api_data["loss"],
        "actions_per_min": api_data["actions_per_min"]
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
