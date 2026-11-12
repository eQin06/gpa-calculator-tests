"""R8: command-line interface.

Usage: python -m gpa_calculator CODE:SCORE:CREDITS [CODE:SCORE:CREDITS ...]
"""
import sys

from gpa_calculator.core import evaluate


def parse_course(text):
    """Turn 'CMPE411:87:6' into ('CMPE411', 87.0, 6)."""
    parts = text.split(":")
    if len(parts) != 3 or not parts[0].strip():
        raise ValueError(f"expected CODE:SCORE:CREDITS, got {text!r}")
    code, score_text, credits_text = parts
    try:
        score = float(score_text)
        credits = int(credits_text)
    except ValueError:
        raise ValueError(f"invalid number in {text!r}")
    return code.strip(), score, credits


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("Error: no courses given. Usage: python -m gpa_calculator CODE:SCORE:CREDITS ...",
              file=sys.stderr)
        return 2
    try:
        courses = [parse_course(arg) for arg in args]
        gpa, standing = evaluate(courses)
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    print(f"GPA: {gpa:.2f}")
    print(f"Standing: {standing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())