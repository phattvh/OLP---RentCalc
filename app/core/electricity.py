# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module tính toán chi phí điện sinh hoạt: Biểu giá bậc thang và đồng giá không kê khai."""

from decimal import Decimal

from .decimal_utils import round_vnd, to_decimal
from .errors import ConfigError, InputError
from .quota import calculate_quota
from .types import (
    ElectricityBreakdownLine,
    ElectricityResult,
    RentCalcConfig,
)


def calculate_tiered_electricity(
    consumption: str | int | Decimal,
    people_count: int,
    config: RentCalcConfig,
) -> ElectricityResult:
    """Tính tiền điện sinh hoạt theo biểu giá bậc thang kết hợp số định mức hộ gia đình.

    Căn cứ pháp lý:
        - Quyết định 1279/QĐ-BCT: Biểu giá bán lẻ điện sinh hoạt 6 bậc.
        - Thông tư 60/2025/TT-BCT: Định mức sử dụng điện cho người thuê nhà trọ.
        - Nghị quyết 204/2025/QH15: Thuế suất VAT điện 8%.

    Thuật toán:
        1. Tính định mức Q = people_count / people_per_quota (không làm tròn).
        2. Hạn mức từng bậc: tier_limit = base_quantity * Q (không làm tròn).
        3. Thành tiền từng bậc: amount = tier_consumption * unit_price (không làm tròn).
        4. Tổng tiền trước thuế: subtotal = tổng amount các bậc.
        5. Thuế VAT: vat = subtotal * vat_rate.
        6. Chỉ làm tròn HALF-UP về số nguyên VNĐ ở tổng tiền cuối cùng (total_rounded).
    """
    cons = to_decimal(consumption)
    if cons < Decimal("0"):
        raise InputError(f"Sản lượng điện tiêu thụ không được là số âm: {consumption}")

    if not config.electricity.tiers:
        raise ConfigError("Cấu hình biểu giá điện không có dữ liệu bậc thang")

    quota = calculate_quota(people_count, config.electricity.people_per_quota)

    # Sắp xếp bậc thang tăng dần theo số thứ tự
    sorted_tiers = sorted(config.electricity.tiers, key=lambda t: t.number)

    remaining = cons
    subtotal = Decimal("0")
    breakdown_lines: list[ElectricityBreakdownLine] = []

    for idx, tier in enumerate(sorted_tiers):
        is_last_tier = idx == len(sorted_tiers) - 1

        if tier.base_quantity is None:
            tier_consumption = remaining
        else:
            base_q = to_decimal(tier.base_quantity)
            if base_q <= Decimal("0"):
                raise ConfigError(f"Sản lượng cơ sở của bậc {tier.number} phải lớn hơn 0")

            tier_limit = base_q * quota
            tier_consumption = min(remaining, tier_limit)

        unit_price = to_decimal(tier.unit_price)
        if unit_price < Decimal("0"):
            raise ConfigError(f"Đơn giá của bậc {tier.number} không được là số âm: {tier.unit_price}")

        amount = tier_consumption * unit_price
        subtotal += amount
        remaining -= tier_consumption

        if tier_consumption > Decimal("0"):
            breakdown_lines.append(
                ElectricityBreakdownLine(
                    tier_number=tier.number,
                    tier_name=tier.name,
                    consumption=tier_consumption,
                    unit_price=unit_price,
                    amount=amount,
                )
            )

    if remaining > Decimal("0"):
        raise ConfigError("Cấu hình biểu giá không thể xử lý hết sản lượng còn lại (thiếu bậc vô hạn)")

    vat_rate = to_decimal(config.electricity.vat_rate)
    if vat_rate < Decimal("0"):
        raise ConfigError(f"Thuế suất VAT không được là số âm: {config.electricity.vat_rate}")

    vat = subtotal * vat_rate
    total_exact = subtotal + vat
    total_rounded = round_vnd(total_exact)

    return ElectricityResult(
        method="tiered",
        people_count=people_count,
        quota=quota,
        consumption=cons,
        subtotal=subtotal,
        vat_rate=vat_rate,
        vat=vat,
        total_exact=total_exact,
        total_rounded=total_rounded,
        breakdown=tuple(breakdown_lines),
    )