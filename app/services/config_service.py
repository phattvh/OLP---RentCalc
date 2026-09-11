# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service quản lý biểu giá và chuyển đổi cấu hình sang Core Engine."""

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any
from sqlalchemy.orm import Session

from app.core.errors import ConfigError
from app.core.types import (
    ElectricityConfig,
    ElectricityTier,
    MeterConfig,
    RentCalcConfig,
    WaterConfig,
)
from app.db.models import TariffConfig
from app.db.repositories.tariff_config_repo import TariffConfigRepository


def validate_config_payload(
    name: str,
    electricity_config: dict[str, Any],
    water_config: dict[str, Any],
    meter_config: dict[str, Any],
) -> None:
    """Xác thực tính hợp lệ của toàn bộ thông số cấu hình trước khi lưu vào CSDL."""
    if not name or not str(name).strip():
        raise ConfigError("Tên cấu hình biểu giá không được để trống.")

    # 1. Thuế VAT điện
    try:
        vat = Decimal(str(electricity_config.get("vat_rate", "")))
        if not (Decimal("0") <= vat <= Decimal("1")):
            raise ConfigError(f"Thuế suất VAT điện ({vat}) phải nằm trong khoảng từ 0 đến 1.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Thuế suất VAT điện không đúng định dạng số thập phân.")

    # 2. Số người / định mức
    try:
        quota = int(str(electricity_config.get("people_per_quota", "")))
        if quota <= 0:
            raise ConfigError("Số người cho một định mức điện phải lớn hơn 0.")
    except (TypeError, ValueError):
        raise ConfigError("Số người cho một định mức điện phải là số nguyên dương.")

    # 3. Danh sách bậc thang điện
    tiers = electricity_config.get("tiers", [])
    if not tiers or len(tiers) < 1:
        raise ConfigError("Biểu giá điện phải có ít nhất 1 bậc thang.")

    total_tiers = len(tiers)
    for idx, t in enumerate(tiers):
        tier_label = t.get("name") or f"Bậc {idx + 1}"
        is_last = (idx == total_tiers - 1)

        # Đơn giá từng bậc
        try:
            price = Decimal(str(t.get("unit_price", "")))
            if price < Decimal("0"):
                raise ConfigError(f"Đơn giá {tier_label} ({price}) không được là số âm.")
        except (InvalidOperation, TypeError, ValueError):
            raise ConfigError(f"Đơn giá {tier_label} không đúng định dạng số.")

        # Ngưỡng sản lượng cơ sở (base_quantity)
        bq = t.get("base_quantity")
        if is_last:
            if bq is not None and str(bq).strip() and str(bq).strip().lower() not in ("none", "null", "vô hạn"):
                raise ConfigError("Bậc thang cuối cùng phải là bậc vô hạn (không giới hạn sản lượng).")
        else:
            if bq is None or not str(bq).strip() or str(bq).strip().lower() in ("none", "null", "vô hạn"):
                raise ConfigError(f"{tier_label} không phải bậc cuối nên bắt buộc phải có định mức sản lượng cơ sở.")
            try:
                bq_dec = Decimal(str(bq).strip())
                if bq_dec <= Decimal("0"):
                    raise ConfigError(f"Định mức sản lượng của {tier_label} phải là số dương lớn hơn 0.")
            except (InvalidOperation, TypeError, ValueError):
                raise ConfigError(f"Định mức sản lượng của {tier_label} không hợp lệ.")

    # 4. Bậc áp khi không kê khai
    try:
        fallback = int(str(electricity_config.get("fallback_tier_number", "")))
        if not (1 <= fallback <= total_tiers):
            raise ConfigError(
                f"Bậc áp khi không kê khai (Bậc {fallback}) không tồn tại trong danh sách biểu giá (có {total_tiers} bậc)."
            )
    except (TypeError, ValueError):
        raise ConfigError("Bậc áp khi không kê khai phải là số nguyên.")

    # 5. Cấu hình nước sinh hoạt
    try:
        w_vat = Decimal(str(water_config.get("vat_rate", "")))
        if not (Decimal("0") <= w_vat <= Decimal("1")):
            raise ConfigError(f"Thuế suất VAT nước ({w_vat}) phải nằm trong khoảng từ 0 đến 1.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Thuế suất VAT nước không đúng định dạng số thập phân.")

    try:
        w_env = Decimal(str(water_config.get("env_fee_rate", "")))
        if not (Decimal("0") <= w_env <= Decimal("1")):
            raise ConfigError(f"Phí bảo vệ môi trường nước ({w_env}) phải nằm trong khoảng từ 0 đến 1.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Phí BVMT nước không đúng định dạng số thập phân.")

    try:
        w_vol = Decimal(str(water_config.get("volume_unit_price", "")))
        if w_vol < Decimal("0"):
            raise ConfigError("Đơn giá nước theo khối không được là số âm.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Đơn giá nước theo khối không hợp lệ.")

    try:
        w_pp = Decimal(str(water_config.get("per_person_unit_price", "")))
        if w_pp < Decimal("0"):
            raise ConfigError("Đơn giá nước khoán theo người không được là số âm.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Đơn giá nước khoán theo người không hợp lệ.")

    # 6. Thông số công tơ
    try:
        m_max = Decimal(str(meter_config.get("max_value", "99999")))
        if m_max <= Decimal("0"):
            raise ConfigError("Giới hạn chỉ số công tơ (max meter) phải lớn hơn 0.")
    except (InvalidOperation, TypeError, ValueError):
        raise ConfigError("Giới hạn chỉ số công tơ không đúng định dạng số.")


class ConfigService:
    """Điều phối cấu hình biểu giá có kiểm soát phiên bản."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = TariffConfigRepository(session)

    def get_active_tariff(self) -> TariffConfig | None:
        """Lấy bản ghi TariffConfig đang có hiệu lực trong CSDL."""
        return self.repo.get_active()

    def to_core_config(self, tariff: TariffConfig) -> RentCalcConfig:
        """Chuyển đổi dữ liệu JSON trong TariffConfig thành RentCalcConfig của app.core."""
        elec_data = tariff.electricity_config
        water_data = tariff.water_config
        meter_data = tariff.meter_config

        tiers = tuple(
            ElectricityTier(
                number=t["number"],
                name=t["name"],
                base_quantity=str(t["base_quantity"]) if t.get("base_quantity") is not None else None,
                unit_price=str(t["unit_price"]),
            )
            for t in elec_data["tiers"]
        )

        elec_config = ElectricityConfig(
            vat_rate=str(elec_data["vat_rate"]),
            people_per_quota=str(elec_data["people_per_quota"]),
            fallback_tier_number=int(elec_data["fallback_tier_number"]),
            tiers=tiers,
        )

        water_config = WaterConfig(
            vat_rate=str(water_data["vat_rate"]),
            env_fee_rate=str(water_data["env_fee_rate"]),
            volume_unit_price=str(water_data["volume_unit_price"]),
            per_person_unit_price=str(water_data["per_person_unit_price"]),
        )

        meter_config = MeterConfig(max_value=str(meter_data.get("max_value", "99999")))

        return RentCalcConfig(
            version=tariff.name,
            electricity=elec_config,
            water=water_config,
            meter=meter_config,
        )

    def get_active_config(self) -> tuple[RentCalcConfig, TariffConfig]:
        """Trả về cả RentCalcConfig (cho Core) và TariffConfig (cho DB Foreign Key)."""
        tariff = self.get_active_tariff()
        if not tariff:
            raise RuntimeError("Chưa có biểu giá nào được kích hoạt trong hệ thống.")
        return self.to_core_config(tariff), tariff

    def create_config(
        self,
        name: str,
        electricity_config: dict[str, Any],
        water_config: dict[str, Any],
        meter_config: dict[str, Any],
        description: str | None = None,
        is_active: bool = True,
    ) -> TariffConfig:
        """Tạo cấu hình biểu giá mới và kích hoạt sau khi kiểm tra hợp lệ toàn bộ thông số."""
        validate_config_payload(
            name=name,
            electricity_config=electricity_config,
            water_config=water_config,
            meter_config=meter_config,
        )
        config = TariffConfig(
            name=name,
            electricity_config=electricity_config,
            water_config=water_config,
            meter_config=meter_config,
            description=description,
            is_active=is_active,
            effective_from=datetime.now(timezone.utc),
        )
        return self.repo.create(config)

    def list_all(self) -> list[TariffConfig]:
        return self.repo.list_all()