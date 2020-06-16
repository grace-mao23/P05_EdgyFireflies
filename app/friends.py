import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_socketio import disconnect
from sqlalchemy import or_, and_
from typing import Union

from app import db
from .auth import login_required
from .models import Book, MessageSession, SavedBook, User

bp: Blueprint = Blueprint("friends", __name__, url_prefix="/friends")


@bp.route("/profile/<int:id>", methods=["GET"])
@login_required
def profile(id: int):
    """
    View a user's profile.

    :param int id: The user ID

    :return: Render template
    """
    user: User = User.query.filter_by(id=id).first_or_404()

    username: str = user.username
    display_name: str = user.display_name
    bio: Union[str, None] = user.bio

    saved_books: Union[list, None] = SavedBook.query.filter_by(
        user_id=user.id).all()

    books: Union[list, None] = []

    if len(saved_books) != 0 or saved_books is not None:
        for saved_book in saved_books:
            books.append(Book.query.filter_by(id=saved_book.book_id).first())

    is_logged_in_user: bool = user.id == session.get("user_id")

    other_user_ids: Union[list, None] = MessageSession.query.filter(
        or_(MessageSession.user_a_id == user.id,
            MessageSession.user_b_id == user.id)).order_by(
                MessageSession.count.desc()).all()[:10]

    for i, other_user_id in enumerate(other_user_ids):
        if other_user_id.user_a_id == user.id:
            other_user_ids[i] = other_user_id.user_b_id
        else:
            other_user_ids[i] = other_user_id.user_a_id

    other_users: list = []

    for other_user_id in other_user_ids:
        other_users.append(User.query.filter_by(id=other_user_id).first())

    return render_template("friends/profile.html",
                           username=username,
                           display_name=display_name,
                           bio=bio,
                           other_users=other_users,
                           saved_books=saved_books,
                           books=books,
                           is_logged_in_user=is_logged_in_user)


@bp.route("/", methods=["GET", "POST"])
@login_required
def edit():
    """
    Edit the user's profile.

    :param: None

    :return: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    bio: Union[str, None] = user.bio

    if request.method == "POST":
        new_bio: Union[str, None] = request.form.get("bio", None)

        if new_bio is None:
            flash("Malformed request.")
        else:
            user.bio = new_bio

            db.session.commit()

            flash("Bio updated.")
            return redirect(
                url_for('friends.profile', id=session.get("user_id")))

    return render_template("friends/edit.html", bio=bio)
