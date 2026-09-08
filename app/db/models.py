# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Định nghĩa các thực thể CSDL (SQLAlchemy Models) theo kiến trúc MappedAsDataclass."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    """Trả về thời gian UTC hiện tại có múi giờ."""
    return datetime.now(timezone.utc)


class Property(Base):
    """Cơ sở cho thuê (dãy phòng trọ, tòa nhà chung cư mini)."""

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(Text, default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=utc_now,
        onupdate=utc_now,
        init=False,
    )

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )


class Room(Base):
    """Phòng trọ thuộc một cơ sở cho thuê."""

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    name: Mapped[str] = mapped_column(String(255))
    people_count: Mapped[int] = mapped_column(default=0)
    water_billing_mode: Mapped[str] = mapped_column(
        String(20), default="volume"
    )  # 'volume' | 'per_person'
    water_people_count: Mapped[int | None] = mapped_column(default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    is_declared: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=utc_now,
        onupdate=utc_now,
        init=False,
    )

    property: Mapped["Property"] = relationship(
        back_populates="rooms", init=False
    )
    meter_readings: Mapped[list["MeterReading"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
        default_factory=list,
        init=False,
    )


class MeterReading(Base):
    """Chỉ số công tơ điện hoặc nước được ghi nhận theo kỳ tháng."""

    __tablename__ = "meter_readings"
    __table_args__ = (
        UniqueConstraint("room_id", "month", "meter_type", name="uq_room_month_meter_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    month: Mapped[str] = mapped_column(String(7))  # 'YYYY-MM'
    meter_type: Mapped[str] = mapped_column(String(20))  # 'electricity' | 'water'
    start_reading: Mapped[str] = mapped_column(String(20))
    end_reading: Mapped[str] = mapped_column(String(20))
    consumption: Mapped[str] = mapped_column(String(20))
    max_value: Mapped[str] = mapped_column(String(20), default="99999")
    notes: Mapped[str | None] = mapped_column(Text, default=None)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now, init=False
    )

    room: Mapped["Room"] = relationship(
        back_populates="meter_readings", init=False
    )


class TariffConfig(Base):
    """Biểu giá tiền điện, nước và cấu hình công tơ có quản lý phiên bản."""

    __tablename__ = "tariff_configs"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(255))
    electricity_config: Mapped[dict[str, Any]] = mapped_column(JSON)
    water_config: Mapped[dict[str, Any]] = mapped_column(JSON)
    meter_config: Mapped[dict[str, Any]] = mapped_column(JSON)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    is_active: Mapped[bool] = mapped_column(default=True)
    effective_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now, init=False
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="tariff_config", default_factory=list, init=False
    )


class Invoice(Base):
    """Hóa đơn tính tiền chi tiết và đối chiếu thực thu theo tháng."""

    __tablename__ = "invoices"
    __table_args__ = (
        UniqueConstraint("room_id", "month", name="uq_invoice_room_month"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    month: Mapped[str] = mapped_column(String(7))  # 'YYYY-MM'
    tariff_config_id: Mapped[int] = mapped_column(ForeignKey("tariff_configs.id"))
    input_snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)
    calculation_result: Mapped[dict[str, Any]] = mapped_column(JSON)
    electricity_total_final: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    water_total_final: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    invoice_total_final: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    actual_collected: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2), default=None
    )
    difference: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2), default=None
    )
    share_token: Mapped[str | None] = mapped_column(
        String(64), unique=True, default=None
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=utc_now, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=utc_now,
        onupdate=utc_now,
        init=False,
    )

    room: Mapped["Room"] = relationship(
        back_populates="invoices", init=False
    )
    tariff_config: Mapped["TariffConfig"] = relationship(
        back_populates="invoices", init=False
    )