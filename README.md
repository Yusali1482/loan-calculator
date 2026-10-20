# Loan Calculator

A command-line tool that works out the monthly payment, total interest and full
month-by-month repayment schedule for a standard amortising loan.

Built in Python with `Decimal` arithmetic, because floating-point numbers are
the wrong tool for money (`0.1 + 0.2 != 0.3`).

## Features

- Monthly payment for any amount, rate and term
- Full amortisation schedule (interest vs principal each month)
- Zero-interest loans handled correctly
- Final payment clears rounding residue so the balance ends at exactly £0.00
- Input validation with clear error messages
- 17 automated tests, run on every push via GitHub Actions

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python -m loan_calculator 5000 8.9 24
python -m loan_calculator 5000 8.9 24 --schedule
```

```
Monthly payment : £228.19
Total interest  : £476.67
Total repayable : £5,476.67
```

## Run the tests

```bash
pytest -v
```

## Design decisions

- **Decimal, not float** - every amount is rounded half-up to whole pennies.
- **Pure functions in `calculator.py`**, with the CLI kept separate in `cli.py`,
  so the logic can be tested without touching the terminal.
- **Frozen dataclass for `Payment`** - schedule rows cannot be changed by accident.

## What I'd improve next

- Add an overpayment option (pay extra each month and see the interest saved)
- Support different compounding conventions
- Export the schedule to CSV
