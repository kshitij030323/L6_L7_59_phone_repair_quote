# Lab 6 - Code (Line) Coverage test cases
# Name: Kshitij Gupta | SRN: PES1UG24AM915 | Section: F
# Goal: execute every statement of phone_repair_quote.py at least once.

import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value


# ---------- repair_quote ----------

def test_budget_screen():
    assert repair_quote("screen", "budget", False, False) == 4600


def test_unknown_part_raises():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)


def test_unknown_brand_tier_raises():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("battery", "midrange", False, False)


def test_flagship_battery_warranty_express():
    # flagship doubles cost, non-screen labour 300, warranty zeroes cost, express +500
    assert repair_quote("battery", "flagship", True, True) == 800


# ---------- repair_days ----------

def test_in_stock_quick():
    assert repair_days("battery", True, 2) == 1


def test_no_technicians_screen_out_of_stock():
    assert repair_days("screen", False, 0) == 8


def test_other_part_out_of_stock():
    assert repair_days("battery", False, 1) == 3


# ---------- trade_in_value ----------

def test_trade_in_invalid_input():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 5, False)


def test_trade_in_too_old():
    assert trade_in_value(30000, 60, False) == 0


def test_trade_in_under_one_year_cracked():
    assert trade_in_value(30000, 6, True) == 9000


def test_trade_in_one_to_two_years():
    assert trade_in_value(30000, 18, False) == 12000


def test_trade_in_two_to_four_years():
    assert trade_in_value(30000, 36, False) == 6000
