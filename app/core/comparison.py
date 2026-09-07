# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module đối chiếu số tiền chủ nhà thực thu so với biểu giá quy định nhà nước."""

from decimal import Decimal

from .decimal_utils import to_decimal
from .types import ComparisonResult


def compare_with_actual(
    actual_collected: str | int | Decimal,
    regulated_total: str | int | Decimal,
) -> ComparisonResult:
    """Đối chiếu tiền thực tế chủ nhà thu so với số tiền tính đúng quy định.

    Công thức:
        difference = actual_collected - regulated_total
        is_overcharged = difference > 0

    Ý nghĩa pháp lý:
        Căn cứ Nghị định số 133/2026/NĐ-CP, việc chủ nhà trọ thu vượt quá mức quy định
        (difference > 0) là hành vi vi phạm và có nguy cơ bị xử phạt 20–30 triệu đồng kèm hoàn trả.
        Nếu difference <= 0: Chủ nhà thu đúng hoặc thu thấp hơn quy định.
    """
    actual = to_decimal(actual_collected)
    regulated = to_decimal(regulated_total)

    difference = actual - regulated
    is_overcharged = difference > Decimal("0")

    return ComparisonResult(
        actual_collected=actual,
        regulated_total=regulated,
        difference=difference,
        is_overcharged=is_overcharged,
    )