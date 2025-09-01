import folium
import pandas as pd

def create_tower_jump_map(df: pd.DataFrame, output_path: str):
    """Creates an interactive map to visualize tower jumps.

    Args:
        df: A DataFrame with trajectory data, including a 'is_tower_jump' column.
        output_path: The path to save the HTML map file.
    """
    # Create a map centered on the average location.
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # Add the trajectory as a line.
    points = df[['latitude', 'longitude']].values.tolist()
    folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(m)

    # Add markers for tower jumps.
    tower_jumps = df[df['is_tower_jump']]
    for _, row in tower_jumps.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            popup=f"Tower Jump\nTimestamp: {row['timestamp_utc']}"
        ).add_to(m)

    # Save the map to an HTML file.
    m.save(output_path)
    print(f"Map saved to {output_path}")


