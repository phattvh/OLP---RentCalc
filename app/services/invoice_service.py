# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service quản lý hóa đơn và đối chiếu thực thu."""

from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.comparison import compare_with_actual
from app.core.decimal_utils import to_decimal
from app.db.models import Invoice
from app.db.repositories.invoice_repo import InvoiceRepository
from app.services.calculation_service import CalculationService


class InvoiceService:
    """Quản lý các thao tác hóa đơn và ghi nhận số tiền chủ nhà thực thu."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = InvoiceRepository(session)
        self.calc_service = CalculationService(session)

    def generate(self, room_id: int, month: str) -> Invoice:
        return self.calc_service.generate_invoice(room_id, month)

    def get(self, invoice_id: int) -> Invoice | None:
        return self.repo.get(invoice_id)

    def update_actual_collected(
        self, invoice_id: int, actual_collected_str: str
    ) -> Invoice:
        """Ghi nhận tiền thực thu và tính chênh lệch so với quy định."""
        invoice = self.repo.get(invoice_id)
        if not invoice:
            raise ValueError(f"Không tìm thấy hóa đơn ID {invoice_id}")

        actual = to_decimal(actual_collected_str)
        comparison = compare_with_actual(
            actual_collected=actual,
            regulated_total=invoice.invoice_total_final,
        )

        invoice.actual_collected = comparison.actual_collected
        invoice.difference = comparison.difference
        self.session.commit()
        self.session.refresh(invoice)
        return invoice