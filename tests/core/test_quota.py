# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử tính định mức theo docs/CALCULATION_RULES.md §4.3."""

from decimal import Decimal as D
import pytest

from app.core.errors import ConfigError, InputError
from app.core.quota import calculate_quota


def test_calculate_quota_exact():
    assert calculate_quota(0, "4") == D("0")
    assert calculate_quota(1, "4") == D("0.25")
    assert calculate_quota(2, "4") == D("0.5")
    assert calculate_quota(3, "4") == D("0.75")
    assert calculate_quota(4, "4") == D("1")
    assert calculate_quota(5, "4") == D("1.25")
    assert calculate_quota(7, "4") == D("1.75")
    assert calculate_quota(8, "4") == D("2")


def test_calculate_quota_errors():
    with pytest.raises(InputError):
        calculate_quota(-1, "4")
    with pytest.raises(ConfigError):
        calculate_quota(4, "0")
    with pytest.raises(ConfigError):
        calculate_quota(4, "-4")