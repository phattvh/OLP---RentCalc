# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Router quản lý xác thực đăng nhập / đăng xuất cho chủ nhà và người thuê."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth import get_current_user_optional, require_tenant, verify_password
from app.db.repositories.invoice_repo import InvoiceRepository

from app.auth import get_current_user_optional, verify_password
from app.db.models import User
from app.db.session import get_db
from app.web.templates import templates

router = APIRouter(tags=["auth"])


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: User | None = Depends(get_current_user_optional)):
    if user:
        return RedirectResponse("/my-invoices" if user.role == "tenant" else "/", status_code=303)
    return templates.TemplateResponse(
        request=request, name="auth/login.html.j2", context={"error": None}
    )


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    stmt = select(User).where(User.username == username.strip())
    user = db.scalars(stmt).first()

    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html.j2",
            context={"error": "Tên đăng nhập hoặc mật khẩu không chính xác!"},
            status_code=400,
        )

    # Đăng nhập thành công -> điều hướng theo vai trò
    redirect_url = "/my-invoices" if user.role == "tenant" else "/"
    response = RedirectResponse(redirect_url, status_code=303)
    response.set_cookie("user_id", str(user.id), httponly=True, samesite="lax")
    return response


@router.get("/logout")
@router.post("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user_id")
    return response

@router.get("/my-invoices", response_class=HTMLResponse)
def my_invoices(
    request: Request,
    user: User = Depends(require_tenant),
    db: Session = Depends(get_db),
):
    """Trang xem danh sách hóa đơn dành riêng cho Người thuê phòng."""
    repo = InvoiceRepository(db)
    invoices = repo.list_by_room(user.room_id) if user.room_id else []
    
    return templates.TemplateResponse(
        request=request,
        name="tenant/invoices.html.j2",
        context={
            "user": user,
            "invoices": invoices,
        },
    )