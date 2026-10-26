"""Reset the database and fill it with synthetic data.

Usage: python seed.py
WARNING: drops all tables first. Synthetic data only – no real customers.
"""
import os
import shutil
from datetime import date, timedelta

from app import create_app
from app.models import (Allergen as A, Customer, DeliveryMethod, DietaryLabel as D,
                        EventCategory as E, FoodItem, GuestGroup, Order, OrderLine)
from app.models.repositories import CustomerRepository, FoodItemRepository, OrderRepository
from app.models.repositories.db import init_db

DEV_PASSWORD = "ektemat-dev"

# Lunch dishes follow the autumn menu draft in
# labb_claude_cowork/docs/04_Data/04_reference_lunch-menu-autumn_2026-10-20.txt
FOOD_ITEMS = [
    FoodItem("Fish soup with Bergen cod", "Fiskesuppe med Bergens-torsk", 189,
             {E.LUNCH_MEETING, E.CONFERENCE}, "Root vegetables and sourdough bread.", 10,
             {A.FISH, A.MILK, A.GLUTEN, A.CELERY}),
    FoodItem("Slow-cooked lamb from Voss", "Sakte-kokt lam fra Voss", 245,
             {E.LUNCH_MEETING, E.CONFERENCE, E.CONFIRMATION}, "Served with barley risotto.", 10,
             {A.MILK, A.GLUTEN, A.CELERY}),
    FoodItem("Beetroot and chickpea salad", "Rødbete- og kikertsalat", 165,
             {E.LUNCH_MEETING, E.CONFERENCE, E.BIRTHDAY}, "With goat cheese from Hardanger.", 8,
             {A.MILK, A.MUSTARD}, {D.VEGETARIAN, D.GLUTEN_FREE}),
    FoodItem("Rakfisk tasting", "Rakfisk-smaking", 210,
             {E.CHRISTMAS_PARTY}, "Seasonal, November only.", 12, {A.FISH, A.MILK}),
    FoodItem("Pinnekjøtt Christmas dinner", "Pinnekjøtt med kålrabistappe", 395,
             {E.CHRISTMAS_PARTY}, "Salted, dried lamb ribs with swede mash and potatoes.", 15,
             {A.MILK, A.CELERY}, {D.GLUTEN_FREE}),
    FoodItem("Tapas platter", "Tapasbord", 225,
             {E.BIRTHDAY, E.CONFIRMATION, E.OTHER}, "Cured meats, cheeses, olives and bread.", 10,
             {A.MILK, A.GLUTEN, A.NUTS}),
    FoodItem("Three-course wedding dinner", "Treretters bryllupsmiddag", 695,
             {E.WEDDING}, "Starter, main course with local lamb or fish, and dessert.", 30,
             {A.FISH, A.MILK, A.GLUTEN, A.NUTS, A.EGGS}),
    FoodItem("Kransekake (almond ring cake)", "Kransekake", 95,
             {E.WEDDING, E.CONFIRMATION}, "Traditional almond cake, serves one per portion.", 20,
             {A.NUTS, A.EGGS}, {D.GLUTEN_FREE, D.LACTOSE_FREE}),
    FoodItem("Coffee and cake", "Kaffe og kake", 85,
             {E.BIRTHDAY, E.CONFIRMATION, E.CONFERENCE, E.OTHER}, "Coffee, tea and homemade cake.", 10,
             {A.MILK, A.GLUTEN, A.EGGS}, {D.VEGETARIAN}),
    FoodItem("Vegan lentil stew", "Vegansk linsegryte", 155,
             {E.LUNCH_MEETING, E.CONFERENCE}, "Draft dish – not yet on the menu.", 10,
             set(), {D.VEGAN, D.VEGETARIAN, D.GLUTEN_FREE, D.LACTOSE_FREE}, published=False),
]


def main() -> None:
    password = os.environ.get("SEED_PASSWORD")
    if not password:
        password = DEV_PASSWORD
        print(f"SEED_PASSWORD not set – using the dev default '{DEV_PASSWORD}'.")

    app = create_app()
    with app.app_context():
        print(f"Resetting database at {app.config['DATABASE']} (all data and uploaded images are deleted).")
        init_db()
        shutil.rmtree(app.config["UPLOAD_FOLDER"], ignore_errors=True)  # images belonged to the old data

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
            event_type=E.LUNCH_MEETING,
            event_date=date.today() + timedelta(days=14),
            delivery_method=DeliveryMethod.DELIVERY,
            delivery_address="Testgaten 1, 5003 Bergen",
            guest_groups=[GuestGroup(10, "Main group"),
                          GuestGroup(2, "Gluten-free", diet_notes="gluten")],
            lines=[OrderLine(soup.id, 10, soup.price_nok),
                   OrderLine(lamb.id, 10, lamb.price_nok)],
        ))

    print(f"Seeded {len(FOOD_ITEMS)} food items (1 unpublished), 3 customers (1 admin) and 1 sample order.")


if __name__ == "__main__":
    main()
