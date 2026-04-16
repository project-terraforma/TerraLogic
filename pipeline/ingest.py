import subprocess
import json
import argparse
import os

os.environ["PYTHONUTF8"] = "1"

# Preset bounding boxes for easy city selection
CITIES = {
    "san_francisco": "-122.51,37.70,-122.36,37.81",
    "los_angeles":   "-118.67,33.70,-118.15,34.34",
    "new_york":      "-74.26,40.48,-73.70,40.92",
    "chicago":       "-87.94,41.64,-87.52,42.02",
    "salinas":       "-121.70,36.60,-121.56,36.72",
}

def download_places(city: str, output_path: str):
    bbox = CITIES.get(city)
    if not bbox:
        print(f"Unknown city: {city}")
        print(f"Available cities: {list(CITIES.keys())}")
        return

    print(f"Downloading Places data for {city}...")
    print(f"Bounding box: {bbox}")

    result = subprocess.run([
        "overturemaps", "download",
        f"--bbox={bbox}",
        "-f", "geojson",
        "--type=place",
        "-o", output_path
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return

    # Load and summarize
    with open(output_path, encoding="utf-8") as f:
        data = json.load(f)

    places = data.get("features", [])
    print(f"\n✅ Downloaded {len(places)} places → {output_path}")

    # Show a sample
    if places:
        sample = places[0]
        props = sample.get("properties", {})
        print("\n--- Sample place ---")
        print(f"  Name:     {props.get('names', {}).get('primary', 'N/A')}")
        print(f"  Category: {props.get('categories', {}).get('primary', 'N/A')}")
        print(f"  Address:  {props.get('addresses', [{}])[0].get('freeform', 'N/A')}")
        print(f"  Country:  {props.get('addresses', [{}])[0].get('country', 'N/A')}")

    return places

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Overture Maps Places data")
    parser.add_argument("--city", default="san_francisco", help="City to download")
    parser.add_argument("--output", default="data/places.geojson", help="Output file path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    download_places(args.city, args.output)