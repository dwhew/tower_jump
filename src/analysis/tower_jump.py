from ptrail.ptrail.trajectory import PTRAILDataFrame
from ptrail.features.kinematic_features import KinematicFeatures

def detect_tower_jumps(pdf: PTRAILDataFrame, speed_threshold: float = 45.0) -> PTRAILDataFrame:
    """Detects tower jumps in a trajectory based on a speed threshold.

    Args:
        pdf: A PTRAILDataFrame containing the trajectory data.
        speed_threshold: The speed threshold in m/s.

    Returns:
        A new PTRAILDataFrame with a new 'is_tower_jump' column.
    """
    # Calculate kinematic features, including speed.
    kinematic_features_df = KinematicFeatures.generate_kinematic_features(pdf)

    # Identify tower jumps based on the speed threshold.
    kinematic_features_df['is_tower_jump'] = kinematic_features_df['Speed'] > speed_threshold

    return kinematic_features_df
