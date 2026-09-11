# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử hàm validate_month cho định dạng kỳ tính phí YYYY-MM."""

import pytest
from app.core.errors import InputError
from app.core.month import validate_month


def test_validate_month_valid():
    """Kiểm thử các định dạng tháng YYYY-MM hợp lệ."""
    assert validate_month("2026-01") == "2026-01"
    assert validate_month("2026-09") == "2026-09"
    assert validate_month("2026-12") == "2026-12"
    assert validate_month("  2026-05  ") == "2026-05"


def test_validate_month_invalid():
    """Kiểm thử chặn các định dạng tháng không hợp lệ."""
    # Tháng ngoài khoảng 01-12
    with pytest.raises(InputError):
        validate_month("2026-13")

    with pytest.raises(InputError):
        validate_month("2026-00")

    with pytest.raises(InputError):
        validate_month("2026-99")

    # Thiếu số 0 ở tháng 1 chữ số
    with pytest.raises(InputError):
        validate_month("2026-9")

    # Sai cấu trúc phân cách
    with pytest.raises(InputError):
        validate_month("202609")

    with pytest.raises(InputError):
        validate_month("abc-def")

    # Giá trị rỗng hoặc None
    with pytest.raises(InputError):
        validate_month("")

    with pytest.raises(InputError):
        validate_month(None)
