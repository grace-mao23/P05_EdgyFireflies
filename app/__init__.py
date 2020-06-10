import os

from flask import (Flask, render_template)
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from app.forms import SearchForm


# Created SQLAlchemy object, but is not binded to any Flask application
db = SQLAlchemy()

# Created SocketIO object, but is not binded to any Flask application
socketio = SocketIO()


def create_app(config=None):
    """Create and configure a Flask app.
    Args:
      config: A test configuration object.

    Returns:
      A Flask application instance.
    """
    # Application configuartion
    # ---START---

    app = Flask(__name__)

    database_url = os.environ.get("DATABASE_URL", None)

    if database_url is None:
        database_url = f"sqlite:///{os.path.join(app.instance_path, 'database.sqlite')}"

    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
                            SQLALCHEMY_DATABASE_URI=database_url,
                            SQLALCHEMY_TRACK_MODIFICATIONS=False,
                            TESTING=os.environ.get("TESTING", False))

    if config is not None:
        app.config.update(config)

    # ---END---

    # Register blueprints
    # ---START---

    from app import auth, books, friends

    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)
    app.register_blueprint(friends.bp)

    # ---END---

    # Database and socketio configuration
    # ---START---

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

    # ---END---

    # Define middlewares
    # ---START---

    @app.teardown_request
    def teardown_session(exception=None):
        db.session.remove()

    # ---END---

    # Define boilerplate routes. Replace or delete for an actual application.
    # ---START---

    @app.route("/hello")
    def hello():
        return "Hello, world!"

    app.add_url_rule("/", endpoint="index")

    @app.route("/search", methods=['GET', 'POST'])
    def search():
        SEARCH_LIMIT = 100
        PER_ROW = 3

        form = SearchForm()

        full_results = None

        if form.validate_on_submit():
            url = "http://openlibrary.org/search.json?q=" + str(form.search.data)
            results = ["f"]

            # cut results off
            results = results[:SEARCH_LIMIT]

            # pad results
            while len(results) % PER_ROW != 0:
                results.append(None)

            full_results = []

            print(full_results)

            for i in range(len(results) // PER_ROW):
                full_results.append(results[i * PER_ROW:(i + 1) * PER_ROW])

        return render_template('search.html',
                               form=form,
                               query=form.search.data,
                               limit=SEARCH_LIMIT,
                               results=full_results)
    # ---END---

    return app
