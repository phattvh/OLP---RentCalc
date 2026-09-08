# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản lý hóa đơn tiền phòng và bóc tách từng bậc lũy tiến."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.repositories.invoice_repo import InvoiceRepository
from app.db.session import get_db
from app.services.calculation_service import CalculationService
from app.services.sharing_service import SharingService
from app.web.templates import templates

router = APIRouter(prefix="/invoices")


@router.get("", response_class=HTMLResponse)
def list_invoices(
    request: Request,
    property_id: int | None = None,
    month: str | None = None,
    db: Session = Depends(get_db),
):
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
    db: Session = Depends(get_db),
):
    service = CalculationService(db)
    invoice = service.generate_invoice(room_id=room_id, month=month.strip())
    return RedirectResponse(f"/invoices/{invoice.id}", status_code=303)


@router.get("/{invoice_id}", response_class=HTMLResponse)
def invoice_detail(invoice_id: int, request: Request, db: Session = Depends(get_db)):
    invoice = InvoiceRepository(db).get(invoice_id)
    if not invoice:
        return RedirectResponse("/invoices", status_code=303)

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