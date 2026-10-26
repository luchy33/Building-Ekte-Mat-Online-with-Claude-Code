import pytest

from app import create_app
from app.models.repositories.db import init_db
from config import TestConfig


@pytest.fixture
def app(tmp_path):
    app = create_app(TestConfig, DATABASE=str(tmp_path / "test.sqlite"))
    with app.app_context():
        init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
