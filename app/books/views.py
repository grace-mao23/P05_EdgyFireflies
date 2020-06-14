from flask import (Blueprint, render_template, request, session, redirect,
                   url_for)

from app.books.models import Author, Book

from app import db
from app.auth.views import login_required
from app.forms import SearchForm
from urllib.request import urlopen
import urllib.request as urllib
import json

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

    SEARCH_LIMIT = 100
    PER_ROW = 3

    form = SearchForm()

    full_results = None
    dict = {}
    pics = []

    if form.validate_on_submit():
        #search through Google API
        data = '+'.join(form.search.data.split(' '))

        url = "https://www.googleapis.com/books/v1/volumes?q=" + str(data)
        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        req = urllib.Request(url, headers=hdr)
        books = json.loads(urllib.urlopen(req).read())["items"]

        #loop through queried books
        for i in range(len(books)):
            book = Book.query.filter_by(isbn = isbn).first()
            #if book doesn't exist in the database yet, collect data from APIs
            if book == None:
                #collecting title and author from Google API
                isbn = books[i]['volumeInfo']['industryIdentifiers'][0]['identifier']
                title = books[i]['volumeInfo']['title']
                author_name = books[i]['volumeInfo']['authors'][0]
                cover_url = books[i]['volumeInfo']['imageLinks']['thumbnail']
                dict[title] = author_name
                pics.append(cover_url)
                #collecting tags from OpenLibary API
                url_2 = "https://openlibrary.org/api/books?bibkeys=ISBN:" + str(isbn) + "&jscmd=data&format=json"
                req = urllib.Request(url_2, headers=hdr)
                tags = json.loads(urllib.urlopen(req).read())['ISBN:'+str(isbn)]['details']['subjects']
                #create book
                new_book = Book(title = title, isbn = isbn, cover_url = cover_url, tags = tags)
                #search for author in database
                author = Author.query.filter_by(author_name = books[i]['volumeInfo']['authors'][0]).first()
                if author == None:
                    new_author = Author(author_name)
                    new_author.books.append(new_book)
                    db.session.add(new_author)
                else:
                    author.books.append(new_book)
                    db.session.add(author)
                #commit new book
                db.session.add(new_book)
                db.session.commit()
            #if it does exist, collect data from database
            else:
                dict[books.title] = books.author_name
                pics.append(books.cover_url)

        print(dict)
        #print(dict) ['imageLinks']['thumbnail']
        url = "http://openlibrary.org/search.json?q=" + str(form.search.data)

    if request.method == "POST":
        pass

    return render_template('books/browse.html',
                           form=form,
                           query=form.search.data,
                           limit=SEARCH_LIMIT,
                           results=full_results,
                           dict = dict,
                           pics = pics)



    #return render_template("books/browse.html")


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
