# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản lý hóa đơn tiền phòng và bóc tách từng bậc lũy tiến."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_current_user_optional, require_owner
from app.db.models import User
from app.db.repositories.invoice_repo import InvoiceRepository
from app.db.session import get_db
from app.services.calculation_service import CalculationService
from app.services.pdf_service import render_html_to_pdf
from app.services.sharing_service import SharingService
from app.web.templates import templates

router = APIRouter(prefix="/invoices")


@router.get("", response_class=HTMLResponse)
def list_invoices(
    request: Request,
    property_id: int | None = None,
    month: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role == "tenant":
        return RedirectResponse("/my-invoices", status_code=303)
    if user.role != "owner":
        raise HTTPException(status_code=403, detail="Chỉ chủ cơ sở mới có quyền xem toàn bộ hóa đơn")

    repo = InvoiceRepository(db)
    if property_id is not None:
        invoices = repo.list_by_property(property_id=property_id, month=month)
    else:
        invoices = repo.list_all(month=month)
    return templates.TemplateResponse(
        request=request,
        name="invoices/list.html.j2",
        context={
            "invoices": invoices,
            "selected_property_id": property_id,
            "selected_month": month,
        },
    )


@router.post("/generate", response_class=RedirectResponse)
def generate_invoice(
    room_id: int = Form(...),
    month: str = Form(...),
    _: User = Depends(require_owner),
    db: Session = Depends(get_db),
):
    service = CalculationService(db)
    invoice = service.generate_invoice(room_id=room_id, month=month.strip())
    return RedirectResponse(f"/invoices/{invoice.id}", status_code=303)


@router.get("/{invoice_id}", response_class=HTMLResponse)
def invoice_detail(
    invoice_id: int,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    invoice = InvoiceRepository(db).get(invoice_id)
    if not invoice:
        return RedirectResponse("/invoices" if user.role == "owner" else "/my-invoices", status_code=303)

    if user.role == "tenant" and invoice.room_id != user.room_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền xem hóa đơn của phòng khác")

    sharing_service = SharingService(db)
    share_token = sharing_service.get_or_create_token(invoice_id)

    return templates.TemplateResponse(
        request=request,
        name="invoices/detail.html.j2",
        context={
            "invoice": invoice,
            "share_token": share_token,
            "calc": invoice.calculation_result,
            "snap": invoice.input_snapshot,
        },
    )


@router.get("/{invoice_id}/pdf")
def export_invoice_pdf(
    invoice_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Xuất hóa đơn tiền phòng ra file PDF chính thức (hỗ trợ cả ID số có xác thực và share token công khai)."""
    repo = InvoiceRepository(db)
    user = get_current_user_optional(request, db)

    if invoice_id.isdigit():
        invoice = repo.get(int(invoice_id))
        if not invoice:
            raise HTTPException(status_code=404, detail="Không tìm thấy hóa đơn")
        if not user:
            raise HTTPException(status_code=401, detail="Vui lòng đăng nhập để tải hóa đơn")
        if user.role == "tenant" and invoice.room_id != user.room_id:
            raise HTTPException(status_code=403, detail="Bạn không có quyền tải hóa đơn của phòng khác")
    else:
        # Cho phép truy cập bằng public share token
        invoice = repo.get_by_share_token(invoice_id)
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
        headers={"Content-Disposition": f'attachment; filename="hoa-don-{invoice.month}-phong-{invoice.room_id}.pdf"'},
    )