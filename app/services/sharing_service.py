# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service tạo và kiểm tra token chia sẻ hóa đơn công khai."""

import secrets
from sqlalchemy.orm import Session

from app.db.models import Invoice
from app.db.repositories.invoice_repo import InvoiceRepository


class SharingService:
    """Quản lý chia sẻ hóa đơn qua URL an toàn."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = InvoiceRepository(session)

    def get_or_create_token(self, invoice_id: int) -> str:
        invoice = self.repo.get(invoice_id)
        if not invoice:
            raise ValueError(f"Không tìm thấy hóa đơn ID {invoice_id}")

        if not invoice.share_token:
            invoice.share_token = secrets.token_urlsafe(32)
            self.session.commit()
            self.session.refresh(invoice)
        return invoice.share_token

    def get_invoice_by_token(self, token: str) -> Invoice | None:
        return self.repo.get_by_share_token(token)