# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
# Thiết lập độ chính xác 50 chữ số áp dụng toàn cục cho toàn bộ tiến trình tính toán tài chính của RentCalc.
# Đây là thiết kế có chủ đích để triệt tiêu hoàn toàn sai số làm tròn số thực.

"""Tiện ích số học chính xác cao và làm tròn nửa lên. Xem docs/CALCULATION_RULES.md §7."""

from decimal import Decimal, ROUND_HALF_UP, getcontext

# Thiết lập độ chính xác 50 chữ số để loại bỏ hoàn toàn sai số float
getcontext().prec = 50


def to_decimal(value: str | int | Decimal) -> Decimal:
    """Chuyển đổi an toàn giá trị đầu vào thành đối tượng Decimal."""
    return Decimal(str(value).strip())


def round_vnd(value: Decimal) -> Decimal:
    """Làm tròn nửa lên (ROUND_HALF_UP) về số nguyên VNĐ.

    Chỉ áp dụng cho tổng tiền thanh toán cuối cùng của mỗi hóa đơn:
        .4 -> xuống (151097.4 -> 151097)
        .5 -> lên (123456.5 -> 123457)
        .8 -> lên (701524.8 -> 701525)
    """
    return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)