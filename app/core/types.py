# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Định nghĩa cấu trúc dữ liệu bất biến (immutable dataclasses) cho Core Engine."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

ElectricityMethod = Literal["tiered", "flat_fallback"]
WaterBillingMode = Literal["volume", "per_person"]


@dataclass(frozen=True)
class ElectricityTier:
    """Cấu hình một bậc thang biểu giá điện."""

    number: int
    name: str
    base_quantity: str | None
    unit_price: str


@dataclass(frozen=True)
class ElectricityConfig:
    """Cấu hình tổng thể quy tắc tính tiền điện."""

    vat_rate: str
    people_per_quota: str
    fallback_tier_number: int
    tiers: tuple[ElectricityTier, ...]


@dataclass(frozen=True)
class WaterConfig:
    """Cấu hình quy tắc tính tiền nước."""

    vat_rate: str
    env_fee_rate: str
    volume_unit_price: str
    per_person_unit_price: str


@dataclass(frozen=True)
class MeterConfig:
    """Cấu hình thông số công tơ."""

    max_value: str


@dataclass(frozen=True)
class RentCalcConfig:
    """Cấu hình biểu giá hợp nhất toàn hệ thống."""

    version: str
    electricity: ElectricityConfig
    water: WaterConfig
    meter: MeterConfig


@dataclass(frozen=True)
class ElectricityBreakdownLine:
    """Dòng chi tiết diễn giải sản lượng và thành tiền của một bậc thang điện."""

    tier_number: int
    tier_name: str
    consumption: Decimal
    unit_price: Decimal
    amount: Decimal


@dataclass(frozen=True)
class ElectricityResult:
    """Kết quả tính toán chi phí điện hoàn chỉnh."""

    method: ElectricityMethod
    people_count: int
    quota: Decimal | None
    consumption: Decimal
    subtotal: Decimal
    vat_rate: Decimal
    vat: Decimal
    total_exact: Decimal
    total_rounded: Decimal
    breakdown: tuple[ElectricityBreakdownLine, ...]


@dataclass(frozen=True)
class WaterResult:
    """Kết quả tính toán chi phí nước hoàn chỉnh."""

    mode: WaterBillingMode
    quantity: Decimal
    unit_price: Decimal
    water_before_tax: Decimal
    vat_rate: Decimal
    vat: Decimal
    env_fee_rate: Decimal
    env_fee: Decimal
    total_exact: Decimal
    total_rounded: Decimal


@dataclass(frozen=True)
class ComparisonResult:
    """Kết quả đối chiếu tiền thực tế chủ nhà thu so với quy chuẩn nhà nước."""

    actual_collected: Decimal
    regulated_total: Decimal
    difference: Decimal
    is_overcharged: bool