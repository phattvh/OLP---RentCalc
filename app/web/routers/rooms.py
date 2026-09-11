# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản lý phòng trọ (Rooms)."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_owner
from app.db.models import Room
from app.db.repositories.property_repo import PropertyRepository
from app.db.repositories.room_repo import RoomRepository
from app.db.session import get_db
from app.web.templates import templates

router = APIRouter(dependencies=[Depends(require_owner)])


@router.get("/properties/{property_id}/rooms/new", response_class=HTMLResponse)
def new_room_form(property_id: int, request: Request, db: Session = Depends(get_db)):
    prop = PropertyRepository(db).get(property_id)
    return templates.TemplateResponse(
        request=request, name="rooms/form.html.j2", context={"property": prop, "room": None}
    )


@router.post("/properties/{property_id}/rooms", response_class=RedirectResponse)
def create_room(
    property_id: int,
    name: str = Form(...),
    people_count: int = Form(1),
    water_billing_mode: str = Form("volume"),
    water_people_count: int = Form(None),
    is_declared: bool = Form(True),
    notes: str = Form(None),
    db: Session = Depends(get_db),
):
    repo = RoomRepository(db)
    people_count = max(1, people_count)
    if water_billing_mode not in ("volume", "per_person"):
        water_billing_mode = "volume"
    if water_people_count is not None:
        water_people_count = max(0, water_people_count)

    room = Room(
        property_id=property_id,
        name=name.strip(),
        people_count=people_count,
        water_billing_mode=water_billing_mode,
        water_people_count=water_people_count,
        is_declared=is_declared,
        notes=notes.strip() if notes else None,
    )
    repo.create(room)
    return RedirectResponse(f"/properties/{property_id}", status_code=303)


@router.get("/rooms/{room_id}", response_class=HTMLResponse)
def room_detail(room_id: int, request: Request, db: Session = Depends(get_db)):
    room = RoomRepository(db).get(room_id)
    if not room:
        return RedirectResponse("/properties", status_code=303)
    return templates.TemplateResponse(
        request=request, name="rooms/detail.html.j2", context={"room": room}
    )


@router.post("/rooms/{room_id}/delete", response_class=RedirectResponse)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    room = repo.get(room_id)
    property_id = room.property_id if room else None
    repo.delete(room_id)
    if property_id:
        return RedirectResponse(f"/properties/{property_id}", status_code=303)
    return RedirectResponse("/properties", status_code=303)