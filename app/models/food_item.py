from dataclasses import dataclass
from typing import Optional

from app.models.enums import EventType


@dataclass
class FoodItem:
    """A dish on the menu ("Dish" in the Lab 7 domain model). Prices in NOK per person."""
    name_no: str
    name_en: str
    price_per_person_nok: int
    event_type: EventType
    description: str = ""
    allergens: str = ""  # comma-separated for now, e.g. "fish,gluten"
    image_filename: Optional[str] = None
    active: bool = True
    id: Optional[int] = None

    @property
    def allergen_list(self) -> list[str]:
        return [a.strip() for a in self.allergens.split(",") if a.strip()]
