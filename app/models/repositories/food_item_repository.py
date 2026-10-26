from typing import Optional

from app.models.enums import EventType
from app.models.food_item import FoodItem
from app.models.repositories.db import get_db


class FoodItemRepository:
    def add(self, item: FoodItem) -> FoodItem:
        db = get_db()
        cur = db.execute(
            "INSERT INTO food_item (name_no, name_en, description, price_per_person_nok,"
            " event_type, allergens, image_filename, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (item.name_no, item.name_en, item.description, item.price_per_person_nok,
             item.event_type.value, item.allergens, item.image_filename, int(item.active)),
        )
        db.commit()
        item.id = cur.lastrowid
        return item

    def get(self, item_id: int) -> Optional[FoodItem]:
        row = get_db().execute("SELECT * FROM food_item WHERE id = ?", (item_id,)).fetchone()
        return self._to_item(row) if row else None

    def list_all(self, active_only: bool = False) -> list[FoodItem]:
        sql = "SELECT * FROM food_item"
        if active_only:
            sql += " WHERE active = 1"
        rows = get_db().execute(sql + " ORDER BY event_type, name_en").fetchall()
        return [self._to_item(r) for r in rows]

    def list_by_event_type(self, event_type: EventType) -> list[FoodItem]:
        rows = get_db().execute(
            "SELECT * FROM food_item WHERE event_type = ? AND active = 1 ORDER BY name_en",
            (event_type.value,),
        ).fetchall()
        return [self._to_item(r) for r in rows]

    @staticmethod
    def _to_item(row) -> FoodItem:
        return FoodItem(
            id=row["id"],
            name_no=row["name_no"],
            name_en=row["name_en"],
            description=row["description"],
            price_per_person_nok=row["price_per_person_nok"],
            event_type=EventType(row["event_type"]),
            allergens=row["allergens"],
            image_filename=row["image_filename"],
            active=bool(row["active"]),
        )
