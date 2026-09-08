# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Repository thao tác dữ liệu cơ sở cho thuê."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Property


class PropertyRepository:
    """Quản lý các thao tác truy vấn và lưu trữ cho Property."""

    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Property]:
        stmt = select(Property).order_by(Property.name)
        return list(self.session.scalars(stmt).all())

    def get(self, property_id: int) -> Property | None:
        return self.session.get(Property, property_id)

    def create(self, prop: Property) -> Property:
        self.session.add(prop)
        self.session.commit()
        self.session.refresh(prop)
        return prop

    def update(self, prop: Property) -> Property:
        self.session.commit()
        self.session.refresh(prop)
        return prop

    def delete(self, property_id: int) -> bool:
        prop = self.get(property_id)
        if prop:
            self.session.delete(prop)
            self.session.commit()
            return True
        return False