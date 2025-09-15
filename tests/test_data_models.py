import os
import pandas as pd
import geopandas as gpd
from src.data_models import load_and_standardize_data

def test_load_and_standardize_data():
    # Create a dummy CSV file for testing
    data = {
        'user_id': ['2', '2', '2', '2'],
        'Latitude': [34.0522, 34.0522, 34.0532, 50],
        'Longitude': [-118.2437, -118.2437, -118.2447, 50],
        'UTCDateTime': [
            '2025-07-09 11:59:00',
            '2025-07-09 12:00:00',
            '2025-07-09 12:01:00',
            '2025-07-09 12:02:00' # This point will be filtered out
        ]
    }
    df = pd.DataFrame(data)
    test_csv_path = 'tests/sample_data.csv'
    df.to_csv(test_csv_path, index=False)

    # Call the function with the dummy CSV
    gdf = load_and_standardize_data(test_csv_path)

    # Assert that the returned object is a GeoDataFrame
    assert isinstance(gdf, gpd.GeoDataFrame)

    # Assert that the columns are standardized
    assert 'latitude' in gdf.columns
    assert 'longitude' in gdf.columns
    assert 'timestamp_utc' in gdf.columns

    # Assert that the data is loaded correctly
    assert len(gdf) == 4

    # Clean up the dummy CSV file
    os.remove(test_csv_path)