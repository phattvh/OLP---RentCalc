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