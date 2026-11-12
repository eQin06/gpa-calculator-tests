# GPA Calculator – Requirements

## R1. Score input
- A score is a number (int or float) in the range [0, 100], inclusive.
- A score outside this range raises `ValueError`.
- A non-numeric score (for example a string, `None` or a bool) raises `TypeError`.

## R2. Score to letter grade
Lower bounds are inclusive.

| Score        | Letter |
|--------------|--------|
| 90 – 100     | AA     |
| 85 – < 90    | BA     |
| 80 – < 85    | BB     |
| 75 – < 80    | CB     |
| 70 – < 75    | CC     |
| 65 – < 70    | DC     |
| 60 – < 65    | DD     |
| 50 – < 60    | FD     |
| 0 – < 50     | FF     |

Example: 89.99 is BA, 90 is AA.

## R3. Letter grade to grade points
| AA  | BA  | BB  | CB  | CC  | DC  | DD  | FD  | FF  |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 4.0 | 3.5 | 3.0 | 2.5 | 2.0 | 1.5 | 1.0 | 0.5 | 0.0 |

- Letters are case-insensitive and surrounding spaces are ignored (" ba " is BA).
- Any other letter raises `ValueError`.

## R4. Credits
- Credits are an integer from 1 to 8, inclusive.
- Credits outside this range raise `ValueError`.
- Non-integer credits (for example 3.5 or "3") raise `TypeError`.

## R5. GPA calculation
- GPA = sum(grade points × credits) / sum(credits).
- The result is rounded to 2 decimal places, with halves rounded up (2.345 → 2.35).
- An empty course list raises `ValueError`.

## R6. Repeated courses
- If the same course code appears more than once, only the last entry counts.
- Course codes are compared case-insensitively ("cmpe411" equals "CMPE411").

## R7. Academic standing
Inputs: GPA (after R6), total credits (after R6), and whether any counted course has FD or FF.

| Rule | GPA          | Total credits ≥ 15 | Any FD/FF | Standing      |
|------|--------------|--------------------|-----------|---------------|
| 1    | < 2.00       | –                  | –         | Probation     |
| 2    | 2.00 – < 3.00| –                  | –         | Satisfactory  |
| 3    | ≥ 3.00       | No                 | –         | Satisfactory  |
| 4    | ≥ 3.00       | Yes                | Yes       | Satisfactory  |
| 5    | 3.00 – < 3.50| Yes                | No        | Honor         |
| 6    | ≥ 3.50       | Yes                | No        | High Honor    |

("–" means the condition does not matter.)

## R8. Command-line interface
- Usage: `python -m gpa_calculator CODE:SCORE:CREDITS [CODE:SCORE:CREDITS ...]`
- Example: `python -m gpa_calculator CMPE411:87:6 MATH101:72:4`
- On success it prints two lines and exits with code 0:
  `GPA: 2.90`
  `Standing: Satisfactory`
- On invalid input, or with no arguments, it prints a message starting with `Error:` to stderr and exits with code 2.