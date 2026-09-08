# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử tầng Repositories với CSDL."""

import pytest
from app.db.models import Property, Room, MeterReading, TariffConfig, Invoice
from app.db.repositories import (
    PropertyRepository,
    RoomRepository,
    MeterReadingRepository,
    TariffConfigRepository,
    InvoiceRepository,
)
from app.db.session import SessionLocal


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_property_repository_crud(db):
    repo = PropertyRepository(db)
    prop = Property(name="Khu trọ Test", address="123 Test St")
    saved = repo.create(prop)
    assert saved.id is not None
    assert saved.name == "Khu trọ Test"

    found = repo.get(saved.id)
    assert found is not None
    assert found.name == "Khu trọ Test"

    saved.name = "Khu trọ Test Updated"
    repo.update(saved)
    assert repo.get(saved.id).name == "Khu trọ Test Updated"

    deleted = repo.delete(saved.id)
    assert deleted is True
    assert repo.get(saved.id) is None


def test_tariff_config_repository(db):
    repo = TariffConfigRepository(db)
    active = repo.get_active()
    assert active is not None
    assert "tiers" in active.electricity_config
    all_configs = repo.list_all()
    assert len(all_configs) >= 1