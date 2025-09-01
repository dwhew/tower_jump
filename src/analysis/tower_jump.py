import pandas as pd
import geopandas as gpd
from geopy.distance import geodesic
from datetime import timedelta

# Removed ptrail imports due to compatibility issues
# from ptrail.core.TrajectoryDF import PTRAILDataFrame
# from ptrail.features.kinematic_features import KinematicFeatures

def detect_tower_jumps(gdf: gpd.GeoDataFrame, speed_threshold: float = 45.0) -> gpd.GeoDataFrame:
    """Detects tower jumps in a trajectory based on a speed threshold.

    Args:
        gdf: A GeoDataFrame containing the trajectory data.
        speed_threshold: The speed threshold in m/s.

    Returns:
        A new GeoDataFrame with a new 'is_tower_jump' column.
    """
    # This function currently relies on ptrail's KinematicFeatures, which is causing compatibility issues.
    # For now, it will return the input GeoDataFrame without modifications.
    # TODO: Re-implement tower jump detection without ptrail or resolve ptrail compatibility.
    print("Warning: Tower jump detection is currently disabled due to ptrail compatibility issues.")
    return gdf

def find_stay_points(
    gdf: gpd.GeoDataFrame,
    distance_threshold: float = 100.0,  # meters
    time_threshold: timedelta = timedelta(minutes=5),
) -> list[tuple[int, int]]:
    """Detects stay points in a trajectory based on distance and time thresholds.

    Args:
        gdf: A GeoDataFrame containing the trajectory data.
        distance_threshold: The maximum distance (in meters) between points to be considered part of the same stay.
        time_threshold: The minimum time duration for a cluster of points to be considered a stay point.

    Returns:
        A list of tuples, where each tuple (start_index, end_index) represents the start and end indices
        of a detected stay point in the input GeoDataFrame.
    """
    stay_points = []
    i = 0
    while i < len(gdf):
        j = i + 1
        while j < len(gdf):
            # Get coordinates and timestamps from GeoDataFrame
            coords_i = (gdf.iloc[i].geometry.y, gdf.iloc[i].geometry.x)
            coords_j = (gdf.iloc[j].geometry.y, gdf.iloc[j].geometry.x)
            distance = geodesic(coords_i, coords_j).meters

            time_diff = gdf.iloc[j].timestamp - gdf.iloc[i].timestamp

            if distance <= distance_threshold:
                j += 1
            else:
                break

        # Check if the cluster of points forms a valid stay point
        if j - i > 1 and (gdf.iloc[j-1].timestamp - gdf.iloc[i].timestamp) >= time_threshold:
            stay_points.append((i, j - 1))
        i = j

    return stay_points
