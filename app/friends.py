from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from typing import Union

from app import db
from .auth import login_required
from .models import Book, SavedBook, User

bp: Blueprint = Blueprint("friends", __name__, url_prefix="/friends")


@bp.route("/profile", methods=["GET"])
@login_required
def profile():
    """
    Return the profile view of a logged in user.

    :param: None
    
    :return: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    username: str = user.username
    display_name: str = user.display_name
    bio: Union[str, None] = user.bio

    saved_books: Union[list, None] = SavedBook.query.filter_by(
        user_id=user.id).all()

    books: Union[list, None] = []

    if len(saved_books) == 0 or saved_books is None:
        flash("No saved books found.")
    else:
        for saved_book in saved_books:
            books.append(Book.query.filter_by(id=saved_book.book_id).first())

    return render_template("friends/profile.html",
                           username=username,
                           display_name=display_name,
                           bio=bio,
                           saved_books=saved_books,
                           books=books)


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

    return render_template("friends/edit.html", bio=bio)