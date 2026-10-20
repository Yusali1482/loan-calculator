"""Core loan calculations.

Money is handled with Decimal, never float, so pennies cannot drift.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List

PENNY = Decimal("0.01")


def _money(value) -> Decimal:
    """Round any numeric value to whole pennies (half-up)."""
    return Decimal(str(value)).quantize(PENNY, rounding=ROUND_HALF_UP)


def _validate(principal, annual_rate_pct, months) -> None:
    if Decimal(str(principal)) <= 0:
        raise ValueError("principal must be greater than zero")
    if Decimal(str(annual_rate_pct)) < 0:
        raise ValueError("annual rate cannot be negative")
    if not isinstance(months, int) or isinstance(months, bool) or months < 1:
        raise ValueError("months must be a whole number of at least 1")


@dataclass(frozen=True)
class Payment:
    month: int
    payment: Decimal
    interest: Decimal
    principal: Decimal
    balance: Decimal


def monthly_payment(principal, annual_rate_pct, months: int) -> Decimal:
    """Fixed monthly repayment for a standard amortising loan."""
    _validate(principal, annual_rate_pct, months)
    p = Decimal(str(principal))
    r = Decimal(str(annual_rate_pct)) / 100 / 12
    if r == 0:
        return _money(p / months)
    growth = (1 + r) ** months
    return _money(p * r * growth / (growth - 1))


def amortisation_schedule(principal, annual_rate_pct, months: int) -> List[Payment]:
    """Month-by-month breakdown. The final payment clears any rounding residue."""
    _validate(principal, annual_rate_pct, months)
    r = Decimal(str(annual_rate_pct)) / 100 / 12
    fixed = monthly_payment(principal, annual_rate_pct, months)
    balance = _money(principal)
    schedule: List[Payment] = []
    for month in range(1, months + 1):
        interest = _money(balance * r)
        if month == months:
            principal_part = balance
            payment = principal_part + interest
        else:
            principal_part = fixed - interest
            payment = fixed
        balance = balance - principal_part
        schedule.append(Payment(month, payment, interest, principal_part, balance))
    return schedule


def total_interest(schedule: List[Payment]) -> Decimal:
    return sum((p.interest for p in schedule), Decimal("0.00"))
