# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service ghi nhận chỉ số công tơ và tự động tính lượng tiêu thụ."""

from sqlalchemy.orm import Session

from app.core.meter import calculate_consumption
from app.db.models import MeterReading
from app.db.repositories.meter_reading_repo import MeterReadingRepository
from app.services.config_service import ConfigService


class MeterService:
    """Quản lý cập nhật chỉ số công tơ điện và nước."""

    def __init__(self, session: Session):
        self.session = session
        self.config_service = ConfigService(session)
        self.repo = MeterReadingRepository(session)

    def record_reading(
        self,
        room_id: int,
        month: str,
        meter_type: str,
        start_reading: str,
        end_reading: str,
        notes: str | None = None,
    ) -> MeterReading:
        """Validate chỉ số và tính consumption bằng app.core.meter."""
        core_config, _ = self.config_service.get_active_config()
        max_val = core_config.meter.max_value

        consumption = calculate_consumption(
            start=start_reading,
            end=end_reading,
            max_value=max_val,
        )

        reading = MeterReading(
            room_id=room_id,
            month=month,
            meter_type=meter_type,
            start_reading=start_reading,
            end_reading=end_reading,
            consumption=str(consumption),
            max_value=max_val,
            notes=notes,
        )
        return self.repo.create_or_update(reading)