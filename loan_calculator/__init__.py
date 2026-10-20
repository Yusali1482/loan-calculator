"""Loan maths with exact decimal arithmetic."""
from .calculator import Payment, amortisation_schedule, monthly_payment, total_interest

__all__ = ["Payment", "amortisation_schedule", "monthly_payment", "total_interest"]
