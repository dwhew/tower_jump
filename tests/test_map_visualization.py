import os
import pandas as pd
from src.visualization.map_visualization import create_tower_jump_map

def test_create_tower_jump_map():
    # Create a dummy DataFrame for testing
    data = {
        'latitude': [34.0522, 34.0523, 34.0524, 34.0525],
        'longitude': [-118.2437, -118.2438, -118.2439, -118.2440],
        'timestamp_utc': [
            '2025-07-09 12:00:00',
            '2025-07-09 12:01:00',
            '2025-07-09 12:02:00',
            '2025-07-09 12:03:00'
        ],
        'is_tower_jump': [False, True, False, True]
    }
    df = pd.DataFrame(data)

    # Define a temporary output path
    output_path = 'tests/test_map.html'

    # Call the function
    create_tower_jump_map(df, output_path)

    # Assert that the HTML file was created
    assert os.path.exists(output_path)

    # Optional: Assert some content in the HTML file
    with open(output_path, 'r') as f:
        content = f.read()
        assert "folium" in content
        assert "Tower Jump" in content

    # Clean up the created HTML file
    os.remove(output_path)
