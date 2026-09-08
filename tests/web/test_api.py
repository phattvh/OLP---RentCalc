# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử các routes Web và API FastAPI."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.2.0"


def test_dashboard_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "RentCalc" in response.text
    assert "Bảng điều khiển tổng quan" in response.text


def test_properties_pages():
    # Danh sách cơ sở
    res_list = client.get("/properties")
    assert res_list.status_code == 200
    assert "Cơ sở cho thuê" in res_list.text

    # Form thêm mới
    res_form = client.get("/properties/new")
    assert res_form.status_code == 200


def test_admin_configs_page():
    res = client.get("/admin/configs")
    assert res.status_code == 200
    assert "Quản lý biểu giá" in res.text


def test_invoices_list_page():
    res = client.get("/invoices")
    assert res.status_code == 200

    res_filtered = client.get("/invoices?property_id=1")
    assert res_filtered.status_code == 200


def test_template_filters():
    from app.web.templates import format_vnd, format_pct
    from decimal import Decimal

    assert format_vnd(None) == "0"
    assert format_vnd(1234567) == "1,234,567"
    assert format_vnd(Decimal("1234567.89")) == "1,234,568"
    assert format_vnd("invalid") == "invalid"

    assert format_pct(None) == "0%"
    assert format_pct(0.08) == "8%"
    assert format_pct(Decimal("0.05")) == "5%"
    assert format_pct("invalid") == "invalid"