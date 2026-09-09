# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router trang chủ Dashboard hiển thị số liệu thống kê tổng quan."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.db.models import User
from app.db.repositories.invoice_repo import InvoiceRepository
from app.db.repositories.property_repo import PropertyRepository
from app.db.repositories.tariff_config_repo import TariffConfigRepository
from app.db.session import get_db
from app.web.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_current_user_optional),
):
    if user and user.role == "tenant":
        return RedirectResponse("/my-invoices", status_code=303)
    prop_repo = PropertyRepository(db)
    config_repo = TariffConfigRepository(db)
    inv_repo = InvoiceRepository(db)

    properties = prop_repo.list_all()
    active_config = config_repo.get_active()
    all_invoices = inv_repo.list_all()

    total_rooms = sum(len(p.rooms) for p in properties)
    recent_invoices = all_invoices[:5]
    
    # Thống kê hóa đơn vi phạm quy chuẩn (chủ nhà thu vượt mức)
    overcharge_invoices = [
        inv for inv in all_invoices if inv.difference is not None and inv.difference > 0
    ]

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html.j2",
        context={
            "properties": properties,
            "total_properties": len(properties),
            "total_rooms": total_rooms,
            "total_invoices": len(all_invoices),
            "active_config": active_config,
            "recent_invoices": recent_invoices,
            "overcharge_count": len(overcharge_invoices),
            "overcharge_invoices": overcharge_invoices,
        },
    )