import os
import sys
import json
from datetime import datetime

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def export_corrections(input_path: str, output_path: str, min_confidence: float = 0.7):
    """
    Export high-confidence flagged places as an
    Overture-compatible GeoJSON correction file.

    Only exports places where:
    - action_needed is True
    - confidence >= min_confidence
    - status is not 'open' (nothing to correct)
    """

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    features = []
    skipped = 0
    exported = 0

    for item in data:
        scored = item["scored"]

        # ── Filter: only export actionable high-confidence corrections ──
        if not scored["action_needed"]:
            skipped += 1
            continue
        if scored["confidence"] < min_confidence:
            skipped += 1
            continue
        if scored["status"] == "open":
            skipped += 1
            continue

        # ── Build Overture-compatible GeoJSON feature ──
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": item["coordinates"]
            },
            "properties": {
                # Original place info
                "place_id":     item["id"],
                "name":         item["name"],
                "address":      item["address"],

                # Correction payload
                "correction": {
                    "status":       scored["status"],
                    "confidence":   scored["confidence"],
                    "priority":     scored["priority"],
                    "issues":       scored["issues"],
                    "citations":    scored["citations"],
                    "label":        scored["label"],
                },

                # Metadata
                "validated_by":   "TerraLogic — Agentic Places Validator",
                "validated_at":   datetime.utcnow().isoformat() + "Z",
                "source_dataset": "Overture Maps Places (GeoParquet)",
                "project":        "Project Terraforma — Spring 2026",
            }
        }

        features.append(feature)
        exported += 1

        print(
            f"[EXPORTED] {item['name'][:40]:<40} "
            f"→ {scored['status']:<10} "
            f"confidence: {scored['confidence']}"
        )

    # ── Build final GeoJSON FeatureCollection ──
    geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "title":           "TerraLogic Correction Export",
            "description":     "High-confidence stale place corrections for Overture Maps",
            "generated_at":    datetime.utcnow().isoformat() + "Z",
            "total_exported":  exported,
            "total_skipped":   skipped,
            "min_confidence":  min_confidence,
            "format":          "Overture-compatible GeoJSON",
        },
        "features": features
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    print(f"\n✅ Exported {exported} corrections → {output_path}")
    print(f"   ⏭  Skipped {skipped} places (open, low confidence, or no action needed)")
    print(f"\n--- Correction breakdown ---")

    # ── Summary breakdown ──
    statuses = {}
    for feature in features:
        s = feature["properties"]["correction"]["status"]
        statuses[s] = statuses.get(s, 0) + 1

    for status, count in statuses.items():
        print(f"   {status:<12}: {count}")


# ── CLI ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Export high-confidence corrections as Overture-compatible GeoJSON"
    )
    parser.add_argument(
        "--input",
        default="data/scored_results.json",
        help="Path to scored results JSON"
    )
    parser.add_argument(
        "--output",
        default="data/corrections.geojson",
        help="Output GeoJSON file path"
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.7,
        help="Minimum confidence threshold for export (default: 0.7)"
    )
    args = parser.parse_args()

    export_corrections(args.input, args.output, args.min_confidence)