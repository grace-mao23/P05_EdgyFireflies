from app import db
from app.auth.models import User


class Friend(db.Model):
    """Defines the Friend class.

    Columns:
      session_id: PK
      user_id_one: FK
      user_id_two: FK
    """
    session_id = db.Column(db.Integer, primary_key=True)
    user_id_one = db.Column(db.ForeignKey(User.user_id), nullable=False)
    user_id_two = db.Column(db.ForeignKey(User.user_id), nullable=False)


class ChatHistory(db.Model):
    """Defines the ChatHistory class.

    Columns:
      session_id: PK
      message
      timestamp
    """
    session_id = db.Column(db.ForeignKey(Friend.session_id), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    friend = db.relationship(Friend, lazy="joined", backref="chats")
