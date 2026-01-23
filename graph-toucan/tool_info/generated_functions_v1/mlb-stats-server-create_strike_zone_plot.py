from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime
import seaborn as sns

def mlb_stats_server_create_strike_zone_plot(
    data: pd.DataFrame,
    title: Optional[str] = '',
    colorby: Optional[str] = 'pitch_type',
    legend_title: Optional[str] = None,
    annotation: Optional[str] = 'pitch_type'
) -> Dict[str, Any]:
    """
    Produces a pitches overlaid on a strike zone using StatCast data.

    Args:
        data (pd.DataFrame): StatCast pandas.DataFrame of StatCast pitcher data
        title (str, optional): Title of plot. Defaults to ''.
        colorby (str, optional): Which category to color the mark with.
            Options: 'pitch_type', 'pitcher', 'description', or a column within data. Defaults to 'pitch_type'.
        legend_title (str, optional): Title for the legend. Defaults to based on colorby.
        annotation (str, optional): What to annotate in the marker.
            Options: 'pitch_type', 'release_speed', 'effective_speed', 'launch_speed', or something else in the data.
            Defaults to 'pitch_type'.

    Returns:
        Dict containing:
            - plot_data: structured pitch data for visualization
            - plot_config: configuration metadata for the plot
            - generated_plot: base64-encoded image string
            - metadata: additional context about the output
            - success: whether the plot was successfully created
            - error: error message if failed
    """
    try:
        # Input validation
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input 'data' must be a pandas DataFrame")
        if data.empty:
            raise ValueError("Input 'data' is empty")
        if 'plate_x' not in data.columns or 'plate_z' not in data.columns:
            raise ValueError("Data must contain 'plate_x' and 'plate_z' columns")

        # Validate colorby column
        if colorby not in data.columns and colorby not in ['pitch_type', 'pitcher', 'description']:
            raise ValueError(f"colorby='{colorby}' not found in data columns and is not a valid default option")

        # Validate annotation column
        if annotation not in data.columns and annotation not in ['pitch_type', 'release_speed', 'effective_speed', 'launch_speed']:
            raise ValueError(f"annotation='{annotation}' not found in data columns and is not a valid default option")

        # Set default legend title
        if legend_title is None:
            legend_title = colorby.replace('_', ' ').title()

        # Extract required coordinates
        x = data['plate_x'].values
        y = data['plate_z'].values

        # Get color category values
        color_category = data[colorby].values if colorby in data.columns else data['pitch_type'].values

        # Get annotation labels
        annotation_label = data[annotation].values if annotation in data.columns else data['pitch_type'].values

        # Define strike zone bounds (standard MLB strike zone)
        sz_left = -0.83  # -0.83 ft (approx -10 inches)
        sz_right = 0.83   # 0.83 ft (approx +10 inches)
        sz_bottom = 1.5   # 1.5 ft from ground
        sz_top = 3.5      # 3.5 ft from ground

        # Create the plot
        plt.figure(figsize=(8, 10))
        ax = plt.gca()

        # Plot strike zone
        strike_zone = plt.Rectangle((sz_left, sz_bottom), sz_right-sz_left, sz_top-sz_bottom,
                                    linewidth=2, edgecolor='black', facecolor='none', linestyle='--')
        ax.add_patch(strike_zone)

        # Create color mapping
        unique_colors = np.unique(color_category)
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_colors)))
        color_map = {cat: colors[i] for i, cat in enumerate(unique_colors)}

        # Plot pitches
        for i in range(len(x)):
            ax.plot(x[i], y[i], 'o', color=color_map[color_category[i]], markersize=8, alpha=0.7)
            # Add annotation
            if pd.notna(annotation_label[i]):
                ax.annotate(str(annotation_label[i]), (x[i], y[i]), xytext=(5, 5), textcoords='offset points',
                            fontsize=8, alpha=0.7)

        # Customize plot
        plt.xlim(-3, 3)
        plt.ylim(0, 5)
        plt.xlabel('Horizontal Location (ft)')
        plt.ylabel('Vertical Location (ft)')
        plt.title(title if title else 'Pitch Location in Strike Zone')
        plt.grid(True, alpha=0.3)

        # Add legend
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[cat], markersize=8) 
                  for cat in unique_colors]
        plt.legend(handles, unique_colors, title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')

        # Adjust layout to prevent legend cutoff
        plt.tight_layout()

        # Save plot to base64 string
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plot_image = base64.b64encode(buffer.read()).decode()
        plt.close()

        # Prepare output
        plot_data = {
            'x': x.tolist(),
            'y': y.tolist(),
            'color_category': color_category.tolist(),
            'annotation_label': [str(label) if pd.notna(label) else None for label in annotation_label],
            'pitch_metadata': data.to_dict('records')
        }

        plot_config = {
            'title': title if title else 'Pitch Location in Strike Zone',
            'legend_title': legend_title,
            'strike_zone_bounds': {
                'left': sz_left,
                'right': sz_right,
                'bottom': sz_bottom,
                'top': sz_top
            },
            'color_mapping': {str(k): f"rgb({int(v[0]*255)},{int(v[1]*255)},{int(v[2]*255)})" for k, v in color_map.items()}
        }

        metadata = {
            'total_pitches': len(data),
            'pitch_types_present': data['pitch_type'].unique().tolist() if 'pitch_type' in data.columns else [],
            'date_generated': datetime.now().isoformat(),
            'source_data_shape': {
                'rows': data.shape[0],
                'columns': data.shape[1]
            }
        }

        return {
            'plot_data': plot_data,
            'plot_config': plot_config,
            'generated_plot': f"data:image/png;base64,{plot_image}",
            'metadata': metadata,
            'success': True,
            'error': ''
        }

    except Exception as e:
        return {
            'plot_data': {},
            'plot_config': {},
            'generated_plot': '',
            'metadata': {},
            'success': False,
            'error': str(e)
        }