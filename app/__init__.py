import os

from flask import Flask, flash, redirect, url_for
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from googleapiclient.discovery import build, Resource
from typing import Union

# Created SQLAlchemy object
db: SQLAlchemy = SQLAlchemy()

# Define Flask SocketIO and related variables
socketio: SocketIO = SocketIO()

# Define Google API client
api_key: Union[str, None] = os.environ.get("GOOGLE_BOOKS_API_KEY", None)

if api_key is None:
    raise ValueError("Missing API key")

service: Resource = build("books", "v1", developerKey=api_key)


def create_app(config: dict = None) -> Flask:
    """
    Create and configure a Flask app.

    :param dict config: The test configuration object

    :return: A Flask application instance.
    """
    app: Flask = Flask(__name__)

    database_url: str = os.environ.get("DATABASE_URL", None)

    if database_url is None:
        database_url: str = f"sqlite:///{os.path.join(app.instance_path, 'database.sqlite')}"

    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
                            SQLALCHEMY_DATABASE_URI=database_url,
                            SQLALCHEMY_TRACK_MODIFICATIONS=False,
                            TESTING=os.environ.get("TESTING", False))

    if config is not None:
        app.config.update(config)

    # Register blueprints

    from app import auth, books, friends, match

    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(friends.bp)
    app.register_blueprint(match.bp)

    # Database and socketio configuration

    db.init_app(app)
    socketio.init_app(app)

    try:
        os.makedirs(app.instance_path)
        # Drop and create the table if not exist
        with app.app_context():
            db.drop_all()
            db.create_all()
    except OSError:
        pass

    # Define middlewares

    @app.teardown_request
    def teardown_session(exception: Exception = None) -> None:
        """
        Teardown the current session on request teardown.

        :param Exception exception: Any exception thrown

        :returns: None
        """
        db.session.remove()

    # Define boilerplate routes. Replace or delete for an actual application.

    app.add_url_rule("/", endpoint="index")

    # Define error handling

    @app.errorhandler(404)
    def handle_404_not_found(error):
        flash(f"{error}")
        return redirect(url_for("index"))

    return app
