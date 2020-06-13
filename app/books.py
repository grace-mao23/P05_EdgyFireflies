import os
import json

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from googleapiclient.discovery import build, Resource
from typing import Union

from app import db, service
from .auth import login_required
from .models import Book, User, SavedBook

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
    Search for a book in the database or through Google Books API.
    Limit the results to only ten entries.

    :param None:
    
    :returns: Render template
    """
    books: Union[list, None] = None

    if request.method == "POST":
        books = []

        bookname: str = request.form["search_book"]

        books += Book.query.filter(Book.bookname.contains(
            bookname.lower())).limit(10).all()

        if len(books) < 10:
            fetched_books: Union[list, None] = None

            fetched_books = service.volumes().list(
                q=f"intitle={bookname}").execute().get("items", None)

            for i, book in enumerate(fetched_books):
                book_title: Union[str, None] = book[
                    "volumeInfo"]["title"] if book["volumeInfo"].get(
                        "title", None) is not None else None

                author: Union[str, None] = ",".join(
                    book["volumeInfo"]["authors"]) if book["volumeInfo"].get(
                        "authors", None) is not None else None

                isbn: Union[str,
                            None] = book["volumeInfo"]["industryIdentifiers"][
                                0]["identifier"] if book["volumeInfo"].get(
                                    "industryIdentifiers", None
                                ) is not None and "ISBN" in book["volumeInfo"][
                                    "industryIdentifiers"][0]["type"] else None

                description: Union[str, None] = book["volumeInfo"].get(
                    "description", None)

                categories: Union[str, None] = ",".join(
                    book["volumeInfo"]
                    ["categories"]) if book["volumeInfo"].get(
                        "categories", None) is not None else None

                possible_book: Union[Book, None] = Book.query.filter_by(
                    isbn=isbn).first() if isbn is not None else None

                if possible_book is None and all(
                        map(lambda x: x is not None,
                            (book_title, author, isbn))):
                    created_book: Book = Book(bookname=book_title,
                                              author=author,
                                              isbn=isbn,
                                              description=description,
                                              categories=categories)

                    db.session.add(created_book)
                    db.session.commit()

                    fetched_books[i] = created_book
                else:
                    fetched_books[i] = possible_book

            books += fetched_books
            books = [book for book in books if book is not None]
            books = list(set(books))
            books = books[:10]

    return render_template("books/browse.html", books=books)


@bp.route("/save", methods=["POST"])
def save_book():
    """
    Save a book given its book ID.

    :param: None

    :return: Redirection
    """
    book_id: str = request.form["book_id"]

    book: Book = Book.query.filter_by(id=book_id).first_or_404()

    save_book: SavedBook = SavedBook(book_id=book_id,
                                     user_id=session.get("user_id"))

    db.session.add(save_book)
    db.session.commit()

    return redirect(url_for("books.book", id=book_id))


@bp.route("/book/<int:id>", methods=["GET"])
def book(id: int):
    """
    See the details of a book.

    :param int id: The book ID

    :returns: Render template
    """
    book: Book = Book.query.filter_by(id=id).first_or_404()

    bookname: str = book.bookname
    author: list = book.author.split(",")
    isbn: str = book.isbn
    description: Union[
        list, None] = book.description if book.description != None else None
    categories: Union[list, None] = book.categories.split(
        ",") if book.categories != None else None

    return render_template("books/book.html",
                           bookname=bookname,
                           author=author,
                           isbn=isbn,
                           description=description,
                           categories=categories)


@bp.route("/mybooks", methods=["GET"])
def my_books():
    """
    Show all the books of a given user.

    :param: None

    :returns: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    saved_books: Union[list, None] = SavedBook.query.filter_by(
        user_id=user.id).all()

    if saved_books is None:
        return redirect(url_for("index"))

    for i, saved_book in enumerate(saved_books):
        saved_books[i] = Book.query.filter_by(id=saved_book.book_id).first()

    return render_template("books/mybooks.html", saved_books=saved_books)
