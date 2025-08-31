import geopandas as gpd
import pandas as pd
from ptrail.preprocessing.filters import Filters
from ptrail.core.TrajectoryDF import PTRAILDataFrame

def load_and_standardize_data(file_path: str) -> PTRAILDataFrame:
    """Loads raw data, standardizes columns, filters noise, and returns a PTRAILDataFrame.

    Args:
        file_path: The path to the raw data file.

    Returns:
        A PTRAILDataFrame with standardized and filtered data.
    """
    # Read the raw CSV data.
    df = pd.read_csv(file_path)

    # Create a PTRAILDataFrame.
    pdf = PTRAILDataFrame(df, 
                            latitude='latitude', 
                            longitude='longitude', 
                            datetime='timestamp_utc', 
                            traj_id='user_id')

    # Filter out noise based on a maximum speed threshold (1000 km/h).
    filtered_pdf = Filters.filter_by_max_speed(pdf, max_speed=278)

    return filtered_pdf
