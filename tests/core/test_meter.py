# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử biên và định dạng công tơ theo docs/CALCULATION_RULES.md §5."""

from decimal import Decimal as D
import pytest

from app.core.errors import MeterReadingError
from app.core.meter import calculate_consumption, parse_meter_reading


def test_parse_valid_readings():
    assert parse_meter_reading("00.120") == D("120")
    assert parse_meter_reading("99.850") == D("99850")
    assert parse_meter_reading("00120") == D("120")
    assert parse_meter_reading("120") == D("120")
    assert parse_meter_reading("99999") == D("99999")
    assert parse_meter_reading(120) == D("120")
    assert parse_meter_reading(D("120")) == D("120")


def test_parse_invalid_readings():
    for invalid in ["", "   ", "abc", "-5", "12,5", "1.23", "12.34"]:
        with pytest.raises(MeterReadingError):
            parse_meter_reading(invalid)


def test_calculate_consumption_normal():
    assert calculate_consumption("100", "100", "99999") == D("0")
    assert calculate_consumption("0", "120", "99999") == D("120")
    assert calculate_consumption("100", "250", "99999") == D("150")


def test_calculate_consumption_rollover():
    # 99850 -> 120 (qua 99999) = 100000 - 99850 + 120 = 270
    assert calculate_consumption("99850", "120", "99999") == D("270")
    # 99999 -> 0 = 1
    assert calculate_consumption("99999", "0", "99999") == D("1")


def test_calculate_consumption_custom_max():
    # Công tơ 4 chữ số: max = 9999
    assert calculate_consumption("9900", "50", "9999") == D("150")