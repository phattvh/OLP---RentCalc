# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Repository thao tác dữ liệu hóa đơn (Invoice)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Invoice, Room


class InvoiceRepository:
    """Quản lý lưu trữ và truy vấn hóa đơn tiền phòng."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_room_and_month(self, room_id: int, month: str) -> Invoice | None:
        stmt = select(Invoice).where(Invoice.room_id == room_id, Invoice.month == month)
        return self.session.scalars(stmt).first()

    def get(self, invoice_id: int) -> Invoice | None:
        return self.session.get(Invoice, invoice_id)

    def get_by_share_token(self, share_token: str) -> Invoice | None:
        stmt = select(Invoice).where(Invoice.share_token == share_token)
        return self.session.scalars(stmt).first()

    def list_by_room(self, room_id: int) -> list[Invoice]:
        stmt = (
            select(Invoice)
            .where(Invoice.room_id == room_id)
            .order_by(Invoice.month.desc())
        )
        return list(self.session.scalars(stmt).all())

    def list_by_property(
        self, property_id: int, month: str | None = None
    ) -> list[Invoice]:
        stmt = (
            select(Invoice)
            .join(Room, Invoice.room_id == Room.id)
            .where(Room.property_id == property_id)
        )
        if month:
            stmt = stmt.where(Invoice.month == month)
        stmt = stmt.order_by(Invoice.month.desc(), Room.name)
        return list(self.session.scalars(stmt).all())

    def create_or_update(self, invoice: Invoice) -> Invoice:
        existing = self.get_by_room_and_month(invoice.room_id, invoice.month)
        if existing:
            existing.tariff_config_id = invoice.tariff_config_id
            existing.input_snapshot = invoice.input_snapshot
            existing.calculation_result = invoice.calculation_result
            existing.electricity_total_final = invoice.electricity_total_final
            existing.water_total_final = invoice.water_total_final
            existing.invoice_total_final = invoice.invoice_total_final
            existing.actual_collected = invoice.actual_collected
            existing.difference = invoice.difference
            if invoice.share_token:
                existing.share_token = invoice.share_token
            self.session.commit()
            self.session.refresh(existing)
            return existing
        else:
            self.session.add(invoice)
            self.session.commit()
            self.session.refresh(invoice)
            return invoice

    def delete(self, invoice_id: int) -> bool:
        inv = self.get(invoice_id)
        if inv:
            self.session.delete(inv)
            self.session.commit()
            return True
        return False