# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử đối chiếu thực thu theo docs/CALCULATION_RULES.md §8."""

from decimal import Decimal as D

from app.core.comparison import compare_with_actual


def test_comparison_overcharged():
    # Thực thu 480k, quy định 269.244 -> Thu vượt 210.756
    r = compare_with_actual("480000", "269244")
    assert r.difference == D("210756")
    assert r.is_overcharged is True


def test_comparison_exact_match():
    r = compare_with_actual("269244", "269244")
    assert r.difference == D("0")
    assert r.is_overcharged is False


def test_comparison_undercharged():
    # Chủ nhà thu hỗ trợ 250k < quy định 269.244 -> chênh lệch âm
    r = compare_with_actual("250000", "269244")
    assert r.difference == D("-19244")
    assert r.is_overcharged is False