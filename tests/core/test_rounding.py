# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử quy tắc làm tròn nửa lên (HALF_UP) theo docs/CALCULATION_RULES.md §7."""

from decimal import Decimal as D

from app.core.decimal_utils import round_vnd


def test_round_vnd_half_up():
    assert round_vnd(D("151097.4")) == D("151097")  # .4 xuống
    assert round_vnd(D("701524.8")) == D("701525")  # .8 lên
    assert round_vnd(D("123456.5")) == D("123457")  # .5 lên
    assert round_vnd(D("123456.49")) == D("123456")
    assert round_vnd(D("0")) == D("0")
    assert round_vnd(D("0.5")) == D("1")


def test_round_vnd_large_numbers():
    # Số lớn không bị mất độ chính xác
    large = D("9876543210987654321.5")
    expected = D("9876543210987654322")
    assert round_vnd(large) == expected