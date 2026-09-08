# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Repository thao tác dữ liệu chỉ số công tơ (MeterReading)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MeterReading


class MeterReadingRepository:
    """Quản lý lưu trữ và truy vấn chỉ số công tơ điện nước."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_room_month_type(
        self, room_id: int, month: str, meter_type: str
    ) -> MeterReading | None:
        stmt = select(MeterReading).where(
            MeterReading.room_id == room_id,
            MeterReading.month == month,
            MeterReading.meter_type == meter_type,
        )
        return self.session.scalars(stmt).first()

    def list_by_room(self, room_id: int) -> list[MeterReading]:
        stmt = (
            select(MeterReading)
            .where(MeterReading.room_id == room_id)
            .order_by(MeterReading.month.desc())
        )
        return list(self.session.scalars(stmt).all())

    def list_by_room_and_month(self, room_id: int, month: str) -> list[MeterReading]:
        stmt = select(MeterReading).where(
            MeterReading.room_id == room_id, MeterReading.month == month
        )
        return list(self.session.scalars(stmt).all())

    def get(self, reading_id: int) -> MeterReading | None:
        return self.session.get(MeterReading, reading_id)

    def create_or_update(self, reading: MeterReading) -> MeterReading:
        existing = self.get_by_room_month_type(
            reading.room_id, reading.month, reading.meter_type
        )
        if existing:
            existing.start_reading = reading.start_reading
            existing.end_reading = reading.end_reading
            existing.consumption = reading.consumption
            existing.max_value = reading.max_value
            existing.notes = reading.notes
            self.session.commit()
            self.session.refresh(existing)
            return existing
        else:
            self.session.add(reading)
            self.session.commit()
            self.session.refresh(reading)
            return reading

    def delete(self, reading_id: int) -> bool:
        reading = self.get(reading_id)
        if reading:
            self.session.delete(reading)
            self.session.commit()
            return True
        return False