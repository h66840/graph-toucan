from typing import Dict, List, Any, Optional
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime

def mlb_stats_server_create_teams_plot(
    data: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a scatter plot for MLB teams based on Fangraphs team data.
    
    Args:
        data (pd.DataFrame): DataFrame containing Fangraphs team data with team names and stats.
        x_axis (str): Column name to use for x-axis values.
        y_axis (str): Column name to use for y-axis values.
        title (Optional[str]): Optional title for the plot.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - plot_data (Dict): Structured data for the plot including teams, x/y values, and labels.
            - plot_config (Dict): Configuration metadata including axis labels, title, and timestamp.
            - image_url (str): Base64-encoded PNG image of the scatter plot.
            - success (bool): Whether the plot was generated successfully.
            - error_message (str, optional): Error description if success is False.
    """
    try:
        # Validate inputs
        if not isinstance(data, pd.DataFrame):
            return {
                "success": False,
                "error_message": "Input 'data' must be a pandas DataFrame."
            }
        
        if x_axis not in data.columns:
            return {
                "success": False,
                "error_message": f"Column '{x_axis}' not found in data."
            }
        
        if y_axis not in data.columns:
            return {
                "success": False,
                "error_message": f"Column '{y_axis}' not found in data."
            }
        
        if 'Team' not in data.columns:
            return {
                "success": False,
                "error_message": "Column 'Team' not found in data. Required for team labeling."
            }
        
        # Extract relevant data
        teams = data['Team'].tolist()
        x_values = data[x_axis].astype(float).tolist()
        y_values = data[y_axis].astype(float).tolist()
        
        # Create labels for each point
        labels = [f"{team}: {x:.2f}, {y:.2f}" for team, x, y in zip(teams, x_values, y_values)]
        
        # Generate plot
        plt.figure(figsize=(10, 8))
        plt.scatter(x_values, y_values, alpha=0.7)
        
        # Annotate each point with team name
        for i, team in enumerate(teams):
            plt.annotate(team, (x_values[i], y_values[i]), fontsize=9, alpha=0.8, ha='right')
        
        # Set labels and title
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plot_title = title if title else f"{y_axis} vs {x_axis}"
        plt.title(plot_title)
        plt.grid(True, alpha=0.3)
        
        # Save plot to bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        # Create image URL (data URI)
        image_url = f"data:image/png;base64,{image_base64}"
        
        # Prepare output
        plot_data = {
            "teams": teams,
            "x_values": x_values,
            "y_values": y_values,
            "labels": labels
        }
        
        plot_config = {
            "x_axis_label": x_axis,
            "y_axis_label": y_axis,
            "title": plot_title,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
        
        return {
            "plot_data": plot_data,
            "plot_config": plot_config,
            "image_url": image_url,
            "success": True
        }
    
    except Exception as e:
        return {
            "success": False,
            "error_message": str(e)
        }