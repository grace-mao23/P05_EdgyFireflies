import click
import os

from flask import Flask, render_template
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Created SQLAlchemy object, but is not binded to any Flask application
db = SQLAlchemy()


def create_app(config=None):
    """Create and configure a Flask app.

    Args:
      config: A test configuration object.
    
    Returns:
      A Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    database_url = os.environ.get("DATABASE_URL", None)

    if database_url is None:
        database_url = f"sqlite:///{os.path.join(app.instance_path, 'database.sqlite')}"

    app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
                            SQLALCHEMY_DATABASE_URI=database_url,
                            SQLALCHEMY_TRACK_MODIFICATIONS=False)

    if config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(config)

    db.init_app(app)
    app.cli.add_command(clear_db_command)

    try:
        os.makedirs(app.instance_path)
        with app.app_context():
            clear_db()
    except OSError:
        pass

    # Define a /hello route. Replace or delete for an actual application.
    @app.route("/hello")
    def hello():
        return "Hello, world!"

    return app


def clear_db():
    """Clear a new or existing database.

    Args:
      None

    Returns:
      None
    """
    db.drop_all()
    db.create_all()


@click.command("clear-db")
@with_appcontext
def clear_db_command():
    """Invoke the clear_db function.

    Args:
      None

    Returns:
      None
    """
    clear_db()
    click.echo("Cleared the database.")
