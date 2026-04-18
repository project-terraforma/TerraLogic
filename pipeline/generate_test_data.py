import os
import json
from mock_agent import mock_validate_place

os.environ["PYTHONUTF8"] = "1"

with open("data/places.geojson", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"][:100]  # take first 100
results = []

for i, place in enumerate(features):
    props = place.get("properties") or {}
    name = (props.get("names") or {}).get("primary", "Unknown")
    addr = (props.get("addresses") or [{}])[0].get("freeform", "")
    result = mock_validate_place(place)

    results.append({
        "id": place.get("id", f"place_{i}"),
        "name": name,
        "address": addr,
        "coordinates": place.get("geometry", {}).get("coordinates", []),
        "validation": result.model_dump()
    })
    print(f"[{i+1}/100] {name} → {result.status} ({result.confidence})")

with open("data/validated_sample.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n✅ Saved 100 mock validated places to data/validated_sample.json")