# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router ghi nhận chỉ số công tơ điện và nước."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.repositories.room_repo import RoomRepository
from app.db.session import get_db
from app.services.meter_service import MeterService
from app.web.templates import templates

router = APIRouter()


@router.get("/rooms/{room_id}/readings/new", response_class=HTMLResponse)
def new_reading_form(room_id: int, request: Request, db: Session = Depends(get_db)):
    room = RoomRepository(db).get(room_id)
    return templates.TemplateResponse(
        request=request, name="meter_readings/form.html.j2", context={"room": room}
    )


@router.post("/rooms/{room_id}/readings", response_class=RedirectResponse)
def record_reading(
    room_id: int,
    month: str = Form(...),  # YYYY-MM
    meter_type: str = Form(...),  # electricity | water
    start_reading: str = Form(...),
    end_reading: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db),
):
    service = MeterService(db)
    service.record_reading(
        room_id=room_id,
        month=month.strip(),
        meter_type=meter_type.strip(),
        start_reading=start_reading.strip(),
        end_reading=end_reading.strip(),
        notes=notes,
    )
    return RedirectResponse(f"/rooms/{room_id}", status_code=303)