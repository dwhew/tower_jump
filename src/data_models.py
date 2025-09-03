import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

def load_and_standardize_data(file_path: str) -> gpd.GeoDataFrame:
    """Loads raw data and standardizes it into a GeoDataFrame.

    Args:
        file_path: The path to the raw data file.

    Returns:
        A GeoDataFrame with standardized data.
    """
    # Read the raw CSV data.
    df = pd.read_csv(file_path)

    # Drop rows with missing Latitude, Longitude, or UTCDateTime
    df.dropna(subset=['Latitude', 'Longitude', 'UTCDateTime'], inplace=True)

    # Create a GeoDataFrame.
    geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Rename columns to standardize
    gdf = gdf.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude', 'UTCDateTime': 'timestamp_utc'})

    # Ensure timestamp column is datetime objects
    gdf['timestamp_utc'] = pd.to_datetime(gdf['timestamp_utc'])

    return gdf
