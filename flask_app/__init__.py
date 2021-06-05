from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Single Database used accross all app
# `db` is intialized in `create_app()`
db = SQLAlchemy()

def create_app():
    """
    Simple flask-app factory used to initialize this app. The name follows
    Flask conventions and it should not be changed.
    """

    # Initialize Flask
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = b'\xf8N>\xfc\xa3~R\x99kHUwR\xb6\xe26'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Database intialization
    db.__init__(app)

    # Blueprints registration
    from .authSession import authBlueprint
    from .anonymousSession import anonymousBlueprint

    app.register_blueprint(authBlueprint)
    app.register_blueprint(anonymousBlueprint)

    return app
