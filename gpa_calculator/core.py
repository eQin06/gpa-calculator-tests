"""GPA calculator. The rules come from REQUIREMENTS.md (R1 to R7)."""
from decimal import Decimal, ROUND_HALF_UP

# R2: (lower bound, letter), checked from the highest bound down.
LETTER_BOUNDS = [
    (90, "AA"),
    (85, "BA"),
    (80, "BB"),
    (75, "CB"),
    (70, "CC"),
    (65, "DC"),
    (60, "DD"),
    (50, "FD"),
    (0, "FF"),
]

# R3
GRADE_POINTS = {
    "AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5, "CC": 2.0,
    "DC": 1.5, "DD": 1.0, "FD": 0.5, "FF": 0.0,
}

FAILING_LETTERS = {"FD", "FF"}   # R7
MIN_CREDITS = 1                  # R4
MAX_CREDITS = 8                  # R4
HONOR_MIN_CREDITS = 15           # R7


def validate_score(score):
    """R1: a score must be a number in [0, 100]."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError(f"score must be a number, got {score!r}")
    if not 0 <= score <= 100:
        raise ValueError(f"score must be between 0 and 100, got {score}")


def score_to_letter(score):
    """R2: convert a score to a letter grade."""
    validate_score(score)
    for lower_bound, letter in LETTER_BOUNDS:
        if score >= lower_bound:
            return letter


def letter_to_points(letter):
    """R3: convert a letter grade to grade points."""
    if not isinstance(letter, str):
        raise ValueError(f"unknown letter grade {letter!r}")
    key = letter.strip().upper()
    if key not in GRADE_POINTS:
        raise ValueError(f"unknown letter grade {letter!r}")
    return GRADE_POINTS[key]


def validate_credits(credits):
    """R4: credits must be an integer from 1 to 8."""
    if isinstance(credits, bool) or not isinstance(credits, int):
        raise TypeError(f"credits must be an integer, got {credits!r}")
    if not MIN_CREDITS <= credits <= MAX_CREDITS:
        raise ValueError(f"credits must be between 1 and 8, got {credits}")


def deduplicate_courses(courses):
    """R6: if a course code repeats, only the last entry counts."""
    latest = {}
    for code, score, credits in courses:
        latest[code.upper()] = (code, score, credits)
    return list(latest.values())


def calculate_gpa(courses):
    """R5: credit-weighted GPA, rounded half up to 2 decimals.

    courses is a list of (code, score, credits) tuples.
    """
    if not courses:
        raise ValueError("course list is empty")
    for _code, score, credits in courses:
        validate_score(score)
        validate_credits(credits)

    total_points = Decimal(0)
    total_credits = 0
    for _code, score, credits in deduplicate_courses(courses):
        points = letter_to_points(score_to_letter(score))
        total_points += Decimal(str(points)) * credits
        total_credits += credits

    gpa = (total_points / total_credits).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(gpa)


def academic_standing(gpa, total_credits, has_failing):
    """R7: the decision table for academic standing."""
    if gpa < 2.00:
        return "Probation"                      # rule 1
    if gpa < 3.00:
        return "Satisfactory"                   # rule 2
    if total_credits < HONOR_MIN_CREDITS or has_failing:
        return "Satisfactory"                   # rules 3 and 4
    if gpa < 3.50:
        return "Honor"                          # rule 5
    return "High Honor"                         # rule 6


def evaluate(courses):
    """Return (gpa, standing) for a list of (code, score, credits) tuples."""
    gpa = calculate_gpa(courses)
    counted = deduplicate_courses(courses)
    total_credits = sum(credits for _code, _score, credits in counted)
    has_failing = any(score_to_letter(score) in FAILING_LETTERS for _code, score, _credits in counted)
    return gpa, academic_standing(gpa, total_credits, has_failing)