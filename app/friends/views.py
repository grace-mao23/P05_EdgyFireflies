from flask import (Blueprint, render_template, session)

from app import db
from app.auth.views import login_required
from app.auth.models import User
from app.books.models import SavedBook
from app.friends.models import ChatHistory

bp = Blueprint("friends", __name__, url_prefix="/friend")

# Define matching algorithm
# ---START---


def find_potential_friends():
    """Returns a list of users that could be friends with a user.

    Algorithm:
      1. The user should have favorited books with ratings and written reviews.
      2. Get all other users that have the same or a subset of the user’s favorite books.
      3. Get the user ratings and written reviews for all other users that meet the criteria from the previous step.
      4. Perform semantic analysis on all written reviews.
      5. Construct vectors that compare the original user to all other users for each book.
      6. Calculate the angle or the distance difference between the vectors for a measure of “user closeness”.
      7. Sum the angle or the distance differences and multiply it by the number of shared favorite books since the other users could have fewer books than the original set.
      8. Return the users in order of lowest score.

    """
    pass


# ---END---


@bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    """Returns the profile view of a logged in user.

    Elements:
      Show Recent Messages (To be implemented)
      Show Friends
      Show Reading List
    
    Args:
      None
    
    Returns:
      A rendered Jinja template.
    """
    friends = User.query.get(session.get("user_id")).friends
    reading_list = SavedBook.query.filter_by(
        user_id=session.get("user_id")).all()

    return render_template("friends/profile.html",
                           friends=friends,
                           reading_list=reading_list)


@bp.route("/match", methods=["GET"])
@login_required
def match():
    """Returns a list of potential friends to match for a logged in user.

    Elements:
      Search Friends (To be implemented)
      List of Potential Friends (To be implemented)

    Args:
      None

    Returns:
      A rendered Jinja template.
    """
    return render_template("friends/match.html")


@bp.route("/chat/<int:session_id>", methods=["GET"])
@login_required
def chat(session_id):
    """Returns the chat session for a logged in user.

    Elements:
      Real Time Chat with SocketsIO (To be implemented)

    Args:
      None
    
    Returns:
      A rendered Jinja template.
    """
    chat_history = ChatHistory.query.filter_by(session_id=session_id).first()

    return render_template("friends/chat.html")
