# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router trang chủ Dashboard hiển thị số liệu thống kê tổng quan."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.repositories.property_repo import PropertyRepository
from app.db.repositories.tariff_config_repo import TariffConfigRepository
from app.web.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    prop_repo = PropertyRepository(db)
    config_repo = TariffConfigRepository(db)

    properties = prop_repo.list_all()
    active_config = config_repo.get_active()

    total_rooms = sum(len(p.rooms) for p in properties)

    return templates.TemplateResponse(
        "dashboard/index.html.j2",
        {
            "request": request,
            "properties": properties,
            "total_properties": len(properties),
            "total_rooms": total_rooms,
            "active_config": active_config,
        },
    )