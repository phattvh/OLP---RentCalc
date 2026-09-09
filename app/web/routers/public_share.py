# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Trang công khai cho người thuê xem hóa đơn qua share_token, không cần đăng nhập."""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.repositories.invoice_repo import InvoiceRepository
from app.db.session import get_db
from app.web.templates import templates

router = APIRouter(prefix="/share", tags=["public"])


@router.get("/{token}", response_class=HTMLResponse)
def view_shared_invoice(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Hiển thị hóa đơn công khai dạng read-only."""
    invoice = InvoiceRepository(db).get_by_share_token(token)
    if not invoice:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn hoặc liên kết không hợp lệ")

    return templates.TemplateResponse(
        request=request,
        name="public/shared_invoice.html.j2",
        context={
            "invoice": invoice,
            "calc": invoice.calculation_result,
            "snap": invoice.input_snapshot,
            "is_public": True,
        },
    )