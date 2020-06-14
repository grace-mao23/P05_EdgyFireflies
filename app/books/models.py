from app import db
from app.auth.models import User


class Author(db.Model):
    """Defines the Author class.

    Columns:
      author_id: PK
      author_name
    """
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String, unique=True, nullable=False)
    books = db.relationship('Book', backref='Author')

    def __init__(self, author_name):
        self.author_name = author_name

class Book(db.Model):
    """Defines the Book class.

    Columns:
      book_id: PK
      book_name
      author_id: FK
      isbn
      book_genres
      year
      tags
    """
    __table_args__ = {"extend_existing": True}
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey(Author.author_id), nullable=False)
    title = db.Column(db.String, unique=True, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    cover_url = db.Column(db.String, nullable=True)
    tags = db.Column(db.String, nullable=True)

    def __init__(self, title, isbn, cover_url, tags):
        self.title = title
        self.isbn = isbn
        self.cover_url = cover_url
        self.tags = tags


# class Review(db.Model):
#     """Defines the Review class.
#
#     Columns:
#       review_id: PK
#       user_id: FK
#       review
#       upvote
#     """
#     review_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.ForeignKey(User.user_id), nullable=False)
#     review = db.Column(db.String, nullable=False)
#     upvote = db.Column(db.Integer, nullable=True)


class SavedBook(db.Model):
    """Defines the SavedBook class.

    Columns:
      book_id: FK
      user_id: FK
      rating
      review_id
    """
    saved_book_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey(Book.book_id), nullable=False)
    user_id = db.Column(db.ForeignKey(User.user_id), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
