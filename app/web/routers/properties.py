# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản lý cơ sở cho thuê (Properties)."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.db.models import Property
from app.db.repositories.property_repo import PropertyRepository
from app.db.session import get_db
from app.web.templates import templates

router = APIRouter()


@router.get("", response_class=HTMLResponse)
def list_properties(request: Request, db: Session = Depends(get_db)):
    repo = PropertyRepository(db)
    properties = repo.list_all()
    return templates.TemplateResponse(
        "properties/list.html.j2",
        {"request": request, "properties": properties},
    )


@router.get("/new", response_class=HTMLResponse)
def new_property_form(request: Request):
    return templates.TemplateResponse(
        "properties/form.html.j2",
        {"request": request, "property": None},
    )


@router.post("", response_class=RedirectResponse)
def create_property(
    name: str = Form(...),
    address: str = Form(None),
    description: str = Form(None),
    db: Session = Depends(get_db),
):
    repo = PropertyRepository(db)
    prop = Property(name=name.strip(), address=address, description=description)
    repo.create(prop)
    return RedirectResponse("/properties", status_code=303)


@router.get("/{property_id}", response_class=HTMLResponse)
def property_detail(property_id: int, request: Request, db: Session = Depends(get_db)):
    repo = PropertyRepository(db)
    prop = repo.get(property_id)
    if not prop:
        return RedirectResponse("/properties", status_code=303)
    return templates.TemplateResponse(
        "properties/detail.html.j2",
        {"request": request, "property": prop},
    )


@router.post("/{property_id}/delete", response_class=RedirectResponse)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    repo = PropertyRepository(db)
    repo.delete(property_id)
    return RedirectResponse("/properties", status_code=303)