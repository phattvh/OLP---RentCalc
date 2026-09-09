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
async def create_config(
    request: Request,
    db: Session = Depends(get_db),
):
    form_data = await request.form()
    name = str(form_data.get("name", "")).strip()
    description = form_data.get("description")
    if description is not None:
        description = str(description).strip()

    vat_rate = str(form_data.get("vat_rate", "0.08")).strip()
    people_per_quota = str(form_data.get("people_per_quota", "4")).strip()
    fallback_tier_number = int(form_data.get("fallback_tier_number", 3))

    tier_prices = form_data.getlist("tier_price")
    tier_qtys = form_data.getlist("tier_qty")
    tier_names = form_data.getlist("tier_name")

    if tier_prices:
        tiers = []
        total_tiers = len(tier_prices)
        for i in range(total_tiers):
            is_last = (i == total_tiers - 1)
            p = str(tier_prices[i]).strip()
            q = str(tier_qtys[i]).strip() if i < len(tier_qtys) else ""
            tname = str(tier_names[i]).strip() if i < len(tier_names) else f"Bậc {i + 1}"

            tiers.append({
                "number": i + 1,
                "name": tname or f"Bậc {i + 1}",
                "base_quantity": None if (is_last or not q or q.lower() in ("none", "null", "vô hạn")) else q,
                "unit_price": p,
            })
    else:
        # Fallback hỗ trợ các ca kiểm thử hoặc form cũ
        t1_qty = str(form_data.get("t1_qty", "50")).strip()
        t1_price = str(form_data.get("t1_price", "1984")).strip()
        t2_qty = str(form_data.get("t2_qty", "50")).strip()
        t2_price = str(form_data.get("t2_price", "2050")).strip()
        t3_qty = str(form_data.get("t3_qty", "100")).strip()
        t3_price = str(form_data.get("t3_price", "2380")).strip()
        t4_qty = str(form_data.get("t4_qty", "100")).strip()
        t4_price = str(form_data.get("t4_price", "2998")).strip()
        t5_qty = str(form_data.get("t5_qty", "100")).strip()
        t5_price = str(form_data.get("t5_price", "3350")).strip()
        t6_price = str(form_data.get("t6_price", "3460")).strip()

        tiers = [
            {"number": 1, "name": "Bậc 1", "base_quantity": t1_qty, "unit_price": t1_price},
            {"number": 2, "name": "Bậc 2", "base_quantity": t2_qty, "unit_price": t2_price},
            {"number": 3, "name": "Bậc 3", "base_quantity": t3_qty, "unit_price": t3_price},
            {"number": 4, "name": "Bậc 4", "base_quantity": t4_qty, "unit_price": t4_price},
            {"number": 5, "name": "Bậc 5", "base_quantity": t5_qty, "unit_price": t5_price},
            {"number": 6, "name": "Bậc 6", "base_quantity": None, "unit_price": t6_price},
        ]

    water_vat = str(form_data.get("water_vat", "0.05")).strip()
    water_env = str(form_data.get("water_env", "0.10")).strip()
    water_volume_price = str(form_data.get("water_volume_price", "8500")).strip()
    water_person_price = str(form_data.get("water_person_price", "80000")).strip()
    meter_max = str(form_data.get("meter_max", "99999")).strip() or "99999"

    electricity_config = {
        "vat_rate": vat_rate,
        "people_per_quota": people_per_quota,
        "fallback_tier_number": fallback_tier_number,
        "tiers": tiers,
    }

    water_config = {
        "vat_rate": water_vat,
        "env_fee_rate": water_env,
        "volume_unit_price": water_volume_price,
        "per_person_unit_price": water_person_price,
    }

    meter_config = {"max_value": meter_max}

    service = ConfigService(db)
    service.create_config(
        name=name,
        description=description,
        electricity_config=electricity_config,
        water_config=water_config,
        meter_config=meter_config,
        is_active=True,
    )
    return RedirectResponse("/admin/configs", status_code=303)