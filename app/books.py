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
    
    :return: A redirection or render template
    """
    if session.get("user_id", None) is None:
        return render_template("landing.html")

    return redirect(url_for("books.home"))


@bp.route("/home", methods=["GET"])
@login_required
def home():
    """
    Return the home view for a logged in user.

    :param None:
    
    :return: Render template
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
    
    :return: Render template
    """
    books: Union[list, None] = None

    if request.method == "POST":
        books = []

        bookname: Union[str, None] = request.form.get("search_book", None)

        if bookname is None:
            flash("Invalid request.")
            return redirect(url_for("books.browse"))

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

                author: Union[str, None] = ", ".join(
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

                thumbnail: Union[str, None] = book["volumeInfo"][
                    "imageLinks"]["thumbnail"] if book["volumeInfo"].get(
                        "imageLinks",
                        None) and book["volumeInfo"]["imageLinks"].get(
                            "thumbnail") is not None else None

                if book_title is not None and db.session.query(
                        Book.query.filter_by(
                            bookname=book_title).exists()).scalar():
                    fetched_books[i] = Book.query.filter_by(
                        bookname=book_title).first_or_404()
                    continue

                if author is not None and db.session.query(
                        Book.query.filter_by(author=author).exists()).scalar():
                    fetched_books[i] = Book.query.filter_by(
                        author=author).first_or_404()
                    continue

                if isbn is not None and db.session.query(
                        Book.query.filter_by(bookname=isbn).exists()).scalar():
                    fetched_books[i] = Book.query.filter_by(
                        isbn=isbn).first_or_404()
                    continue

                if all(map(lambda x: x is not None,
                           (book_title, author, isbn))):
                    created_book: Book = Book(bookname=book_title,
                                              author=author,
                                              isbn=isbn,
                                              description=description,
                                              categories=categories,
                                              thumbnail=thumbnail)

                    db.session.add(created_book)
                    db.session.commit()

                    fetched_books[i] = created_book

            books += fetched_books
            books = [
                book for book in books
                if book is not None and not isinstance(book, dict)
            ]
            books = list(set(books))
            books = books[:10]

    return render_template("books/browse.html", books=books)


@bp.route("/save", methods=["POST"])
@login_required
def save_book():
    """
    Save a book given its book ID.

    :param: None

    :return: Redirection
    """
    book_id: Union[str, None] = request.form.get("book_id", None)

    if book_id is None:
        flash("Invalid request.")
        return redirect(url_for("index"))

    book: Book = Book.query.filter_by(id=book_id).first_or_404()

    save_book: SavedBook = SavedBook(book_id=book_id,
                                     user_id=session.get("user_id"))

    db.session.add(save_book)
    db.session.commit()

    return redirect(url_for("books.book", id=book_id))


@bp.route("/book/<int:id>", methods=["GET"])
@login_required
def book(id: int):
    """
    See the details of a book.

    :param int id: The book ID

    :return: Render template
    """
    book: Book = Book.query.filter_by(id=id).first_or_404()
    saved_book: SavedBook = SavedBook.query.filter_by(
        book_id=id, user_id=session.get("user_id")).first_or_404()

    bookname: str = book.bookname
    author: list = book.author.split(", ")
    isbn: str = book.isbn
    description: Union[list, None] = book.description
    categories: Union[list, None] = book.categories.split(
        ",") if book.categories != None else None
    thumbnail: Union[str, None] = book.thumbnail
    average_rating: Union[int, None] = book.average_rating

    my_rating: Union[int, None] = saved_book.rating
    my_review: Union[str, None] = saved_book.review

    return render_template("books/book.html",
                           book_id=id,
                           bookname=bookname,
                           author=author,
                           isbn=isbn,
                           description=description,
                           categories=categories,
                           thumbnail=thumbnail,
                           average_rating=average_rating,
                           my_rating=my_rating,
                           my_review=my_review)


@bp.route("/mybooks", methods=["GET"])
@login_required
def my_books():
    """
    Show all the books of a given user.

    :param: None

    :return: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    saved_books: Union[list, None] = SavedBook.query.filter_by(
        user_id=user.id).all()

    books: Union[list, None] = []

    if len(saved_books) == 0 or saved_books is None:
        flash("No saved books found.")
    else:
        for saved_book in saved_books:
            books.append(Book.query.filter_by(id=saved_book.book_id).first())

    return render_template("books/mybooks.html",
                           books=books,
                           saved_books=saved_books)


@bp.route("/book/<int:id>/review", methods=["GET", "POST"])
@login_required
def review(id: int):
    """
    Review a book with a numeric rating and/or written review.

    :param int id: The book ID

    :return: Redirection
    """
    book: Book = Book.query.filter_by(id=id).first_or_404()

    saved_book: SavedBook = SavedBook.query.filter_by(
        book_id=id, user_id=session.get("user_id")).first_or_404()

    bookname: str = book.bookname

    saved_rating: Union[int, None] = saved_book.rating
    saved_review: Union[str, None] = saved_book.review

    if request.method == "POST":
        rating: Union[int, str, None] = request.form.get("rating", None)
        review: Union[str, None] = request.form.get("review", None)

        if rating is None or review is None:
            flash("Malformed request.")
        else:
            rating = int(rating)

            saved_book.rating = rating
            saved_book.review = review

            book.average_rating = ((book.average_rating * book.total_ratings) +
                                   rating) / (book.total_ratings + 1)
            book.total_ratings += 1

            db.session.commit()

            return redirect(url_for("books.book", id=id))

    return render_template("books/review.html",
                           bookname=bookname,
                           saved_rating=saved_rating,
                           saved_review=saved_review)


@bp.route("/book/<int:id>/add/reading", methods=["GET"])
@login_required
def add_to_reading_list(id: int):
    """
    Add a book to the user's reading list.

    :param int id: The book ID

    :return: Redirection
    """
    saved_book: SavedBook = SavedBook.query.filter_by(
        book_id=id, user_id=session.get("user_id")).first_or_404()

    saved_book.to_be_read = True

    db.session.commit()

    return redirect(url_for("books.my_books"))


@bp.route("/book/<int:id>/remove/reading", methods=["GET"])
@login_required
def remove_from_reading_list(id: int):
    """
    Remove a book from the user's reading list.

    :param int id: The book ID

    :return: Redirection
    """
    saved_book: SavedBook = SavedBook.query.filter_by(
        book_id=id, user_id=session.get("user_id")).first_or_404()

    saved_book.to_be_read = False

    db.session.commit()

    return redirect(url_for("books.my_books"))
