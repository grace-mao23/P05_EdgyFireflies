from flask import (Blueprint, render_template)

from app import db
from app.auth.views import login_required

bp = Blueprint("friend",
               __name__,
               url_prefix="/friend",
               template_folder="templates",
               static_folder="static")

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
def get_profile():
    """Returns the profile view of a logged in user.

    Elements:
      Show Recent Messages (To be implemented)
      Show Friends (To be implemented)
      Show Reading List (To be implemented)
    
    Args:
      None
    
    Returns:
      A rendered Jinja template.
    """
    return render_template("profile.html")


@bp.route("/match", methods=["GET"])
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
    return render_template("match.html")


@bp.route("/chat/<int:session_id>", methods=["GET"])
def chat(session_id):
    """Returns the chat session for a logged in user.

    Elements:
      Real Time Chat with SocketsIO (To be implemented)

    Args:
      None
    
    Returns:
      A rendered Jinja template.
    """
    return render_template("chat.html")