"""Reset the database and fill it with synthetic data.

Usage: python seed.py
WARNING: drops all tables first. Synthetic data only – no real customers.
"""
import os
from datetime import date, timedelta

from app import create_app
from app.models import (Customer, DeliveryMethod, EventType, FoodItem, GuestGroup,
                        Order, OrderLine)
from app.models.repositories import CustomerRepository, FoodItemRepository, OrderRepository
from app.models.repositories.db import init_db

DEV_PASSWORD = "ektemat-dev"

# Lunch dishes follow the autumn menu draft in
# labb_claude_cowork/docs/04_Data/04_reference_lunch-menu-autumn_2026-10-20.txt
FOOD_ITEMS = [
    FoodItem("Fiskesuppe med Bergens-torsk", "Fish soup with Bergen cod", 189, EventType.LUNCH_MEETING,
             "Root vegetables and sourdough bread.", "fish,milk,gluten,celery"),
    FoodItem("Sakte-kokt lam fra Voss", "Slow-cooked lamb from Voss", 245, EventType.LUNCH_MEETING,
             "Served with barley risotto.", "milk,gluten,celery"),
    FoodItem("Rødbete- og kikertsalat", "Beetroot and chickpea salad", 165, EventType.LUNCH_MEETING,
             "With goat cheese from Hardanger. Vegetarian.", "milk,mustard"),
    FoodItem("Rakfisk-smaking", "Rakfisk tasting", 210, EventType.PARTY,
             "Seasonal, November only.", "fish,milk"),
    FoodItem("Tapasbord", "Tapas platter", 225, EventType.PARTY,
             "Cured meats, cheeses, olives and bread.", "milk,gluten,nuts"),
    FoodItem("Treretters bryllupsmiddag", "Three-course wedding dinner", 695, EventType.WEDDING_DINNER,
             "Starter, main course with local lamb or fish, and dessert.", "fish,milk,gluten,nuts"),
    FoodItem("Kransekake", "Kransekake (almond ring cake)", 95, EventType.WEDDING_DINNER,
             "Traditional almond cake.", "nuts"),
    FoodItem("Kaffe og kake", "Coffee and cake", 85, EventType.OTHER,
             "Coffee, tea and homemade cake.", "milk,gluten"),
]


def main() -> None:
    password = os.environ.get("SEED_PASSWORD")
    if not password:
        password = DEV_PASSWORD
        print(f"SEED_PASSWORD not set – using the dev default '{DEV_PASSWORD}'.")

    app = create_app()
    with app.app_context():
        print(f"Resetting database at {app.config['DATABASE']} (all data is deleted).")
        init_db()

        food_repo = FoodItemRepository()
        for item in FOOD_ITEMS:
            food_repo.add(item)

        customer_repo = CustomerRepository()
        admin = Customer("Ekte Mat Admin", "admin@ektemat.example", is_admin=True)
        private = Customer("Test Private Customer", "private.customer@example.com", phone="+47 400 00 001")
        corporate = Customer("Test Corporate Customer AS", "lunch@corporate.example.com",
                             customer_type="corporate", organisation_number="999999999",
                             phone="+47 400 00 002")
        for customer in (admin, private, corporate):
            customer.set_password(password)
            customer_repo.add(customer)

        soup, lamb = FOOD_ITEMS[0], FOOD_ITEMS[1]
        OrderRepository().add(Order(
            order_number="EM-0001",
            customer_id=corporate.id,
            event_type=EventType.LUNCH_MEETING,
            event_date=date.today() + timedelta(days=14),
            delivery_method=DeliveryMethod.DELIVERY,
            delivery_address="Testgaten 1, 5003 Bergen",
            guest_groups=[GuestGroup(10, "Main group"),
                          GuestGroup(2, "Gluten-free", diet_notes="gluten")],
            lines=[OrderLine(soup.id, 8, soup.price_per_person_nok),
                   OrderLine(lamb.id, 4, lamb.price_per_person_nok)],
        ))

    print(f"Seeded {len(FOOD_ITEMS)} food items, 3 customers (1 admin) and 1 sample order.")


if __name__ == "__main__":
    main()
