# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử tính nước theo docs/CALCULATION_RULES.md §6."""

from decimal import Decimal as D
import pytest

from app.core.errors import InputError
from app.core.water import calculate_water


def test_water_zero_volume(official_config):
    r = calculate_water(mode="volume", volume="0", config=official_config)
    assert r.water_before_tax == D("0")
    assert r.vat == D("0")
    assert r.env_fee == D("0")
    assert r.total_rounded == D("0")


def test_water_per_person(official_config):
    # 4 người x 80.000 = 320.000 trước thuế
    # VAT 5%: 16.000, Phí BVMT 10%: 32.000 -> Tổng: 368.000
    r = calculate_water(mode="per_person", people_count=4, config=official_config)
    assert r.water_before_tax == D("320000")
    assert r.vat == D("16000")
    assert r.env_fee == D("32000")
    assert r.total_rounded == D("368000")


def test_water_input_errors(official_config):
    with pytest.raises(InputError):
        calculate_water(mode="volume", volume="-1", config=official_config)
    with pytest.raises(InputError):
        calculate_water(mode="volume", volume=None, config=official_config)
    with pytest.raises(InputError):
        calculate_water(mode="per_person", people_count=None, config=official_config)
    with pytest.raises(InputError):
        calculate_water(mode="per_person", people_count=-2, config=official_config)