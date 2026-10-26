from flask import Blueprint, render_template

from app.models import EventType
from app.models.repositories import FoodItemRepository

bp = Blueprint("shop", __name__)


@bp.route("/")
def index():
    items = FoodItemRepository().list_all(active_only=True)
    menu = {event_type: [i for i in items if i.event_type == event_type] for event_type in EventType}
    return render_template("shop/index.html", menu=menu)
