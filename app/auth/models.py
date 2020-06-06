from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (check_password_hash, generate_password_hash)

from app import db


class User(db.Model):
    """Defines the user class.

    Columns:
      user_id: PK
      email
      username
      password
      elo
    """
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    elo = db.Column(db.Integer, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, given_password):
        """Hashes the given password
        
        Args:
          self: The User class.
          given_password: A given password.

        Returns:
          None
        """
        self._password = generate_password_hash(given_password)

    def check_password(self, given_password):
        """Checks the given password against the stored hash.

        Args:
          self: The User class.
          given_password: A given password.

        Returns:
          A boolean on the validity of the check.
        """
        return check_password_hash(self.password, given_password)
