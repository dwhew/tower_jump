import geopandas as gpd
import pandas as pd
from ptrail.core.TrajectoryDF import PTRAILDataFrame
import pandas as pd

def load_and_standardize_data(file_path: str) -> PTRAILDataFrame:
    """Loads raw data and standardizes it into a PTRAILDataFrame.

    Args:
        file_path: The path to the raw data file.

    Returns:
        A PTRAILDataFrame with standardized data.
    """
    # Read the raw CSV data.
    df = pd.read_csv(file_path)

    # Create a PTRAILDataFrame.
    pdf = PTRAILDataFrame(df,
                            latitude='latitude',
                            longitude='longitude',
                            datetime='timestamp_utc',
                            traj_id='user_id')

    return pdf
