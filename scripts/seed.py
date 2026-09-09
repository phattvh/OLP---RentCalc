# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Script nạp dữ liệu mẫu ban đầu: Biểu giá chính thức 2026, cơ sở và phòng trọ mẫu."""

import sys
from pathlib import Path

# Thêm thư mục gốc của dự án vào sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, timezone
from app.auth import hash_password
from app.db.models import Property, Room, TariffConfig, User
from app.db.session import SessionLocal


OFFICIAL_ELECTRICITY = {
    "vat_rate": "0.08",
    "people_per_quota": "4",
    "fallback_tier_number": 3,
    "tiers": [
        {"number": 1, "name": "Bậc 1", "base_quantity": "50", "unit_price": "1984"},
        {"number": 2, "name": "Bậc 2", "base_quantity": "50", "unit_price": "2050"},
        {"number": 3, "name": "Bậc 3", "base_quantity": "100", "unit_price": "2380"},
        {"number": 4, "name": "Bậc 4", "base_quantity": "100", "unit_price": "2998"},
        {"number": 5, "name": "Bậc 5", "base_quantity": "100", "unit_price": "3350"},
        {"number": 6, "name": "Bậc 6", "base_quantity": None, "unit_price": "3460"},
    ],
}

OFFICIAL_WATER = {
    "vat_rate": "0.05",
    "env_fee_rate": "0.10",
    "volume_unit_price": "8500",
    "per_person_unit_price": "80000",
}

OFFICIAL_METER = {"max_value": "99999"}


def seed():
    """Khởi tạo cấu hình và dữ liệu mẫu nếu chưa tồn tại."""
    db = SessionLocal()
    try:
        # 1. Nạp biểu giá chính thức
        if db.query(TariffConfig).filter_by(is_active=True).count() == 0:
            config = TariffConfig(
                name="Biểu giá chính thức 2026",
                description="Căn cứ QĐ 1279/QĐ-BCT, TT 60/2025/TT-BCT & NQ 204/2025/QH15",
                electricity_config=OFFICIAL_ELECTRICITY,
                water_config=OFFICIAL_WATER,
                meter_config=OFFICIAL_METER,
                is_active=True,
                effective_from=datetime.now(timezone.utc),
            )
            db.add(config)
            db.commit()
            print("✓ Đã nạp Biểu giá chính thức 2026")

        # 2. Nạp cơ sở mẫu
        prop = db.query(Property).first()
        if not prop:
            prop = Property(
                name="Nhà trọ Mẫu TP.HCM",
                address="280 An Dương Vương, Phường 4, Quận 5, TP.HCM",
                description="Khu trọ sinh viên gần trường Đại học Sư phạm TP.HCM",
            )
            db.add(prop)
            db.commit()
            db.refresh(prop)
            print("✓ Đã nạp Cơ sở mẫu")

        # 3. Nạp 2 phòng trọ mẫu
        if db.query(Room).filter_by(property_id=prop.id).count() == 0:
            r1 = Room(
                property_id=prop.id,
                name="Phòng 101",
                people_count=4,
                water_billing_mode="volume",
                is_declared=True,
                notes="4 sinh viên thuê chung, đã đăng ký tạm trú",
            )
            r2 = Room(
                property_id=prop.id,
                name="Phòng 102",
                people_count=1,
                water_billing_mode="per_person",
                is_declared=False,
                notes="1 người thuê, chưa kê khai tạm trú (áp Bậc 3)",
            )
            db.add_all([r1, r2])
            db.commit()
            print("✓ Đã nạp 2 phòng trọ mẫu (Phòng 101 & 102)")

        # 4. Nạp tài khoản demo phân quyền
        if db.query(User).count() == 0:
            sample_room = db.query(Room).first()
            owner_user = User(
                username="owner",
                password_hash=hash_password("owner123"),
                role="owner",
            )
            tenant_user = User(
                username="tenant101",
                password_hash=hash_password("tenant123"),
                role="tenant",
                room_id=sample_room.id if sample_room else None,
            )
            db.add_all([owner_user, tenant_user])
            db.commit()
            print("✓ Đã nạp tài khoản demo: owner (chủ nhà) & tenant101 (người thuê)")

        print("🎉 Seed dữ liệu thành công hoàn tất!")
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi khi seed dữ liệu: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()