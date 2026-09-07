# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module xử lý chỉ số và tính toán điện năng tiêu thụ qua công tơ cơ khí."""

import re
from decimal import Decimal

from .decimal_utils import to_decimal
from .errors import MeterReadingError


def parse_meter_reading(raw: str | int | Decimal) -> Decimal:
    """Chuẩn hóa và chuyển đổi chỉ số công tơ thành Decimal.

    Quy tắc:
        - Xử lý định dạng phân cách hiển thị công tơ cơ khí (ví dụ '00.120' -> 120, '99.850' -> 99850).
        - Chấp nhận số nguyên không âm.
        - Ném MeterReadingError nếu rỗng, chứa chữ cái, số âm hoặc sai định dạng.
    """
    if isinstance(raw, Decimal):
        if raw < Decimal("0"):
            raise MeterReadingError("Chỉ số công tơ không được là số âm")
        return raw

    s = str(raw).strip()

    if not s:
        raise MeterReadingError("Chỉ số công tơ không được để trống")

    if "," in s:
        raise MeterReadingError("Không hỗ trợ dấu phẩy trong chỉ số công tơ cơ khí")

    if "." in s:
        # Dấu chấm chỉ hợp lệ khi phân cách theo nhóm 3 chữ số (ví dụ: 00.120, 99.850)
        if not re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
            raise MeterReadingError(
                f"Định dạng chỉ số công tơ không hợp lệ: '{s}'. Dấu chấm chỉ dùng phân cách hàng nghìn (ví dụ 00.120 hoặc 99.850)."
            )
        s = s.replace(".", "")

    if not s.isdigit():
        raise MeterReadingError(f"Chỉ số công tơ phải là số nguyên không âm: '{raw}'")

    return to_decimal(s)


def calculate_consumption(
    start_reading: str | int | Decimal,
    end_reading: str | int | Decimal,
    max_value: str | int | Decimal,
) -> Decimal:
    """Tính toán sản lượng tiêu thụ thực tế giữa hai kỳ chỉ số.

    Hỗ trợ cơ chế quay vòng công tơ cơ khí (Rollover):
        - Nếu end >= start: consumption = end - start
        - Nếu end < start (quay vòng qua max_value):
            consumption = (max_value + 1) - start + end
    """
    start = parse_meter_reading(start_reading)
    end = parse_meter_reading(end_reading)
    max_val = to_decimal(max_value)

    if max_val <= Decimal("0"):
        raise MeterReadingError("Giá trị tối đa của công tơ phải lớn hơn 0")

    if end >= start:
        return end - start

    # Xử lý quay vòng công tơ
    rollover_base = max_val + Decimal("1")
    return rollover_base - start + end