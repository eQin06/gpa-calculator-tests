"""Unit tests for R8: call the CLI's main() function directly, in the same process."""
import pytest

from gpa_calculator.__main__ import main, parse_course


def test_parse_course_splits_and_converts():
    assert parse_course("CMPE411:87:6") == ("CMPE411", 87.0, 6)


@pytest.mark.parametrize("text", ["CMPE411:87", ":87:6", "CMPE411:abc:6"])
def test_parse_course_rejects_bad_format(text):
    with pytest.raises(ValueError):
        parse_course(text)


def test_main_prints_result(capsys):
    assert main(["CMPE411:87:6", "MATH101:72:4"]) == 0
    assert capsys.readouterr().out.splitlines() == ["GPA: 2.90", "Standing: Satisfactory"]


def test_main_without_arguments_returns_2(capsys):
    assert main([]) == 2
    assert capsys.readouterr().err.startswith("Error:")


def test_main_invalid_score_returns_2(capsys):
    assert main(["A:101:3"]) == 2
    assert capsys.readouterr().err.startswith("Error:")