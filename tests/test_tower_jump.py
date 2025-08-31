import sys
import os
import pandas as pd
import numpy as np
from ptrail.core.TrajectoryDF import PTRAILDataFrame

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis.tower_jump import detect_tower_jumps

def test_detect_tower_jumps():
    # Create a sample dataframe with a tower jump.
    df = pd.DataFrame([
        {'user_id': 1, 'timestamp_utc': '2022-01-01 00:00:00', 'latitude': 40.7128, 'longitude': -74.0060, 'horizontal_accuracy_m': 10},
        {'user_id': 1, 'timestamp_utc': '2022-01-01 00:00:01', 'latitude': 40.7129, 'longitude': -74.0061, 'horizontal_accuracy_m': 10}, # Normal segment
        {'user_id': 1, 'timestamp_utc': '2022-01-01 00:00:02', 'latitude': 34.0522, 'longitude': -118.2437, 'horizontal_accuracy_m': 10}, # Tower jump
        {'user_id': 1, 'timestamp_utc': '2022-01-01 00:00:03', 'latitude': 34.0523, 'longitude': -118.2438, 'horizontal_accuracy_m': 10}, # Normal segment
    ])
    pdf = PTRAILDataFrame(df, 
                          latitude='latitude', 
                          longitude='longitude', 
                          datetime='timestamp_utc', 
                          traj_id='user_id')

    # Detect tower jumps.
    result_pdf = detect_tower_jumps(pdf)

    # Check the results.
    expected_jumps = np.array([False, True, False, False])
    assert 'is_tower_jump' in result_pdf.columns
    assert np.array_equal(result_pdf['is_tower_jump'].values, expected_jumps)