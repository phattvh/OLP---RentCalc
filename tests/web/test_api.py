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

def test_rollover_meter_reading_via_ui():
    """Kiểm thử gửi dữ liệu công tơ quay vòng (end < start) qua web."""
    from app.db.session import SessionLocal
    from app.db.models import Room
    db = SessionLocal()
    room = db.query(Room).first()
    db.close()
    assert room is not None

    # Đầu kỳ 99850, cuối kỳ 120 -> sản lượng qua vòng = (99999 + 1) - 99850 + 120 = 270
    response = client.post(
        f"/rooms/{room.id}/readings",
        data={
            "month": "2026-10",
            "meter_type": "electricity",
            "start_reading": "99850",
            "end_reading": "120",
            "notes": "Kiểm thử công tơ quay vòng",
        },
        follow_redirects=False,
    )
    assert response.status_code == 303
    
import pytest
from app.auth import hash_password, verify_password, require_owner, require_tenant
from app.db.models import User, Room
from app.db.session import SessionLocal
from app.services.calculation_service import CalculationService
from app.services.sharing_service import SharingService
from app.services.pdf_service import render_html_to_pdf


def test_auth_password_hashing():
    """Kiểm thử hàm băm mật khẩu và đối chiếu PBKDF2."""
    pwd = "my_secret_pass_123"
    h = hash_password(pwd)
    assert h != pwd
    assert verify_password(pwd, h) is True
    assert verify_password("wrong_password", h) is False
    assert verify_password(pwd, "invalid_format") is False


def test_auth_role_dependencies():
    """Kiểm thử guard phân quyền require_owner & require_tenant."""
    owner = User(username="test_owner", password_hash="h", role="owner")
    tenant = User(username="test_tenant", password_hash="h", role="tenant")

    assert require_owner(owner) == owner
    with pytest.raises(Exception):
        require_owner(tenant)

    assert require_tenant(tenant) == tenant
    with pytest.raises(Exception):
        require_tenant(owner)


def test_login_and_logout_flow():
    """Kiểm thử luồng đăng nhập đúng/sai và đăng xuất."""
    # 1. GET login page
    res = client.get("/login")
    assert res.status_code == 200
    assert "Đăng nhập hệ thống" in res.text

    # 2. Sai thông tin -> báo lỗi 400
    res_wrong = client.post(
        "/login",
        data={"username": "not_exist_user", "password": "wrong_pass"},
    )
    assert res_wrong.status_code == 400
    assert "không chính xác" in res_wrong.text

    # 3. Đăng nhập đúng Owner -> redirect về Dashboard
    res_owner = client.post(
        "/login",
        data={"username": "owner", "password": "owner123"},
        follow_redirects=False,
    )
    assert res_owner.status_code == 303
    assert res_owner.headers["location"] == "/"
    assert "user_id" in res_owner.headers.get("set-cookie", "")

    # 4. Đăng nhập đúng Tenant -> redirect về trang hóa đơn cá nhân
    res_tenant = client.post(
        "/login",
        data={"username": "tenant101", "password": "tenant123"},
        follow_redirects=False,
    )
    assert res_tenant.status_code == 303
    assert res_tenant.headers["location"] == "/my-invoices"

    # 5. Đăng xuất -> redirect về /login
    res_logout = client.get("/logout", follow_redirects=False)
    assert res_logout.status_code == 303
    assert res_logout.headers["location"] == "/login"


def test_tenant_my_invoices_page():
    """Kiểm thử trang xem hóa đơn của người thuê."""
    db = SessionLocal()
    tenant = db.query(User).filter_by(username="tenant101").first()
    db.close()
    assert tenant is not None

    # Chưa login -> 401
    res_unauth = client.get("/my-invoices")
    assert res_unauth.status_code == 401

    # Đã login với cookie của tenant
    client.cookies.set("user_id", str(tenant.id))
    res_auth = client.get("/my-invoices")
    assert res_auth.status_code == 200
    assert "Hóa đơn tiền phòng của bạn" in res_auth.text
    client.cookies.clear()


def test_pdf_export_and_public_share():
    """Kiểm thử render PDF, trang chia sẻ công khai và link tải PDF."""
    # 1. Test hàm render PDF
    pdf_bytes = render_html_to_pdf("<h1>RentCalc Invoice</h1>")
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")

    # 2. Tạo hóa đơn mẫu và lấy token
    db = SessionLocal()
    room = db.query(Room).first()
    assert room is not None
    inv = CalculationService(db).generate_invoice(room_id=room.id, month="2026-11")
    token = SharingService(db).get_or_create_token(inv.id)
    db.close()

    # 3. Xem trang chia sẻ công khai
    res_share = client.get(f"/share/{token}")
    assert res_share.status_code == 200
    assert "HÓA ĐƠN TIỀN ĐIỆN NƯỚC MINH BẠCH" in res_share.text

    # Token không tồn tại -> 404
    res_404 = client.get("/share/invalid_token_xyz")
    assert res_404.status_code == 404

    # 4. Tải file PDF từ trang công khai
    res_public_pdf = client.get(f"/share/{token}/pdf")
    assert res_public_pdf.status_code == 200
    assert res_public_pdf.headers["content-type"] == "application/pdf"
    assert res_public_pdf.content.startswith(b"%PDF")

    # 5. Tải file PDF từ trang chủ nhà
    res_owner_pdf = client.get(f"/invoices/{inv.id}/pdf")
    assert res_owner_pdf.status_code == 200
    assert res_owner_pdf.headers["content-type"] == "application/pdf"
    assert res_owner_pdf.content.startswith(b"%PDF")