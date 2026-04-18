import os
import json
from pydantic import BaseModel
from agent import ValidationResult

os.environ["PYTHONUTF8"] = "1"


class ScoredResult(BaseModel):
    # Core score
    confidence: float           # 0.0 - 1.0 final confidence
    priority: str               # "high" | "medium" | "low"

    # Dashboard display
    color: str                  # "red" | "yellow" | "green"
    label: str                  # human readable label
    action_needed: bool         # should this appear in review queue?

    # Pass through from agent
    status: str                 # open | closed | moved | uncertain
    issues: list[str]
    citations: list[str]

    # Penalty breakdown (for transparency)
    base_confidence: float      # raw confidence from agent
    citation_penalty: float     # penalty for missing citations
    consistency_penalty: float  # penalty for status/confidence mismatch


def score_result(result: ValidationResult) -> ScoredResult:
    """
    Takes a raw ValidationResult from the agent and produces
    a ScoredResult with priority, color, and dashboard signals.
    """

    base_confidence = result.confidence
    citation_penalty = 0.0
    consistency_penalty = 0.0

    # ── PENALTY 1: Missing citations ──────────────────────────────────
    # If issues exist but no citations → agent made unsupported claims
    if result.issues and not result.citations:
        citation_penalty = 0.30  # heavy penalty — no evidence
    elif result.issues and len(result.citations) < len(result.issues):
        citation_penalty = 0.10  # mild penalty — partial evidence

    # ── PENALTY 2: Status / confidence mismatch ───────────────────────
    # High confidence should only come with clear status
    if result.status == "uncertain" and result.confidence > 0.6:
        consistency_penalty = 0.20  # can't be uncertain AND confident
    if result.status == "open" and result.confidence < 0.4:
        consistency_penalty = 0.10  # suspiciously low confidence for open

    # ── FINAL CONFIDENCE ──────────────────────────────────────────────
    final_confidence = round(
        max(0.0, base_confidence - citation_penalty - consistency_penalty), 2
    )

    # ── PRIORITY ──────────────────────────────────────────────────────
    # High priority = likely wrong, needs human review fast
    if result.status in ("closed", "moved") and final_confidence >= 0.7:
        priority = "high"
    elif result.status == "uncertain" or final_confidence < 0.5:
        priority = "medium"
    else:
        priority = "low"

    # ── COLOR (for map pins) ──────────────────────────────────────────
    if priority == "high":
        color = "red"
    elif priority == "medium":
        color = "yellow"
    else:
        color = "green"

    # ── LABEL (for dashboard cards) ───────────────────────────────────
    label_map = {
        "open":      "Verified open",
        "closed":    "Likely closed",
        "moved":     "Possibly relocated",
        "uncertain": "Needs review",
    }
    label = label_map.get(result.status, "Unknown")

    # ── ACTION NEEDED ─────────────────────────────────────────────────
    # Only surface in review queue if there's something to act on
    action_needed = priority in ("high", "medium") or bool(result.issues)

    return ScoredResult(
        confidence=final_confidence,
        priority=priority,
        color=color,
        label=label,
        action_needed=action_needed,
        status=result.status,
        issues=result.issues,
        citations=result.citations,
        base_confidence=base_confidence,
        citation_penalty=citation_penalty,
        consistency_penalty=consistency_penalty,
    )


# ── Batch scoring ─────────────────────────────────────────────────────
def score_all(input_path: str, output_path: str):
    """
    Score all validated places from validated_sample.json
    and save results to scored_results.json
    """
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    scored = []
    stats = {"high": 0, "medium": 0, "low": 0}

    for item in data:
        raw = item["validation"]
        result = ValidationResult(**raw)
        scored_result = score_result(result)

        stats[scored_result.priority] += 1

        scored.append({
            "id": item["id"],
            "name": item["name"],
            "address": item["address"],
            "coordinates": item["coordinates"],
            "scored": scored_result.model_dump()
        })

        print(
            f"[{scored_result.color.upper()}] {item['name'][:40]:<40} "
            f"→ {scored_result.label:<20} "
            f"confidence: {scored_result.confidence}"
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scored, f, indent=2)

    print(f"\n✅ Scored {len(scored)} places → {output_path}")
    print(f"   🔴 High priority:   {stats['high']}")
    print(f"   🟡 Medium priority: {stats['medium']}")
    print(f"   🟢 Low priority:    {stats['low']}")


# ── CLI ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Score validated Overture Places")
    parser.add_argument("--input",  default="data/validated_sample.json")
    parser.add_argument("--output", default="data/scored_results.json")
    args = parser.parse_args()

    score_all(args.input, args.output)