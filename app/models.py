from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    """
    Defines the user class.

    :attribute Column id: The user ID
    :attribute Column username: The user's username
    :attribute Column display_name: The user's display name
    :attribute Column _password: The user's password
    """
    id: db.Column = db.Column(db.Integer, primary_key=True)
    username: db.Column = db.Column(db.String, unique=True, nullable=False)
    display_name: db.Column = db.Column(db.String, unique=True, nullable=False)
    _password: db.Column = db.Column("password", db.String, nullable=False)

    @hybrid_property
    def password(self: object) -> str:
        """
        Return the stored user password.

        :param object self: The User class
        
        :returns: The password of type str
        """
        return self._password

    @password.setter
    def password(self: object, given_password: str) -> None:
        """
        Hash the given password.

        :param object self: The User class
        :param str given_password: The given password

        :returns: None
        """
        self._password = generate_password_hash(given_password)

    def check_password(self: object, given_password: str) -> bool:
        """
        Check the given password against the stored hash.

        :param object self: The User class
        :param str given_password: The given password

        :returns: True or False on if the given password is valid
        """
        return check_password_hash(self.password, given_password)


class Book(db.Model):
    """
    Defines the book class.

    :attribute Column id: The book ID
    :attribute Column bookname: The book's name
    """
    id: db.Column = db.Column(db.Integer, primary_key=True)
    bookname: db.Column = db.Column(db.String, unique=True, nullable=False)
    author: db.Column = db.Column(db.String, nullable=False)
    isbn: db.Column = db.Column(db.String, unique=True, nullable=False)
    description: db.Column = db.Column(db.String, nullable=True)
    categories: db.Column = db.Column(db.String, nullable=True)
