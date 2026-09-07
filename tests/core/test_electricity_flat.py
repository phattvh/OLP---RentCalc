# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử tính điện không kê khai theo docs/CALCULATION_RULES.md §4.4."""

from decimal import Decimal as D
import pytest

from app.core.electricity import calculate_flat_fallback_electricity
from app.core.errors import ConfigError, InputError
from app.core.types import ElectricityConfig, RentCalcConfig


def test_flat_fallback_calculation(official_config):
    r = calculate_flat_fallback_electricity("120", official_config)
    assert r.method == "flat_fallback"
    assert r.consumption == D("120")
    assert r.subtotal == D("120") * D("2380")
    assert r.vat == r.subtotal * D("0.08")
    assert r.total_rounded == D("308448")


def test_flat_fallback_missing_tier():
    # Cấu hình không có bậc 3
    broken_config = RentCalcConfig(
        version="broken",
        electricity=ElectricityConfig(
            vat_rate="0.08",
            people_per_quota="4",
            fallback_tier_number=99,  # Không tồn tại
            tiers=(),
        ),
        water=None,
        meter=None,
    )
    with pytest.raises(ConfigError):
        calculate_flat_fallback_electricity("100", broken_config)


def test_flat_fallback_negative():
    with pytest.raises(InputError):
        calculate_flat_fallback_electricity("-50", None)