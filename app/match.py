from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_socketio import emit, join_room, leave_room
from hashlib import sha1
from math import acos, sqrt
from textblob import TextBlob
from typing import Union
from werkzeug.security import gen_salt

from app import db, socketio
from .auth import login_required
from .models import User, Book, MessageSession, SavedBook

bp: Blueprint = Blueprint("match", __name__, url_prefix="/match")


def dot_product(vec_a: tuple, vec_b: tuple) -> Union[int, float]:
    """
    Calculate the dot product of two vectors.

    :param tuple vec_a: Vector A
    :param tuple vec_b: Vector B

    :return: int or float of the resulting product
    """
    return sum((a * b) for a, b in zip(vec_a, vec_b))


def vector_length(vec: tuple) -> float:
    """
    Calculate the length of a vector.

    :param tuple vec: A vector

    :return: float of the length
    """
    return sqrt(dot_product(vec, vec))


def theta_difference(vec_a: tuple, vec_b: tuple) -> float:
    """
    Calculate the theta difference between two vectors.

    :param tuple vec_a: Vector A
    :param tuple vec_b: Vector B

    :return: float of the resulting product
    """
    return acos(
        dot_product(vec_a, vec_b) /
        (vector_length(vec_a) * vector_length(vec_b)))


def quantify_vector(vec: tuple) -> tuple:
    """
    Quantify a given vector.
    Modify the given vector.

    :param tuple vec: A tuple consisting of rating and review

    :return: None
    """
    blob: TextBlob = TextBlob(vec[1])

    return (vec[0], blob.sentiment.polarity + 1)


@bp.route("/", methods=["GET"])
@login_required
def match():
    """
    Match two users with common book interests.

    :param: None

    :return: Redirection or render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    reading_lists: list = SavedBook.query.filter_by(user_id=user.id).all()

    potential_friends: Union[list, None] = []

    for book in reading_lists:
        fetched_users: list = SavedBook.query.filter(
            SavedBook.book_id == book.book_id,
            SavedBook.user_id != user.id).all()

        for i, fetched_book in enumerate(fetched_users):
            fetched_users[i] = User.query.filter_by(
                id=fetched_book.user_id).first()

        fetched_users = list(set(fetched_users))

        if len(fetched_users) != 0:
            potential_friends += fetched_users

    potential_friends = list(set(potential_friends[:10]))

    elo: Union[list, None] = []

    for book in reading_lists:
        elo_round: list = []

        for potential_friend in potential_friends:
            friend_book: SavedBook = SavedBook.query.filter_by(
                book_id=book.book_id, user_id=potential_friend.id).first()

            if friend_book is None or friend_book.rating is None or friend_book.review is None:
                elo_round.append(1)
                continue

            user_vector: tuple = quantify_vector((book.rating, book.review))
            friend_vector: tuple = quantify_vector(
                (friend_book.rating, friend_book.review))

            elo_round.append(theta_difference(user_vector, friend_vector))

        elo.append(elo_round)

    elo = [sum(i) for i in zip(*elo)]

    if len(elo) == 0:
        elo = None
    elif len(potential_friends) == 0:
        potential_friends = None
    else:
        elo, potential_friends = (list(t) for t in zip(
            *sorted(zip(elo, potential_friends))))

    return render_template("match/result.html",
                           elo=elo,
                           potential_friends=potential_friends)


@bp.route("/connect", methods=["GET", "POST"])
@login_required
def connect() -> None:
    """
    Connect with another user.

    :param int id: The user ID

    :return: None
    """
    other_user_id: Union[int, str,
                         None] = request.form.get("other_user_id", None)

    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    if other_user_id is None:
        flash("Malformed request.")
        return redirect(url_for("index"))
    else:
        other_user_id = int(other_user_id)

        other_user: User = User.query.filter_by(
            id=other_user_id).first_or_404()

        print(
            MessageSession.query.filter_by(user_a_id=user.id,
                                           user_b_id=other_user.id).first())

        print(
            MessageSession.query.filter_by(user_a_id=other_user.id,
                                           user_b_id=user.id).first())

        if not db.session.query(
                MessageSession.query.filter_by(user_a_id=user.id,
                                               user_b_id=other_user.id).
                exists()).scalar() and not db.session.query(
                    MessageSession.query.filter_by(
                        user_a_id=other_user.id,
                        user_b_id=user.id).exists()).scalar():
            message_session: MessageSession = MessageSession(
                user_a_id=user.id, user_b_id=other_user.id, room=gen_salt(12))

            db.session.add(message_session)
            db.session.commit()

    display_name: str = user.display_name

    return render_template("match/connect.html",
                           display_name=display_name,
                           other_user_id=other_user_id)


@socketio.on("join", namespace="/match/connect")
def handle_join(payload: dict):
    """
    Handle on join for session.

    :param dict payload: Incoming payload

    :return: SocketIO response
    """
    user_id: int = session.get("user_id")
    other_user_id: int = int(payload["other_user_id"])

    message_session: Union[MessageSession, None] = MessageSession.query.filter(
        (MessageSession.user_a_id == user_id
         and MessageSession.user_b_id == other_user_id)
        or (MessageSession.user_a_id == other_user_id
            and MessageSession.user_b_id == user_id)).first()

    if message_session is None:
        flash("Socket connection failed.")
        return redirect(url_for("index"))

    room: str = message_session.room

    join_room(room)

    emit("status", {"data": "Message session initiated."},
         callback=print("join", payload),
         room=room)


@socketio.on("request", namespace="/match/connect")
def handle_chat_message(payload: dict):
    """
    Handle incoming chat messages.
    Echo back the payload.

    :param dict payload: Incoming payload

    :return: SocketIO response
    """
    user_id: int = session.get("user_id")
    other_user_id: int = int(payload["other_user_id"])

    message_session: Union[MessageSession, None] = MessageSession.query.filter(
        (MessageSession.user_a_id == user_id
         and MessageSession.user_b_id == other_user_id)
        or (MessageSession.user_a_id == other_user_id
            and MessageSession.user_b_id == user_id)).first()

    if message_session is None:
        flash("Socket connection failed.")
        return redirect(url_for("index"))

    room: str = message_session.room

    print(room)

    emit("response", payload, callback=print("response", payload), room=room)


@socketio.on("leave", namespace="/match/connect")
def handle_leave(payload: dict):
    """
    Handle exit for session.

    :param dict payload: Incoming payload

    :return: SocketIO response
    """
    user_id: int = session.get("user_id")
    other_user_id: int = int(payload["other_user_id"])

    message_session: Union[MessageSession, None] = MessageSession.query.filter(
        (MessageSession.user_a_id == user_id
         and MessageSession.user_b_id == other_user_id)
        or (MessageSession.user_a_id == other_user_id
            and MessageSession.user_b_id == user_id)).first()

    if message_session is None:
        flash("Socket connection failed.")
        return redirect(url_for("index"))

    room: str = message_session.room

    leave_room(room)

    emit("status", {"data": "Message session exited."},
         callback=print("leave", payload),
         room=room)
