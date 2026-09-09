# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Trang công khai cho người thuê xem hóa đơn qua share_token, không cần đăng nhập."""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.services.pdf_service import render_html_to_pdf
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


@router.get("/{token}/pdf")
def export_shared_invoice_pdf(
    token: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Tải PDF trực tiếp từ liên kết chia sẻ công khai không cần đăng nhập."""
    invoice = InvoiceRepository(db).get_by_share_token(token)
    if not invoice:
        raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn")

    html_content = templates.TemplateResponse(
        request=request,
        name="invoices/pdf_template.html.j2",
        context={
            "invoice": invoice,
            "calc": invoice.calculation_result,
            "snap": invoice.input_snapshot,
        },
    ).body.decode("utf-8")

    pdf_bytes = render_html_to_pdf(html_content)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="hoa-don-minh-bach-{invoice.month}.pdf"'},
    )