import geopandas as gpd
from src.analysis.tower_jump import find_stay_points

def detect_transit_periods(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Detects transit periods in a trajectory.

    Args:
        gdf: GeoDataFrame with trajectory data.

    Returns:
        GeoDataFrame with 'is_transit' column.
    """
    gdf['is_transit'] = False
    stay_points = find_stay_points(gdf)

    if not stay_points:
        # If there are no stay points, we assume the entire trajectory is transit.
        gdf['is_transit'] = True
        return gdf

    # Mark all points as transit initially
    gdf['is_transit'] = True

    # Mark points within stay points as not transit
    for start, end in stay_points:
        gdf.loc[start:end, 'is_transit'] = False

    return gdf
