# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Repository thao tác dữ liệu cấu hình biểu giá (TariffConfig)."""

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models import TariffConfig


class TariffConfigRepository:
    """Quản lý lưu trữ và kiểm soát phiên bản biểu giá."""

    def __init__(self, session: Session):
        self.session = session

    def get_active(self) -> TariffConfig | None:
        stmt = (
            select(TariffConfig)
            .where(TariffConfig.is_active.is_(True))
            .order_by(TariffConfig.effective_from.desc())
        )
        return self.session.scalars(stmt).first()

    def list_all(self) -> list[TariffConfig]:
        stmt = select(TariffConfig).order_by(TariffConfig.effective_from.desc())
        return list(self.session.scalars(stmt).all())

    def get(self, config_id: int) -> TariffConfig | None:
        return self.session.get(TariffConfig, config_id)

    def deactivate_all(self) -> None:
        stmt = update(TariffConfig).values(is_active=False)
        self.session.execute(stmt)
        self.session.commit()

    def create(self, config: TariffConfig) -> TariffConfig:
        if config.is_active:
            self.deactivate_all()
        self.session.add(config)
        self.session.commit()
        self.session.refresh(config)
        return config

    def set_active(self, config_id: int) -> TariffConfig | None:
        target = self.get(config_id)
        if not target:
            return None
        self.deactivate_all()
        target.is_active = True
        self.session.commit()
        self.session.refresh(target)
        return target