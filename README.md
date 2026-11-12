# GPA Calculator – Test Suite

CMPE 411 term project. A small GPA calculator written in Python, tested at two levels
(unit and end-to-end) and compared with LLM-generated tests (AI element A).

The rules the calculator follows are in [REQUIREMENTS.md](REQUIREMENTS.md). Every test
traces back to a rule there (R1 to R8).

## Requirements

- Python 3.9 or newer
- Git

## Install and run (under 5 minutes)

```bash
git clone <this-repository-url>
cd gpa-calculator-tests
python -m venv .venv
```

Activate the virtual environment:

- Windows (PowerShell): `.venv\Scripts\activate`
- macOS / Linux: `source .venv/bin/activate`

Then install and run the tests:

```bash
pip install -r requirements.txt
pytest
```

With branch coverage:

```bash
pytest --cov=gpa_calculator --cov-branch
```

## Using the calculator

```bash
python -m gpa_calculator CMPE411:87:6 MATH101:72:4
```

Output:

```
GPA: 2.90
Standing: Satisfactory
```

Each argument is `CODE:SCORE:CREDITS`.

## Project structure

```
gpa_calculator/       the application
  core.py             grading, GPA and standing logic (R1–R7)
  __main__.py         command-line interface (R8)
tests/
  unit/               unit tests: boundary values, equivalence partitions, decision table
  e2e/                end-to-end tests that run the CLI as a separate process
  llm/                LLM-generated tests (AI element)
REQUIREMENTS.md       the specification and test oracle
```