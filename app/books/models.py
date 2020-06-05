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
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, unique=True, nullable=False)
    author_id = db.Column(db.ForeignKey(Author.author_id), nullable=False)
    isbn = db.Column(db.String, nullable=True)
    book_genres = db.Column(db.String, nullable=True)
    year = db.Column(db.DateTime, nullable=True)
    tags = db.Column(db.String, nullable=True)


class Review(db.Model):
    """Defines the Review class.

    Columns:
      review_id: PK
      user_id: FK
      review
      upvote
    """
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.user_id), nullable=False)
    review = db.Column(db.String, nullable=False)
    upvote = db.Column(db.Integer, nullable=True)


class SavedBook(db.Model):
    """Defines the SavedBook class.
    
    Columns:
      book_id: FK
      user_id: FK
      rating
      review_id
    """
    book_id = db.Column(db.ForeignKey(Book.book_id), nullable=False)
    user_id = db.Column(db.ForeignKey(User.user_id), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review_id = db.Column(db.ForeignKey(Review.review_id), nullable=False)
