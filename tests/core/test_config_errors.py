# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử cấu hình lỗi theo docs/CALCULATION_RULES.md §10."""

import pytest
from dataclasses import replace

from app.core.electricity import calculate_tiered_electricity
from app.core.errors import ConfigError
from app.core.types import (
    ElectricityConfig,
    ElectricityTier,
    MeterConfig,
    RentCalcConfig,
    WaterConfig,
)


def test_config_missing_infinite_tier():
    # Mọi bậc đều có giới hạn, không có bậc vô hạn cuối cùng
    config = RentCalcConfig(
        version="broken",
        electricity=ElectricityConfig(
            vat_rate="0.08",
            people_per_quota="4",
            fallback_tier_number=1,
            tiers=(
                ElectricityTier(1, "Bậc 1", "50", "1984"),
                ElectricityTier(2, "Bậc 2", "50", "2050"),
            ),
        ),
        water=WaterConfig("0.05", "0.10", "8500", "80000"),
        meter=MeterConfig("99999"),
    )
    # 200 kWh vượt quá 50 + 50 -> Phải ném ConfigError
    with pytest.raises(ConfigError):
        calculate_tiered_electricity("200", 4, config)


def test_config_negative_vat_rate():
    config = RentCalcConfig(
        version="broken",
        electricity=ElectricityConfig(
            vat_rate="-0.08",
            people_per_quota="4",
            fallback_tier_number=1,
            tiers=(ElectricityTier(1, "Bậc 1", None, "1984"),),
        ),
        water=WaterConfig("0.05", "0.10", "8500", "80000"),
        meter=MeterConfig("99999"),
    )
    with pytest.raises(ConfigError):
        calculate_tiered_electricity("100", 4, config)

def test_negative_price_in_infinite_tier_rejected(official_config):
    # Cấu hình bậc 6 có đơn giá âm (-1000)
    bad = replace(
        official_config,
        electricity=replace(
            official_config.electricity,
            tiers=tuple(
                replace(t, unit_price="-1000") if t.number == 6 else t
                for t in official_config.electricity.tiers
            ),
        ),
    )
    with pytest.raises(ConfigError):
        calculate_tiered_electricity("120", 4, bad)