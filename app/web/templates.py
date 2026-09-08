# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Cấu hình Jinja2Templates chia sẻ cho các routers."""

from decimal import Decimal, InvalidOperation
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")


def format_vnd(value: str | int | Decimal | None) -> str:
    """Format số tiền VNĐ với dấu phân cách hàng nghìn, không mất chính xác."""
    if value is None:
        return "0"
    try:
        d = Decimal(str(value))
        return f"{d:,.0f}"
    except (InvalidOperation, ValueError):
        return str(value)


def format_pct(value: str | int | Decimal | None) -> str:
    """Format tỷ lệ phần trăm (vd: 0.08 -> 8%)."""
    if value is None:
        return "0%"
    try:
        d = Decimal(str(value))
        return f"{d:.0%}"
    except (InvalidOperation, ValueError):
        return str(value)


templates.env.filters["vnd"] = format_vnd
templates.env.filters["pct"] = format_pct