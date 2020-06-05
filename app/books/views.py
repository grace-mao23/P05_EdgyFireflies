from flask import (Blueprint, render_template, request)

from app import db
from app.auth.views import login_required

bp = Blueprint("books",
               __name__,
               url_prefix="/books",
               template_folder="templates",
               static_folder="static")


@bp.route("/home", methods=["GET"])
@login_required
def home():
    """Returns the home view for a logged in user.

    Elements:
      See My Profile (To be implemented)
      Browse Books (To be implemented)
      Match Potential Friends (To be implemented)

    Args:
      None

    Returns:
      A rendered Jinja template.
    """
    return render_template("home.html")


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

    return render_template("browse.html")


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
    return render_template("review.html")


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

    return render_template("review.html")
