"""Unit tests for R1 to R4: scores, letters and credits."""
import pytest

from gpa_calculator.core import letter_to_points, score_to_letter, validate_credits


# R2 – boundary values: the last value below each bound and the bound itself.
@pytest.mark.parametrize("score, expected", [
    (100, "AA"), (90, "AA"), (89.99, "BA"),
    (85, "BA"), (84.99, "BB"),
    (80, "BB"), (79.99, "CB"),
    (75, "CB"), (74.99, "CC"),
    (70, "CC"), (69.99, "DC"),
    (65, "DC"), (64.99, "DD"),
    (60, "DD"), (59.99, "FD"),
    (50, "FD"), (49.99, "FF"),
    (0, "FF"),
])
def test_score_to_letter_boundaries(score, expected):
    assert score_to_letter(score) == expected


# R1 – boundary values just outside the valid range [0, 100].
@pytest.mark.parametrize("score", [-0.01, 100.01])
def test_score_out_of_range_is_rejected(score):
    with pytest.raises(ValueError):
        score_to_letter(score)


# R1 – equivalence partitioning: one representative per invalid type class.
@pytest.mark.parametrize("score", ["85", None, True])
def test_non_numeric_score_is_rejected(score):
    with pytest.raises(TypeError):
        score_to_letter(score)


# R3 – every valid letter, plus case and whitespace partitions.
@pytest.mark.parametrize("letter, expected", [
    ("AA", 4.0), ("BA", 3.5), ("BB", 3.0), ("CB", 2.5), ("CC", 2.0),
    ("DC", 1.5), ("DD", 1.0), ("FD", 0.5), ("FF", 0.0),
    ("ba", 3.5), (" BA ", 3.5),
])
def test_letter_to_points(letter, expected):
    assert letter_to_points(letter) == expected


@pytest.mark.parametrize("letter", ["A", "XX", ""])
def test_unknown_letter_is_rejected(letter):
    with pytest.raises(ValueError):
        letter_to_points(letter)


# R4 – boundary values for credits in [1, 8].
@pytest.mark.parametrize("credits", [1, 8])
def test_valid_credit_boundaries(credits):
    validate_credits(credits)  # must not raise


@pytest.mark.parametrize("credits", [0, 9])
def test_credits_out_of_range_are_rejected(credits):
    with pytest.raises(ValueError):
        validate_credits(credits)


@pytest.mark.parametrize("credits", [3.5, "3"])
def test_non_integer_credits_are_rejected(credits):
    with pytest.raises(TypeError):
        validate_credits(credits)