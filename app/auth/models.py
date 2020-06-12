from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import (check_password_hash, generate_password_hash)

from app import db

friend_requests = db.Table(
    "friend_requests",
    db.Column("sender_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("receiver_id", db.Integer, db.ForeignKey("user.user_id")),
)

friends = db.Table(
    "friends",
    db.Column("session_id", db.Integer, primary_key=True),
    db.Column("friend_one_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("friend_two_id", db.Integer, db.ForeignKey("user.user_id")),
)


class User(db.Model):
    """Defines the user class.

    Columns:
      user_id: PK
      email
      username
      password
      friends
      elo
    """
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    bio = db.Column(db.String, unique=True, nullable=True)
    friends = db.relationship(
        "User",
        secondary=friends,
        primaryjoin=(user_id == friends.c.friend_one_id),
        secondaryjoin=(user_id == friends.c.friend_two_id),
        backref=db.backref("friended", lazy="dynamic"),
        lazy="dynamic")
    friend_requests = db.relationship(
        "User",
        secondary=friend_requests,
        primaryjoin=(user_id == friend_requests.c.sender_id),
        secondaryjoin=(user_id == friend_requests.c.receiver_id),
        backref=db.backref("friend_requested", lazy="dynamic"),
        lazy="dynamic")
    elo = db.Column(db.Integer, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, given_password):
        """Hash the given password

        Args:
          self: The User class.
          given_password: A given password.

        Returns:
          None
        """
        self._password = generate_password_hash(given_password)

    def check_password(self, given_password):
        """Check the given password against the stored hash.

        Args:
          self: The User class.
          given_password: A given password.

        Returns:
          A boolean on the validity of the check.
        """
        return check_password_hash(self.password, given_password)

    def is_friend(self, user):
        """"Check if two users are already friends."""
        return self.friends.filter(
            friends.c.friend_one_id ==
            user.user_id).count() > 0 or self.friends.filter(
                friends.c.friend_two_id == user.use_id).count() > 0

    def send_friend_request(self, user):
        """Sends a friend request to a user."""
        if not self.friend_requests.filter(friend_requests.c.receiver_id == user.id).count() > 0:
            self.friend_requests.append(user)

    def accept_friend_request(self, user):
        """Accepts a friend request from a user."""
        if not self.is_friend(user) and self.friend_requests.filter(
                friend_requests.c.sender_id == user.id).count() > 0:
            self.friends.append(user)
            self.friend_requests.remove(user)
