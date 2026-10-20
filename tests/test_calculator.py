from decimal import Decimal

import pytest

from loan_calculator import amortisation_schedule, monthly_payment, total_interest


def test_known_textbook_payment():
    # £10,000 at 6% over 12 months is the standard worked example: £860.66
    assert monthly_payment(10000, 6, 12) == Decimal("860.66")


def test_zero_interest_splits_evenly():
    assert monthly_payment(1200, 0, 12) == Decimal("100.00")


def test_schedule_has_one_row_per_month():
    assert len(amortisation_schedule(5000, 8.9, 24)) == 24


def test_schedule_ends_at_exactly_zero():
    assert amortisation_schedule(5000, 8.9, 24)[-1].balance == Decimal("0.00")


def test_principal_repaid_equals_amount_borrowed():
    schedule = amortisation_schedule(7500, 12.5, 36)
    assert sum(p.principal for p in schedule) == Decimal("7500.00")


def test_interest_falls_over_time():
    schedule = amortisation_schedule(5000, 8.9, 24)
    assert schedule[0].interest > schedule[-1].interest


def test_total_interest_matches_payments_minus_principal():
    schedule = amortisation_schedule(5000, 8.9, 24)
    paid = sum(p.payment for p in schedule)
    assert total_interest(schedule) == paid - Decimal("5000.00")


def test_zero_rate_has_no_interest():
    assert total_interest(amortisation_schedule(1200, 0, 12)) == Decimal("0.00")


@pytest.mark.parametrize(
    "principal, rate, months",
    [(0, 5, 12), (-100, 5, 12), (1000, -1, 12), (1000, 5, 0), (1000, 5, 1.5), (1000, 5, True)],
)
def test_invalid_inputs_are_rejected(principal, rate, months):
    with pytest.raises(ValueError):
        monthly_payment(principal, rate, months)
