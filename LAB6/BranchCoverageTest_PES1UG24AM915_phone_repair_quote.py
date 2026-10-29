# Lab 6 - Branch Coverage test cases
# Name: Kshitij Gupta | SRN: PES1UG24AM915 | Section: F
# Goal: make every decision in phone_repair_quote.py evaluate to both True and False.

import pytest
from phone_repair_quote import repair_quote, repair_days, trade_in_value


# ---------- repair_quote ----------

def test_part_not_in_price_list_true():
    with pytest.raises(ValueError, match="unknown part"):
        repair_quote("speaker", "budget", False, False)


def test_brand_tier_invalid_true():
    with pytest.raises(ValueError, match="unknown brand tier"):
        repair_quote("screen", "premium", False, False)


def test_budget_screen_no_warranty_no_express():
    # flagship False, screen True, warranty False, express False
    assert repair_quote("screen", "budget", False, False) == 4600


def test_flagship_screen_express():
    # flagship True, screen True, express True
    assert repair_quote("screen", "flagship", False, True) == 9100


def test_budget_camera_no_warranty():
    # screen False -> labour 300, warranty False
    assert repair_quote("camera", "budget", False, False) == 2800


def test_warranty_non_screen_part_is_free():
    # under_warranty True and part != "screen" True -> cost = 0
    assert repair_quote("charging_port", "flagship", True, False) == 300


def test_warranty_does_not_cover_screen():
    # under_warranty True but part != "screen" False -> cost kept
    assert repair_quote("screen", "budget", True, False) == 4600


def test_warranty_battery_express():
    assert repair_quote("battery", "budget", True, True) == 800


# ---------- repair_days ----------

def test_technicians_free_parts_in_stock():
    # technicians_free == 0 False, not parts_in_stock False
    assert repair_days("battery", True, 2) == 1


def test_no_technicians_parts_in_stock():
    # technicians_free == 0 True
    assert repair_days("battery", True, 0) == 3


def test_out_of_stock_screen():
    # part == "screen" True
    assert repair_days("screen", False, 1) == 6


def test_out_of_stock_camera():
    # part == "screen" False, part == "camera" True
    assert repair_days("camera", False, 1) == 6


def test_out_of_stock_other_part():
    # both screen/camera checks False -> +2
    assert repair_days("charging_port", False, 1) == 3


def test_out_of_stock_no_technicians_screen():
    assert repair_days("screen", False, 0) == 8


# ---------- trade_in_value ----------

def test_trade_in_non_positive_price():
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(0, 5, False)


def test_trade_in_negative_age():
    # original_price <= 0 False, age_months < 0 True
    with pytest.raises(ValueError, match="invalid input"):
        trade_in_value(20000, -1, False)


def test_trade_in_older_than_48_months():
    assert trade_in_value(20000, 49, False) == 0


def test_trade_in_exactly_48_months():
    # age > 48 False at boundary -> falls to 20% band
    assert trade_in_value(20000, 48, False) == 4000


def test_trade_in_new_phone_zero_months():
    assert trade_in_value(20000, 0, False) == 12000


def test_trade_in_exactly_12_months():
    assert trade_in_value(20000, 12, False) == 12000


def test_trade_in_13_months():
    assert trade_in_value(20000, 13, False) == 8000


def test_trade_in_exactly_24_months():
    assert trade_in_value(20000, 24, False) == 8000


def test_trade_in_25_months():
    assert trade_in_value(20000, 25, False) == 4000


def test_trade_in_screen_cracked_halves_value():
    assert trade_in_value(20000, 12, True) == 6000


def test_trade_in_cracked_old_band_floor_division():
    # 999 * 20 // 100 = 199, cracked -> 99
    assert trade_in_value(999, 30, True) == 99
