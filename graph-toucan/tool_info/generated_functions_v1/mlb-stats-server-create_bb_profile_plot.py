from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime
import numpy as np

def mlb_stats_server_create_bb_profile_plot(data: pd.DataFrame, parameter: str = 'launch_angle') -> Dict[str, Any]:
    """
    Plots a given StatCast parameter split by bb_type (batted ball type).
    
    Args:
        data (pd.DataFrame): pandas.DataFrame of StatCast batter data (retrieved through statcast, statcast_batter, etc)
        parameter (str, optional): StatCast parameter to plot. Defaults to 'launch_angle'.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - plot_data (Dict): Values of the parameter grouped by bb_type
            - parameter (str): The parameter that was plotted
            - bb_types_present (List[str]): List of batted ball types present in the data
            - summary_statistics (Dict): Mean, median, and count for each bb_type
            - plot_metadata (Dict): Metadata including timestamp, data size, date range, and plate appearances
    """
    # Input validation
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input 'data' must be a pandas DataFrame.")
    if parameter not in data.columns:
        raise ValueError(f"Parameter '{parameter}' not found in DataFrame columns.")
    if 'bb_type' not in data.columns:
        raise ValueError("Column 'bb_type' not found in DataFrame.")
    
    # Drop rows where bb_type or parameter is missing
    df_clean = data[['bb_type', parameter]].dropna()
    
    # Group by bb_type and extract values
    grouped = df_clean.groupby('bb_type')[parameter].apply(list).to_dict()
    
    # Summary statistics
    summary_stats = {}
    for bb_type, values in grouped.items():
        summary_stats[bb_type] = {
            'mean': float(np.mean(values)),
            'median': float(np.median(values)),
            'count': int(len(values))
        }
    
    # Metadata
    plot_metadata = {
        'creation_timestamp': datetime.now().isoformat(),
        'data_size': len(data),
        'date_range': None,
        'plate_appearances': len(data),
    }
    
    # Extract date range if 'game_date' column exists
    if 'game_date' in data.columns:
        try:
            game_dates = pd.to_datetime(data['game_date'], errors='coerce').dropna()
            if not game_dates.empty:
                plot_metadata['date_range'] = {
                    'start': game_dates.min().strftime('%Y-%m-%d'),
                    'end': game_dates.max().strftime('%Y-%m-%d')
                }
        except Exception:
            pass  # fallback: leave as None
    
    result = {
        'plot_data': grouped,
        'parameter': parameter,
        'bb_types_present': list(grouped.keys()),
        'summary_statistics': summary_stats,
        'plot_metadata': plot_metadata
    }
    
    return result