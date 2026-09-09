# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Module xác thực người dùng và phân quyền theo cookie phiên làm việc."""

import hashlib
import secrets
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.session import get_db


def hash_password(password: str) -> str:
    """Băm mật khẩu sử dụng PBKDF2-HMAC-SHA256 với salt ngẫu nhiên."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )
    return f"{salt}${key.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    """Xác thực mật khẩu đối chiếu với chuỗi hash đã lưu."""
    try:
        salt, key_hex = password_hash.split("$")
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return secrets.compare_digest(key.hex(), key_hex)
    except Exception:
        return False


def get_current_user_optional(
    request: Request, db: Session = Depends(get_db)
) -> User | None:
    """Lấy thông tin người dùng hiện tại từ cookie, nếu chưa đăng nhập trả về None."""
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    try:
        return db.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> User:
    """Yêu cầu bắt buộc người dùng phải đăng nhập."""
    user = get_current_user_optional(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Vui lòng đăng nhập để tiếp tục")
    return user


def require_owner(user: User = Depends(get_current_user)) -> User:
    """Chỉ cho phép tài khoản Chủ cơ sở (owner) truy cập."""
    if user.role != "owner":
        raise HTTPException(status_code=403, detail="Chỉ chủ cơ sở mới có quyền thao tác")
    return user


def require_tenant(user: User = Depends(get_current_user)) -> User:
    """Chỉ cho phép tài khoản Người thuê (tenant) truy cập."""
    if user.role != "tenant":
        raise HTTPException(status_code=403, detail="Chỉ người thuê phòng mới có quyền xem")
    return user