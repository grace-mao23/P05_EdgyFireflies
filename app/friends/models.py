from app import db
from app.auth.models import (User, friends)


class ChatHistory(db.Model):
    """Defines the ChatHistory class.

    Columns:
      session_id: PK
      message
      timestamp
    """
    chat_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.ForeignKey(friends.c.session_id), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
