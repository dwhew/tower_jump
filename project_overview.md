# Project: Location Trajectory Analysis

## 1. Project Goal

The objective of this project is to develop two Python algorithms that run on AWS infrastructure to analyze user location data. The algorithms will:
1.  **Detect "Tower Jumps"**: Identify and flag noisy, inaccurate location points caused by cell tower triangulation errors.
2.  **Detect "Transit"**: Identify periods when a user is traveling between significant locations (stay-points).

## 2. Data Sources

We process location data from two sources, which are combined into a single, standardized format for analysis:

-   **Carrier Data**: Cell tower location data (less precise).
-   **App Data**: Mobile application location data (potentially more precise, from GPS).

### Standardized Data Record Fields:
-   `user_id`: Unique identifier for the user.
-   `timestamp_utc`: The UTC timestamp of the location ping.
-   `latitude`: The latitude coordinate.
-   `longitude`: The longitude coordinate.
-   `horizontal_accuracy_m`: The radius of uncertainty in meters.

## 3. Core Problems to Solve

### Tower Jump Detection
-   **Problem**: A user's phone may connect to a distant cell tower, creating an impossibly fast "jump" in their location history.
-   **Example**: A user in downtown Manhattan, NY, shows a brief ping in New Jersey, NJ, and then immediately back in Manhattan. The NJ ping is a tower jump.
-   **Success Criterion**: Correctly identify these jumps with >99% accuracy and assign a confidence score.

### Transit Detection
-   **Problem**: We need to distinguish between periods when a user is stationary at a location (e.g., home, work, a restaurant) and when they are traveling between these locations.
-   **Example**: A user drives from their home in CT to JFK airport in NY. The entire drive through NY to the airport should be marked as "transit."
-   **Success Criterion**: Correctly label segments of the user's trajectory as "transit" and assign a confidence score.

## 4. Expected Output

For each user, the final output will be a labeled set of trajectory points and aggregated time segments, indicating whether each point/segment is a "Tower Jump" or "Transit."
