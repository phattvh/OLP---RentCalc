# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Hệ thống ngoại lệ phân cấp dành riêng cho Core Engine."""


class RentCalcError(Exception):
    """Ngoại lệ cơ sở cho toàn bộ hệ thống RentCalc."""

    pass


class ConfigError(RentCalcError):
    """Ngoại lệ khi cấu hình biểu giá, thuế suất hoặc hạn mức không hợp lệ."""

    pass


class InputError(RentCalcError):
    """Ngoại lệ khi tham số đầu vào (số người, sản lượng, chỉ số) không hợp lệ."""

    pass


class MeterReadingError(InputError):
    """Ngoại lệ khi chỉ số công tơ không đúng định dạng hoặc vượt quá giá trị tối đa."""

    pass