# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""7 trường hợp kiểm thử công bố kèm đề thi tuyển PMNM 2026.
Không dung sai: mọi assert phải khớp từng đồng."""

from decimal import Decimal as D

from app.core.comparison import compare_with_actual
from app.core.electricity import (
    calculate_flat_fallback_electricity,
    calculate_tiered_electricity,
)
from app.core.meter import calculate_consumption, parse_meter_reading
from app.core.water import calculate_water


def test_tc01_four_people_120_kwh(official_config):
    r = calculate_tiered_electricity("120", 4, official_config)
    assert [(l.tier_number, l.consumption, l.amount) for l in r.breakdown] == [
        (1, D("50"), D("99200")),
        (2, D("50"), D("102500")),
        (3, D("20"), D("47600")),
    ]
    assert r.subtotal == D("249300")
    assert r.vat == D("19944")
    assert r.total_exact == D("269244")
    assert r.total_rounded == D("269244")


def test_tc02_five_people_quota_1_25(official_config):
    r = calculate_tiered_electricity("200", 5, official_config)
    assert r.quota == D("1.25")
    assert [(l.tier_number, l.consumption, l.amount) for l in r.breakdown] == [
        (1, D("62.5"), D("124000")),
        (2, D("62.5"), D("128125")),
        (3, D("75"), D("178500")),
    ]
    assert r.subtotal == D("430625")
    assert r.vat == D("34450")
    assert r.total_rounded == D("465075")


def test_tc03_one_person_rounds_down(official_config):
    r = calculate_tiered_electricity("60", 1, official_config)
    assert [(l.tier_number, l.consumption, l.amount) for l in r.breakdown] == [
        (1, D("12.5"), D("24800")),
        (2, D("12.5"), D("25625")),
        (3, D("25"), D("59500")),
        (4, D("10"), D("29980")),
    ]
    assert r.subtotal == D("139905")
    assert r.vat == D("11192.4")
    assert r.total_exact == D("151097.4")
    assert r.total_rounded == D("151097")


def test_tc04_rollover_five_digit_meter(official_config):
    assert parse_meter_reading("99.850") == D("99850")
    assert parse_meter_reading("00.120") == D("120")
    consumption = calculate_consumption("99.850", "00.120", official_config.meter.max_value)
    assert consumption == D("270")
    r = calculate_tiered_electricity(consumption, 4, official_config)
    assert r.subtotal == D("649560")
    assert r.vat == D("51964.8")
    assert r.total_exact == D("701524.8")
    assert r.total_rounded == D("701525")


def test_tc05_flat_tier3_when_not_declared(official_config):
    r = calculate_flat_fallback_electricity("120", official_config)
    assert r.method == "flat_fallback"
    assert r.subtotal == D("285600")
    assert r.vat == D("22848")
    assert r.total_rounded == D("308448")
    declared = calculate_tiered_electricity("120", 4, official_config)
    assert r.total_rounded - declared.total_rounded == D("39204")


def test_tc06_water_by_volume(official_config):
    r = calculate_water(mode="volume", volume="12", config=official_config)
    assert r.water_before_tax == D("102000")
    assert r.vat == D("5100")
    assert r.env_fee == D("10200")
    assert r.total_exact == D("117300")
    assert r.total_rounded == D("117300")


def test_tc07_overcharge_difference(official_config):
    r = compare_with_actual("480000", "269244")
    assert r.difference == D("210756")
    assert r.is_overcharged is True