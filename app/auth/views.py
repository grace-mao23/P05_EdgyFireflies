import functools

from flask import (Blueprint, session, redirect, url_for, request, flash,
                   render_template)

from app import db
from app.auth.models import User

bp = Blueprint("auth",
               __name__,
               url_prefix="/auth",
               template_folder="templates")

# Define middlewares
# ---START---


def login_required(view):
    """A view decorator that redirects unauthenticated user to the login in.

    Args:
      view: A Flask view

    Returns:
      A wrapped view that either redirects to the login page or proceed as normal.
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id", None) is None:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


# ---END---


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Logs in a registered user:
        1. Checks the given password as the stored hash.
        2. Adds the user id to the session.
    
    Args:
      None

    Returns:
      A redirect to index or the login page.
    """
    if request.method == "POST":
        username, password = request.form["username"], request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("Username not valid.")
        elif not user.check_password(password):
            flash("Password not valid.")
        else:
            session.clear()
            session["user_id"] = user.user_id
            return redirect(url_for("index"))

    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user:
        1. Validate the email.
        2. Validate the username.
        3. Hashes the password.

    Args:
      None
    
    Returns:
      A redirect to login or the registration page.
    """
    if request.method == "POST":
        email, username, password = request.form["email"], request.form[
            "username"], request.form["password"]

        if not email:
            flash("Email is missing.")
        elif not username:
            flash("Username is missing.")
        elif not password:
            flash("Password is missing.")
        elif db.session.query(
                User.query.filter_by(username=username).exists()).scalar():
            flash(f"{username} already taken.")
        else:
            db.session.add(
                User(email=email, username=username, password=password))
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/logout", methods=["GET"])
def logout():
    """Logs out the user in session.

    Args:
      None

    Returns:
      A redirect to index.
    """
    session.clear()
    return redirect(url_for("index"))
