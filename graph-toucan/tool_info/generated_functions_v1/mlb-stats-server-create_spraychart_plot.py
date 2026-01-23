from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, Circle

def mlb_stats_server_create_spraychart_plot(
    data: pd.DataFrame,
    team_stadium: Optional[str] = None,
    title: Optional[str] = '',
    size: Optional[int] = 100,
    colorby: Optional[str] = 'events',
    legend_title: Optional[str] = None,
    width: Optional[int] = 500,
    height: Optional[int] = 500
) -> Dict[str, Any]:
    """
    Produces a spraychart using statcast data overlayed on specified stadium.

    Args:
        data: Pandas DataFrame containing StatCast batter data with hit coordinates.
        team_stadium: Name of the team whose stadium layout to use.
        title: Optional title for the plot.
        size: Size of hit markers on the plot.
        colorby: Column name or category to color the hits by ('events', 'player', or a column in data).
        legend_title: Optional title for the legend.
        width: Width of the plot (excluding legend).
        height: Height of the plot.

    Returns:
        Dictionary containing:
        - plot_data: Structured data for the spraychart including hit positions and stadium layout.
        - plot_metadata: Configuration metadata used in rendering.
        - visualization_url: Base64-encoded PNG image of the plot.
        - success: Boolean indicating success.
        - error_message: Error details if success is False.
    """
    try:
        # Input validation
        if data is None or data.empty:
            return {
                "success": False,
                "error_message": "Input data is required and cannot be empty."
            }

        if 'hc_x' not in data.columns or 'hc_y' not in data.columns:
            return {
                "success": False,
                "error_message": "Data must contain 'hc_x' and 'hc_y' columns for hit coordinates."
            }

        # Default team stadium if not provided
        if not team_stadium:
            team_stadium = "Generic"

        # Determine color category
        if colorby == 'events':
            if 'events' not in data.columns:
                return {
                    "success": False,
                    "error_message": "Data must contain 'events' column when colorby='events'."
                }
            color_values = data['events'].fillna('Unknown')
        elif colorby == 'player':
            if 'player_name' not in data.columns:
                return {
                    "success": False,
                    "error_message": "Data must contain 'player_name' column when colorby='player'."
                }
            color_values = data['player_name'].fillna('Unknown')
        else:
            if colorby not in data.columns:
                return {
                    "success": False,
                    "error_message": f"Column '{colorby}' not found in data."
                }
            color_values = data[colorby].fillna('Unknown')

        unique_colors = color_values.unique()
        color_map = {val: plt.cm.tab10(i % 10) for i, val in enumerate(unique_colors)}
        colors = [color_map[val] for val in color_values]

        # Set legend title
        if legend_title is None:
            legend_title = colorby.capitalize()

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
        ax.set_xlim(0, 200)
        ax.set_ylim(0, 130)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title if title else f"Spray Chart - {team_stadium}")

        # Draw stadium layout (simplified baseball field)
        outfield_fence = Arc((100, 0), 200, 200, theta1=0, theta2=180, color="green", linewidth=2)
        first_base_line = Rectangle((100, 0), 90, 2, angle=45, color="brown")
        third_base_line = Rectangle((100, 0), 90, 2, angle=135, color="brown")
        pitcher_mound = Circle((100, 63.7), 9, color="brown", alpha=0.3)
        home_plate = Rectangle((100, 0), 1.5, 1.5, angle=45, color="black")

        ax.add_patch(outfield_fence)
        ax.add_patch(first_base_line)
        ax.add_patch(third_base_line)
        ax.add_patch(pitcher_mound)
        ax.add_patch(home_plate)

        # Plot hits
        ax.scatter(data['hc_x'], data['hc_y'], c=colors, s=size, alpha=0.7, edgecolors='black', linewidth=0.5)

        # Add legend
        if len(unique_colors) <= 10:  # Only show legend if not too many categories
            handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[val], markersize=8) for val in unique_colors]
            ax.legend(handles, unique_colors, title=legend_title, loc='upper right', bbox_to_anchor=(1.15, 1))

        # Save plot to bytes buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        # Construct stadium layout paths (simplified representation)
        stadium_layout = {
            "outfield_arc": {"center": [100, 0], "width": 200, "height": 200, "start_angle": 0, "end_angle": 180},
            "first_base_line": {"start": [100, 0], "length": 90, "angle": 45},
            "third_base_line": {"start": [100, 0], "length": 90, "angle": 135},
            "pitcher_mound": {"center": [100, 63.7], "radius": 9},
            "home_plate": {"center": [100, 0], "size": 1.5, "angle": 45}
        }

        # Prepare output
        plot_data = {
            "x": data['hc_x'].tolist(),
            "y": data['hc_y'].tolist(),
            "color_category": color_values.tolist(),
            "stadium_layout": stadium_layout
        }

        plot_metadata = {
            "title": title if title else "",
            "team_stadium": team_stadium,
            "width": width,
            "height": height,
            "size": size,
            "colorby": colorby,
            "legend_title": legend_title if legend_title else colorby.capitalize()
        }

        visualization_url = f"data:image/png;base64,{image_base64}"

        return {
            "plot_data": plot_data,
            "plot_metadata": plot_metadata,
            "visualization_url": visualization_url,
            "success": True
        }

    except Exception as e:
        return {
            "success": False,
            "error_message": f"Failed to generate spraychart: {str(e)}"
        }