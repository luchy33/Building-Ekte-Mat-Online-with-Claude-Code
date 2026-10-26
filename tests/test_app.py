from app.models import EventType, FoodItem
from app.models.repositories import FoodItemRepository


def test_shop_index_lists_food_items(app, client):
    with app.app_context():
        FoodItemRepository().add(FoodItem("Fiskesuppe", "Fish soup", 189, EventType.LUNCH_MEETING))

    response = client.get("/")

    assert response.status_code == 200
    assert b"Fish soup" in response.data
    assert b"189 NOK per person" in response.data
