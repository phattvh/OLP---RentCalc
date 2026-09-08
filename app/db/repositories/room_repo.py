# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Repository thao tác dữ liệu phòng trọ (Room)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Room


class RoomRepository:
    """Quản lý các thao tác truy vấn và lưu trữ cho Room."""

    def __init__(self, session: Session):
        self.session = session

    def list_by_property(self, property_id: int) -> list[Room]:
        stmt = select(Room).where(Room.property_id == property_id).order_by(Room.name)
        return list(self.session.scalars(stmt).all())

    def get(self, room_id: int) -> Room | None:
        return self.session.get(Room, room_id)

    def create(self, room: Room) -> Room:
        self.session.add(room)
        self.session.commit()
        self.session.refresh(room)
        return room

    def update(self, room: Room) -> Room:
        self.session.commit()
        self.session.refresh(room)
        return room

    def delete(self, room_id: int) -> bool:
        room = self.get(room_id)
        if room:
            self.session.delete(room)
            self.session.commit()
            return True
        return False