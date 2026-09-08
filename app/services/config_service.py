# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service quản lý biểu giá và chuyển đổi cấu hình sang Core Engine."""

from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session

from app.core.types import (
    ElectricityConfig,
    ElectricityTier,
    MeterConfig,
    RentCalcConfig,
    WaterConfig,
)
from app.db.models import TariffConfig
from app.db.repositories.tariff_config_repo import TariffConfigRepository


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
        """Tạo cấu hình biểu giá mới và kích hoạt."""
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