from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    # TODO (later plan): restrict to customers with is_admin once login exists.
    return render_template("admin/index.html")
