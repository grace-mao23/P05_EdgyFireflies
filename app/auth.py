import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from typing import Union

from app import db
from .models import User

bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """
    A view decorator that redirects unauthenticated user to the login in.

    :param view: The Flask view

    :returns: A wrapped view or redirection to the login page
    """
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id", None) is None:
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in a registered user:
        1. Checks the given password as the stored hash
        2. Adds the user id to the session

    :param: None

    :returns: A redirection to index or the login page
    """
    if request.method == "POST":
        username: Union[str, None] = request.form.get("username", None)
        password: Union[str, None] = request.form.get("password", None)

        if username is None and password is None:
            flash("Malformed request.")
            return redirect(url_for("index"))

        user: User = User.query.filter_by(username=username).first()

        if user is None:
            flash("Username not valid.")
        elif not user.check_password(password):
            flash("Password not valid.")
        else:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user:
        1. Validate the email
        2. Validate the username
        3. Hashes the password

    :param None:

    :returns: A redirection or render template
    """
    if request.method == "POST":
        username: Union[str, None] = request.form.get("username", None)
        display_name: Union[str, None] = request.form.get("display_name", None)
        password: Union[str, None] = request.form.get("password", None)

        if all(map(lambda x: x is None, (username, display_name, password))):
            flash("Malformed request.")
            return redirect(url_for("index"))

        if not username:
            flash("Username is missing.")
        elif not display_name:
            flash("Display name is missing.")
        elif not password:
            flash("Password is missing.")
        elif db.session.query(
                User.query.filter_by(username=username).exists()).scalar():
            flash(f"{username} already taken.")
        else:
            db.session.add(
                User(username=username,
                     display_name=display_name,
                     password=password))
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Log out the user in session.
    
    :param None:
    
    :returns: A redirect to index
    """
    session.clear()
    return redirect(url_for("index"))


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """
    Update the current user's settings.

    :param None:
    
    :returns: Render template
    """
    if request.method == "POST":
        display_name: Union[str, None] = request.form[
            "display_name"] if request.form["display_name"] != "" else None
        current_password: Union[
            str, None] = request.form["current_password"] if request.form[
                "current_password"] != "" else None
        new_password: Union[str, None] = request.form[
            "new_password"] if request.form["new_password"] != "" else None
        confirm_password: Union[
            str, None] = request.form["confirm_password"] if request.form[
                "confirm_password"] != "" else None

        user: User = User.query.filter_by(id=session.get("user_id")).first()

        if display_name is not None:
            user.display_name = display_name
            db.session.commit()
            flash(f"Display name updated to {display_name}.")

        if all(
                map(lambda x: x is not None,
                    (current_password, new_password, confirm_password))):
            if current_password is None:
                flash("Missing current password.")
            elif new_password is None:
                flash("Missing new password.")
            elif confirm_password is None:
                flash("Missing confirm password.")
            elif new_password != confirm_password:
                flash("Mismatch new passwords.")
            else:
                if user.check_password(current_password):
                    user.password = new_password
                    db.session.commit()
                    flash("Password is updated.")
                else:
                    flash("Failed to update the password.")

    return render_template("auth/settings.html")
