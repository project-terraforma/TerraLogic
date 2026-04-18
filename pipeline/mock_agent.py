import random
from agent import ValidationResult

def mock_validate_place(place: dict) -> ValidationResult:
    """
    Returns a fake but realistic ValidationResult.
    Use this while waiting for API credits.
    """
    roll = random.random()

    if roll < 0.60:
        return ValidationResult(
            status="open",
            confidence=round(random.uniform(0.75, 0.95), 2),
            issues=[],
            citations=["https://mock-source.com/verified"]
        )
    elif roll < 0.80:
        return ValidationResult(
            status="uncertain",
            confidence=round(random.uniform(0.3, 0.6), 2),
            issues=["Insufficient data found online"],
            citations=[]
        )
    elif roll < 0.93:
        return ValidationResult(
            status="closed",
            confidence=round(random.uniform(0.7, 0.92), 2),
            issues=["Business appears permanently closed"],
            citations=["https://mock-source.com/closure-notice"]
        )
    else:
        return ValidationResult(
            status="moved",
            confidence=round(random.uniform(0.65, 0.85), 2),
            issues=["Business may have relocated"],
            citations=["https://mock-source.com/new-location"]
        )