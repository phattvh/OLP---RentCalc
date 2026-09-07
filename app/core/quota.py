# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module tính toán định mức số hộ dùng điện. Xem docs/CALCULATION_RULES.md §4.3.
Căn cứ pháp lý: TT 60/2025/TT-BCT; QĐ 1279/QĐ-BCT."""

from decimal import Decimal

from .decimal_utils import to_decimal
from .errors import ConfigError, InputError


def calculate_quota(
    people_count: int,
    people_per_quota: str | int | Decimal,
) -> Decimal:
    """Tính toán số định mức hộ dùng điện (Quota Q).

    Căn cứ Thông tư số 60/2025/TT-BCT và Quyết định 1279/QĐ-BCT:
        Cứ 4 người thuê nhà trọ được tính là 1 định mức hộ gia đình (Q = people_count / 4).
        Ví dụ:
            1 người -> Q = 0.25
            2 người -> Q = 0.50
            3 người -> Q = 0.75
            4 người -> Q = 1.00
            5 người -> Q = 1.25

    TUYỆT ĐỐI KHÔNG làm tròn số định mức Q để bảo đảm sự công bằng và chính xác.
    """
    if people_count < 0:
        raise InputError(f"Số người không được là số âm: {people_count}")

    denom = to_decimal(people_per_quota)
    if denom <= Decimal("0"):
        raise ConfigError(f"Số người trên một định mức phải lớn hơn 0: {people_per_quota}")

    return Decimal(people_count) / denom