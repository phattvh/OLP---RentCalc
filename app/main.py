# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Điểm khởi chạy ứng dụng FastAPI RentCalc."""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.routers import (
    admin_config,
    comparisons,
    dashboard,
    invoices,
    meter_readings,
    properties,
    rooms,
)

app = FastAPI(
    title="RentCalc",
    description="Ứng dụng minh bạch hóa chi phí dịch vụ thiết yếu (Điện & Nước) nhà trọ",
    version="0.2.0",
)

# Đảm bảo thư mục static tồn tại trước khi mount
os.makedirs("app/static/css", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Đăng ký các routers nghiệp vụ
app.include_router(dashboard.router)
app.include_router(properties.router, prefix="/properties", tags=["properties"])
app.include_router(rooms.router, tags=["rooms"])
app.include_router(meter_readings.router, tags=["meters"])
app.include_router(invoices.router, tags=["invoices"])
app.include_router(admin_config.router, prefix="/admin", tags=["admin"])
app.include_router(comparisons.router, tags=["comparisons"])


@app.get("/health")
def health():
    """Endpoint kiểm tra tình trạng sống của ứng dụng cho Docker và CI/CD."""
    return {"status": "ok", "version": "0.2.0"}