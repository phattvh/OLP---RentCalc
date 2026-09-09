# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản trị cấu hình biểu giá điện nước nhà nước."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_owner
from app.db.session import get_db
from app.services.config_service import ConfigService
from app.web.templates import templates

router = APIRouter(dependencies=[Depends(require_owner)])


@router.get("/configs", response_class=HTMLResponse)
def list_configs(request: Request, db: Session = Depends(get_db)):
    service = ConfigService(db)
    configs = service.list_all()
    return templates.TemplateResponse(
        request=request, name="admin/configs/list.html.j2", context={"configs": configs}
    )


@router.get("/configs/new", response_class=HTMLResponse)
def new_config_form(request: Request):
    return templates.TemplateResponse(
        request=request, name="admin/configs/form.html.j2", context={}
    )


@router.post("/configs", response_class=RedirectResponse)
def create_config(
    name: str = Form(...),
    description: str = Form(None),
    vat_rate: str = Form("0.08"),
    people_per_quota: str = Form("4"),
    fallback_tier_number: int = Form(3),
    # Ngưỡng và Giá 6 bậc điện
    t1_qty: str = Form("50"),
    t1_price: str = Form("1984"),
    t2_qty: str = Form("50"),
    t2_price: str = Form("2050"),
    t3_qty: str = Form("100"),
    t3_price: str = Form("2380"),
    t4_qty: str = Form("100"),
    t4_price: str = Form("2998"),
    t5_qty: str = Form("100"),
    t5_price: str = Form("3350"),
    t6_price: str = Form("3460"),
    # Giá nước
    water_vat: str = Form("0.05"),
    water_env: str = Form("0.10"),
    water_volume_price: str = Form("8500"),
    water_person_price: str = Form("80000"),
    # Công tơ
    meter_max: str = Form("99999"),
    db: Session = Depends(get_db),
):
    service = ConfigService(db)

    electricity_config = {
        "vat_rate": vat_rate.strip(),
        "people_per_quota": people_per_quota.strip(),
        "fallback_tier_number": fallback_tier_number,
        "tiers": [
            {"number": 1, "name": "Bậc 1", "base_quantity": t1_qty.strip(), "unit_price": t1_price.strip()},
            {"number": 2, "name": "Bậc 2", "base_quantity": t2_qty.strip(), "unit_price": t2_price.strip()},
            {"number": 3, "name": "Bậc 3", "base_quantity": t3_qty.strip(), "unit_price": t3_price.strip()},
            {"number": 4, "name": "Bậc 4", "base_quantity": t4_qty.strip(), "unit_price": t4_price.strip()},
            {"number": 5, "name": "Bậc 5", "base_quantity": t5_qty.strip(), "unit_price": t5_price.strip()},
            {"number": 6, "name": "Bậc 6", "base_quantity": None, "unit_price": t6_price.strip()},
        ],
    }

    water_config = {
        "vat_rate": water_vat.strip(),
        "env_fee_rate": water_env.strip(),
        "volume_unit_price": water_volume_price.strip(),
        "per_person_unit_price": water_person_price.strip(),
    }

    meter_config = {"max_value": meter_max.strip() or "99999"}

    service.create_config(
        name=name.strip(),
        description=description,
        electricity_config=electricity_config,
        water_config=water_config,
        meter_config=meter_config,
        is_active=True,
    )
    return RedirectResponse("/admin/configs", status_code=303)