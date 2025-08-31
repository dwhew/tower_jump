import argparse
from src.data_models import load_and_standardize_data

def main():
    """Main function to run the location trajectory analysis."""
    parser = argparse.ArgumentParser(description="Analyze location data to detect tower jumps and transit periods.")
    parser.add_argument("--input", required=True, help="Path to the raw location data CSV file.")
    parser.add_argument("--output", required=True, help="Path where the processed CSV file will be saved.")
    args = parser.parse_args()

    print(f"Loading and standardizing data from {args.input}...")
    gdf = load_and_standardize_data(args.input)

    # Placeholder for analysis functions
    print("Analyzing data for tower jumps and transit periods...")

    # Placeholder for saving results
    print(f"Saving processed data to {args.output}...")

if __name__ == "__main__":
    main()
