# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử tầng Application Services."""

import pytest
from app.db.session import SessionLocal
from app.db.models import Property, Room
from app.services import (
    ConfigService,
    CalculationService,
    MeterService,
    InvoiceService,
    SharingService,
)


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_config_service(db):
    service = ConfigService(db)
    core_config, tariff = service.get_active_config()
    assert tariff is not None
    assert core_config.version == tariff.name
    assert len(core_config.electricity.tiers) == 6


def test_meter_and_calculation_service(db):
    prop = db.query(Property).first()
    room = db.query(Room).filter_by(property_id=prop.id, is_declared=True).first()

    # 1. Ghi nhận chỉ số
    meter_service = MeterService(db)
    r_elec = meter_service.record_reading(
        room_id=room.id,
        month="2026-10",
        meter_type="electricity",
        start_reading="100",
        end_reading="220",
    )
    assert r_elec.consumption == "120"

    r_water = meter_service.record_reading(
        room_id=room.id,
        month="2026-10",
        meter_type="water",
        start_reading="10",
        end_reading="26",
    )
    assert r_water.consumption == "16"

    # 2. Sinh hóa đơn
    calc_service = CalculationService(db)
    invoice = calc_service.generate_invoice(room.id, "2026-10")
    assert invoice.id is not None
    assert invoice.electricity_total_final > 0
    assert invoice.water_total_final > 0
    assert invoice.invoice_total_final == invoice.electricity_total_final + invoice.water_total_final

    # 3. Đối chiếu thực thu
    inv_service = InvoiceService(db)
    updated = inv_service.update_actual_collected(invoice.id, "500000")
    assert updated.actual_collected == 500000
    assert updated.difference is not None

    # 4. Chia sẻ
    sharing_service = SharingService(db)
    token = sharing_service.get_or_create_token(invoice.id)
    assert token is not None
    shared = sharing_service.get_invoice_by_token(token)
    assert shared.id == invoice.id