from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from .auth import login_required
from .models import User

bp: Blueprint = Blueprint("friends", __name__, url_prefix="/friends")


@bp.route("/profile", methods=["GET"])
def profile():
    """
    Return the profile view of a logged in user.

    :param None:
    
    :returns: Render template
    """
    user: User = User.query.filter_by(id=session.get("user_id")).first_or_404()

    username: str = user.username
    display_name: str = user.display_name

    return render_template("friends/profile.html",
                           username=username,
                           display_name=display_name)
