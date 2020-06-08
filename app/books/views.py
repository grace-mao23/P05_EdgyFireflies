from flask import (Blueprint, render_template, request, session, redirect,
                   url_for)

from app import db
from app.auth.views import login_required

bp = Blueprint("books", __name__)


@bp.route("/")
def index():
    """Returns the landing view for an unauthenticated user.

    Args:
      None

    Returns:
      None
    """
    if session.get("user_id", None) is None:
        return render_template("landing.html")

    return redirect(url_for("books.home"))


@bp.route("/home", methods=["GET"])
@login_required
def home():
    """Returns the home view for a logged in user.

    Elements:
      See My Profile (See home.html)
      Browse Books (See home.html)
      Match Potential Friends (See home.html)

    Args:
      None

    Returns:
      A rendered Jinja template.
    """
    return render_template("books/home.html")


@bp.route("/browse", methods=["GET", "POST"])
@login_required
def browse():
    """Returns the browsing view for a logged in user.

    Elements:
      Browse by Title (To be implemented)

    Args:
      None

    Returns:
      A rendered Jinja template.
    """
    if request.method == "POST":
        pass

    return render_template("books/browse.html")


@bp.route("/review/<int:book_id>", methods=["GET"])
@login_required
def get_review(book_id):
    """Returns the book review view for a logged in user.

    Elements:
      Show All Stored Book Info (To be implemented)
      Show Personal Numeric Rating (To be implemented)
      Show Personal Review (To be implemented)
      Show Other Reviews (To be implemented)

    Args:
      book_id: The ID of a book in the database.

    Returns:
      A rendered Jinja template.
    """
    return render_template("books/review.html")


@bp.route("/review/<int:book_id>/update", methods=["POST"])
@login_required
def update_review(book_id):
    """Updates either a book's numeric rating or written review for a logged in user.

    Elements:
      Update Personal Numeric Rating (To be implemented)
      Update Personal Review (To be implemented)

    Args:
      book_id: The ID of a book in the database.

    Returns:
      A rendered Jinja template.
    """
    if request.method == "POST":
        pass

    return render_template("books/review.html")


@bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Updates the current user's settings.

    Updatable:
      Email
      Password

    Args:
      None
    
    Returns:
      A rendered Jinja template.
    """
    if request.method == "POST":
        pass

    return render_template("books/settings.html")
