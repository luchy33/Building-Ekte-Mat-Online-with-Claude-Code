from flask import Blueprint, abort, render_template

from app.controllers.auth import image_response
from app.models import EventCategory, ImageError
from app.models.repositories import FoodItemRepository, ImageStore

bp = Blueprint("shop", __name__)


@bp.route("/")
def index():
    items = FoodItemRepository().list_all(published_only=True)
    menu = {category: [i for i in items if category in i.categories] for category in EventCategory}
    return render_template("shop/index.html", menu=menu)


@bp.route("/images/<filename>")
def image(filename):
    try:
        data = ImageStore().read_food(filename)
    except ImageError:
        abort(404)
    return image_response(data, ImageStore.mime_type(filename))
