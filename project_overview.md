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

## 5. Technical Approach

The project will be developed iteratively, starting with a minimal working example (MWE) to establish a baseline. The MWE will use simplified algorithms to provide an end-to-end working pipeline. Following the MWE, more advanced features and the full probabilistic methodology will be implemented in a separate `dev` branch.

The project will be implemented in Python, leveraging a probabilistic approach to handle the inherent uncertainty in location data. The core of the methodology is to model each location point not as a fixed coordinate, but as a 2D Gaussian probability distribution based on its `horizontal_accuracy`.

Key libraries and technologies include:
-   **Data Handling and Preprocessing**: `ptrail`, `pandas`, `geopandas`
-   **Geospatial Analysis**: `shapely`, `haversine`
-   **Machine Learning (for clustering/classification)**: `scikit-learn`

The analysis will be conducted in the following phases:
1.  **Preprocessing**: Raw data will be cleaned, structured, and enriched using the `ptrail` library. This includes noise filtering, trajectory segmentation, and feature engineering.
2.  **Probabilistic Modeling**: Each location point will be modeled as a 2D Gaussian distribution.
3.  **Tower Jump Detection**: Uses an "impossible travel" paradigm, calculating the probability that the velocity between two points exceeds a plausible maximum. A multi-factor confidence score will be generated.
4.  **Stay Point Detection**: A probabilistic version of the DBSCAN clustering algorithm will be used to identify significant locations (stay points).
5.  **Transit Detection**: Transit segments will be identified as the travel between stay points, with a confidence score based on the certainty of the origin and destination, as well as the coherence of the path.

## 6. Expected Output

The final output will consist of two main deliverables:

### 6.1. Point-Level Flagged Output

A detailed, point-level dataset with the following schema:

| Column Name                 | Data Type       | Description                                                                                                                                      |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | 
| `point_id`                  | `UUID`          | A unique identifier for each location record.                                                                                                    |
| `user_id`                   | `String`        | A unique identifier for the user or device.                                                                                                      |
| `timestamp_utc`             | `Timestamp (UTC)` | The timestamp of the location ping.                                                                                                              |
| `latitude`                  | `Float`         | The WGS84 latitude of the reported location.                                                                                                     |
| `longitude`                 | `Float`         | The WGS84 longitude of the reported location.                                                                                                    |
| `horizontal_accuracy_m`     | `Float`         | The horizontal accuracy radius in meters.                                                                                                        |
| `original_source`           | `Enum`          | The source of the data: 'carrier' or 'app'.                                                                                                      |
| `trajectory_id`             | `UUID`          | Identifier for the trajectory this point belongs to.                                                                                             |
| `point_type`                | `Enum`          | The classification of the point. Values: `stay_point`, `transit_point`, `tower_jump_origin`, `tower_jump_terminus`, `unobserved_transit_origin`, `unobserved_transit_terminus`, `gross_error` |
| `event_id`                  | `UUID`          | A unique ID linking all points in a single event (a specific stay, transit, or jump). Null if not part of an event.                                  |
| `confidence_score`          | `Float`         | The confidence score associated with the event this point belongs to.                                                                            |

### 6.2. Aggregated Location Report

A higher-level summary of mobility patterns, consisting of two tables:

**Stay Points Summary Table**

| Column Name                   | Data Type       | Description                                                                                             |
| ----------------------------- | --------------- | ------------------------------------------------------------------------------------------------------- |
| `user_id`                     | `String`        | The unique identifier for the user.                                                                     |
| `stay_point_id`               | `UUID`          | The unique identifier for this specific stay point (corresponds to `event_id`).                         |
| `centroid_latitude`           | `Float`         | The latitude of the calculated U-centroid for the stay point.                                           |
| `centroid_longitude`          | `Float`         | The longitude of the calculated U-centroid for the stay point.                                          |
| `centroid_uncertainty_radius` | `Float`         | The uncertainty radius (in meters) of the U-centroid, reflecting the aggregate uncertainty of the cluster. |
| `total_visits`                | `Integer`       | The total number of times this stay point was visited in the reporting period.                          |
| `avg_duration_seconds`        | `Float`         | The average duration of a visit to this stay point, in seconds.                                         |
| `median_duration_seconds`     | `Float`         | The median duration of a visit to this stay point, in seconds.                                          |
| `first_seen`                  | `Timestamp (UTC)` | The timestamp of the first recorded visit to this stay point.                                           |
| `last_seen`                   | `Timestamp (UTC)` | The timestamp of the most recent recorded visit to this stay point.                                     |

**Transit Summary Table**

| Column Name                 | Data Type       | Description                                                                                             |
| --------------------------- | --------------- | ------------------------------------------------------------------------------------------------------- |
| `user_id`                   | `String`        | The unique identifier for the user.                                                                     |
| `transit_corridor_id`       | `UUID`          | A unique identifier for the corridor, defined by the origin-destination pair.                           |
| `origin_stay_point_id`      | `UUID`          | The ID of the origin stay point (foreign key to Stay Points table).                                     |
| `destination_stay_point_id` | `UUID`          | The ID of the destination stay point (foreign key to Stay Points table).                                |
| `total_trips`               | `Integer`       | The total number of observed trips along this corridor in the reporting period.                         |
| `avg_transit_time_seconds`  | `Float`         | The average duration of a trip along this corridor, in seconds.                                         |
| `median_transit_time_seconds` | `Float`         | The median duration of a trip along this corridor, in seconds.                                          |
| `avg_directness_score`      | `Float`         | The average spatial cohesion score for trips along this corridor.                                       |
