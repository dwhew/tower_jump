import sys
import os

import pandas as pd
import numpy as np
import geopandas as gpd

from src.analysis.tower_jump import detect_tower_jumps


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_detect_tower_jumps_basic():
    # Create a sample GeoDataFrame with a tower jump.
    data = {
        'user_id': [1, 1, 1, 1],
        'timestamp': pd.to_datetime([
            '2022-01-01 00:00:00',
            '2022-01-01 00:00:01',
            '2022-01-01 00:00:02',
            '2022-01-01 00:00:03',
        ]),
        'latitude': [40.7128, 40.7129, 34.0522, 34.0523],
        'longitude': [-74.0060, -74.0061, -118.2437, -118.2438],
        'horizontal_accuracy_m': [10, 10, 10, 10]  # Low accuracy, so a
                                                 # jump should be detected
    }
    gdf = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(data['longitude'], data['latitude']),
        crs="EPSG:4326"
    )

    # Detect tower jumps.
    result_gdf = detect_tower_jumps(gdf, speed_threshold=45.0)

    # Check the results.
    # The tower jump is from point 1 to point 2 (index 1 to 2).
    # So, point at index 2 should be flagged as a tower jump.
    expected_jumps = np.array([False, False, True, False])
    assert 'is_tower_jump' in result_gdf.columns
    assert np.array_equal(result_gdf['is_tower_jump'].values, expected_jumps)


def test_detect_tower_jumps_probabilistic_high_accuracy():
    # Create a sample GeoDataFrame where a large distance might be plausible
    # due to high accuracy
    data = {
        'user_id': [1, 1, 1, 1],
        'timestamp': pd.to_datetime([
            '2022-01-01 00:00:00',
            '2022-01-01 00:00:01',
            '2022-01-01 00:00:02',
            '2022-01-01 00:00:03',
        ]),
        'latitude': [40.7128, 40.7129, 40.7130, 40.7131],
        'longitude': [-74.0060, -74.0061, -74.0062, -74.0063],
        'horizontal_accuracy_m': [1000, 1000, 1000, 1000]  # High accuracy,
                                                        # so even a large
                                                        # jump might not be
                                                        # flagged
    }
    gdf = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(data['longitude'], data['latitude']),
        crs="EPSG:4326"
    )

    # Detect tower jumps with a high speed threshold
    result_gdf = detect_tower_jumps(gdf, speed_threshold=10.0)  # A lower
                                                            # speed threshold
                                                            # to test the
                                                            # accuracy impact

    # With high accuracy, even a seemingly fast movement might be considered
    # plausible. In this simplified probabilistic model, if the actual
    # distance is not significantly larger than the sum of accuracies, it
    # might not be flagged as a jump. For this specific test case, with a
    # small movement and high accuracy, no jump should be detected.
    expected_jumps = np.array([False, False, False, False])
    assert 'is_tower_jump' in result_gdf.columns
    assert np.array_equal(result_gdf['is_tower_jump'].values, expected_jumps)
