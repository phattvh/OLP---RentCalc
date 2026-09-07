# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module tính toán chi phí nước sinh hoạt theo khối hoặc theo đầu người."""

from decimal import Decimal

from .decimal_utils import round_vnd, to_decimal
from .errors import ConfigError, InputError
from .types import RentCalcConfig, WaterBillingMode, WaterResult


def calculate_water(
    mode: WaterBillingMode,
    config: RentCalcConfig,
    volume: str | int | Decimal | None = None,
    people_count: int | None = None,
) -> WaterResult:
    """Tính tiền nước sinh hoạt kèm Thuế VAT (5%) và Phí Bảo vệ môi trường nước thải (10%).

    Phương thức tính:
        - Theo khối ('volume'): Dựa trên chỉ số đồng hồ nước (m³).
        - Theo người ('per_person'): Khoán tiền nước theo số nhân khẩu/tháng.

    Quy tắc thuế & phí:
        Cả Thuế VAT và Phí BVMT đều được tính trực tiếp trên tiền nước trước thuế (water_before_tax).
        Không tính phí đè lên phí.
    """
    if mode == "volume":
        if volume is None:
            raise InputError("Phương thức tính nước theo khối yêu cầu nhập sản lượng (volume)")
        quantity = to_decimal(volume)
        if quantity < Decimal("0"):
            raise InputError(f"Khối lượng nước tiêu thụ không được là số âm: {volume}")
        unit_price = to_decimal(config.water.volume_unit_price)

    elif mode == "per_person":
        if people_count is None:
            raise InputError("Phương thức tính nước theo đầu người yêu cầu nhập số người (people_count)")
        if people_count < 0:
            raise InputError(f"Số người tính nước không được là số âm: {people_count}")
        quantity = Decimal(people_count)
        unit_price = to_decimal(config.water.per_person_unit_price)

    else:
        raise InputError(f"Phương thức tính nước không hợp lệ: '{mode}'. Chỉ chấp nhận 'volume' hoặc 'per_person'")

    if unit_price < Decimal("0"):
        raise ConfigError(f"Đơn giá nước không được là số âm: {unit_price}")

    water_before_tax = quantity * unit_price

    vat_rate = to_decimal(config.water.vat_rate)
    env_fee_rate = to_decimal(config.water.env_fee_rate)

    if vat_rate < Decimal("0"):
        raise ConfigError(f"Thuế suất VAT nước không hợp lệ: {vat_rate}")
    if env_fee_rate < Decimal("0"):
        raise ConfigError(f"Tỷ lệ phí BVMT nước không hợp lệ: {env_fee_rate}")

    vat = water_before_tax * vat_rate
    env_fee = water_before_tax * env_fee_rate

    total_exact = water_before_tax + vat + env_fee
    total_rounded = round_vnd(total_exact)

    return WaterResult(
        mode=mode,
        quantity=quantity,
        unit_price=unit_price,
        water_before_tax=water_before_tax,
        vat_rate=vat_rate,
        vat=vat,
        env_fee_rate=env_fee_rate,
        env_fee=env_fee,
        total_exact=total_exact,
        total_rounded=total_rounded,
    )