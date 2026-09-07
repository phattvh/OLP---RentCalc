# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
""" Xem docs/CALCULATION_RULES.md §4–§6.
Fixture này CHỈ dùng cho test; engine không được import nó."""

import pytest

from app.core.types import (
    ElectricityConfig,
    ElectricityTier,
    MeterConfig,
    RentCalcConfig,
    WaterConfig,
)

@pytest.fixture
def official_config() -> RentCalcConfig:
    return RentCalcConfig(
        version="official-2026",
        electricity=ElectricityConfig(
            vat_rate="0.08",
            people_per_quota="4",
            fallback_tier_number=3,
            tiers=(
                ElectricityTier(1, "Bậc 1", "50", "1984"),
                ElectricityTier(2, "Bậc 2", "50", "2050"),
                ElectricityTier(3, "Bậc 3", "100", "2380"),
                ElectricityTier(4, "Bậc 4", "100", "2998"),
                ElectricityTier(5, "Bậc 5", "100", "3350"),
                ElectricityTier(6, "Bậc 6", None, "3460"),
            ),
        ),
        water=WaterConfig(
            vat_rate="0.05",
            env_fee_rate="0.10",
            volume_unit_price="8500",
            per_person_unit_price="80000",
        ),
        meter=MeterConfig(max_value="99999"),
    )