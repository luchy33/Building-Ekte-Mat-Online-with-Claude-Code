from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.controllers.auth import is_safe_next, log_in, log_out, login_required
from app.models import Customer
from app.models.repositories import CustomerRepository

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/")
@login_required
def index():
    return render_template("account/index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    errors, form = [], request.form
    if request.method == "POST":
        customer_type = form.get("customer_type", "private")
        customer = Customer(
            name=form.get("name", "").strip(),
            email=form.get("email", "").strip().lower(),
            phone=form.get("phone", "").strip() or None,
            customer_type=customer_type,
            organisation_number=(form.get("organisation_number", "").replace(" ", "") or None)
            if customer_type == "corporate" else None,
        )
        errors = customer.validate_registration(form.get("password", ""), form.get("confirm_password", ""))
        repo = CustomerRepository()
        if not errors and repo.get_by_email(customer.email):
            errors.append("An account with this e-mail address already exists.")
        if not errors and customer.organisation_number and repo.get_by_organisation_number(customer.organisation_number):
            errors.append("This organisation number is already registered.")
        if not errors:
            customer.set_password(form["password"])
            repo.add(customer)
            log_in(customer)
            flash(f"Welcome, {customer.name}! Your account has been created.", "success")
            return redirect(url_for("account.index"))
    return render_template("account/register.html", errors=errors, form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    next_url = request.values.get("next", "")
    error = None
    if request.method == "POST":
        customer = CustomerRepository().get_by_email(request.form.get("email", "").strip().lower())
        if customer is None or not customer.check_password(request.form.get("password", "")):
            error = "Wrong e-mail address or password."
        else:
            log_in(customer)
            flash(f"Logged in as {customer.name}.", "success")
            if is_safe_next(next_url):
                return redirect(next_url)
            return redirect(url_for("admin.index" if customer.is_admin else "account.index"))
    return render_template("account/login.html", error=error, next_url=next_url,
                           email=request.form.get("email", ""))


@bp.route("/logout", methods=["POST"])
def logout():
    log_out()
    flash("You have been logged out.", "success")
    return redirect(url_for("shop.index"))
