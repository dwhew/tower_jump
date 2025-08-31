import geopandas as gpd
import pandas as pd
from ptrail.preprocessing.filters import Filters
from ptrail.ptrail.trajectory import PTRAILDataFrame

def load_and_standardize_data(file_path: str) -> gpd.GeoDataFrame:
    """Loads raw data, standardizes columns, filters noise, and returns a GeoDataFrame.

    Args:
        file_path: The path to the raw data file.

    Returns:
        A GeoDataFrame with standardized and filtered data.
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

    # Convert to a GeoDataFrame for compatibility.
    gdf = gpd.GeoDataFrame(filtered_pdf, geometry=gpd.points_from_xy(filtered_pdf.longitude, filtered_pdf.latitude))

    return gdf
