import argparse
from src.data_models import load_and_standardize_data
from src.analysis.tower_jump import detect_tower_jumps
from src.visualization.map_visualization import create_tower_jump_map

def main():
    """Main function to run the location trajectory analysis."""
    parser = argparse.ArgumentParser(description="Analyze location data to detect tower jumps and transit periods.")
    parser.add_argument("--input", required=True, help="Path to the raw location data CSV file.")
    parser.add_argument("--output", required=True, help="Path where the processed CSV file will be saved.")
    parser.add_argument("--map_output", help="Path where the HTML map will be saved.")
    args = parser.parse_args()

    print(f"Loading and standardizing data from {args.input}...")
    gdf = load_and_standardize_data(args.input)

    print("Detecting tower jumps...")
    gdf_with_jumps = detect_tower_jumps(gdf)

    # Placeholder for transit detection
    print("Analyzing data for transit periods...")

    if args.map_output:
        print(f"Creating and saving map to {args.map_output}...")
        create_tower_jump_map(gdf_with_jumps, args.map_output)

    print(f"Saving processed data to {args.output}...")
    gdf_with_jumps.to_csv(args.output, index=False)

    print("Processing complete.")

if __name__ == "__main__":
    main()
