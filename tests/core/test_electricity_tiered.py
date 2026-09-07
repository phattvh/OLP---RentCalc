# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử ranh giới bậc thang điện theo docs/CALCULATION_RULES.md §4."""

from decimal import Decimal as D
import pytest

from app.core.electricity import calculate_tiered_electricity
from app.core.errors import InputError


def test_tier_boundaries_at_quota_one(official_config):
    # Ranh giới bậc 1: 50 kWh
    r50 = calculate_tiered_electricity("50", 4, official_config)
    assert len(r50.breakdown) == 1
    assert r50.breakdown[0].consumption == D("50")
    assert r50.subtotal == D("50") * D("1984")

    # Bậc 2: 100 kWh (50 bậc 1 + 50 bậc 2)
    r100 = calculate_tiered_electricity("100", 4, official_config)
    assert len(r100.breakdown) == 2
    assert r100.breakdown[1].consumption == D("50")

    # Bậc 3: 200 kWh (50 + 50 + 100)
    r200 = calculate_tiered_electricity("200", 4, official_config)
    assert len(r200.breakdown) == 3
    assert r200.breakdown[2].consumption == D("100")


def test_zero_consumption(official_config):
    r0 = calculate_tiered_electricity("0", 4, official_config)
    assert r0.consumption == D("0")
    assert r0.subtotal == D("0")
    assert r0.vat == D("0")
    assert r0.total_rounded == D("0")


def test_beyond_tier_six(official_config):
    # 1000 kWh -> 400 kWh qua 5 bậc đầu, 600 kWh ở bậc 6
    r1000 = calculate_tiered_electricity("1000", 4, official_config)
    assert r1000.breakdown[5].consumption == D("600")
    assert r1000.breakdown[5].unit_price == D("3460")


def test_quota_zero_all_fallback_to_last_tier(official_config):
    # Theo chính sách §10: Q=0 thì các bậc hữu hạn = 0, toàn bộ rơi bậc 6
    r = calculate_tiered_electricity("100", 0, official_config)
    assert r.quota == D("0")
    assert r.breakdown[5].consumption == D("100")
    assert r.subtotal == D("100") * D("3460")


def test_negative_consumption_raises_error(official_config):
    with pytest.raises(InputError):
        calculate_tiered_electricity("-10", 4, official_config)