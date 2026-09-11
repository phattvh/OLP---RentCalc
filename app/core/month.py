# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Hàm xác thực định dạng kỳ tính phí (tháng) theo chuẩn YYYY-MM."""

import re
from app.core.errors import InputError

MONTH_REGEX = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


def validate_month(month: str) -> str:
    """Kiểm tra định dạng tháng theo chuẩn YYYY-MM (từ tháng 01 đến 12).
    
    Hợp lệ: '2026-09', '2026-12'
    Không hợp lệ: '2026-99', 'abc-def', '2026-9', '202609'
    """
    if not month or not isinstance(month, str):
        raise InputError("Kỳ tính phí (tháng) không được để trống.")
    cleaned = month.strip()
    if not MONTH_REGEX.match(cleaned):
        raise InputError(
            f"Định dạng tháng '{month}' không hợp lệ. Phải theo chuẩn YYYY-MM (ví dụ: 2026-09)."
        )
    return cleaned
