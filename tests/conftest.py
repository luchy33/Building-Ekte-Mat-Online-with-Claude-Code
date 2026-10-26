import pytest

from app import create_app
from app.models import Customer, EventCategory, FoodItem
from app.models.repositories import CustomerRepository, FoodItemRepository
from app.models.repositories.db import init_db
from config import TestConfig

PASSWORD = "secret-pass-1"


@pytest.fixture
def app(tmp_path):
    app = create_app(TestConfig, DATABASE=str(tmp_path / "test.sqlite"), UPLOAD_FOLDER=str(tmp_path / "uploads"))
    with app.app_context():
        init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def _add_customer(app, **fields) -> Customer:
    with app.app_context():
        customer = Customer(**fields)
        customer.set_password(PASSWORD)
        return CustomerRepository().add(customer)


@pytest.fixture
def customer(app):
    return _add_customer(app, name="Test Customer", email="customer@example.com")


@pytest.fixture
def admin(app):
    return _add_customer(app, name="Test Admin", email="admin@example.com", is_admin=True)


def login(client, email, password=PASSWORD, **extra):
    return client.post("/account/login", data={"email": email, "password": password, **extra})


@pytest.fixture
def admin_client(client, admin):
    login(client, admin.email)
    return client


@pytest.fixture
def food_item(app):
    with app.app_context():
        return FoodItemRepository().add(FoodItem(
            name_en="Fish soup", name_no="Fiskesuppe", price_nok=189,
            categories={EventCategory.LUNCH_MEETING}, min_order_quantity=10))
