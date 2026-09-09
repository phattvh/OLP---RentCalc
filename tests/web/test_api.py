# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Kiểm thử các routes Web và API FastAPI với xác thực signed cookie và phân quyền RBAC."""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from app.auth import (
    hash_password,
    require_owner,
    require_tenant,
    sign_user_id,
    verify_password,
    verify_signed_user_id,
)
from app.db.models import Room, User
from app.db.session import SessionLocal
from app.main import app
from app.services.calculation_service import CalculationService
from app.services.pdf_service import render_html_to_pdf
from app.services.sharing_service import SharingService
from app.web.templates import format_pct, format_vnd

client = TestClient(app)


def get_auth_cookies(role: str = "owner") -> dict:
    """Tạo signed cookie hợp lệ cho vai trò owner hoặc tenant."""
    db = SessionLocal()
    user = db.query(User).filter_by(role=role).first()
    db.close()
    assert user is not None
    return {"user_id": sign_user_id(user.id)}


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_dashboard_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "RentCalc" in response.text
    assert "Bảng điều khiển" in response.text


def test_properties_pages():
    cookies = get_auth_cookies("owner")
    # Danh sách cơ sở
    res_list = client.get("/properties", cookies=cookies)
    assert res_list.status_code == 200
    assert "Cơ sở cho thuê" in res_list.text

    # Form thêm mới
    res_form = client.get("/properties/new", cookies=cookies)
    assert res_form.status_code == 200


def test_admin_configs_page():
    cookies = get_auth_cookies("owner")
    res = client.get("/admin/configs", cookies=cookies)
    assert res.status_code == 200
    assert "Quản lý biểu giá" in res.text


def test_create_custom_five_tier_config():
    """Kiểm thử cấu hình biểu giá động 5 bậc từ UI (không bị giới hạn 6 bậc)."""
    cookies = get_auth_cookies("owner")
    res = client.post(
        "/admin/configs",
        data=[
            ("name", "Biểu giá 5 bậc thử nghiệm"),
            ("description", "Dự thảo biểu giá điện 5 bậc"),
            ("vat_rate", "0.08"),
            ("people_per_quota", "4"),
            ("fallback_tier_number", "3"),
            ("tier_qty", "100"),
            ("tier_price", "1806"),
            ("tier_name", "Bậc 1"),
            ("tier_qty", "100"),
            ("tier_price", "2167"),
            ("tier_name", "Bậc 2"),
            ("tier_qty", "200"),
            ("tier_price", "2729"),
            ("tier_name", "Bậc 3"),
            ("tier_qty", "300"),
            ("tier_price", "3250"),
            ("tier_name", "Bậc 4"),
            ("tier_qty", ""),
            ("tier_price", "3611"),
            ("tier_name", "Bậc 5"),
            ("water_volume_price", "9000"),
            ("water_person_price", "85000"),
            ("water_vat", "0.05"),
            ("water_env", "0.10"),
            ("meter_max", "999999"),
        ],
        cookies=cookies,
        follow_redirects=False,
    )
    assert res.status_code == 303


def test_invoices_list_page():
    cookies = get_auth_cookies("owner")
    res = client.get("/invoices", cookies=cookies)
    assert res.status_code == 200

    res_filtered = client.get("/invoices?property_id=1", cookies=cookies)
    assert res_filtered.status_code == 200


def test_template_filters():
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
    cookies = get_auth_cookies("owner")
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
        cookies=cookies,
        follow_redirects=False,
    )
    assert response.status_code == 303


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


def test_signed_cookie_verification():
    """Kiểm thử cơ chế ký và xác thực cookie chống giả mạo quyền hạn."""
    user_id = 42
    signed = sign_user_id(user_id)
    assert verify_signed_user_id(signed) == user_id

    # Cookie giả mạo, không có chữ ký hoặc chữ ký sai
    assert verify_signed_user_id(str(user_id)) is None
    assert verify_signed_user_id(f"{user_id}.invalid_signature") is None
    assert verify_signed_user_id("") is None
    assert verify_signed_user_id(None) is None


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

    # 3. Đăng nhập đúng Owner -> redirect về Dashboard và nhận signed cookie
    res_owner = client.post(
        "/login",
        data={"username": "owner", "password": "owner123"},
        follow_redirects=False,
    )
    assert res_owner.status_code == 303
    assert res_owner.headers["location"] == "/"
    cookie_header = res_owner.headers.get("set-cookie", "")
    assert "user_id" in cookie_header

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

    # Đã login với signed cookie của tenant
    res_auth = client.get("/my-invoices", cookies={"user_id": sign_user_id(tenant.id)})
    assert res_auth.status_code == 200
    assert "Hóa đơn tiền phòng của bạn" in res_auth.text


def test_rbac_protection_and_cookie_tampering():
    """Kiểm thử bảo mật RBAC: chặn truy cập không quyền và cookie giả mạo."""
    # 1. Truy cập trang Owner khi chưa đăng nhập -> 401
    assert client.get("/properties").status_code == 401
    assert client.get("/admin/configs").status_code == 401
    assert client.get("/invoices").status_code == 401

    # 2. Giả mạo cookie bằng user_id thô (chưa ký HMAC) -> 401
    db = SessionLocal()
    owner = db.query(User).filter_by(role="owner").first()
    db.close()
    assert owner is not None

    res_tampered = client.get("/properties", cookies={"user_id": str(owner.id)})
    assert res_tampered.status_code == 401

    # 3. Tenant truy cập trang quản trị Owner -> 403 Forbidden
    tenant_cookies = get_auth_cookies("tenant")
    assert client.get("/properties", cookies=tenant_cookies).status_code == 403
    assert client.get("/admin/configs", cookies=tenant_cookies).status_code == 403


def test_pdf_export_and_public_share():
    """Kiểm thử render PDF, trang chia sẻ công khai và link tải PDF."""
    owner_cookies = get_auth_cookies("owner")

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

    # 3. Xem trang chia sẻ công khai (Không cần đăng nhập)
    res_share = client.get(f"/share/{token}")
    assert res_share.status_code == 200
    assert "HÓA ĐƠN TIỀN ĐIỆN NƯỚC MINH BẠCH" in res_share.text

    # Token không tồn tại -> 404
    res_404 = client.get("/share/invalid_token_xyz")
    assert res_404.status_code == 404

    # 4. Tải file PDF từ trang công khai (Không cần đăng nhập)
    res_public_pdf = client.get(f"/share/{token}/pdf")
    assert res_public_pdf.status_code == 200
    assert res_public_pdf.headers["content-type"] == "application/pdf"
    assert res_public_pdf.content.startswith(b"%PDF")

    # 5. Tải file PDF từ trang chủ nhà (Có đăng nhập Owner)
    res_owner_pdf = client.get(f"/invoices/{inv.id}/pdf", cookies=owner_cookies)
    assert res_owner_pdf.status_code == 200
    assert res_owner_pdf.headers["content-type"] == "application/pdf"
    assert res_owner_pdf.content.startswith(b"%PDF")

    # 6. Tải file PDF qua URL /invoices/{token}/pdf với share token
    res_token_pdf = client.get(f"/invoices/{token}/pdf")
    assert res_token_pdf.status_code == 200
    assert res_token_pdf.headers["content-type"] == "application/pdf"
    assert res_token_pdf.content.startswith(b"%PDF")


def test_custom_404_page():
    """Kiểm thử trang báo lỗi 404 tùy biến giao diện."""
    res = client.get("/non-existent-route-random-12345")
    assert res.status_code == 404
    assert "404" in res.text
    assert "Không tìm thấy trang yêu cầu" in res.text


def test_navbar_auth_state():
    """Kiểm thử hiển thị động trên Navbar theo trạng thái đăng nhập."""
    # 1. Chưa đăng nhập: hiện nút Đăng nhập
    res_anon = client.get("/")
    assert res_anon.status_code == 200
    assert "Đăng nhập" in res_anon.text

    # 2. Đăng nhập Chủ trọ: hiện Chủ trọ và nút Đăng xuất
    db = SessionLocal()
    owner = db.query(User).filter_by(username="owner").first()
    tenant = db.query(User).filter_by(username="tenant101").first()
    db.close()

    res_owner = client.get("/", cookies={"user_id": sign_user_id(owner.id)})
    assert res_owner.status_code == 200
    assert "Chủ trọ" in res_owner.text
    assert "Đăng xuất" in res_owner.text

    # 3. Đăng nhập Người thuê: hiện Khách, link Hóa đơn của tôi và nút Đăng xuất
    res_tenant = client.get("/my-invoices", cookies={"user_id": sign_user_id(tenant.id)})
    assert res_tenant.status_code == 200
    assert "Khách" in res_tenant.text
    assert "Hóa đơn của tôi" in res_tenant.text
    assert "Đăng xuất" in res_tenant.text
    assert "Tổng quan" not in res_tenant.text

    # 4. Người thuê vào trang chủ / -> tự động redirect về /my-invoices
    res_tenant_root = client.get("/", cookies={"user_id": sign_user_id(tenant.id)}, follow_redirects=False)
    assert res_tenant_root.status_code == 303
    assert res_tenant_root.headers["location"] == "/my-invoices"


def test_invoice_snapshot_immutability():
    """Kiểm thử tính bất biến của hóa đơn: bảo toàn snapshot lịch sử không bị ghi đè."""
    db = SessionLocal()
    room = db.query(Room).first()
    assert room is not None
    calc = CalculationService(db)

    # 1. Sinh hóa đơn lần đầu cho tháng 2026-12
    inv1 = calc.generate_invoice(room_id=room.id, month="2026-12")
    inv1_id = inv1.id
    inv1_total = inv1.invoice_total_final
    inv1_tariff_id = inv1.tariff_config_id

    # 2. Gọi lại không truyền force_recalculate -> trả về chính hóa đơn đã chốt
    inv2 = calc.generate_invoice(room_id=room.id, month="2026-12")
    assert inv2.id == inv1_id
    assert inv2.invoice_total_final == inv1_total
    assert inv2.tariff_config_id == inv1_tariff_id
    db.close()