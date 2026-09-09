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
    assert r.breakdown[-1].consumption == D("100")
    assert r.subtotal == D("100") * D("3460")


def test_negative_consumption_raises_error(official_config):
    with pytest.raises(InputError):
        calculate_tiered_electricity("-10", 4, official_config)


def test_fractional_quota_five_people(official_config):
    """5 người = 1.25 định mức (định mức bậc 1 là 50 * 1.25 = 62.5 kWh)."""
    r = calculate_tiered_electricity("62.5", 5, official_config)
    assert r.quota == D("1.25")
    assert len(r.breakdown) == 1
    assert r.breakdown[0].consumption == D("62.5")
    assert r.subtotal == D("62.5") * D("1984")


def test_single_kwh_consumption(official_config):
    """Tiêu thụ tối thiểu 1 kWh."""
    r1 = calculate_tiered_electricity("1", 4, official_config)
    assert r1.consumption == D("1")
    assert r1.breakdown[0].consumption == D("1")
    assert r1.subtotal == D("1984")
    # VAT 8%: 1984 * 0.08 = 158.72 -> total = 2142.72 -> round = 2143
    assert r1.total_rounded == D("2143")


def test_tier_boundaries_300_and_400(official_config):
    """Kiểm tra ranh giới bậc 4 (300 kWh) và bậc 5 (400 kWh)."""
    # 300 kWh: 50 + 50 + 100 + 100 = 4 bậc
    r300 = calculate_tiered_electricity("300", 4, official_config)
    assert len(r300.breakdown) == 4
    assert r300.breakdown[3].consumption == D("100")
    assert r300.breakdown[3].unit_price == D("2998")

    # 400 kWh: 50 + 50 + 100 + 100 + 100 = 5 bậc
    r400 = calculate_tiered_electricity("400", 4, official_config)
    assert len(r400.breakdown) == 5
    assert r400.breakdown[4].consumption == D("100")
    assert r400.breakdown[4].unit_price == D("3350")