from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Gets rid of stupid warning message

    # Database intialization
    db.__init__(app)

    # LoginManager setup
    login_manager = LoginManager()
    login_manager.login_view = "anonymousBlueprint.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Custom 404 page
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Blueprints registration
    from .authSession import authBlueprint
    from .anonymousSession import anonymousBlueprint

    app.register_blueprint(authBlueprint)
    app.register_blueprint(anonymousBlueprint)

    return app
