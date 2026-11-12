"""Unit tests for R5 to R7: GPA, repeated courses and academic standing."""
import pytest

from gpa_calculator.core import academic_standing, calculate_gpa, evaluate


# R5 – weighted average: (4.0*6 + 2.0*4) / 10 = 3.20
def test_gpa_is_credit_weighted():
    assert calculate_gpa([("CMPE411", 95, 6), ("MATH101", 72, 4)]) == 3.20


# R5 – rounding half up: inputs chosen so the exact GPA ends in 5.
def test_gpa_rounds_half_up():
    # (4.0*3 + 3.5*2 + 0.0*3) / 8 = 19/8 = 2.375 -> 2.38
    courses = [("A", 95, 3), ("B", 87, 2), ("C", 10, 3)]
    assert calculate_gpa(courses) == 2.38


def test_empty_course_list_is_rejected():
    with pytest.raises(ValueError):
        calculate_gpa([])


# R6 – only the last entry of a repeated course counts, codes are case-insensitive.
def test_repeated_course_keeps_last_entry():
    courses = [("cmpe411", 40, 6), ("CMPE411", 95, 6)]
    assert calculate_gpa(courses) == 4.00


# R7 – decision table, one test per rule.
@pytest.mark.parametrize("rule, gpa, credits, has_failing, expected", [
    (1, 1.99, 20, False, "Probation"),
    (2, 2.00, 20, False, "Satisfactory"),
    (2, 2.99, 20, False, "Satisfactory"),
    (3, 3.80, 14, False, "Satisfactory"),
    (4, 3.80, 15, True, "Satisfactory"),
    (5, 3.00, 15, False, "Honor"),
    (5, 3.49, 15, False, "Honor"),
    (6, 3.50, 15, False, "High Honor"),
])
def test_academic_standing_decision_table(rule, gpa, credits, has_failing, expected):
    assert academic_standing(gpa, credits, has_failing) == expected


# R6 + R7 – a failed attempt that was repeated no longer blocks honors.
def test_repeated_failure_does_not_block_honor():
    courses = [("A", 30, 8), ("A", 95, 8), ("B", 92, 8)]
    assert evaluate(courses) == (4.00, "High Honor")