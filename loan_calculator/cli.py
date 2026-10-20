"""Command-line interface: python -m loan_calculator 5000 8.9 24 --schedule"""
import argparse
import sys
from typing import List, Optional

from .calculator import amortisation_schedule, monthly_payment, total_interest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Work out the cost of a loan.")
    parser.add_argument("principal", help="amount borrowed, e.g. 5000")
    parser.add_argument("rate", help="annual interest rate in percent, e.g. 8.9")
    parser.add_argument("months", type=int, help="loan term in months")
    parser.add_argument("--schedule", action="store_true", help="print every payment")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        payment = monthly_payment(args.principal, args.rate, args.months)
        schedule = amortisation_schedule(args.principal, args.rate, args.months)
    except (ValueError, ArithmeticError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    interest = total_interest(schedule)
    print(f"Monthly payment : £{payment:,.2f}")
    print(f"Total interest  : £{interest:,.2f}")
    print(f"Total repayable : £{sum(p.payment for p in schedule):,.2f}")

    if args.schedule:
        print(f"\n{'Month':>5} {'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>10}")
        for p in schedule:
            print(f"{p.month:>5} {p.payment:>10,.2f} {p.interest:>10,.2f} "
                  f"{p.principal:>10,.2f} {p.balance:>10,.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
