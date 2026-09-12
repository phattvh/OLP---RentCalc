# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Điểm khởi chạy ứng dụng FastAPI RentCalc."""

import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db.models import User
from app.db.session import SessionLocal
from app.web.templates import templates
from app.web.routers import auth
from app.web.routers import (
    admin_config,
    comparisons,
    dashboard,
    invoices,
    meter_readings,
    properties,
    public_share,
    rooms,
)

app = FastAPI(
    title="RentCalc",
    description="Ứng dụng minh bạch hóa chi phí dịch vụ thiết yếu (Điện & Nước) nhà trọ",
    version="1.0.0",
)

# Đảm bảo thư mục static tồn tại trước khi mount
os.makedirs("app/static/css", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.middleware("http")
async def attach_user_middleware(request: Request, call_next):
    """Middleware gắn thông tin người dùng đang đăng nhập vào request.state.user."""
    from app.auth import verify_signed_user_id
    cookie_val = request.cookies.get("user_id")
    user_id = verify_signed_user_id(cookie_val)
    user = None
    if user_id:
        try:
            with SessionLocal() as db:
                user = db.get(User, user_id)
        except Exception:
            user = None
    request.state.user = user
    return await call_next(request)


# Đăng ký các routers nghiệp vụ
app.include_router(dashboard.router)
app.include_router(properties.router, prefix="/properties", tags=["properties"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(meter_readings.router, tags=["meters"])
app.include_router(invoices.router, tags=["invoices"])
app.include_router(admin_config.router, prefix="/admin", tags=["admin"])
app.include_router(comparisons.router, tags=["comparisons"])
app.include_router(public_share.router)
app.include_router(auth.router)


@app.get("/health")
def health():
    """Endpoint kiểm tra tình trạng sống của ứng dụng cho Docker và CI/CD."""
    return {"status": "ok", "version": "1.0.0"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Bắt lỗi HTTP (như 404, 401) và hiển thị giao diện tùy biến thân thiện."""
    if exc.status_code == 401 and "text/html" in request.headers.get("accept", ""):
        return RedirectResponse("/login", status_code=303)
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request, name="errors/404.html.j2", status_code=404
        )
    return templates.TemplateResponse(
        request=request,
        name="errors/500.html.j2",
        status_code=exc.status_code,
        context={"detail": str(exc.detail)},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Bắt lỗi 500 không xử lý được để tránh lộ traceback hệ thống ra ngoài."""
    return templates.TemplateResponse(
        request=request, name="errors/500.html.j2", status_code=500
    )


