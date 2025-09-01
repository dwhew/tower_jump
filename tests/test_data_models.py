import os
import pandas as pd
from ptrail.core.TrajectoryDF import PTRAILDataFrame
from src.data_models import load_and_standardize_data

def test_load_and_standardize_data():
    # Create a dummy CSV file for testing
    data = {
        'user_id': ['2', '2', '2', '2'],
        'latitude': [34.0522, 34.0522, 34.0532, 50],
        'longitude': [-118.2437, -118.2437, -118.2447, 50],
        'timestamp_utc': [
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
    ptrail_df = load_and_standardize_data(test_csv_path)

    # Assert that the returned object is a PTRAILDataFrame
    assert isinstance(ptrail_df, PTRAILDataFrame)

    # Assert that the columns are standardized
    assert 'lat' in ptrail_df.columns
    assert 'lon' in ptrail_df.columns
    assert 'traj_id' in ptrail_df.index.names
    assert 'DateTime' in ptrail_df.index.names

    # Assert that the data is loaded correctly
    assert len(ptrail_df.loc['2']) == 4

    # Clean up the dummy CSV file
    os.remove(test_csv_path)
