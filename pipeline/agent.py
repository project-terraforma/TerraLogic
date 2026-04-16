import os
import json
import anthropic
from pydantic import BaseModel
from typing import Literal

os.environ["PYTHONUTF8"] = "1"


class ValidationResult(BaseModel):
    status: Literal["open", "closed", "moved", "uncertain"]
    confidence: float       # 0.0 – 1.0
    issues: list[str]       # problems found (empty if none)
    citations: list[str]    # source URLs used to verify


def validate_place(place: dict) -> ValidationResult:
    """
    Validate one Overture Maps GeoJSON feature against the real world.

    Steps:
      1. Use the web_search server-side tool so Claude can look up the place.
      2. Parse Claude's findings into a structured ValidationResult via Pydantic.
    """
    client = anthropic.Anthropic()

    # --- extract fields -------------------------------------------------------
    props = place.get("properties") or {}
    geometry = place.get("geometry") or {}

    name = (props.get("names") or {}).get("primary") or "Unknown"
    addresses = props.get("addresses") or [{}]
    addr = addresses[0] if addresses else {}
    address  = addr.get("freeform", "")
    city     = addr.get("locality", "")
    region   = addr.get("region", "")
    country  = addr.get("country", "")
    category = (props.get("categories") or {}).get("primary", "")
    coords   = geometry.get("coordinates", [])

    full_address = ", ".join(filter(None, [address, city, region, country]))

    # --- step 1: web-search research ------------------------------------------
    messages: list[dict] = [{
        "role": "user",
        "content": (
            f"Research this business to verify it is still accurate:\n\n"
            f"Name: {name}\n"
            f"Address: {full_address}\n"
            f"Category: {category}\n"
            f"Coordinates: {coords}\n\n"
            "Use web search to check:\n"
            "• Is it still open / operating?\n"
            "• Is the address still correct?\n"
            "• Has it moved or changed business type?\n\n"
            "Summarise what you found, including any URLs you used."
        ),
    }]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=(
                "You are a place-validation agent. "
                "CRITICAL RULES:\n"
                "1. Never state a place is closed unless you find explicit evidence.\n"
                "2. If you cannot find the business online, set status to 'uncertain', not 'closed'.\n"
                "3. Every issue you list MUST have a source URL backing it up.\n"
                "4. When sources conflict, lower your confidence score below 0.5.\n"
                "5. No assumption without evidence."
            ),
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break
        elif response.stop_reason == "pause_turn":
            # server-side tool loop hit its iteration cap — continue
            continue
        else:
            # max_tokens or unexpected stop — exit gracefully
            break

    # pull the text summary out of the final assistant turn
    research_summary = next(
        (b.text for b in response.content if getattr(b, "type", None) == "text"),
        "No research findings available.",
    )

    # --- step 2: structure the findings ---------------------------------------
    struct_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=(
            "You are a data structuring assistant. "
            "Always respond with valid JSON only. No explanation, no markdown, just raw JSON."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Based on the research below, provide a structured validation result "
                f"for the place '{name}' at '{full_address}'.\n\n"
                f"Research findings:\n{research_summary}\n\n"
                "Return ONLY a JSON object with these exact fields:\n"
                "status: 'open', 'closed', 'moved', or 'uncertain'\n"
                "confidence: float 0.0-1.0\n"
                "issues: list of strings (empty list if none)\n"
                "citations: list of URLs from the research (empty if none)\n\n"
                "Example:\n"
                '{"status": "closed", "confidence": 0.92, '
                '"issues": ["Permanently closed as of 2024"], '
                '"citations": ["https://yelp.com/..."]}'
            ),
        }],
    )

    raw = next(
        (b.text for b in struct_response.content if getattr(b, "type", None) == "text"),
        "{}",
    )
    try:
        data = json.loads(raw)
        return ValidationResult(**data)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Warning: Could not parse response: {e}")
        return ValidationResult(
            status="uncertain",
            confidence=0.0,
            issues=["Agent returned malformed response"],
            citations=[],
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate a place record from an Overture Maps GeoJSON file."
    )
    parser.add_argument(
        "--input", default="data/places.geojson", help="Path to the GeoJSON file"
    )
    parser.add_argument(
        "--index", type=int, default=0, help="Index of the place to validate (default: 0)"
    )
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])
    if args.index >= len(features):
        print(f"Error: index {args.index} out of range (file has {len(features)} features).")
        raise SystemExit(1)

    place = features[args.index]
    props = place.get("properties") or {}
    name = (props.get("names") or {}).get("primary", "Unknown")
    addrs = props.get("addresses") or [{}]
    addr_str = addrs[0].get("freeform", "") if addrs else ""

    print(f"Validating place #{args.index}: {name}")
    print(f"Address: {addr_str}")
    print("-" * 50)

    result = validate_place(place)
    print(json.dumps(result.model_dump(), indent=2))
