from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from typing import Union

from app import db, service
from .auth import login_required
from .models import Book, User

bp: Blueprint = Blueprint("books", __name__)


@bp.route("/", methods=["GET"])
def index():
    """
    Return the landing view for an unauthenticated user or redirection to /home.
    
    :param None:
    
    :returns: A redirection or render template
    """
    if session.get("user_id", None) is None:
        return render_template("landing.html")

    return redirect(url_for("books.home"))


@bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    """
    Return the home view for a logged in user.

    :param None:
    
    :returns: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    display_name: str = user.display_name

    return render_template("books/home.html", display_name=display_name)


@bp.route("/browse", methods=["GET", "POST"])
@login_required
def browse():
    """
    Return the browse view for a logged in user.
    Search for a book in the database.
    Limit the results to only ten entries.

    :param None:
    
    :returns: Render template
    """
    books: Union[list, None] = None

    if request.method == "POST":
        bookname: str = request.form["search_book"]

        books: list = []
        books.append(Book.query.filter_by(bookname=bookname).first())

        if books[0] is None:
            books.pop(0)
            for token in bookname.split():
                books += Book.query.filter(
                    Book.bookname.contains(token.lower())).all()

            books = books[:10]

    return render_template("books/browse.html", books=books)


@bp.route("/lookup", methods=["GET", "POST"])
def lookup_book():
    """
    Lookup book(s) by a given title.

    :param None:

    :returns: Redirection or render template
    """
    books: Union[list, None] = None

    if request.method == "POST":
        book_title: str = request.form["book_title"]

        books = service.volumes.list(intitle=book_title).execute()

    return render_template("books/lookup.html", books=books)


@bp.route("/add", methods=["POST"])
def add_book():
    """
    Add a book to the database

    :param None:

    :returns: Redirection
    """
    return redirect(url_for("index"))
