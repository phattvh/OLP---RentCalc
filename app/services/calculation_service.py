# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Service tính toán hóa đơn tích hợp app.core và lưu trữ snapshot."""

from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.decimal_utils import to_decimal
from app.core.electricity import (
    calculate_flat_fallback_electricity,
    calculate_tiered_electricity,
)
from app.core.water import calculate_water
from app.db.models import Invoice
from app.db.repositories.invoice_repo import InvoiceRepository
from app.db.repositories.meter_reading_repo import MeterReadingRepository
from app.db.repositories.room_repo import RoomRepository
from app.services.config_service import ConfigService


class CalculationService:
    """Tích hợp Core Engine với CSDL để phát hành hóa đơn phòng."""

    def __init__(self, session: Session):
        self.session = session
        self.config_service = ConfigService(session)
        self.room_repo = RoomRepository(session)
        self.meter_repo = MeterReadingRepository(session)
        self.invoice_repo = InvoiceRepository(session)

    def generate_invoice(
        self, room_id: int, month: str, force_recalculate: bool = False
    ) -> Invoice:
        """Tạo mới hoặc bảo toàn snapshot hóa đơn đã phát hành cho một phòng trong tháng chỉ định."""
        existing = self.invoice_repo.get_by_room_and_month(room_id, month)
        if existing and not force_recalculate:
            # Bảo toàn nguyên vẹn snapshot và biểu giá lịch sử đã chốt, không ghi đè khi đổi tariff
            return existing

        room = self.room_repo.get(room_id)
        if not room:
            raise ValueError(f"Không tìm thấy phòng với ID {room_id}")

        core_config, tariff_model = self.config_service.get_active_config()

        elec_reading = self.meter_repo.get_by_room_month_type(
            room_id, month, "electricity"
        )
        water_reading = self.meter_repo.get_by_room_month_type(
            room_id, month, "water"
        )

        elec_consumption = (
            to_decimal(elec_reading.consumption) if elec_reading else Decimal("0")
        )

        # 1. Tính tiền điện theo luật
        if room.is_declared:
            elec_result = calculate_tiered_electricity(
                consumption=elec_consumption,
                people_count=room.people_count,
                config=core_config,
            )
        else:
            elec_result = calculate_flat_fallback_electricity(
                consumption=elec_consumption,
                config=core_config,
            )

        # 2. Tính tiền nước theo chế độ phòng
        if room.water_billing_mode == "volume":
            water_consumption = (
                to_decimal(water_reading.consumption) if water_reading else Decimal("0")
            )
            water_result = calculate_water(
                mode="volume",
                config=core_config,
                volume=water_consumption,
            )
        else:
            water_people = (
                room.water_people_count
                if room.water_people_count is not None
                else room.people_count
            )
            water_result = calculate_water(
                mode="per_person",
                config=core_config,
                people_count=water_people,
            )

        # 3. Đóng gói kết quả bóc tách từng bậc điện
        breakdown_data = [
            {
                "tier_number": line.tier_number,
                "tier_name": line.tier_name,
                "consumption": str(line.consumption),
                "unit_price": str(line.unit_price),
                "amount": str(line.amount),
            }
            for line in elec_result.breakdown
        ]

        calculation_result = {
            "electricity": {
                "method": elec_result.method,
                "people_count": elec_result.people_count,
                "quota": str(elec_result.quota) if elec_result.quota is not None else None,
                "consumption": str(elec_result.consumption),
                "subtotal": str(elec_result.subtotal),
                "vat_rate": str(elec_result.vat_rate),
                "vat": str(elec_result.vat),
                "total_exact": str(elec_result.total_exact),
                "total_rounded": str(elec_result.total_rounded),
                "breakdown": breakdown_data,
            },
            "water": {
                "mode": water_result.mode,
                "quantity": str(water_result.quantity),
                "unit_price": str(water_result.unit_price),
                "water_before_tax": str(water_result.water_before_tax),
                "vat_rate": str(water_result.vat_rate),
                "vat": str(water_result.vat),
                "env_fee_rate": str(water_result.env_fee_rate),
                "env_fee": str(water_result.env_fee),
                "total_exact": str(water_result.total_exact),
                "total_rounded": str(water_result.total_rounded),
            },
        }

        input_snapshot = {
            "room_name": room.name,
            "people_count": room.people_count,
            "is_declared": room.is_declared,
            "water_billing_mode": room.water_billing_mode,
            "water_people_count": room.water_people_count,
            "electricity_reading": {
                "start": elec_reading.start_reading if elec_reading else "0",
                "end": elec_reading.end_reading if elec_reading else "0",
                "consumption": str(elec_consumption),
            },
            "water_reading": {
                "start": water_reading.start_reading if water_reading else "0",
                "end": water_reading.end_reading if water_reading else "0",
                "consumption": str(water_reading.consumption if water_reading else "0"),
            },
        }

        total_final = elec_result.total_rounded + water_result.total_rounded

        existing = self.invoice_repo.get_by_room_and_month(room_id, month)
        actual = existing.actual_collected if existing else None
        diff = actual - total_final if actual is not None else None

        invoice = Invoice(
            room_id=room_id,
            month=month,
            tariff_config_id=tariff_model.id,
            input_snapshot=input_snapshot,
            calculation_result=calculation_result,
            electricity_total_final=elec_result.total_rounded,
            water_total_final=water_result.total_rounded,
            invoice_total_final=total_final,
            actual_collected=actual,
            difference=diff,
        )

        return self.invoice_repo.create_or_update(invoice)