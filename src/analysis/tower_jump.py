import geopandas as gpd
from geopy.distance import geodesic
from datetime import timedelta


def detect_tower_jumps(gdf: gpd.GeoDataFrame, speed_threshold: float = 45.0) -> \
                       gpd.GeoDataFrame:
    """Detects tower jumps in a trajectory.

    Args:
        gdf: GeoDataFrame with trajectory data.
        speed_threshold: Speed threshold in m/s.

    Returns:
        GeoDataFrame with 'is_tower_jump' column.
    """
    gdf['is_tower_jump'] = False

    for i in range(1, len(gdf)):
        p1 = gdf.iloc[i-1]
        p2 = gdf.iloc[i]

        actual_dist_meters = geodesic((p1.geometry.y, p1.geometry.x),
                                      (p2.geometry.y, p2.geometry.x)).meters

        time_diff_seconds = (p2.timestamp_utc - p1.timestamp_utc).total_seconds()

        if time_diff_seconds > 0:
            actual_speed_mps = actual_dist_meters / time_diff_seconds

            # Flag if speed is high
            if actual_speed_mps > speed_threshold:
                gdf.iloc[i, gdf.columns.get_loc('is_tower_jump')] = True

    return gdf


def find_stay_points(
    gdf: gpd.GeoDataFrame,
    distance_threshold: float = 100.0,  # meters
    time_threshold: timedelta = timedelta(minutes=5),
) -> list[tuple[int, int]]:
    """Detects stay points in a trajectory.

    Args:
        gdf: GeoDataFrame with trajectory data.
        distance_threshold: Max distance (m) for same stay.
        time_threshold: Min time duration for a stay point.

    Returns:
        List of (start_index, end_index) for stay points.
    """
    stay_points = []
    i = 0
    while i < len(gdf):
        j = i + 1
        while j < len(gdf):
            coords_i = (gdf.iloc[i].geometry.y, gdf.iloc[i].geometry.x)
            coords_j = (gdf.iloc[j].geometry.y, gdf.iloc[j].geometry.x)
            distance = geodesic(coords_i, coords_j).meters

            if distance <= distance_threshold:
                j += 1
            else:
                break

        if j - i > 1 and \
                (gdf.iloc[j-1].timestamp_utc - gdf.iloc[i].timestamp_utc) >= time_threshold:
            stay_points.append((i, j - 1))
        i = j

    return stay_points
